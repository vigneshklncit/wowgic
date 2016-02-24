import os
DEBUG = True
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = 'puthuPonnuKurichi88921satheesh41137'
#SECRET_KEY = os.environ.get('SECRET_KEY','\xfb\x13\xdf\xa1@i\xd6>V\xc0\xbf\x8fp\x16#Z\x0b\x81\xeb\x16')
#Get the environment information we need to start the server
HOST_NAME = os.environ.get('HOSTNAME','localhost')
APP_NAME = 'wowgicFlaskApp'
IP = os.uname()[1]
NEO4J_IP='127.0.0.1'
PORT = 8080
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = '27017'
MONGODB_USERNAME = 'admin'
MONGODB_PASSWORD = '8ygFBXZHeIW6'
LOGGER_NAME='wowgic_dev'
