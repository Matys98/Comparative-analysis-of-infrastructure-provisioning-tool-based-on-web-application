from fabric import Connection, task, Config
import getpass

def instal_apps(ctx):
    c.run('sudo apt-get update')
    c.run('sudo apt-get install npm -y')
    c.run('sudo apt-get install git -y')

def download_repo(ctx, repo_url):
    c.run('cd /home/$(whoami)')
    c.run('mkdir app')
    c.run('cd /home/$(whoami)/app')
    c.run('git clone ' + repo_url)

def config_node(ctx, repo_dir):
    c.run('cd /home/$(whoami)/app/' + repo_dir)
    c.run('npm install')
    c.run('npm install serve -g')
    c.run('npm install pm2 -g | pm2 update')

def run_app(ctx, app_name):
    c.run('cd /home/$(whoami)/app/my-cv/cv')
    c.run('npm run build')
    c.run('pm2 serve build --name' + app_name)
    c.run('pm2 list')