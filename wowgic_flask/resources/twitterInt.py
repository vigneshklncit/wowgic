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
        cricTweets = tweepy.Cursor(self.api.search, q='#madurai').items(10)
        for tweet in cricTweets:
            feeds.append(tweet._json)
            logger.info("feed from twitter is %s", feeds)
        return feeds

    def retrieveTweetBasedLocation(self,geoCode):
        feeds =[]#{u'lat': 52.5319, u'distance': 2500, u'lng': 13.34253}
        geoCode = str(geoCode['lat']) + ','+ str(geoCode['lng']) +','+ str(geoCode['distance'])
        logger.debug('geoCode#%s',geoCode)
        logger.info('geoCode#%s',geoCode)
        tweets = tweepy.Cursor(self.api.search, q='#happy',geocode=geoCode).items(1)
        for tweet in tweets:
            feeds.append(tweet._json)
            logger.info("location feed from twitter is %s", feeds)
        return feeds
