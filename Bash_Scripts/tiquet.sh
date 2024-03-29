#!/bin/bash

# Input values
while getopts a.d.f.b. flag
do
    case "${flag}" in
        a) ALL=true;;
        d) DATA_BASE=true;;
        f) FRONTEND=true;;
        b) BACKEND=true;;
    esac
done

##################################
#   All commands to deploy tiquet

# 0. Update packages
sudo apt-get install curl -y
#sudo apt-get update
sudo apt install software-properties-common -y

# 1. Install git
sudo apt-get install git -y

# 2. Create app dir
cd 

# 3. Change dir
mkdir app
cd /home/$(whoami)/app

# 4. Clone repo
git clone https://github.com/FLiotta/Tiquet.git

# 5. Change dir
cd /home/$(whoami)/Tiquet/config.ts /home/$(whoami)/app/Tiquet/client/src/config.ts

sed -i 's/cffi==1.14.0/cffi==1.14.1/g' /home/$(whoami)/app/Tiquet/server/requirements.txt

# 6. Copy config file
cp /home/$(whoami)/Tiquet/config.ts /home/$(whoami)/app/Tiquet/client/src/config.ts

if [ $DATA_BASE ] || [ $ALL ]; then
    ##################################
    #   All commands to deploy tiquet database
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
    echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | sudo tee  /etc/apt/sources.list.d/pgdg.list

    # sudo apt-get update

    sudo apt-get install postgresql -y
    sudo apt-get install postgresql-client-common -y
    sudo apt-get install postgresql-client -y

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

    sudo systemctl restart postgresql

    psql -U postgres -c "CREATE DATABASE tiquet"
fi

if [ $FRONTEND ] || [ $ALL ]; then
    ##################################
    #   All commands to deploy tiquet frontend
    # curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -

    # sudo apt-get install nodejs -y
    sudo apt-get install npm -y
    sudo apt install python2 -y
    #sudo apt-get update

    cd /home/$(whoami)/app/Tiquet/client

    # 2. Instal npm
    npm install
    # npm audit fix

    # 3. Instal serve
    sudo npm install serve -g
    sudo npm install save-dev webpack-cli -g

    # 4. Install pm2
    sudo npm install pm2 -g 
    pm2 update

    # 5. Building app
    npm run bundle

    # 6. Run app
    pm2 start --name frontend npm -- start

    # 7. Return to main dir
    cd 
fi

if [ $BACKEND ] || [ $ALL ]; then
    ##################################
    #   All commands to deploy tiquet backend - flask
    # 0. Install Python
    sudo apt install python2 -y
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt-get install python3.8 -y
    sudo apt-get install python3-pip -y
    sudo apt-get install python3-virtualenv -y

    # 1. Fix python packages errors
    sudo apt install libpq-dev -y
    sudo apt install libffi-dev -y

    if [ $BACKEND ]; then
        sudo apt-get install npm -y
        sudo npm install pm2 -g
    fi

    # 2. Change dir to server
    cd /home/$(whoami)/app/Tiquet/server

    python3 -m virtualenv env || virtualenv env
    source env/local/bin/activate || source env/bin/activate

    # 3. Install packages
    echo requests==2.25.1 >> /home/$(whoami)/app/Tiquet/server/requirements.txt
    pip install -r /home/$(whoami)/app/Tiquet/server/requirements.txt 

    if [$BACKEND]; then
        sudo bash -c "cat > /home/$(whoami)/app/Tiquet/server/app/config.py << EOF
        import os

        DEBUG = True
        CORS_HEADERS = 'Content-Type'
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@192.168.56.21:5432/tiquet'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        EOF
        "
    else
        sudo bash -c "cat > /home/$(whoami)/app/Tiquet/server/app/config.py << EOF
        import os

        DEBUG = True
        CORS_HEADERS = 'Content-Type'
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/tiquet'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        EOF
        "
    fi
    # 4. Configure DB
    python3 /home/$(whoami)/app/Tiquet/server/create_tables.py

    # 5. Run application
    cd /home/$(whoami)/app/Tiquet/server
    pm2 start run.py --interpreter python3 --name backend

    deactivate

    cd 
fi
