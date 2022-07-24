from fabric import Connection, task, Config, SerialGroup
import getpass

# from static_page_module/static.py import *
# from static import *

def instal_apps(ctx):
    c.sudo('apt-get update')
    c.sudo('apt-get install npm -y')
    c.sudo('apt-get install git -y')


def download_repo(ctx, repo_url):
   #  c.run('cd /home/$(whoami)')
    c.run('mkdir /home/$(whoami)/app || echo "app exist"')
    with c.cd('/home/$(whoami)/app/'):
      c.run('git clone ' + repo_url)
      

def config_node(ctx, repo_dir):
    with c.cd('/home/$(whoami)/app/my-cv/cv/'):
      c.run('npm install')
      c.sudo('npm install serve -g')
      c.sudo('npm install pm2 -g')
      c.run('pm2 update')

def run_app(ctx, app_name):
    with c.cd('/home/$(whoami)/app/my-cv/cv/'):
      c.run('npm run build')
      result = c.run('cp -r /build/static/ /build/my-cv/ | ls -la /build/static/')
      print(result)
      c.run('pm2 serve build --name ' + app_name)
      c.run('pm2 list')

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
def test(ctx):
   result = c.run('echo complite > test.txt | whoami')
   print(result)

@task
def static_deploy_to_one_instance(ctx):
   print(" Deploy static app to instance: " + vm_host1)

   repo_url = 'https://github.com/Matys98/my-cv.git'
   repo_dir = 'my-cv/cv/'
   app_name = 'web-app'

   instal_apps(ctx)
 
   download_repo(ctx, repo_url)
   
   config_node(ctx, repo_dir)
 
   run_app(ctx, app_name)

   result = c.run('echo complite')
   print(result)

@task
def static_deploy_to_many_instances(ctx):
   
   print(" Deploy static app to instance: " + str(hosts))
   repo_url = 'https://github.com/Matys98/my-cv.git'
   repo_dir = 'my-cv/cv'
   app_name = 'web-app'
   result = ['']
   i = 0
   for c in SerialGroup(hosts):
      instal_apps(ctx)
      clone_repo(ctx, repo_url)
      config_node(ctx, repo_dir)
      run_app(ctx, str(app_name + i))
      result.append(c.run('echo complite'))
      i=+1
   print(result)