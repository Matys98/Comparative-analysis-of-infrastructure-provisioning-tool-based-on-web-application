from fabric import Connection, task, Config, SerialGroup
import patchwork.transfers
import getpass

def instal_apps(ctx, c):
   c.run('sudo apt-get update')
   c.run('sudo apt-get install curl -y')
    
   c.run('wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -')
   c.run('sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main" -y')
    
   c.run('sudo apt-get install grafana -y')
   c.run('sudo systemctl start grafana-server')

def download_influxdb(ctx, c, db_name):
   c.run('sudo apt-get update')
   c.run('sudo apt-get update')
   c.run('curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -')
   c.run('echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list')
    
   c.run('sudo apt-get update')
   c.run('sudo apt install influxdb -y')
   c.run('sudo systemctl start influxdb')
    
   c.run('curl -i -XPOST http://localhost:8086/query --data-urlencode "q=CREATE DATABASE ' + db_name + '"')

def copy_config_files(ctx, c):
   # c.run('mkdir /home/$(whoami)/Grafana')
   patchwork.transfers.rsync(c, './Grafana', '/home/vagrant/')

def configure_solar(ctx, c):
   c.run('sudo cp /home/$(whoami)/Grafana/datasources/sample.yaml /etc/grafana/provisioning/datasources')
   c.run('sudo cp /home/$(whoami)/Grafana/dashbords/sample.yaml /etc/grafana/provisioning/dashboards')
    
   c.run('sudo mkdir /var/lib/grafana/dashboards')
   c.run('sudo cp /home/$(whoami)/Grafana/solar-system.json /var/lib/grafana/dashboards')
    
   c.run('sudo systemctl restart grafana-server')

repo_name = ''
repo_dir = ''
app_name = ''

vm_host1 = 'vagrant@192.168.56.22'
vm_host2 = 'vagrant@192.168.56.22'
vm_host3 = 'vagrant@192.168.56.23'

ssh_path = '/home/matys/.ssh/id_rsa'

c = Connection(host=vm_host1,
              connect_kwargs={"key_filename": ssh_path})
 
def get_password(connection):
   """function required in all tasks where sudo method is used"""
   sudo_pass = getpass.getpass("What's your sudo password?")
   config = Config(overrides={'sudo': {'password': sudo_pass}})
   connection.config = config

@task
def grafana_deploy_to_one_instance(ctx):
   print(" Deploy solar panel app to instance: " + vm_host1)
   db_name = "inverter_power"
   instal_apps(ctx, c)
   download_influxdb(ctx, c, db_name)
   copy_config_files(ctx, c)
   configure_solar(ctx, c)
   result = c.run('echo complite')
   print(result)

@task
def grafana_deploy_to_many_instance(c):
   hosts = [vm_host1, vm_host2]
   db_host = vm_host3
   db_name = 'inverter_power'
   print(" Deploy solar panel app to instance: " + str(hosts) + " \nDeploy db to " + db_host)

   c = Connection(host=db_host,
       connect_kwargs={"key_filename": ssh_path})
   download_influxdb(c, db_name)

   for c in SerialGroup(hosts):
      instal_apps(c)
      copy_config_files(c)
      configure_solar(c)

@task
def grafana_deploy_split_instance(ctx):
   db_name = "inverter_power"
   print(" Deploy influxdb to instance: " + vm_host1)
   c = Connection(host=vm_host1,
              connect_kwargs={"key_filename": ssh_path})
   download_influxdb(ctx, c, db_name)
   print(" Deploy solar panel app to instance: " + vm_host1)
   c = Connection(host=vm_host2,
              connect_kwargs={"key_filename": ssh_path})
   instal_apps(ctx, c)
   copy_config_files(ctx, c)
   configure_solar(ctx, c)

   print("completed")