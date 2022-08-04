echo "Grafana 2 instances"

#   Instance 1 - DataBase

scp ../../grafana.sh  vagrant@192.168.56.21:/home/vagrant/script.sh
scp -r ../../Grafana/  vagrant@192.168.56.21:/home/vagrant/Grafana/

ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.21 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.21 './script.sh -d'

#   Instance 2 - Grafana

scp ../../grafana.sh  vagrant@192.168.56.22:/home/vagrant/script.sh
scp -r ../../Grafana/  vagrant@192.168.56.22:/home/vagrant/Grafana/

ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 "sed -i 's/localhost/192.168.56.21/g' /home/vagrant/Grafana/datasources/sample.yaml"

ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 './script.sh -g'