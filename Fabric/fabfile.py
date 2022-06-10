from fabric import Connection, task, Config, SerialGroup
import getpass
from grafana_module import *
from static_page_module import *
from tiquet_module import tiquet

repo_name = ''
repo_dir = ''
app_name = ''

vm_host1 = 'username@ip_address'
vm_host2 = 'username@ip_address'
vm_host3 = 'username@ip_address'

ssh_path = '/path/to/keyfile/id_rsa'

c = Connection(host=vm_host1,
              connect_kwargs={"key_filename": ssh_path})
 
def get_password(connection):
   """function required in all tasks where sudo method is used"""
   sudo_pass = getpass.getpass("What's your sudo password?")
   config = Config(overrides={'sudo': {'password': sudo_pass}})
   connection.config = config


@task
def static_deploy_to_one_instance(c):
   print(" Deploy static app to instance: " + vm_host1)
   repo_url = 'https://github.com/Matys98/my-cv.git'
   repo_dir = 'my-cv/cv'
   app_name = 'web-app'
   result = ""
   instal_apps(c)
   clone_repo(c, repo_url)
   config_node(c, repo_dir)
   run_app(c, app_name)
   result = c.run('echo complite')
   print(result)

@task
def static_deploy_to_many_instances(c):
   
   print(" Deploy static app to instance: " + str(hosts))
   repo_url = 'https://github.com/Matys98/my-cv.git'
   repo_dir = 'my-cv/cv'
   app_name = 'web-app'
   result = ['']
   i = 0
   for c in SerialGroup(hosts):
      instal_apps(c)
      clone_repo(c, repo_url)
      config_node(c, repo_dir)
      run_app(c, str(app_name + i))
      result.append(c.run('echo complite'))
      i=+1
   print(result)

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

@task
def tiquet_deploy_to_one_instance(c):
   c.run('uname -s')

@task
def tiquet_deploy_to_many_instance(c):
   c.run('uname -s')