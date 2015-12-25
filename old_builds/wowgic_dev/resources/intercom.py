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
import loggerRecord
logger =  loggerRecord.get_logger()
import sys
sys.path.append('common')
sys.path.append('resources')
import globalS
import json
import generic
import loggerRecord
import neo4jInterface
import mongoInt
import twitterInt


twitterInt = twitterInt.twitterInt()
neo4jInt = neo4jInterface.neo4jInterface()
#graphDB=neo4jInt.connect()
graphDB=neo4jInt.connect('localhost:7474/db/data/','neo4j','admin')
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
        #authenticate twitter app


    def createUserNode(self,jsonFBInput):
        decodedFBJson=json.loads(jsonFBInput)
        if mongoInt.insertFBUserLoginData(decodedFBJson):
            neo4jInt.createUserNode(graphDB,decodedFBJson,'user')
            interestList = ['hometown','location','work','education']
            for int in interestList:
                neo4jInt.createInterestNode(graphDB,decodedFBJson,int)
        else:
            logger.debug('user already exists hence skipping the neo4J creation of nodes & interest')
        #once the nodes are created lets fetch the feeds
        return self.retrieveTweets()

    def retrieveTweets(self):
        '''retrieveTweetsBasedHashtag
        '''
        neo4jInt.showInterestNode(graphDB)
        twits = twitterInt.retrieveTweetsBasedHashtag()
        logger.debug('retrieve tweets')
        #page_sanitized = json_util.dumps(twits)
        return twits