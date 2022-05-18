##################################
#   All commands to deploy grafana

# 0. Update packages
sudo apt-get update

# 1. Add grafana repo
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main" -y

# 2. Install grafana
sudo apt-get -y install grafana

# 3. Run grafana
sudo systemctl start grafana-server

#####################################
#   All commands to deploy influxdb

sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -

sudo echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
 
sudo apt update

sudo apt install influxdb

sudo systemctl start influxdb

#####################################
#   All commands to configure grafana

#