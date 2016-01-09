import os
DEBUG = True
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.environ.get('SECRET_KEY','\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16')
#Get the environment information we need to start the server
HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS','127.0.0.1')
APP_NAME = os.environ.get('OPENSHIFT_APP_NAME','flask')
IP = os.environ.get('OPENSHIFT_PYTHON_IP','127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT',8080))
MONGODB_HOST = os.environ.get('OPENSHIFT_MONGODB_DB_HOST','127.0.0.1')
MONGODB_PORT = os.environ.get('OPENSHIFT_MONGODB_DB_PORT','27017')
MONGODB_USERNAME = 'admin'
MONGODB_PASSWORD = '8ygFBXZHeIW6'
LOGGER_NAME='wowgic_dev'
