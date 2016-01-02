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
            logger.debug('mongoDb URI#%s',uri)
            try:
                self.conn = pymongo.MongoClient(uri)
                logger.debug("mongdb connected to openshift")
            except Exception as e:
                logger.debug('Exception raised in starting mongoDB:%s',e)
                self.conn = pymongo.MongoClient() #local mongoDB running
                logger.debug("mongdb connected to localhost")
            #self.conn = pymongo.MongoClient('mongodb://admin:3Xfk5q16Nkbl@python-wowgic.rhcloud.com:27017')
        except Exception as e:
            logger.error("Could not connect to MongoDB: %s", e)
        self.db=self.conn['wowgicflaskapp'] #our global database
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
        coll=self.db['FBLoginUserData']
        self.createConstraint(coll)
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
    #Return Value   :  #
    ############################################################################
    def insertTwitterUserLoginData(self,FBJsonUserLoginData):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        #db = self.conn['userData']
        #
        coll=self.db['TwitterLoginUserData']
        self.createConstraint(coll)
        #instead of updating we can find_one initialyy and then do update operation
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
    #Return Value   :  #
    ############################################################################
    def insertInstagramUserLoginData(self,FBJsonUserLoginData):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        #db = self.conn['userData']
        #
        coll=self.db['InstagramLoginUserData']
        self.createConstraint(coll)
        #instead of updating we can find_one initialyy and then do update operation
        WriteResult =coll.update({'id':FBJsonUserLoginData['id']},FBJsonUserLoginData,True)
        if WriteResult['updatedExisting']:
            logger.warn('mongoDB update method result#%s',WriteResult)
            return 0
        else:
            logger.debug('USer already exists in DB')
            return 1
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
        logger.debug('the index dict is %s',idxDict)
        if not idxDict:
            result = coll.create_index('id') #create & ensure i dont know which is perfect
            logger.debug('constraint create result %s',result)
            result = coll.ensure_index('id')
            logger.debug('constraint ensure result %s',result)
        else:
            logger.debug('already index exists on collection %s',coll)
    ############################################################################
    #Function Name  :  #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def __del__(self):
        ''' basicall call methods like closing the ssh connection exiting the
        sql etc while python cleanup. In case if python encounters KILLSIG this
        method gets invoked and gracefully closes the ssh connection'''
        #self.close()
    ############################################################################
    #Function Name  :  #
    #Input          :  #
    #Return Value   :  #
    ############################################################################
    def insertFeedData(self,feedData):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        #db = self.conn['userData']
        #
        updateCnt = 0
        coll=self.db['feeds']
        for feed in feedData:
            #instead of updating we can find_one initialyy and then do update operation
            WriteResult =coll.update({'id':feed['id']},feed,True)
            if WriteResult['updatedExisting']:
                logger.warn('mongoDB update feed result#%s',WriteResult)
            else:
                logger.debug('USer already exists in DB')
                updateCnt  += updateCnt
        if updateCnt:
            return 1
        else:
            return 0