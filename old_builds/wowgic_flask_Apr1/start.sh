# start.sh
#export SPARK_HOME=/home/satheesh/spark-1.6.0-bin-hadoop2.6
#export SPARK_HOME=/home/ec2-user/spark-1.6.0-bin-hadoop2.6/
#export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export APP_CONFIG_FILE=../config/development.py
#export CELERY_CONFIG_FILE=../instance/flaskapp.cfg
#export CELERY_CONFIG_FILE=../config/development.py
export C_FORCE_ROOT=True
#export APP_CONFIG_FILE=../config/production.py
#service rabbitmq-server start
python app.py -l debug
#uwsgi dragon.ini
#celery -A tasks worker -l info -B
#flower -A tasks --port=5555
