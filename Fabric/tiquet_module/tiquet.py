from fabric import Connection, task, Config
import getpass

def instal_apps(c):
    c.run('apt-get update')
    c.run('apt-get install curl -y')
    c.run('apt install software-properties-common -y')
    c.run('apt-get update')


def config_app(c):
    c.run('apt-get install git -y')
    c.run('cd ')
    c.run('mkdir app')
    c.run('cd app')

    c.run('git clone https://github.com/FLiotta/Tiquet.git')

    c.run('cd ')
    c.run("sed -i 's/cffi==1.14.0/cffi==1.14.1/g' ./app/Tiquet/server/requirements.txt")

def config_db(c):
    c.run('curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg')
    c.run('echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list')
    c.run('apt-get install postgresql -y')
    c.run('apt-get install postgresql-client-common -y')
    c.run('apt-get install postgresql-client -y')

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
    c.run('apt-get install nodejs -y')
    c.run('apt-get install npm -y')

    c.run('apt-get install update')

    c.run('cd ./app/Tiquet/client')

    c.run('npm install')
    c.run('npm audit fix')
    c.run('npm install serve -g')
    c.run('npm install pm2 -g ')


def run_frontend(c, app_name):
    c.run('npm run bundle')
    c.run('pm2 start --name ' + app_name + '_frontend npm -- start')
    c.run('cd ')

def config_backend(c):
    c.run('add-apt-repository ppa:deadsnakes/ppa -y')
    c.run('apt-get install python3.8 -y')
    c.run('apt-get install python3-pip -y')
    c.run('apt-get install python3-virtualenv -y')

    c.run('apt install libpq-dev -y')
    c.run('apt install libffi-dev -y')

    c.run('cd ./app/Tiquet/server')

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
    c.run('python3 create_tables.py')
    c.run('pm2 start run.py --interpreter python3 --name '+ app_name + '_backend')
    c.run('deactivate')
    c.run('cd ')
