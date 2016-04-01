#! /usr/bin/python
#===============================================================================
# File Name      : mongoInt.py
# Date           : 12-22-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : pymongo
#
#===============================================================================
import sys
sys.path.append('common')
import loggerRecord,globalS
logger =  loggerRecord.get_logger()
import pymongo


class mongoInt():
    ''' mongoDB is our priliminary interface which will store users facebook, Instagram,
    twitter datas etc'''
    conn={}
    db=None
    databaseName = 'wowgicflaskapp'
    userCollName = 'FBLoginUserData'
    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        #authenticate twitter app
    ############################################################################
    #Function Name  : connect                                                  #
    #Input          : IP -> IP of the machine to connect                       #
    #               : Username & password to connect with                      #
    #Return Value   : object to interact withe neo4j                           #
    ############################################################################
    def connect(self):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        try:
            #DB_HOST = os.environ.get('OPENSHIFT_MONGODB_DB_HOST','localhost')
            #MONGODB_PORT = os.environ.get('OPENSHIFT_MONGODB_DB_PORT','27017')
            #uri = "mongodb://admin:wowgic@ds043714-a.mongolab.com:43714/wogicdb"
            #uri = 'mongodb://'+globalS.dictDb['MONGODB_USERNAME']+':'+globalS.dictDb['MONGODB_PASSWORD']+'@'+globalS.dictDb['MONGODB_HOST']+':'+globalS.dictDb['MONGODB_PORT']+'/wowgicflaskapp'
            uri = 'mongodb://'+globalS.dictDb['MONGODB_USERNAME']+':'+globalS.dictDb['MONGODB_PASSWORD']+'@'+globalS.dictDb['MONGODB_HOST']+':'+globalS.dictDb['MONGODB_PORT']
            try:
                self.conn = pymongo.MongoClient(connect=False)
                logger.debug("mongdb connected to localhost")
            except Exception as e:
                logger.debug('Exception raised in starting mongoDB:%s',e)
                logger.debug('mongoDb URI#%s',uri)
                self.conn = pymongo.MongoClient(uri) #local mongoDB running
                logger.debug("mongdb connected to openshift")
            #self.conn = pymongo.MongoClient('mongodb://admin:3Xfk5q16Nkbl@python-wowgic.rhcloud.com:27017')
        except Exception as e:
            logger.error("Could not connect to MongoDB: %s", e)
        self.db=self.conn[self.databaseName] #our global database
        self.createCollection(self.userCollName)
        return self.conn

    ############################################################################
    #Function Name  : connect                                                  #
    #Input          : IP -> IP of the machine to connect                       #
    #               : Username & password to connect with                      #
    #Return Value   : object to interact withe neo4j                           #
    ############################################################################
    def close(self):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''
        self.conn.close()
    ############################################################################
    #Function Name  : connect                                                  #
    #Input          : IP -> IP of the machine to connect                       #
    #               : Username & password to connect with                      #
    #Return Value   : 1 on success 0 if user exists                            #
    ############################################################################
    def insertFBUserLoginData(self,FBJsonUserLoginData):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        #db = self.conn['userData']
        #
        coll=self.db[self.userCollName]
        #self.createConstraint(coll)
        #instead of updating we can find_one initialyy and then do update operation
        logger.debug('FBJsonUserLoginData interest:%s',FBJsonUserLoginData['id'])
        WriteResult =coll.update({'id':FBJsonUserLoginData['id']},FBJsonUserLoginData,True)
        if WriteResult['updatedExisting']:
            logger.warn('mongoDB update method result#%s',WriteResult)
            return 0
        else:
            logger.debug('USer DB already exists')
            return 1
    ############################################################################
    #Function Name  :  #
    #Input          :  #
    #Return Value   : 1 if update is success 0 if user update fails
    ############################################################################
    def updateFBUserLoginData(self,jsonDoc):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        #db = self.conn['userData']
        #
        coll=self.db[self.userCollName]
        #instead of updating we can find_one initialyy and then do update operation
        logger.info('doc with last_login is :%s',jsonDoc)
        WriteResult =coll.update_one({'id':jsonDoc['id']},{'$set':{'last_login':jsonDoc['last_login']}})
        logger.debug('mongoDB update_one modified_count#%s matched_count %s',WriteResult.modified_count,WriteResult.matched_count)
        if WriteResult.modified_count:
            return 1
        else:
            logger.error('updating last_login failed in mongodb')
            return 0
    ############################################################################
    #Function Name  :  #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    #def insertInstagramUserLoginData(self,FBJsonUserLoginData):
    #    '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
    #    identified by the base URI of the graph database'''
    #
    #    # Connect to the databases
    #    #db = self.conn['userData']
    #    #
    #    coll=self.db['InstagramLoginUserData']
    #    #self.createConstraint(coll)
    #    #instead of updating we can find_one initialyy and then do update operation
    #    WriteResult =coll.update({'id':FBJsonUserLoginData['id']},FBJsonUserLoginData,True)
    #    if WriteResult['updatedExisting']:
    #        logger.warn('mongoDB update method result#%s',WriteResult)
    #        return 0
    #    else:
    #        logger.debug('USer already exists in DB')
    #        return 1
    ############################################################################
    #Function Name  :  #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def createConstraint(self,coll):
        ''' create constraint Creates an index on this collection.
        Takes either a single key or a list of (key, direction) pairs. The key(s)
        must be an instance of basestring (str in python 3)'''
        idxDict = coll.index_information()
        logger.info('the index dict is %s',idxDict)
        if 'id_1' not in idxDict:
            result = coll.create_index([('id',pymongo.DESCENDING)],unique=True) #remove dup with ID's
            result = coll.create_index([('created_time',pymongo.DESCENDING)]) #based on times
            logger.info('constraint create result %s',result)
            #result = coll.ensure_index('id')
            #logger.debug('constraint ensure result %s',result)
        else:
            logger.debug('already index exists on collection %s',coll)
        return 1
    ############################################################################
    #Function Name  :  #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def __del__(self):
        ''' basicall call methods like closing the ssh connection exiting the
        sql etc while python cleanup. In case if python encounters KILLSIG this
        method gets invoked and gracefully closes the ssh connection'''
        #self.conn.logout()
    ############################################################################
    #Function Name  :  #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def insertFeedData(self,ID,feedData):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        #db = self.conn['userData']
        #
        updateCnt = 0
        self.createCollection(ID)
        coll=self.db[ID]
        #change to fucntional prog
        for feed in feedData:
            #instead of updating we can find_one initialyy and then do update operation
            WriteResult =coll.update({'id':feed['id']},feed,True)
            if WriteResult['updatedExisting']:
                logger.warn('mongoDB update feed id:%s result#%s',feed['id'],WriteResult)
            else:
                logger.debug('feed is insterted into mongoDB:%s',feed['id'])
                updateCnt += updateCnt
        if updateCnt:
            return 1
        else:
            return 0
    ############################################################################
    #Function Name  : createCollection #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def createCollection(self,collInt):
        ''' Get / create a Mongo collection
        '''
        if self.checkCollExists(collInt):
            logger.warn('collection %s already exists in our mongoDB',collInt)
            return 0
        else:
            logger.debug('creating mongoDb collection %s ',collInt)
            try:
                self.db.create_collection(collInt)
            except Exception as e:
                logger.warn('creating collection error %s',e)
            self.createConstraint(self.db[collInt])
            return 1
    ############################################################################
    #Function Name  : retrieveCollection #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def retrieveCollection(self,collName,lastTimeStamp,count=5):
        ''' by passing the collection name fetch recent feeeds. Query the database
        '''
        feeds=[]
        logger.debug('arg is collName = %s & limit = %s',collName,count)
        coll = self.db[collName]
        cursor = coll.find({'created_time': { '$lt': lastTimeStamp } },{'_id':0,'contributors':0,'truncated':0,'in_reply_to_screen_name':0,
                               'in_reply_to_status_id':0,'id_str':0,'favorited':0,'is_quote_status':0,
                               'in_reply_to_user_id_str':0,'in_reply_to_status_id_str':0,'in_reply_to_user_id':0,
                               'metadata':0},limit=count,sort=[('id',pymongo.DESCENDING)])
        logger.info('cursor is %s',cursor.explain())
        feeds=map(lambda x:x,cursor)
        logger.debug('total documents retrieved %s',len(feeds))
        return feeds

    #returns 0 if collection exits
    def checkCollExists(self,collInt):
        ''' Check if a collection exists in Mongodb DB or not . if exists return the total doc count'''
        if collInt in self.db.collection_names():
            totalDocs=self.db[collInt].count()
            logger.debug('collection:%s total doc:%s already exists',collInt,totalDocs)
            return totalDocs
        else:
            logger.warn('collection:%s does not exists',collInt)
            return 0

    #returns 0 if collection exits
    def validateToken(self,ID):
        ''' Check if a collection exists in Mongodb DB or not'''
        coll = self.db[self.userCollName]
        document = coll.find_one({'id':ID},['password'])
        logger.debug('ID:%s lookup in FBJsonUserLoginData',ID)
        #cursor = coll.find()
        logger.debug('cursor is %s',document)
        return document['password']

    def retrieveSinceID(self,ID):
        ''' Check if a collection exists in Mongodb DB or not'''
        coll = self.db[self.userCollName]
        document = coll.find_one({},['id'],sort=[('id',pymongo.DESCENDING)])
        logger.debug('collection %s contains Max id as %s',ID,document)
        return document['id']

    ############################################################################
    #Function Name  : retrieveCollection #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def retrieveTwitterTokens(self,collName):
        ''' retreive the tokens from DB and return them as key value pais
        '''
        tokens=[]
        logger.debug('arg is collName = %s',collName)
        coll = self.db[collName]
        cursor = coll.find({},{'_id':0,'oauth_token':1,'oauth_token_secret':1})
        logger.info('cursor is %s',cursor.explain())
        feeds=map(lambda x:x,cursor)
        logger.debug('total tokens twitter access secret retrieved %s',len(feeds))
        return feeds

    def insertTwitteTokens(self,ID,twitterData):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        #db = self.conn['userData']
        #
        #self.createCollection(ID)
        coll=self.db[ID]
        WriteResult =coll.insert(twitterData)
        logger.debug('writereult is %s',WriteResult)
        if len(WriteResult):
            logger.debug('twitter token succesfuly insereted')
        else:
            logger.warn('Error in inserting twitter token:%s',twitterData)
        return len(WriteResult)
