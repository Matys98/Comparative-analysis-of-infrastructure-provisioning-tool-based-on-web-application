from fabric import Connection, task, Config, SerialGroup
import getpass
from tiquet_module import tiquet

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
def tiquet_deploy_to_one_instance(c):
   print(" Deploy solar panel app to instance: " + vm_host1)
   app_name = "tiquet"
   instal_apps(c)
   config_app(c)
   config_db(c)
   config_backend(c)
   run_backend(c, app_name)
   config_frontend(c)
   run_frontend(c, app_name)

@task
def tiquet_deploy_to_many_instance(c):
   fronend_host = vm_host1
   backend_host = vm_host2
   db_host = vm_host3
   app_name = "tiquet"

   print(" Deploy " + app_name + " frontend to instance:" + fronend_host)
   print(" Deploy " + app_name + " backendend to instance:" + backend_host)
   print(" Deploy " + app_name + " data base to instance:" + db_host)

   # Connecting to Data base instance
   c = Connection(host=db_host,
       connect_kwargs={"key_filename": ssh_path})
   instal_apps(c)
   config_db(c)

   # Connecting to Backend instance
   c = Connection(host=backend_host,
       connect_kwargs={"key_filename": ssh_path})
   instal_apps(c)
   config_app(c)
   config_backend(c)
   run_backend(c, app_name)

   # Connecting to Frontend instance
   c = Connection(host=fronend_host,
       connect_kwargs={"key_filename": ssh_path})
   instal_apps(c)
   config_app(c)
   config_frontend(c)
   run_frontend(c, app_name)