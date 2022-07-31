from fabric import Connection, task, Config, SerialGroup
import getpass
from tiquet_module import tiquet

def instal_apps(c):
    c.run('sudo apt-get update')
    c.run('sudo apt-get install curl -y')
    c.run('sudo apt install software-properties-common -y')
    c.run('sudo apt-get update')


def config_app(c):
    c.run('sudo apt-get install git -y')
    c.run('mkdir app')
    c.run('cd app')
    with c.cd('/home/$(whoami)/app/'):
        c.run('git clone https://github.com/FLiotta/Tiquet.git')

    c.run("sed -i 's/cffi==1.14.0/cffi==1.14.1/g' home/$(whoami)/app/Tiquet/server/requirements.txt")

def config_db(c):
    c.run('curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg')
    c.run('echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list')
    c.run('sudo apt-get install postgresql -y')
    c.run('sudo apt-get install postgresql-client-common -y')
    c.run('sudo apt-get install postgresql-client -y')

    c.run('''
        sudo bash -c "cat > /etc/postgresql/14/main/pg_hba.conf << EOF
        # TYPE  DATABASE        USER            ADDRESS                 METHOD
        local   all             all                                     trust
        # IPv4 local connections:
        host    all             all             127.0.0.1/32            trust
        # IPv6 local connections:
        host    all             all             ::1/128                 trust
        # Allow replication connections from localhost, by a user with the
        # replication privilege.
        host    replication     all             127.0.0.1/32            trust
        host    replication     all             ::1/128                 trust
        local   all             all                                     trust
        EOF
        "
    ''')

    c.run('systemctl restart postgresql')
    c.run('psql -U postgres -c "CREATE DATABASE tiquet"')

def config_frontend(c):
    c.run('sudo apt-get install nodejs -y')
    c.run('sudo apt-get install npm -y')

    c.run('sudo apt-get install update')

    with c.cd('/home/$(whoami)/app/Tiquet/client'):
        c.run('npm install')
        c.run('npm audit fix')
        c.run('npm install serve -g')
        c.run('npm install pm2 -g ')


def run_frontend(c, app_name):
    with c.cd('/home/$(whoami)/app/Tiquet/client'):
        c.run('npm run bundle')
        c.run('pm2 start --name ' + app_name + '_frontend npm -- start')

def config_backend(c):
    c.run('sudo add-apt-repository ppa:deadsnakes/ppa -y')
    c.run('sudo apt-get install python3.8 -y')
    c.run('sudo apt-get install python3-pip -y')
    c.run('sudo apt-get install python3-virtualenv -y')

    c.run('sudo apt install libpq-dev -y')
    c.run('sudo apt install libffi-dev -y')

    c.run('cd ./app/Tiquet/server')
    with c.cd('/home/$(whoami)/app/Tiquet/server'):
        c.run('virtualenv env')
        c.run('source env/bin/activate')
        c.run('echo requests==2.25.1 >> ./requirements.txt')
        c.run('pip install -r ./requirements.txt')
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

def run_backend(c, app_name):
    with c.cd('/home/$(whoami)/app/Tiquet/server'):
        c.run('python3 create_tables.py')
        c.run('pm2 start run.py --interpreter python3 --name '+ app_name + '_backend')
        c.run('deactivate')

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
def tiquet_deploy_to_one_instance(c):
   print(" Deploy solar panel app to instance: " + vm_host1)
   app_name = "tiquet"
   instal_apps(c)
   config_app(c)
   config_db(c)
   config_backend(c)
   run_backend(c, app_name)
   config_frontend(c)
   run_frontend(c, app_name)

@task
def tiquet_deploy_to_many_instance(c):
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
   instal_apps(c)
   config_db(c)

   # Connecting to Backend instance
   c = Connection(host=backend_host,
       connect_kwargs={"key_filename": ssh_path})
   instal_apps(c)
   config_app(c)
   config_backend(c)
   run_backend(c, app_name)

   # Connecting to Frontend instance
   c = Connection(host=fronend_host,
       connect_kwargs={"key_filename": ssh_path})
   instal_apps(c)
   config_app(c)
   config_frontend(c)
   run_frontend(c, app_name)