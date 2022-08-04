from fabric import Connection, task, Config, SerialGroup
import getpass

# from static_page_module/static.py import *
# from static import *

def instal_apps(ctx, c):
    c.sudo('apt-get update')
    c.sudo('apt-get install npm -y')
    c.sudo('apt-get install git -y')
    print("instal_apps_fin")

def download_repo(ctx, c, repo_url):
   #  c.run('cd /home/$(whoami)')
    c.run('mkdir /home/$(whoami)/app || echo "app exist"')
    with c.cd('/home/$(whoami)/app/'):
      c.run('git clone ' + repo_url)
    print("download_repo_fin")

def config_node(ctx, c, repo_dir):
    with c.cd('/home/$(whoami)/app/my-cv/cv/'):
      c.run('npm install')
      c.run('sudo npm install serve -g')
      c.run('sudo npm install pm2 -g')
      # c.run('pm2 update')
    print("config_node_fin")

def run_app(ctx, c, app_name):
    with c.cd('/home/$(whoami)/app/my-cv/cv/'):
      c.run('npm run build')
      # result = c.run('cp -r /build/static/ /build/my-cv/ | ls -la /build/static/')
      print("run_fin")
      c.run('pm2 serve build --name ' + app_name)
      c.run('pm2 list')

repo_name = ''
repo_dir = ''
app_name = ''

vm_host1 = 'vagrant@192.168.56.21'
vm_host2 = 'vagrant@192.168.56.22'
vm_host3 = 'vagrant@192.168.56.23'

ssh_path = '/home/matys/.ssh/id_rsa'
 
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

   c = Connection(host=vm_host1,
              connect_kwargs={"key_filename": ssh_path})

   repo_url = 'https://github.com/Matys98/my-cv.git'
   repo_dir = 'my-cv/cv/'
   app_name = 'web-app'

   instal_apps(ctx, c)
   download_repo(ctx, c, repo_url)
   config_node(ctx, c, repo_dir)
   run_app(ctx, c, app_name)
   result = c.run('echo complite')
   print(result)

@task
def static_deploy_to_many_instances(ctx):
   vm_host1 = '192.168.56.21'
   vm_host2 = '192.168.56.22'
   vm_host3 = '192.168.56.23'
   hosts = [vm_host1, vm_host2, vm_host3]   
   print(" Deploy static app to instance: " + str(hosts))
   repo_url = 'https://github.com/Matys98/my-cv.git'
   repo_dir = 'my-cv/cv'
   app_name = 'web-app'
   result = ['']
   i = 0
   for c in SerialGroup(vm_host1, vm_host2, vm_host3, user="vagrant", 
                        port=22, connect_kwargs={"key_filename": ssh_path}):
      instal_apps(ctx, c)
      download_repo(ctx, c, repo_url)
      config_node(ctx, c, repo_dir)
      run_app(ctx, c, app_name + str(i))
      result.append(c.run('echo complite'))
      i=+1
      c.close()
   print(result)