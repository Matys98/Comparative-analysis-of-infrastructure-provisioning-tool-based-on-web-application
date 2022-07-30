#   Instance 1 - DataBase

scp ../../tiquet.sh  vagrant@192.168.56.21:/home/vagrant/script.sh
scp -r ../../Tiquet/  vagrant@192.168.56.21:/home/vagrant/Tiquet/
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.21 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.21 './script.sh -d'

#   Instance 2 - Frontend

scp ../../tiquet.sh  vagrant@192.168.56.22:/home/vagrant/script.sh
scp -r ../../Tiquet/  vagrant@192.168.56.22:/home/vagrant/Tiquet/
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 './script.sh -f'

#   Instance 3 - Backend

scp ../../tiquet.sh  vagrant@192.168.56.23:/home/vagrant/script.sh
scp -r ../../Tiquet/  vagrant@192.168.56.23:/home/vagrant/Tiquet/
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.23 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.23 './script.sh -b'