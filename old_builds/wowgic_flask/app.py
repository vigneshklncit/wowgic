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
from flask import Flask
import time
import sys
#import util
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
app = Flask(__name__)
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
generic      = generic.generic()

#==============================================================================#
#           Opening log file to record all the cli outputs                     #
#==============================================================================#
sufFileName = compileFileName()
logFileName  = "/tmp/" + sufFileName + ".log"
logger       = loggerRecord.loggerInit(logFileName,args.logLevel)
logger.debug('Log file# %s & TestBed file ',logFileName)


intercom=intercom.intercom()
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
FlaskRestApi.add_resource(FbUserDetails, '/facebook')
#FlaskRestApi.add_resource(Foo, '/Foo', '/Foo/<str:id>')
#FlaskRestApi.add_resource(Bar, '/Bar', '/Bar/<str:id>')
#FlaskRestApi.add_resource(Baz, '/Baz', '/Baz/<str:id>')

@app.route('/')
def hello():
    return 'Hello Wowgic!'

@app.route('/authorize-instagram')
def authorize_instagram():
    from instagram import client
    client_id = '081ccf9e86164090af417c8ce91cc2e4'
    client_secret = '5b623638585b46cd9d35a203e84114e0'

    redirect_uri = (util.get_host() + url_for('handle_instagram_authorization'))
    instagram_client = client.InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    return redirect(instagram_client.get_authorize_url(scope=['basic']))

@app.route('/handle-instagram-authorization')
def handle_instagram_authorization():
    from instagram import client

    code = request.values.get('code')
    if not code:
        return error_response('Missing code')
    try:
        redirect_uri = (util.get_host() + url_for('handle_instagram_authorization'))
        instagram_client = client.InstagramAPI(client_id=INSTAGRAM_CLIENT, client_secret=INSTAGRAM_SECRET, redirect_uri=redirect_uri)
        access_token, instagram_user = instagram_client.exchange_code_for_access_token(code)
        if not access_token:
            return error_response('Could not get access token')
        g.user.instagram_userid = instagram_user['id']
        g.user.instagram_auth   = access_token
        g.user.save()
        deferred.defer(fetch_instagram_for_user, g.user.get_id(), count=20, _queue='instagram')
    except Exception, e:
        return error_response('Error')
    return redirect(url_for('settings_data') + '?after_instagram_auth=True')

if 'debug' in args.logLevel:
    app.debug = True

if __name__ == '__main__':
    # Get the environment information we need to start the server
    #ip = os.environ['OPENSHIFT_PYTHON_IP']
    #port = int(os.environ['OPENSHIFT_PYTHON_PORT'])
    #host_name = os.environ['OPENSHIFT_GEAR_DNS']
    #app.run(host=ip,port=port)
    app.run()
