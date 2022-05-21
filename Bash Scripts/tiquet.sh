#!/bin/bash
##################################
#   All commands to deploy tiquet

# 0. Update packages
sudo apt-get install curl -y
sudo apt-get update
sudo apt install software-properties-common -y

# 1. Install git
sudo apt-get install git -y

# 2. Create app dir
cd 

# 3. Change dir
mkdir app
cd app

# 4. Clone repo
git clone https://github.com/FLiotta/Tiquet.git

# 5. Change dir
cd 

sed -i 's/cffi==1.14.0/cffi==1.14.1/g' ./app/Tiquet/server/requirements.txt

##################################
#   All commands to deploy tiquet database
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list

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

psql -U postgres -c "CREATE DATABASE mytemplate1"

##################################
#   All commands to deploy tiquet frontend
sudo apt-get install nodejs -y
sudo apt-get install npm -y

sudo apt-get update

cd ./app/Tiquet/client

# 2. Instal npm
npm install
npm audit fix

# 3. Instal serve
sudo npm install serve -g

# 4. Install pm2
sudo npm install pm2 -g 
pm2 update

# 5. Building app
npm run bundle

# 6. Run app
pm2 start --name frontend npm -- start

# 7. Return to main dir
cd 

##################################
#   All commands to deploy tiquet backend - flask
# 0. Install Python
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get install python3.8 -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-virtualenv -y

# 1. Fix python packages errors
sudo apt install libpq-dev -y
sudo apt install libffi-dev -y

# 2. Change dir to server
cd ./app/Tiquet/server

virtualenv env
source env/bin/activate

# 3. Install packages
echo requests==2.25.1 >> ./requirements.txt
pip install -r ./requirements.txt
sed -i 's/os.environ.*/"postgresql:postgres:postgres@localhost:5432tiquet"/g' ./app/config.py

# 4. Run application
pm2 start run.py --interpreter python3 --name backend

deactivate

cd 