import os
DEBUG = True
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = 'puthuPonnuKurichi88921satheesh41137'
#os.environ['SPARK_HOME'] = '/home/satheesh/spark-1.6.0-bin-hadoop2.6'
#Get the environment information we need to start the server
HOST_NAME = os.environ.get('HOSTNAME','localhost')
APP_NAME = 'wowgicFlaskApp'
IP = os.uname()[1]
NEO4J_IP='127.0.0.1'
PORT = 7777
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = '27017'
MONGODB_USERNAME = 'admin'
MONGODB_PASSWORD = '8ygFBXZHeIW6'
LOGGER_NAME='wowgic_dev'
