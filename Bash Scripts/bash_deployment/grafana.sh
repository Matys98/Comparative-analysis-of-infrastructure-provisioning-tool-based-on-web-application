scp ../grafana.sh  vagrant@192.168.56.22:/home/vagrant/script.sh
scp -r ../Grafana/  vagrant@192.168.56.22:/home/vagrant/Grafana/
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 'chmod u+x script.sh'
ssh -i ./home/user/.ssh/id_rsa vagrant@192.168.56.22 './script.sh'