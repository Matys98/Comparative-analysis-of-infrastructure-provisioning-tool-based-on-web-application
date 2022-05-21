#!/bin/bash
##################################
#   All commands to deploy tiquet

# 0. Update packages
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
sudo apt-get install postgresql -y
sudo apt-get install postgresql-contrib -y

##################################
#   All commands to deploy tiquet frontend
sudo apt-get install nodejs -y
sudo apt-get install npm -y

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

# 1. Fix python packages errors
sudo apt install libpq-dev
sudo apt install libffi-dev

# 2. Change dir to server
cd ./app/Tiquet/server

# 3. Install packages
pip install -r ./requirements.txt

# 4. Run application
pm2 start run.py --interpreter python3 --name backend

cd 