from fabric import Connection, task, Config, SerialGroup
import patchwork.transfers
import getpass

def install_apps(ctx, c):
    c.run('sudo apt-get install curl -y')
    c.run('sudo apt install software-properties-common -y')
    patchwork.transfers.rsync(c, './Tiquet', '/home/vagrant/')
    print("END install apps")

def config_app(ctx, c):
    c.run('sudo apt-get install git -y')
    c.run('mkdir /home/$(whoami)/app || echo "app exist"')
    with c.cd('/home/$(whoami)/app/'):
        c.run('git clone https://github.com/FLiotta/Tiquet.git')

    c.run("sudo sed -i 's/cffi==1.14.0/cffi==1.14.1/g' /home/$(whoami)/app/Tiquet/server/requirements.txt")
    print("END Config app")

def config_db(ctx, c):
    c.run('curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg')
    c.run('echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list')
    c.run('sudo apt-get install postgresql -y')
    c.run('sudo apt-get install postgresql-client-common -y')
    c.run('sudo apt-get install postgresql-client -y')

    c.run('sudo cp /home/$(whoami)/Tiquet/pg_hba.conf /etc/postgresql/14/main/')

    c.run('sudo systemctl restart postgresql')
    c.run('psql -U postgres -c "CREATE DATABASE tiquet"')
    print("END DB Config")

def config_frontend(ctx, c):
    c.run('sudo apt-get install npm -y')
    c.run('sudo apt install python2 -y')

    c.run('sudo cp /home/$(whoami)/Tiquet/config.ts /home/$(whoami)/app/Tiquet/client/src/config.ts')
    with c.cd('/home/$(whoami)/app/Tiquet/client'):
        c.run('sudo npm install')
        c.run('sudo npm install serve -g')
        c.run('sudo npm install save-dev webpack-cli -g')
        c.run('sudo npm install pm2 -g ')
    print("END Config Frontend")


def run_frontend(ctx, c, app_name):
    with c.cd('/home/$(whoami)/app/Tiquet/client'):
        c.run('npm run bundle || echo "Succes"')
        c.run('pm2 start --name ' + app_name + '_frontend npm -- start')
    print("END Run Frontend")

def config_backend(ctx, c):
    c.run('sudo apt install python2 -y')
    c.run('sudo add-apt-repository ppa:deadsnakes/ppa -y')
    c.run('sudo apt-get install python3.8 -y')
    c.run('sudo apt-get install python3-pip -y')
    c.run('sudo apt-get install python3-virtualenv -y')

    c.run('sudo apt install libpq-dev -y')
    c.run('sudo apt install libffi-dev -y')

    c.run('sudo apt install npm -y')
    c.run('sudo npm install pm2 -g')

    c.run('cd ./app/Tiquet/server')
    with c.cd('/home/$(whoami)/app/Tiquet/server'):
        c.run('python3 -m virtualenv env || virtualenv env')
        c.run('echo requests==2.25.1 >> ./requirements.txt')
        c.run('''
        source env/local/bin/activate || source env/bin/activate
        cat ./requirements.txt | xargs -n 1 pip install || echo "Succes"
        ''')
        c.run('''
                sudo bash -c "cat > ./app/config.py << EOF
                import os

                DEBUG = True
                CORS_HEADERS = 'Content-Type'
                SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/tiquet'
                SQLALCHEMY_TRACK_MODIFICATIONS = False
                EOF
                "
        ''')
    print("END Config Backend")

def run_backend(ctx, c, app_name):
    with c.cd('/home/$(whoami)/app/Tiquet/server'):
        c.run('''
        source env/local/bin/activate || source env/bin/activate
        python3 create_tables.py || echo "Succes"
        ''')
        c.run('''
        source env/local/bin/activate || source env/bin/activate
        pm2 start run.py --interpreter python3 --name '+ app_name + '_backend
        ''')
    print("END Run Backend")

repo_name = ''
repo_dir = ''
app_name = ''

vm_host1 = 'vagrant@192.168.56.21'
vm_host2 = 'vagrant@192.168.56.22'
vm_host3 = 'vagrant@192.168.56.23'

ssh_path = '/home/matys/.ssh/id_rsa'

c = Connection(host=vm_host1,
              connect_kwargs={"key_filename": ssh_path})
 
def get_password(connection):
   """function required in all tasks where sudo method is used"""
   sudo_pass = getpass.getpass("What's your sudo password?")
   config = Config(overrides={'sudo': {'password': sudo_pass}})
   connection.config = config

@task
def tiquet_deploy_to_one_instance(ctx):
   print(" Deploy solar panel app to instance: " + vm_host1)
   c = Connection(host=vm_host1,
              connect_kwargs={"key_filename": ssh_path})
   app_name = "tiquet"
   install_apps(ctx, c)
   config_app(ctx, c)
   config_db(ctx, c)
   config_frontend(ctx, c)
   run_frontend(ctx, c, app_name)
   config_backend(ctx, c)
   run_backend(ctx, c, app_name)
   c.close()

@task
def tiquet_deploy_to_many_instances(ctx):
   vm_host1 = '192.168.56.21'
   vm_host2 = '192.168.56.22'
   vm_host3 = '192.168.56.23'
   hosts = [vm_host1, vm_host2, vm_host3]
   print(" Deploy tiquet app to instance: " + str(hosts))
   i = 0
   for c in SerialGroup(vm_host1, vm_host2, vm_host3, user="vagrant", 
                        port=22, connect_kwargs={"key_filename": ssh_path}):
        app_name = "tiquet"
        install_apps(ctx, c)
        config_app(ctx, c)
        config_db(ctx, c)
        config_frontend(ctx, c)
        run_frontend(ctx, c, app_name+ str(i))
        config_backend(ctx, c)
        run_backend(ctx, c, app_name+ str(i))
        i=+1
        c.close()

@task
def tiquet_deploy_split_instance(ctx):
   fronend_host = vm_host1
   backend_host = vm_host2
   db_host = vm_host3
   app_name = "tiquet"

   print(" Deploy " + app_name + " frontend to instance:" + fronend_host)
   print(" Deploy " + app_name + " backendend to instance:" + backend_host)
   print(" Deploy " + app_name + " data base to instance:" + db_host)

   # Connecting to Data base instance
   c = Connection(host=db_host,
       connect_kwargs={"key_filename": ssh_path})
   install_apps(ctx, c)
   config_db(ctx, c)
   c.close()

   # Connecting to Backend instance
   c = Connection(host=backend_host,
       connect_kwargs={"key_filename": ssh_path})
   install_apps(ctx, c)
   config_app(ctx, c)
   config_backend(ctx, c)
   run_backend(ctx, c, app_name)
   c.close()

   # Connecting to Frontend instance
   c = Connection(host=fronend_host,
       connect_kwargs={"key_filename": ssh_path})
   install_apps(ctx, c)
   config_app(ctx, c)
   config_frontend(ctx, c)
   run_frontend(ctx, c, app_name)
   c.close()
