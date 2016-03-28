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
#from tweepy import RateLimitHandler
#import time
#from tweepy import Cursor
#some concreete solutiuon has to be implemented below is just junk HOT fix
#keys from twitter is stored here temp will be removed once we access the user credentials from mongoDB and load it to globalDict file
#chella's credentials
#sathish ouath ofr location feeds & new user this should not exhaust at any case
#    T_ACCESS_TOKEN = '419412786-cpS2hDmR6cuIf8BD2kSSri0BAWAmXBA3pzcB56Pw',
#    T_ACCESS_SECRET = 'pRx5MNKkmxyImwuhUFMNVOr1NrAWcRmOGUgGTLVYFAjsJ',
#    SATHISH_TOKEN_SECRET = 'iMGjh3MkFGS0yudhe9SadUH5Dxwk9ndiAPrXTE6ivyqr8',
#    SATHISH_TOKEN = '56276642-bOJMDDbpy7B2gCryxMfWgMDGrxgP9NnPJzgMV5fTS',
#    VIVEK_TOKEN_SECRET = '8h1T0x2237pmUWA1Hg7QSi3sPRQt9WN6Okg6A0dMSYvRL',
#    VIVEK_TOKEN = '2976291321-gfESJJC7xBvZk0mv8tbkbYgoMseQChUBwPslbYc')
#
#globalS.dictDb.update(oAuthStrings)

ACCESS_TOKENS = {globalS.dictDb['T_ACCESS_TOKEN']: globalS.dictDb['T_ACCESS_SECRET']}
class twitterInt:
    ''' this class is meant for twitter
    '''
    api=''#universal twitter api

    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        #authenticate twitter app
        self.auth = tweepy.OAuthHandler(globalS.dictDb['T_CONSUMER_KEY'], globalS.dictDb['T_CONSUMER_SECRET'])
        self.api = self.connect(globalS.dictDb['T_ACCESS_TOKEN'], globalS.dictDb['T_ACCESS_SECRET'],wait_on_rate_limit=False)
        #auth.seT_ACCESS_TOKEN(globalS.dictDb['T_ACCESS_TOKEN'], globalS.dictDb['T_ACCESS_SECRET'])
        #self.api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=2,timeout=8)

    def connect(self,oauth_token,oauth_token_secret,**options):
        ''' Sure shot this will give PROBLEMS due to rate limit 1 search tweet exhaust
        '''
        logger.info('twitter connect')
        self.auth.set_access_token(oauth_token, oauth_token_secret)
        if options.get("wait_on_rate_limit"):
            twitterApi = tweepy.API(self.auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=2,timeout=8)
        else:
            twitterApi = tweepy.API(self.auth,wait_on_rate_limit=False,wait_on_rate_limit_notify=True,retry_count=1,timeout=8)
        return twitterApi

    def get_api(self):
        auth = RateLimitHandler(globalS.dictDb['T_CONSUMER_KEY'], globalS.dictDb['T_CONSUMER_SECRET'])
        logger.info('entered ratelimitor')
        for key, secret in ACCESS_TOKENS.items():
                try:
                    auth.add_access_token(key, secret)
                except TweepError, e:
                    logger.debug('key %s , error %s', key, e)
        print 'Token pool size: %d' % len(auth.tokens)
        api = tweepy.API(auth,
                wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api

    #def retrieveTweetsBasedHashtag(self,Q):
    #    ''' Method returns tweets based on feeds or 0 in case of failure
    #    DEPRECATED'''
    #    feeds = []
    #    # tweepy resulting in 400 bad data has to be debug!!
    #    logger.debug('twitter cursor search Q=%s',Q)
    #    if Q is not None:
    #        tweets = tweepy.Cursor(self.api.search, q=Q).items(200)
    #        feeds=list(map(lambda twit:twit._json,tweets))
    #        logger.debug('total tweets retrieved for keyword:%s is %s',Q,len(feeds))
    #        return feeds
    #    else:
    #        logger.error('twitter search string is empty')
    #        return 0

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

    def rateLimitStatus(self,api):
        ''' Show the rate Limits'''
        rateLimits = api.rate_limit_status()
        logger.debug('twitter the rate Limit:%s',rateLimits)
        return  rateLimits['resources']['search']['/search/tweets']

    def retrieveTweetBasedLocation(self,geoCode):
        ''' based on the geo cordinates passed this information fetches the location details
        '''
        api=self.api
        feeds =[]#{u'lat': 52.5319, u'distance': 2500, u'lng': 13.34253}
        #reverse geocoding is also required here to do which is pending
        if not self.rateLimitStatus(api)['remaining']:
            api = self.connect(globalS.dictDb['SATHISH_TOKEN'],globalS.dictDb['SATHISH_TOKEN_SECRET'])
        geoCode = str(geoCode['lat']) + ','+ str(geoCode['lng']) +','+ str(geoCode['distance'])+'km'
        logger.debug('geoCode twitter search#%s',geoCode)
        tweets = tweepy.Cursor(api.search,q='',geocode=geoCode).items(100)
        #feeds=list(map(lambda twt:twt._json,tweets))
        feeds=map(lambda twt:twt._json,tweets)
        logger.debug("location feed geocode:%s from twitter is %s",geoCode,len(feeds))
        return feeds

    def retrieveTweets(self,Q,geoCode):
        '''returns an empty list in case of failure. If length of returned list is
        zero thn something has went wrong
        '''
        #api=self.get_api()
        api=self.api
        feeds =[]#{u'lat': 52.5319, u'distance': 2500, u'lng': 13.34253}
        #reverse geocoding is also required here to do which is pending
        logger.info('geoCode twitter search#%s',geoCode)
        if not self.rateLimitStatus(api)['remaining']:
            logger.warn('trying with viveks ouath')
            api = self.connect(globalS.dictDb['VIVEK_TOKEN'],globalS.dictDb['VIVEK_TOKEN_SECRET'],wait_on_rate_limit=1)
            if not self.rateLimitStatus(api)['remaining']:
                logger.error('twitter rate limit execeeded')
                return feeds
        if Q is not None:
            #tweepy set count to largets number
            tweets = tweepy.Cursor(api.search, q=Q).items()
        elif geoCode :
            geoCode = str(geoCode['lat']) + ','+ str(geoCode['lng']) +','+ str(geoCode['distance'])+'km'
            tweets = tweepy.Cursor(api.search,q='',geocode=geoCode).items()
        else:
            logger.error('twitter search string is empty')
            return feeds

        try:
            feeds=map(lambda twt:twt._json,tweets)
            #feeds=list(map(lambda twt:twt._json,tweets))
        except tweepy.TweepError as e:
            logger.error('raised tweepyerror %s',e)
        logger.info('ratelimitStatus data for /search/tweets:%s',self.rateLimitStatus(api))

        #Thz functionality should be moved to intercom.py
        #map(lambda tw:tw.update({'created_at': 'satheesh'}),feeds)
        #map(lambda tw:tw.update({'created_at': datetime.datetime.strptime(tw['created_at'], '%a %b %d %H:%M:%S +0000 %Y')}),feeds)
        logger.debug('total tweets retrieved for keyword:%s is %s',Q,len(feeds))
        return feeds