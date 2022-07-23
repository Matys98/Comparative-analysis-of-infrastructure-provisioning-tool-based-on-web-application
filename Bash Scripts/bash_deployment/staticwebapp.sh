scp ../staticwebapp.sh  vagrant@192.168.56.23:/home/vagrant/script.sh
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.23 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.23 ./script.sh
