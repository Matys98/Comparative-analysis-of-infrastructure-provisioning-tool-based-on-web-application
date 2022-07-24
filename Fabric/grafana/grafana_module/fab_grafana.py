from fabric import Connection, task, Config
import getpass

def instal_apps(c):
    c.run('apt-get update')
    c.run('apt-get install curl -y')
    
    c.run('wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -')
    c.run('add-apt-repository "deb https://packages.grafana.com/oss/deb stable main" -y')
    
    c.run('apt-get install grafana -y')
    c.run('systemctl start grafana-server')

def download_influxdb(c, db_name):
    c.run('curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -')
    c.run('echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list')
    
    c.run('apt-get update')
    c.run('apt install influxdb -y')
    c.run('systemctl start influxdb')
    
    c.run('curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE' + db_name + '"')

def copy_config_files(c):
    c.run('mkdir ./Grafana')
    c.put('./Grafana', './Grafana')

def configure_solar(c, db_name):
    c.run('cp ./Grafana/datasources/sample.yaml /etc/grafana/provisioning/datasources')
    c.run('cp ./Grafana/dashbords/sample.yaml /etc/grafana/provisioning/dashboards')
    
    c.run('mkdir /var/lib/grafana/dashboards')
    c.run('cp ./Grafana/solar-system.json /var/lib/grafana/dashboards')
    
    c.run('systemctl restart grafana-server')