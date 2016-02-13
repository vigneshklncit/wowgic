# start.sh
export SPARK_HOME=/home/satheesh/spark-1.6.0-bin-hadoop2.6
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
#export APP_CONFIG_FILE=../config/development.py
export APP_CONFIG_FILE=../config/production.py
#service mongod start
python app.py -l debug
