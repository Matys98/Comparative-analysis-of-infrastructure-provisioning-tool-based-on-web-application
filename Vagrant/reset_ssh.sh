ssh-keygen -f "/home/matys/.ssh/known_hosts" -R "192.168.56.21"
ssh-keygen -f "/home/matys/.ssh/known_hosts" -R "192.168.56.22"
ssh-keygen -f "/home/matys/.ssh/known_hosts" -R "192.168.56.23"

ssh-keyscan -H 192.168.56.21 >> /home/matys/.ssh/known_hosts
ssh-keyscan -H 192.168.56.22 >> /home/matys/.ssh/known_hosts
ssh-keyscan -H 192.168.56.23 >> /home/matys/.ssh/known_hosts
