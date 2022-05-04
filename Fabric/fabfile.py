from fabric import Connection, task, Config
import getpass
from my_modules import fab_grafana, fab_jenkins, fab_k8s, fab_node, fab_php, fab_python

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
def python_deploy(ctx):
   c.run('uname -s')

@task
def k8s_deploy(ctx):
   c.run('uname -s')

@task
def grafana_deploy(ctx):
   c.run('uname -s')

@task
def jenkins_deploy(ctx):
   c.run('uname -s')