import os
DEBUG = True
TESTING = True
APP_DEBUG = True
PROPAGATE_EXCEPTIONS = True
TRAP_BAD_REQUEST_ERRORS = True
#os.environ['SPARK_HOME'] = '/home/satheesh/spark-1.6.0-bin-hadoop2.6'
#Get the environment information we need to start the server
HOST_NAME = os.environ.get('HOSTNAME','localhost')
APP_NAME = 'wowgicFlaskApp'
IP = os.uname()[1]
NEO4J_IP='127.0.0.1'
PORT = 7777
LOGGER_NAME='wowgic_dev'
#t_consumer_key= 'HwvpHtsPt3LmOZocZXwtn72Zv'
#service mongod start
#/root/Downloads/neo4j-community-2.3.1/bin/neo4j start
#celery -A tasks worker -l debug -B
#cd /home/satheesh/umongo-linux-all_1-6-2/