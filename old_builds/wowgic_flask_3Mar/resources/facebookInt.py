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
    fbGraph = None
    def get_facebook_oauth_token(self):
        '''fetch the auth token from mongodb and have it here if it about to expire please extend it'''
        #atleast 1 user has to be authenticated and user token has to stored for future use
        fbaccessToken = 'CAAILXMdVJpIBAF1YmD3JRclt68wUJgPIxRZApq9R81vI4daAzy9Sy7hg02RiSE5RlAH1D2CnVMLB51fTMLiPBjn28oN6QWJbhZBmFmK3tyKsa2yqlOZBbLJmRjKtM1G9lZBMZBZBhztAlpooEw2qef5r68yYjYnKtVDflVdhwfjk9xt6EeDxHZBxHHMSSuFBqOle0v6NUuqKgZDZD'
        #globalS.dictDb['fbToken'] = session.get('facebook_token')
        globalS.dictDb['fbToken'] = fbaccessToken
        return globalS.dictDb['fbToken']

    def __init__(self):
        #connect to the API
        if self.fbGraph is None:
            logger.debug('fbgraph is intialised')
            self.fbGraph = GraphAPI(self.get_facebook_oauth_token())

    def getIdLocation(self,id):
        ''' do a rest api for facebook fetching the page location details'''
        #https://lookup-id.com/
        #self.initializeGraph()
        data = {}
        logger.debug('facepy get request for location :%s',id)
        path = str(id)+'?fields=location'
        try:
            data = self.fbGraph.get(path)
        except Exception as e:
            logger.error('facepy raised exception in :%s',e)
        #logger.debug('my data from facebook:%s',data)
        # retrive the access_token from mongoDb
        return data

    def extendOauthToken(self):
        '''this just generates an extended access token so that it lasts 60 days
        '''
        #Returns a tuple with a string describing the extended access token and a datetime instance describing when it expires.
        extended_oauth_token = utils.get_extended_access_token(oauth_token[0],globalS.dictDb['FACEBOOK_APP_ID'],globalS.dictDb['FACEBOOK_APP_SECRET'])
        logger.debug('extended_oauth_token:%s',extended_oauth_token)
        return
