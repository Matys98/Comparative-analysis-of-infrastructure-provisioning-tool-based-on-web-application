#!/bin/bash
##################################
#   All commands to deploy appo - to delete

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
git clone https://github.com/oriravid/Appo-Music.git

# 5. Change dir
cd 

##################################
#   All commands to deploy appo frontend
sudo apt-get install nodejs -y
sudo apt-get install npm -y



##################################
#   All commands to deploy appo backend