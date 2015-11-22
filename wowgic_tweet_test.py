#!/usr/bin/env python

import tweepy
import json 
import pymongo
from tweepy import OAuthHandler

connection = pymongo.MongoClient("localhost", 27017)
db = connection.feeds
consumer_key= 'HwvpHtsPt3LmOZocZXwtn72Zv';
consumer_secret = 'afVEAR0Ri3ZluVItqbDi0kfm7BHSxjwRXbpw9m9kFhXGjnzHKh';
access_token = '419412786-cpS2hDmR6cuIf8BD2kSSri0BAWAmXBA3pzcB56Pw';
access_secret = 'pRx5MNKkmxyImwuhUFMNVOr1NrAWcRmOGUgGTLVYFAjsJ';

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api=tweepy.API(auth)

#words = ["is"]
#with tweetstream.FilterStream(username, password, track=words) as stream:
#    for tweet in stream:
#        db.tweets.save(tweet)
#for status in tweepy.Cursor(api.home_timeline).items(10):
#   print (status)
#   #db.tweets.insert(json.loads(str(status)))
#   db.tweets.insert(status)


class CustomStreamListener(tweepy.StreamListener):
    """
    tweepy.StreamListener is a class provided by tweepy used to access the Twitter 
    Streaming API. It allows us to retrieve tweets in real time.
    """
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()
        
        # Connecting to MongoDB and use the database twitter.
        self.db = pymongo.MongoClient().twitter
 
    def on_data(self, tweet):
        '''
        This will be called each time we receive stream data and store the tweets 
        into the datascience collection.
        '''
        self.db.datascience.insert(json.loads(tweet))
 
    def on_error(self, status_code):
        # This is called when an error occurs
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream
 
    def on_timeout(self):
        # This is called if there is a timeout
        print >> sys.stderr, 'Timeout.....'
        return True # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=["is"])
