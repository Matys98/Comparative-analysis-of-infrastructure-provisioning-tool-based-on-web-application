from fabric import Connection, task, Config, SerialGroup
import getpass
from grafana_module import *

repo_name = ''
repo_dir = ''
app_name = ''

vm_host1 = 'vagrant@192.168.56.21'
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
def grafana_deploy_to_one_instance(c):
   print(" Deploy solar panel app to instance: " + vm_host1)
   instal_apps(c)
   download_influxdb(c, db_name)
   copy_config_files(c)
   configure_solar(c)

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