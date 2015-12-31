#! /usr/bin/python
#===============================================================================
# File Name      : facebookInt.py
# Date           : 12-22-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
import sys
sys.path.append('../common')
import loggerRecord, globalS
from facepy import utils, GraphAPI
logger =  loggerRecord.get_logger()


class facebookInt:
    ''' bla bla
    '''
    def get_facebook_oauth_token(self):
        globalS.dictDb['fbToken'] = session.get('facebook_token')
        return globalS.dictDb['fbToken']

    #connect to the API
#graph = GraphAPI(extended_token)
#https://lookup-id.com/
#group_id = str(286829698078211)
#data = graph.get(group_id + "/feed", page=False, retry=3, limit=5)
#comments = graph.get(post['id'] + '/comments', page=False, retry=3, limit=1)
#this just generates an extended access token so that it lasts 60 days
## retrive the access_token from mongoDb
#Returns a tuple with a string describing the extended access token and a datetime instance describing when it expires.
#extended_oauth_token = utils.get_extended_access_token(oauth_token[0],FACEBOOK_APP_ID,FACEBOOK_APP_SECRET)