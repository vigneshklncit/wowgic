#! /usr/bin/python
#===============================================================================
# File Name      : .py
# Date           : 12-20-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
import loggerRecord
logger =  loggerRecord.get_logger()
####
# Get tweepy set up
import tweepy
from tweepy import Cursor

#keys from twitter is stored here temp will be removed once we access the user credentials
#chella's credentials
consumer_key= 'HwvpHtsPt3LmOZocZXwtn72Zv';
consumer_secret = 'afVEAR0Ri3ZluVItqbDi0kfm7BHSxjwRXbpw9m9kFhXGjnzHKh';
access_token = '419412786-cpS2hDmR6cuIf8BD2kSSri0BAWAmXBA3pzcB56Pw';
access_secret = 'pRx5MNKkmxyImwuhUFMNVOr1NrAWcRmOGUgGTLVYFAjsJ';

class twitterInt:
    ''' bla bla
    '''
    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        #authenticate twitter app
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def retrieveTweetsBasedHashtag(self):
        feeds =[]
        cricTweets = tweepy.Cursor(self.api.search, q='#madurai').items(1)
        for tweet in cricTweets:
            feeds.append(tweet)
            #logger.info("feed from twitter is %s", tweet)
        return feeds
