from fabric import Connection, task, Config
import getpass

def instal_apps(c):
    c.run('apt-get update')
    c.run('apt-get install npm -y')
    c.run('apt-get install git -y')

def dow(c, repo_url):
    c.run('cd ')
    c.run('mkdir app')
    c.run('cd app')
    c.run('git clone ' + repo_url)

def config_node(c, repo_dir):
    c.run('cd ' + repo_dir)
    c.run('npm install')
    c.run('npm install serve -g')
    c.run('npm install pm2 -g | pm2 update')

def run_app(c, app_name):
    c.run('npm run build')
    c.run('pm2 serve build --name' + app_name)
    c.run('pm2 list')