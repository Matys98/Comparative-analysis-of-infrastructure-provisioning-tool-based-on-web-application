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
cd Tiquet

##################################
#   All commands to deploy tiquet database
sudo apt-get install postgresql -y
sudo apt-get install postgresql-contrib -y

##################################
#   All commands to deploy tiquet frontend
cd client

# 2. Instal npm
npm install

# 3. Instal serve
sudo npm install serve -g

# 4. Install pm2
sudo npm install pm2 -g 
pm2 update

# 5. Building app
npm run bundle

# 6. Run app
pm2 start npm --name web-app --run start

# 7. Return to main dir
cd ..

##################################
#   All commands to deploy tiquet backend - flask
# 0. Install Python
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get install python3.8 -y
sudo apt-get install pip -y

# 1. Change dir to server
cd server

pip install -r ./requirements.txt

source env/scripts/activate

python run.py &

cd ..