import os
from celery.schedules import crontab

CELERY_BROKER_URL='amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'mongodb://localhost:27017/'
CELERY_MONGODB_BACKEND_SETTINGS = {
        'database': 'wowgicflaskapp',
        'taskmeta_collection': 'my_taskmeta_collection',
    }
#CELERY_ACCEPT_CONTENT = ['pickle', 'json']
#CELERY_TASK_SERIALIZER='json'
#CELERY_RESULT_SERIALIZER='json'
#CELERY_TIMEZONE='Europe/Oslo'
CELERY_ENABLE_UTC=True
IP = os.uname()[1]
PORT = 8080
NEO4J_IP='127.0.0.1'
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = '27017'
MONGODB_USERNAME = 'admin'
MONGODB_PASSWORD = '8ygFBXZHeIW6'
LOGGER_NAME='wowgic_dev'
CELERYBEAT_SCHEDULE =   {# Executes every Monday morning at 7:30 A.M
    'getAllInterestNode_every15mins': {
    'task': 'tasks.getAllInterestNode',
    'schedule': crontab(minute='*/15'),
        },
    }