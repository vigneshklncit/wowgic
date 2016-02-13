import os
DEBUG = True
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = 'puthuPonnuKurichi88921satheesh41137'
os.environ['SPARK_HOME'] = '/home/satheesh/spark-1.6.0-bin-hadoop2.6'
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
