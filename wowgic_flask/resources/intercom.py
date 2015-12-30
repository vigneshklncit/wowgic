#! /usr/bin/python
#===============================================================================
# File Name      : intercom.py
# Date           : 12-02-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    :
# How to run     :twit_test.py -l info
#                :twit_test.py -h
#===============================================================================
import sys
sys.path.append('common')
sys.path.append('resources')
import globalS
import json
import generic
import neo4jInterface
import mongoInt
import twitterInt
import instagramInt
import facebookInt
import loggerRecord
logger =  loggerRecord.get_logger()


twitterInt = twitterInt.twitterInt()
instagramInt = instagramInt.instagramInt()
facebookInt = facebookInt.facebookInt()
neo4jInt = neo4jInterface.neo4jInterface()
graphDB=neo4jInt.connect()
#graphDB=neo4jInt.connect('localhost:7474/db/data/','neo4j','admin')
####
# End of boilerplate, interesting code starts here:
neo4jInt.createConstraint(graphDB)
mongoInt=mongoInt.mongoInt()

class intercom:
    ''' this file act as a intercaller /router / flow chart whaterver you call. T o& fro
    calling functions interworking between verious interfaces like twitter, Instagram,
    facebook , neo4j & mongoDB lies from here
    '''
    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        mconnect = mongoInt.connect()
        #authenticate twitter app


    def createUserNode(self,decodedFBJson):
        '''
        '''
        #decodedFBJson=json.loads(decodedFBJson)
        if mongoInt.insertFBUserLoginData(decodedFBJson):
            neo4jInt.createUserNode(graphDB,decodedFBJson,'user')
            interestList = ['hometown','location','work','education']
            for int in interestList:
                neo4jInt.createInterestNode(graphDB,decodedFBJson,int)
        else:
            logger.debug('user already exists hence skipping the neo4J creation of nodes & interest')
        #once the nodes are created lets fetch the feeds
        return 1

    def retrieveTweets(self):
        '''retrieveTweetsBasedHashtag
        '''
        passCnt = 0
        neo4jInt.showInterestNode(graphDB)
        twits = twitterInt.retrieveTweetsBasedHashtag()
        passCnt += mongoInt.insertFeedData(twits)
        logger.debug('retrieve tweets')
        #page_sanitized = json_util.dumps(twits)
        return twits

    def instagram_login(self):
        ''' bypasser for instagram login
        '''
        return instagramInt.instagram_login()

    def retrieveMediaBasedTags(self):
        '''
        '''
        passCnt = 0
        feedJson = instagramInt.retrieveMediaBasedTags()
        #feedJson = json.loads(feedJson)
        passCnt += mongoInt.insertFeedData(feedJson)
        return feedJson


    def handle_instagram_authorization(self):
        '''
        '''
        passCnt = 0
        user=instagramInt.handle_instagram_authorization()
        passCnt += mongoInt.insertInstagramUserLoginData(user)
        return "Thanks buddy ! Instagram is authorized"

    def facebook_authorized(self,userJson):
        '''
        '''
        passCnt = 0
        #store the user data along with access_token
        #logger.debug('userJson:%s',userJson)
        try:
            userJson=json.loads(userJson)
        except:
            pass #while passing json directly this is not reqd in production remove this
        #passCnt += mongoInt.insertFBUserLoginData(userJson)
        self.createUserNode(userJson)
        return self.retrieveTweets()
