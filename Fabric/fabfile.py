from fabric import Connection, task, Config
import getpass
from my_modules import fab_git, fab_linux_os, fab_node, fab_python, fab_ruby
from apple_music_module import apple_music
from grafana_module import fab_grafana
from static_page_module import static
from tiquet_module import tiquet


vm_host = 'username@ip_address'
ssh_path = '/path/to/keyfile/id_rsa'

c = Connection(host=vm_host,
              connect_kwargs={"key_filename": ssh_path})
 
def get_password(connection):
   """function required in all tasks where sudo method is used"""
   sudo_pass = getpass.getpass("What's your sudo password?")
   config = Config(overrides={'sudo': {'password': sudo_pass}})
   connection.config = config

@task
def ansible_deploy(ctx):
   c.run('uname -s')

@task
def node_deploy(ctx):
   c.run('uname -s')

@task
def php_deploy(ctx):
   c.run('uname -s')

@task
def grafana_deploy(ctx):
   c.run('uname -s')

@task
def curl_page_response(ctx):
   c.run('curl localhost')
