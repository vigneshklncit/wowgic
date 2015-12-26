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
            #uri = "mongodb://wowgic:wowgic@ds043714.mongolab.com:43714/wogicdb&ssl=true"
            #uri = 'mongodb://'+globalS.dictDb['MONGODB_USERNAME']+':'+globalS.dictDb['MONGODB_PASSWORD']+'@'+globalS.dictDb['MONGODB_HOST']+':'+globalS.dictDb['MONGODB_PORT']+'/wowgicflaskapp'
            uri = 'mongodb://'+globalS.dictDb['MONGODB_USERNAME']+':'+globalS.dictDb['MONGODB_PASSWORD']+'@'+globalS.dictDb['MONGODB_HOST']+':'+globalS.dictDb['MONGODB_PORT']
            try:
                self.conn = pymongo.MongoClient(uri)
                logger.debug("mongdb connected to openshift")
            except:
                self.conn = pymongo.MongoClient() #local mongoDB running
                logger.debug("mongdb connected to localhost")
            #self.conn = pymongo.MongoClient('mongodb://admin:3Xfk5q16Nkbl@python-wowgic.rhcloud.com:27017')
        except Exception as e:
            logger.error("Could not connect to MongoDB: %s", e)
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
        db = self.conn['userData']
        #
        coll=db['FBLoginUserData']
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
    def insertTwitterUserLoginData(self,FBJsonUserLoginData):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''

        # Connect to the databases
        db = self.conn['userData']
        #
        coll=db['TwitterLoginUserData']
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
        db = self.conn['userData']
        #
        coll=db['InstagramLoginUserData']
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
            result = coll.create_index('id')
            result = coll.ensure_index('id')
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


## to print the list of databases
#print conn.database_names()
#
## to print the list of collections in database
#print db.collection_names()
#
#result = db.restaurants.insert_one(
#    {
#
#    }
#result.inserted_id
## Access the Document from the collections
## Document Counts
#print ?Total Documents?, coll_friends.count()
#
## display the first document
#print coll_friends.find_one()
#
## Comparison example
#print ?\n Comparison example \n?
#cur = coll_friends.find({?current_location.city?:
#{?$in?: [?Singapore?]}},
#{?username?: 1, ?_id?: 0})
#
## print the documents through for loop
#for doc in cur:
#print doc
#
#print ?\n?
