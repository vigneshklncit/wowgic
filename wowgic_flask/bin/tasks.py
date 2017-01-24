from celery import Celery
from celery import chain
import sys
sys.path.append('../common')
sys.path.append('../config')
sys.path.append('../resources')

import globalS
import generic
import loggerRecord
import json
from datetime import datetime, timedelta

logFileName='/tmp/wowgic_celery.log'
logger,fhandler       = loggerRecord.loggerInit(logFileName,'debug')
logger.debug('Log file# %s & TestBed file',logFileName)
celery = Celery('tasks', broker='amqp://guest@localhost//')
# Load the default configuration
celery.config_from_object('celeryconfig')
#read config from envt variable
#celery.config_from_envvar('CELERY_CONFIG_FILE')#D:\wowgic-env\wowgic\wowgic_flask\instance\flaskapp.cfg
#filename = os.path.join(app.instance_path, 'application.cfg')
#with open(filename) as f:
#    config = f.read()
globalS.dictDb = celery.conf
logger.debug('celery dictDB contains %s',globalS.dictDb)



'''
Rough Tasks:
First read all the interest nodes from neo4j
create a common module that inokes instagram & twitter
using celery delay method pass argumenmts to that and invoke the tasks
foreach interest node trigger twitter & instagram calls without affecting the hit rate
store them in mongDB
Again read the interest nodes from neo4j
'''

@celery.task
def triggerClassification():
    import intercom
    intercom=intercom.intercom()
    
    setupData = intercom.performnb()
    
    def setFreshCategory(record):
        ID=record[0]['id']
        setCategory.s(ID).delay()
    interesetNodes = intercom.getAllInterestNode()    
    #map(setFreshCategory, interesetNodes)
    '''
    record = []
    data = {}
    data['name'] = 'chennai'
    data['lat'] = None
    data['city'] = None
    data['id'] = '112463015433208'
    record.append(data)'''
    #getAllInterestNode.s().delay()
    tomorrow = datetime.utcnow() + timedelta(days=1)
    return True
    #return triggerClassification.apply_async(eta=tomorrow)


@celery.task
def getAllInterestNode(frequencyReady = None):
    import intercom
    intercom=intercom.intercom()
    ''' after first time login of user this gets invoked by an ID provided by UI
    like Request: https://http://wowgicflaskapp-wowgic.rhcloud.com/id=q13512667
    neo4j has associated feeds ID to be displayed to the user fetch them from mongdb and return it back
    '''
    if frequencyReady != None:
        interesetNodes = intercom.fetchFrequentNode()
    else:
        interesetNodes = intercom.getAllInterestNode()
    logger.debug('feedList:%s',interesetNodes)

    geoDict = {} 
    #for record in interesetNodes:
    #    if record[0]['lat'] is not None:
    #        geoDict.update({'lat':record[0]['lat']})
    #        geoDict.update({'lng':record[0]['lng']})
    #        geoDict.update({'distance':'.5'})#default radius =500m
    #    logger.debug('recordList output of neo4j:%s',record[0]['name'])
    #    if record[0]['city'] is not None:
    #        Q=record[0]['name'] +' '+ record[0]['city']
    #    else:
    #        Q=record[0]['name']
    #    ID=record[0]['id']
    #    logger.debug('fetchInterestFeeds Q=%s geo cordinates =%s',Q,geoDict)
    #    #retrieveTweets.delay(ID,Q,geoDict)
    #    #retrieveMediaBasedTags.delay(ID,Q,geoDict)
    #    #if mongoInt.checkCollExists(ID) > 1:
    #    #    tweets.extend(mongoInt.retrieveCollection(ID))
    #    #else:
    #    #    tweets.extend(self.retrieveTweets(Q,geoDict))
    #    #    tweets.extend(self.retrieveMediaBasedTags(ID,Q,geoDict))
    #    #    geoDict = {}#revert the geo dictionary
    ##sparkInt.Parallelized(tweets)
    ##feedJson=sparkInt.wowFieldTrueOrFalse(tweets)

    def iterFunc(record):
        logger.info('record %s',record)
        geoDict = {}
        if record[0]['lat'] is not None:
            geoDict.update({'lat':record[0]['lat']})
            geoDict.update({'lng':record[0]['lng']})
            geoDict.update({'distance':'.5'})#default radius =500m
        logger.debug('recordList output of neo4j:%s',record[0]['name'])
        if record[0]['city'] is not None:
            Q=record[0]['name'] +' '+ record[0]['city']
        else:
            Q=record[0]['name']
        Q=record[0]['name']
        geoDict={}
        ID=record[0]['id']
        logger.debug('fetchInterestFeeds Q=%s geo cordinates =%s',Q,geoDict)
        #retrieveMediaBasedTags.delay(ID,Q,geoDict)
        #retrieveTweets.delay(ID,Q,geoDict)
        #g=group(retrieveTweets.s(ID,Q,geoDict,debug=True),
        #retrieveMediaBasedTags.s(ID,Q,geoDict,debug=True))
        #res = g()
    #    retrieveMediaBasedTags.s(ID,Q,geoDict).delay()
        #res = chain(retrieveTweets.s(ID,Q,geoDict), runTopicModelling.s(Q, ID), setCategory.s(ID))()
        #res.get()
        #start = chain(retrieveTweets.si(ID,Q,geoDict), triggerCategory.si(ID))()
        retrieveTweets.s(ID,Q,geoDict).delay()

    map(iterFunc,interesetNodes)
    '''
    record = []
    record1 = []
    records = []
    data = {}
    data['name'] = 'chennai'
    data['lat'] = None
    data['city'] = None
    data['id'] = '112621745415708'
    record.append(data)
    records.append(record)
    data = {}
    data['name'] = 'Tirunelveli'
    data['lat'] = None
    data['city'] = None
    data['id'] = '103099979730946'
    record1.append(data)
    records.append(record1)
    #iterFunc(record)
    logger.info('recordsss %s',records)
    map(iterFunc,records)'''

    #jobs = group
    return getAllInterestNode.delay(True)
    #return True


#@celery.task()
@celery.task()
def runTopicModelling(records,keyword, collName):
    import intercom
    intercom=intercom.intercom()
    return intercom.runTopicModel(records,keyword, collName)


@celery.task(name='fetch tweets')
def retrieveTweets(collName,Q,geoDict):
    import intercom
    intercom=intercom.intercom()
    logger.info('retrieveTweets:%s,%s,%s',collName,Q,geoDict)
    #twits = 
    #category = triggerCategory.delay()
    return intercom.retrieveTweets(collName,Q,geoDict)


@celery.task(rate_limit='8/m')
#@celery.task()
def retrieveMediaBasedTags(collName,Q,geoDict):
    logger.info('retrieveMediaBasedTags:%s,%s,%s',collName,Q,geoDict)
    return intercom.retrieveMediaBasedTags(collName,Q,geoDict)

@celery.task(name='set.category')
def setCategory(ID):
    import intercom
    intercom=intercom.intercom()
    return intercom.unSetNB(ID)
    #return intercom.runClassifier(ID)

#start = chain(triggerClassification.si(),getAllInterestNode.si())()
#triggerClassification()
#triggerCategory()
getAllInterestNode()
if __name__ == '__main__':
    celery.start()
