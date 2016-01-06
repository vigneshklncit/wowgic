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
#from flask_restful import fields, marshal_with, reqparse, Resource, Api
from flask import url_for, request, session, redirect, Flask , flash, jsonify
from flask_oauth import OAuth
import time
import sys
import json
import argparse
sys.path.append('common')
sys.path.append('resources')
import globalS
import generic
import loggerRecord

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

#app.logger.addHandler(fhandler) #associate the app logger with general logger
app.logger_name = loggerRecord.get_logger() #associate the app logger with general logger
import intercom
intercom=intercom.intercom()

@app.route('/')
def hello():
    ''' this is just to check the index url is working '''
    #flash('') # this requires a rendering HTNL templete
    return 'Hello Wowgic! Here data + play + magic'

#change the url & in production we have to remove the try catch remove GET in production
@app.route('/testing',methods=['GET', 'POST'])
def testing():
    feedList =[]
    #facbook tmp input given by chella ltr retrive from app and give as inpu to this variable
    ####
    #Vivek Su
    jsonFBInput = '{"id":"1240560189303114","name":"Mari Satheesh","hometown":{"id":"106076206097781","name":"Madurai, India"},"location":{"id":"106377336067638","name":"Bangalore, India"},"education":[{"school":{"id":"135521326484377","name":"Cathy Matriculationn Higher Secondary School"},"type":"High School"},{"school":{"id":"131854716845812","name":"KLN College of Engineering"},"type":"College"},{"school":{"id":"112188602140934","name":"kln"},"type":"College"}],"work":[{"employer":{"id":"114041451939962","name":"Sonus Networks"}}]}'
    #jsonFBInput ='{"id":"858104450925558","name":"Vivek Subburaju","hometown":{"id":"106076206097781","name":"Madurai, India"},"location":{"id":"106078429431815","name":"London, United Kingdom"},"education":[{"school":{"id":"140607792619596","name":"Mahatma Montessori Matriculation Higher Secondary School"},"type":"High School"},{"school":{"id":"6449932074","name":"Royal Holloway, University of London"},"type":"College"},{"concentration":[{"id":"105415696160112","name":"International Business"}],"school":{"id":"107951082570918","name":"LIBA"},"type":"College","year":{"id":"144044875610606","name":"2011"}},{"school":{"id":"107927999241155","name":"Loyola College Chennai"},"type":"College","year":{"id":"137616982934053","name":"2006"}}],"work":[{"employer":{"id":"400618623480960","name":"Onestep Solutions Debt Recovery Software"},"position":{"id":"1002495616484486","name":"Principal Consultant- Data Quality"},"start_date":"2015-12-15"},{"end_date":"2014-12-31","employer":{"id":"134577187146","name":"Cognizant"},"start_date":"2013-01-01"},{"end_date":"2013-01-01","employer":{"id":"177419101744","name":"Pearson English Business Solutions"},"location":{"id":"102186159822587","name":"Chennai, India"},"start_date":"2011-01-01"},{"end_date":"2011-01-01","employer":{"id":"108134792547341","name":"Tata Consultancy Services"},"start_date":"2008-01-01"},{"end_date":"2008-01-01","employer":{"id":"42189185115","name":"Wipro"},"start_date":"2006-01-01"}]}'
    data = request.data
    try:
        jsonFBInput = json.loads(data)
    except:
        ####
        #Satheesh
        jsonFBInput = json.loads(jsonFBInput)
    feedList.extend(intercom.facebook_authorized(jsonFBInput))
    #intercom.getMydata()
    #feedList.append(intercom.retrieveMediaBasedTags())
    #flash('just for testing')
    return json.dumps(feedList)

@app.route('/refreshUserFeeds',methods=['GET','POST'])
def refreshUserFeeds():
    ''' after first time login of user this gets invoked by an ID provided by UI
    like Request: https://http://wowgicflaskapp-wowgic.rhcloud.com/id=q13512667
    neo4j has associated feeds ID to be displayed to the user fetch them from mongdb and return it back
    '''
    try:
        ID = resp['id']
    except:
        ID="858104450925558"
    logger.debug('ID posted:%s',ID)
    feedList =[]
    feedList.extend(intercom.fetchNeo4jInterestNode(ID))
    return json.dumps(feedList)

@app.route('/locationFeeds',methods=['POST'])
def locationFeeds():
    ''' Based on location and user provided radius lets retrive the tweets
    '''
    geoData = request.data
    geoDict = json.loads(geoData)
    logger.debug('geoData posted:%s',geoDict)
    feedList =[]
    feedList.extend(intercom.retrieveLocationBasedTags(geoDict))
    return json.dumps(feedList)
#------------------------------------------------------------------------------#
#                   instagram authentication                                   #
#------------------------------------------------------------------------------#

@app.route('/instagram_login')
def instagram_login():
    return intercom.instagram_login()

@app.route('/_handle_instagram_authorization')
def _handle_instagram_authorization():
    #flash('You were successfully logged in via INSTAGRAM')
    return intercom.handle_instagram_authorization()
#-------------------------------------------------------------------------------
# facebook authentication
#-------------------------------------------------------------------------------
# To get an access token to consume the API on behalf of a user, use a suitable OAuth library for your platform
globalS.dictDb['FACEBOOK_APP_ID'] = '575443062564498'
globalS.dictDb['FACEBOOK_APP_SECRET'] = '3112a499e27dcd991b9869a5dd5524c0'
oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=globalS.dictDb['FACEBOOK_APP_ID'],
    consumer_secret=globalS.dictDb['FACEBOOK_APP_SECRET'],
    request_token_params={'scope': 'email'}
)

@app.route('/facebook_login')
def facebook_login():
    return facebook.authorize(callback=url_for('_facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler #this decorator passes the req as response below
def _facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    me.data['fb_oauth_token'] = session['oauth_token']
    globalS.dictDb['fb_oauth_token'] = session['oauth_token']
    intercom.facebook_authorized(me.data)
    return 'Logged in as me=%s me.data=%s redirect=%s' % \
        (me, me.data, request.args.get('next'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')

''' below is not required
#-------------------------------------------------------------------------------
# twitter authentication
#-------------------------------------------------------------------------------
# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1.1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key= 'HwvpHtsPt3LmOZocZXwtn72Zv',
    consumer_secret = 'afVEAR0Ri3ZluVItqbDi0kfm7BHSxjwRXbpw9m9kFhXGjnzHKh'
)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

@app.route('/twitLoginCheck')
def twitLoginCheck():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('twitterLogin'))
    access_token = access_token[0]
    #return render_template('index.html')
    return 0

@app.route('/twitterLogin')
def twitterLogin():
    return twitter.authorize(callback=url_for('twitOauthAuthorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/twitterLogout')
def twitterLogout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('twitLoginCheck'))

@app.route('/twitOauthAuthorized')
@twitter.authorized_handler
def twitOauthAuthorized(resp):
    #resp = twitter.authorized_response()
    logger.debug('twitter resp:%s',resp)
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['twitter_oauth'] = resp
    return 'twitter authorized'
'''
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
