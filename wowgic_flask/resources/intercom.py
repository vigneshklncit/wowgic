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
import generic
import json
from pygeocoder import Geocoder
import neo4jInterface
import mongoInt
import twitterInt
import instagramInt
import facebookInt
import loggerRecord
import random
#import sparkInt
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
mconnect = mongoInt.connect()
#sparkInt=sparkInt.sparkInt()

class intercom:
    ''' this file act as a intercaller /router / flow chart whaterver you call. T o& fro
    calling functions interworking between verious interfaces like twitter, Instagram,
    facebook , neo4j & mongoDB lies from here
    '''
    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        #mconnect = mongoInt.connect()
        #sparkInt.connect()
        #authenticate twitter app

    def createUserNode(self,decodedFBJson):
        '''
        latitude & longitude also needs to be stored in neo4j for retrival of reveland tweets
        '''
        #decodedFBJson=json.loads(decodedFBJson) remove true for now
        #if mongoInt.insertFBUserLoginData(decodedFBJson) or True:
        mongoInt.insertFBUserLoginData(decodedFBJson)
        neo4jInt.createUserNode(graphDB,decodedFBJson,'user')
        interestList = ['hometown','location','work','education']
        for intr in interestList:
            if 'work' in intr:
                keyIs='employer'
            elif 'education' in intr:
                keyIs='school'
            if intr in decodedFBJson:
                if isinstance(decodedFBJson[intr],list):
                    for itm in decodedFBJson[intr]:
                        if itm.get('type') == None:
                                itm['type'] = keyIs
                        data = facebookInt.getIdLocation(itm[keyIs]['id'])
                        logger.debug('Facebook get address using id:%s',data)
                        if 'location' in data:
                            itm[keyIs].update(data['location'])
                else:
                    data = facebookInt.getIdLocation(decodedFBJson[intr]['id'])
                    logger.debug('Facebook get address using id:%s',data)
                    decodedFBJson[intr].update(data['location'])
                #add IF check whther interest is part of data provided
                neo4jInt.createInterestNode(graphDB,decodedFBJson,intr)
                #creating mongoDb interest nodes with ID as thy are unique
                if not mongoInt.createCollection(decodedFBJson['id']):
                    logger.warn('unable to create collection in mongodb')
            else:
                logger.debug('user key doesnot exists')
        logger.debug('dataFb decodedFBJson:%s',decodedFBJson)
        #else:
        logger.debug('user already exists hence skipping the neo4J creation of nodes & interest')
        #once the nodes are created lets fetch the feeds
        return 1

    def retrieveTweets(self,ID,Q,geoCode):
        '''retrieveTweetsBasedHashtag from twitter
        '''
        passCnt = 0
        logger.debug('retrieve tweets')

        twits = twitterInt.retrieveTweets(Q,geoCode)
        #twits = twitterInt.retrieveTweetsBasedHashtag(Q)
        #if geoCode:
        #    twits.extend(twitterInt.retrieveTweetBasedLocation(geoCode))
        logger.debug('storing tweets of twitter of both location baseed on keyworad mongoDb')
        #twits=sparkInt.wowFieldTrueOrFalse(twits)
        passCnt += mongoInt.insertFeedData(ID,twits)
        #page_sanitized = json_util.dumps(twits)
        # below returning to be removed has to be done from mongoDB only
        return twits

    def instagram_login(self):
        ''' bypasser for instagram login as decorator functions are used This
        function is called from app.py & calls instagramInt function
        '''
        return instagramInt.instagram_login()

    def retrieveMediaBasedTags(self,ID,Q,geoDict):
        '''instagram feeds this function is hanging correct it
        '''
        passCnt = 0
        logger.debug('retrieve instagram medias')
        #tag search in instagram remove comma
        #Q.replace(',','')
        feedJson = instagramInt.retrieveMediaBasedTags(Q,geoDict)
        if geoDict:
            logger.debug('geoDict for instagram based media retrieve')
            feedJson.extend(instagramInt.getLocationSearch(geoDict))
        #else:
        #    # Example addr: 875 N Michigan Ave, Chicago, IL 60611
        #    results = Geocoder.geocode(Q)
        #    latlng=results.coordinates
        #    logger.debug('google geocode api coordinate pair:%s',latlng)
        #    geoDict.update({'lat':latlng[0]})
        #    geoDict.update({'lng':latlng[1]})
        #    geoDict.update({'distance':'.5'})#default radius =500m
        logger.debug('geo cord to search in instagram is %s',geoDict)
        #feedJson.extend(instagramInt.getLocationSearch(geoDict))
        #feedJson = json.loads(feedJson)
        logger.debug('store instagram media in mongoDb')
        #use spark removed unwanted feilds in json & add a key:value
        #feedJson=sparkInt.wowFieldTrueOrFalse(feedJson)
        passCnt += mongoInt.insertFeedData(ID,feedJson)
        # below returning to be removed has to be done from mongoDB only
        return feedJson

    def refreshFeeds(self):
        ''' this method is invoked when user hits 2nd time and we fetch his interest
        via the ID provided by UI and fetch the corresponding neo4j interest nodes
        returning feed Ids.
        Also invoked for the very first time as well aftr cr8ing neo4j nodes ( this statment is tricky lets refine)
        '''
        #fetch neo4j interest based on ID's

    def fetchInterestFeeds(self,ID):
        '''fetch the all neo4j interest nodes returning name & city then using those
        tags look for mongoDb collection if not then do search in twitter &
        instagram and store the output in mongoDb in a collection mapped to interest nodes'''
        recordList = neo4jInt.getInterestNode(graphDB,ID)
        geoDict = {}
        tweets=[]
        #parse the recordList and frame the has tags here
        for record in recordList:
            if record[0]['lat'] is not None:
                geoDict.update({'lat':record[0]['lat']})
                geoDict.update({'lng':record[0]['lng']})
                geoDict.update({'distance':'.5'})#default radius =500m
            logger.info('recordList output of neo4j:%s',record[0]['name'])
            if record[0]['city'] is not None:
                Q=record[0]['name'] +' '+ record[0]['city']
            else:
                Q=record[0]['name']
            ID=record[0]['id']
            logger.debug('fetchInterestFeeds ID:%s Q=%s geo cordinates =%s',ID,Q,geoDict)
            if mongoInt.checkCollExists(ID) > 1:
                tweets.extend(mongoInt.retrieveCollection(ID))
            else:
                tweets.extend(self.retrieveTweets(ID,Q,geoDict))
                tweets.extend(self.retrieveMediaBasedTags(ID,Q,geoDict))
                geoDict = {}#revert the geo dictionary
        #sparkInt.Parallelized(tweets)
        #feedJson=sparkInt.wowFieldTrueOrFalse(tweets)
        return tweets

    def handle_instagram_authorization(self):
        '''
        '''
        passCnt = 0
        user=instagramInt._handle_instagram_authorization()
        passCnt += mongoInt.insertInstagramUserLoginData(user)
        return "Thanks buddy ! Instagram is authorized"

    def FBLoginData(self,userJson):
        '''
        very first time user comes in
        '''
        #store the user data along with access_token
        #logger.debug('userJson:%s',userJson)
        try:
            userJson=json.loads(userJson)
        except:
            pass #while passing json directly this is not reqd in production remove this
        #passCnt += mongoInt.insertFBUserLoginData(userJson)
        logger.info('FB data obtained is %s',userJson)
        self.createUserNode(userJson)
        logger.debug('fetch interest based feeds')
        #feedList=self.fetchInterestFeeds(userJson['id'])
        return userJson['id'] #return 1 on success 0 on failure

    def retrieveLocationBasedTags(self,geoCode):
        ''' the slidebar feature based on radius dragging is done here both twitter
        & instagram datas are retrieved'''
        passCnt = 0
        feedList=[]
        feedList.extend(twitterInt.retrieveTweetBasedLocation(geoCode))
        #do a reverse geocoding and hit with feeds
        feedList.extend(instagramInt.getLocationSearch(geoCode))
        #passCnt += mongoInt.insertInstagramUserLoginData(user)
        random.shuffle(feedList)
        return feedList

    def verifyAuthUser(self,ID):
        ''' just return the password token stored in mongoDB
        '''
        return mongoInt.validateToken(ID)

    def getAllInterestNode(self):
        ''' just return the password token stored in mongoDB
        '''
        return neo4jInt.getAllInterestNode(graphDB)
