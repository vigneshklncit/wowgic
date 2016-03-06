#! /usr/bin/python
#===============================================================================
# File Name      : .py
# Date           : 12-20-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
import loggerRecord,globalS
logger =  loggerRecord.get_logger()
####
# Get tweepy set up
import tweepy
from tweepy import Cursor

#keys from twitter is stored here temp will be removed once we access the user credentials from mongoDB and load it to globalDict file
#chella's credentials
oAuthStrings = dict(t_consumer_key= 'HwvpHtsPt3LmOZocZXwtn72Zv',
t_consumer_secret = 'afVEAR0Ri3ZluVItqbDi0kfm7BHSxjwRXbpw9m9kFhXGjnzHKh',
t_access_token = '419412786-cpS2hDmR6cuIf8BD2kSSri0BAWAmXBA3pzcB56Pw',
t_access_secret = 'pRx5MNKkmxyImwuhUFMNVOr1NrAWcRmOGUgGTLVYFAjsJ')

globalS.dictDb.update(oAuthStrings)

class twitterInt:
    ''' this class is meant for twitter
    '''
    api=''
    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        #authenticate twitter app
        auth = tweepy.OAuthHandler(globalS.dictDb['t_consumer_key'], globalS.dictDb['t_consumer_secret'])
        auth.set_access_token(globalS.dictDb['t_access_token'], globalS.dictDb['t_access_secret'])
        self.api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=2)

    def retrieveTweetsBasedHashtag(self,Q):
        ''' Method returns tweets based on feeds or 0 in case of failure'''
        feeds =[]
        # tweepy resulting in 400 bad data has to be debug!!
        logger.debug('twitter cursor search Q=%s',Q)
        if Q is not None:
            tweets = tweepy.Cursor(self.api.search, q=Q).items(200)
            #for tweet in tweets:
            #    feeds.append(tweet._json)
            feeds=list(map(lambda x:x._json,tweets))
            logger.debug('total tweets retrieved for keyword:%s is %s',Q,len(feeds))
            return feeds
        else:
            logger.error('twitter search string is empty')
            return 0

    def verifyCredentials():
        ''' This returns 1 in case twitter credentials are authorized else results in
        failure'''
        userObj = self.api.verify_credentials()
        if userObj:
            logger.debug('twitter is it authenticated:%s',userObj.name)
            return 1
        else:
            logger.debug( 'Invalid Authentication')
            return 0

    def rateLimitStatus(self):
        ''' Show the rate Limits'''
        rateLimits = self.api.rate_limit_status()
        logger.debug('twitter the rate Limit:%s',rateLimits)
        return  rateLimits['resources']['statuses']['/statuses/home_timeline']

    def retrieveTweetBasedLocation(self,geoCode):
        ''' based on the geo cordinates passed this information fetches the location details
        '''
        feeds =[]#{u'lat': 52.5319, u'distance': 2500, u'lng': 13.34253}
        #reverse geocoding is also required here to do which is pending
        geoCode = str(geoCode['lat']) + ','+ str(geoCode['lng']) +','+ str(geoCode['distance'])+'km'
        logger.debug('geoCode twitter search#%s',geoCode)
        tweets = tweepy.Cursor(self.api.search,q='',geocode=geoCode,rpp=10).items(10)
        for tweet in tweets:
            feeds.append(tweet._json)
        logger.debug("location feed geocode:%s from twitter is %s",geoCode,len(feeds))
        return feeds

    def retrieveTweets(self,Q,geoCode):
        '''
        '''
        feeds =[]#{u'lat': 52.5319, u'distance': 2500, u'lng': 13.34253}
        #reverse geocoding is also required here to do which is pending
        logger.debug('geoCode twitter search#%s',geoCode)
        #self.rateLimitStatus()
        try:
            if Q is not None:
                #tweepy set count to largets number
                tweets = tweepy.Cursor(self.api.search, q=Q).items(200)
            elif geoCode :
                geoCode = str(geoCode['lat']) + ','+ str(geoCode['lng']) +','+ str(geoCode['distance'])+'km'
                tweets = tweepy.Cursor(self.api.search,q='',geocode=geoCode).items(200)
            else:
                logger.error('twitter search string is empty')
                return 0
        except tweepy.TweepError as e:
            self.rateLimitStatus()
            logger.error('raised tweepyerror %s',e)
        #for tweet in tweets:
        #    feeds.append(tweet._json)
        feeds=list(map(lambda x:x._json,tweets))
        logger.debug('total tweets retrieved for keyword:%s is %s',Q,len(feeds))
        return feeds