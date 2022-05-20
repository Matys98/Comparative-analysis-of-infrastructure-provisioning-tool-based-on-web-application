#!/bin/bash
#   Commands needed
sudo apt-get install curl -y

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

# 1. Adding database
curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE inverter_power"

# 2. Copy data sources config
sudo cp ./Grafana/datasources/sample.yaml /etc/grafana/provisioning/datasources

# 3. Copy dashbords config
sudo cp ./Grafana/dashbords/sample.yaml /etc/grafana/provisioning/dashboards

# 3. Copy dashbord
sudo mkdir /var/lib/grafana/dashboards
sudo cp ./Grafana/solar-system.json /var/lib/grafana/dashboards

# 5. Load config
sudo systemctl restart grafana-server

# 2 days