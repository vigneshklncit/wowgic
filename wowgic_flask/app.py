#! /usr/bin/python
#===============================================================================
# File Name      : app.py
# Date           : 12-02-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    :
# How to run     :twit_test.py -l info
#                :twit_test.py -h
#===============================================================================
from flask_restful import fields, marshal_with, reqparse, Resource, Api
from flask import url_for, request, session, redirect, Flask , flash
import time
import sys
import os
import argparse
sys.path.append('common')
sys.path.append('resources')
import globalS
import generic
import loggerRecord
import intercom
import json

#from bson import ObjectId
#
#class JSONEncoder(json.JSONEncoder):
#    def default(self, o):
#        if isinstance(o, ObjectId):
#            return str(o)
#        return json.JSONEncoder.default(self, o)


#parse the run-time args passed
parser = argparse.ArgumentParser(description='  To get the mra.log,rc.log,\
        qpTraces & tcpdump to the log viewer machine or any user defined server\
        all in one place with a single click. Works among multiple Active Pairs \
        (MPE\'s, MRA\'s)..................................................\
        Example: ./app CAM-92410 -c serverRack_C6GRsetup.cfg or ./loggy \
        CAM-92410 or ./app -v ',add_help=True)
#parser.add_argument('testName',help='Name suffixed to log file name generated')
#if the def file is not passed as arg thn take the default file.
parser.add_argument('-c', '--config',default='serverRack.def',help='definition file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.3')
parser.add_argument("-l", "--logLevel",default='error',help="Enable standard output verbosity")
args = parser.parse_args()
#create a flask app
app = Flask(__name__,instance_relative_config=True)
# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
app.config.from_envvar('APP_CONFIG_FILE')
FlaskRestApi = Api(app) #creating a flask-restfull api

############################################################################
#Function Name  : compileFileName                                          #
#Input          : Nil                                                      #
#Return Value   : just sets the suffix fileName for logs                   #
############################################################################
def compileFileName():
    dayTime      = generic.dateTimeFields()
    dayTime      = 'wowgic'+'_'+dayTime
    return dayTime
############################################################################

globalS.init()#intialize the global variables
globalS.dictDb = app.config
generic      = generic.generic()

#==============================================================================#
#           Opening log file to record all the cli outputs                     #
#==============================================================================#
sufFileName = compileFileName()
logFileName  = "/tmp/" + sufFileName + ".log"
logger,fhandler       = loggerRecord.loggerInit(logFileName,args.logLevel)
logger.debug('Log file# %s & TestBed file',logFileName)
logger.debug('global dictDB file# %s',globalS.dictDb['MONGODB_PASSWORD'])
#logger.debug('global app file# %s',app.config)

app.logger.addHandler(fhandler) #associate the app logger with general logger
app.logger_name = loggerRecord.get_logger() #associate the app logger with general logger
intercom=intercom.intercom()
#FbUserDetails is for testing the app
class FbUserDetails(Resource):
    def get(self):
        #facbook tmp input given by chella ltr retrive from app and give as inpu to this variable
        ####
        #Satheesh
        jsonFBInput = '{"id":"1240560189303114","name":"Mari Satheesh","hometown":{"id":"106076206097781","name":"Madurai, India"},"location":{"id":"106377336067638","name":"Bangalore, India"},"education":[{"school":{"id":"135521326484377","name":"Cathy Matriculationn Higher Secondary School"},"type":"High School"},{"school":{"id":"131854716845812","name":"KLN College of Engineering"},"type":"College"},{"school":{"id":"112188602140934","name":"kln"},"type":"College"}],"work":[{"employer":{"id":"114041451939962","name":"Sonus Networks"}}]}'
        ####
        #Vivek Su
        #jsonFBInput ='{"id":"858104450925382","name":"Vivek Subburaju","hometown":{"id":"106076206097781","name":"Madurai, India"},"location":{"id":"106078429431815","name":"London, United Kingdom"},"education":[{"school":{"id":"140607792619596","name":"Mahatma Montessori Matriculation Higher Secondary School"},"type":"High School"},{"school":{"id":"6449932074","name":"Royal Holloway, University of London"},"type":"College"},{"concentration":[{"id":"105415696160112","name":"International Business"}],"school":{"id":"107951082570918","name":"LIBA"},"type":"College","year":{"id":"144044875610606","name":"2011"}},{"school":{"id":"107927999241155","name":"Loyola College Chennai"},"type":"College","year":{"id":"137616982934053","name":"2006"}}],"work":[{"employer":{"id":"400618623480960","name":"Onestep Solutions Debt Recovery Software"},"position":{"id":"1002495616484486","name":"Principal Consultant- Data Quality"},"start_date":"2015-12-15"},{"end_date":"2014-12-31","employer":{"id":"134577187146","name":"Cognizant"},"start_date":"2013-01-01"},{"end_date":"2013-01-01","employer":{"id":"177419101744","name":"Pearson English Business Solutions"},"location":{"id":"102186159822587","name":"Chennai, India"},"start_date":"2011-01-01"},{"end_date":"2011-01-01","employer":{"id":"108134792547341","name":"Tata Consultancy Services"},"start_date":"2008-01-01"},{"end_date":"2008-01-01","employer":{"id":"42189185115","name":"Wipro"},"start_date":"2006-01-01"}]}'
        feeds = intercom.createUserNode(jsonFBInput)

        #feeds=json.dumps(dict(feeds))
        #logger.debug('feed is %s',feeds)
        #return JSONEncoder().encode(feeds)
        for feed in feeds:
            #feed=json.loads(json.dumps(feed))
            logger.debug('feed twitter text is#%s',feed.text)
            return feed
        #return "type error"

class Departmental_Salary(Resource):
    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("select * from salaries where Department='%s'"%department_name.upper())
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
        #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient

FlaskRestApi.add_resource(Departmental_Salary, '/dept/<string:department_name>')
#FlaskRestApi.add_resource(FbUserDetails, '/facebook')
#FlaskRestApi.add_resource(Foo, '/Foo', '/Foo/<str:id>')
#FlaskRestApi.add_resource(Bar, '/Bar', '/Bar/<str:id>')
#FlaskRestApi.add_resource(Baz, '/Baz', '/Baz/<str:id>')

@app.route('/')
def hello():
    flash('data + play + magic = WOwgic')
    return 'Hello Wowgic!'

#------------------------------------------------------------------------------#
#                   instagram authentication                                   #
#------------------------------------------------------------------------------#

@app.route('/instagram_login')
def instagram_login():
    return intercom.instagram_login()

@app.route('/handle_instagram_authorization')
def handle_instagram_authorization():
    flash('You were successfully logged in via INSTAGRAM')
    return intercom.handle_instagram_authorization()
#-------------------------------------------------------------------------------
# facebook authentication
#-------------------------------------------------------------------------------

@app.route('/facebook_login')
def facebook_login():
    return intercom.facebook_login()

@app.route('/login/authorized')
#@facebook.authorized_handler
def facebook_authorized(resp):
    flash('You were successfully logged in via INSTAGRAM')
    return intercom.facebook_authorized(resp)

if 'debug' in args.logLevel:
    app.debug = True

if __name__ == '__main__':
    # Get the environment information we need to start the server
    #ip = os.environ['OPENSHIFT_PYTHON_IP']
    #port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    #host_name = os.environ['OPENSHIFT_GEAR_DNS']
    #app.run(host=app.config.get('IP'),port=app.config.get('PORT'))
    app.run(host=globalS.dictDb['IP'],port=app.config.get('PORT'))
    #app.run()
