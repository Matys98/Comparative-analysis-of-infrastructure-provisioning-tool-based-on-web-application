#   Instance 1

scp ../../grafana.sh  vagrant@192.168.56.21:/home/vagrant/script.sh
scp -r ../../Grafana/  vagrant@192.168.56.21:/home/vagrant/Grafana/

ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.21 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.21 './script.sh -a'

#   Instance 2

scp ../../grafana.sh  vagrant@192.168.56.22:/home/vagrant/script.sh
scp -r ../../Grafana/  vagrant@192.168.56.22:/home/vagrant/Grafana/

ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 './script.sh -a'

#   Instance 3

scp ../../grafana.sh  vagrant@192.168.56.23:/home/vagrant/script.sh
scp -r ../../Grafana/  vagrant@192.168.56.23:/home/vagrant/Grafana/

ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.23 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.23 './script.sh -a'