from fabric.api import *
import os
import subprocess
import time
import sys

PROJECT_NAME = '{{project_name}}'

def install():
	local('bower install')
	virtualenv()
	
def reset_db():
	try:
		local('psql -h localhost -c "drop database %s"' % PROJECT_NAME)
	except:
		pass
	local('psql -h localhost -c "create database %s"' % PROJECT_NAME)
	local('python manage.py syncdb --noinput --no-initial-data')
	local('python manage.py createsuperuser --username admin --email admin@%s.com' % PROJECT_NAME)
	local('python manage.py syncdb --noinput')
	local('python manage.py migrate')

def heroku():
	local('git init')
	prepare('Heroku initial commit')
	local('heroku create')
	local('git push heroku master')
	local('heroku ps:scale web=1')
	heroku_setup()

def heroku_add_remote():
	appname = raw_input('Enter app name to connect to:')
	venv('git remote add heroku git@heroku.com:%s.git' % appname)

def heroku_reset_db():
	local('heroku pg:reset DATABASE_URL')
	local('heroku run python manage.py syncdb')
	local('heroku run python manage.py migrate')

def rename_heroku():
	name = raw_input('Enter new app name:') 
	local('heroku apps:rename %s' % name)

def compile_less():
	try:
		local('lessc {0}/static/css/style.less {0}/static/css/style.css -w -x'.format(PROJECT_NAME))
	except:
		pass

def prepare(commit_message=None):
	compile_less()
	if not commit_message:
		commit_message = raw_input('Enter git commit message:')
	local("git add -A && git commit -m '%s'" % commit_message)
	local("heroku config:add DJANGO_SETTINGS_MODULE=%s.settings.production" % PROJECT_NAME)
	#local("git push")

def restore_db():
	dump_file = raw_input("Enter dump file:")
	if not dump_file:
		dump_file = "b001.dump"
	try:
		local('psql -h localhost -c "drop database %s"' % PROJECT_NAME)
	except:
		pass
	local('psql -h localhost -c "create database %s"' % PROJECT_NAME)
	local("/Applications/Postgres.app/Contents/MacOS/bin/pg_restore --verbose --clean --no-acl --no-owner -h localhost -d %s %s" % (PROJECT_NAME, dump_file))
	local("python manage.py clearsessions")
	
def heroku_setup():
	# Config variables
	#local('heroku config:add DEBUG=False')
	#local('heroku config:add STATIC_URL=http://cdn.fanaticahosting.com/%s/' % PROJECT_NAME)
	# Standard add-ons
	local("heroku addons:add memcachier:dev")


def push(no_static=False):
	local("git push heroku master")
	if not no_static:
		local("heroku run python manage.py collectstatic --noinput -i admin")
	local("heroku run python manage.py compress --force")
	local("heroku run python manage.py clearsessions")

def deploy():
	prepare()
	push()

def deploy_no_static():
	prepare()
	push(True)

def virtualenv():
	# Create virtualenv
	subprocess.call(["virtualenv", "venv", "--distribute"])
	venv('pip install -r requirements.txt')
	venv("pip freeze > requirements.txt")

def venv(command):
	source = 'source venv/bin/activate && '
	subprocess.call(source + command, shell=True)