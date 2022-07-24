#!/bin/bash
#   All commands to deploy static web app

# 0. Update packages
sudo apt-get update

# 1. Install npm
sudo apt-get install npm -y

# 2. Install git
sudo apt-get install git -y

# 3. Create app dir
cd 

# 4. Change dir
mkdir app 
cd app

# 5. Clone repo
git clone https://github.com/Matys98/my-cv.git

# 6. Change dir
cd my-cv/cv

# 7. Instal npm
npm install

# 8. Instal serve
sudo npm install serve -g

# 9. Install pm2
sudo npm install pm2 -g | pm2 update

npm run build

# 10. Change package.json
    # delete homepage from file

cp -r /home/$(whoami)/app/my-cv/cv/build/static/ /home/$(whoami)/app/my-cv/cv/build/my-cv/
mv /home/$(whoami)/app/my-cv/cv/build/static/ /home/$(whoami)/app/my-cv/cv/build/my-cv/
# 11. Run app
pm2 serve build --name web-app

echo "succes"

