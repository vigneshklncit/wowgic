#! /usr/bin/python
import time
import sys
import string
import json
import re
import tweepy
sys.path.append('../wowgic_dev')
import globalS
from tweepy import *
from py2neo import *
import neo4jInterface
from textblob import TextBlob
from tweepy.streaming import StreamListener

consumer_key= 'HwvpHtsPt3LmOZocZXwtn72Zv';
consumer_secret = 'afVEAR0Ri3ZluVItqbDi0kfm7BHSxjwRXbpw9m9kFhXGjnzHKh';
access_token = '419412786-cpS2hDmR6cuIf8BD2kSSri0BAWAmXBA3pzcB56Pw';
access_secret = 'pRx5MNKkmxyImwuhUFMNVOr1NrAWcRmOGUgGTLVYFAjsJ';
dictDb = {}
#connect our DB
neo4jInt = neo4jInterface.neo4jInterface()
#graphDB=neo4jInt.connect('localhost:7474/db/data/','neo4j','admin')
graphDB=neo4jInt.connect()

try:
    #neo4J create a unique for a node only then a create operation will be successfull
    graphDB.cypher.execute("""CREATE CONSTRAINT ON (n:name) ASSERT n.id IS UNIQUE """)
    graphDB.cypher.execute("""CREATE CONSTRAINT ON (n:category) ASSERT n.name IS UNIQUE """)
    pass
except:
    pass

####
#read the file of dictionary words and load into a python dict
dictfile = 'egdict.txt'
a = open(dictfile)
lines = a.readlines()
a.close()
dic = {}

# a default category for simple word lists
current_category = "Default"
# inhale the dictionary
for line in lines:
    if line[0:2] == '>>':
        current_category = string.strip( line[2:] )
        dic[current_category]= []
        tmp =[]
        #print current_category
    else:
        line = line.strip()
        if len(line) > 0:
            #print line
            tmp.append(line)
            dic[current_category]= tmp

def creatCategoryNode():
        labels=['category']
        print dic.get('cCategory')
        for pattern in dic.get('cCategory'):
            print("pattern:",pattern)
            create_node_query = """
            WITH {pattern} AS p
            CREATE (n:category{name:p})     RETURN n   """
            # Send Cypher query.
            n=graphDB.cypher.execute(create_node_query,pattern=pattern)
#create category node
creatCategoryNode()

class listener(StreamListener):
    def categoryMaterialize(self,text):
        material =[]
        for pattern in dic.get('cCategory'):
            if re.search(pattern,text,re.I|re.L):
               material.append(pattern)
        if len(material) <=0:
            material =['Volunteer']
        return tuple(material)

    def locationAreas(self,text):
        for pattern in dic.get('Areas'):
        #print ("pattern :%s",pattern)
            if re.search(pattern,text,re.I|re.L):
                return pattern

    def creatNode(self,data_json):
        labels=['users']
        print "satheesh1"
        add_tweet_query = """
        WITH {data_json} AS data
        UNWIND data AS t
        MERGE (u:users {id:t.id})
            ON CREATE SET
             """+   (('u:'+',u:'.join(labels)+",") if labels else '') +"""
                u.typesh=t.typesh,
                u.screen_name=t.user.screen_name,
                u.id=t.id,
                u.created_at=t.user.created_at,
                u.text=t.text,
                u.category=t.category,
                u.area_place=t.area_place,
                u.location=t.location,
                u.time_zone=t.time_zone,
                u.utc_offset=t.utc_offset,
                u.profile_image_url=t.profile_image_url,
                u.geo_enabled=t.geo_enabled,
                u.verified=t.verified,
                u.notifications=t.notifications
            """ +   (("ON MATCH SET\n  u:"+',u:'.join(labels)) if labels else '') +"""
            RETURN u
        """
        # Send Cypher query.
        n=graphDB.cypher.execute(add_tweet_query,data_json=data_json)

        relation_query = """
        MATCH (a:Person),(b:Person)
        WHERE a.name = 'Node A' AND b.name = 'Node B'
        CREATE (a)-[r:RELTYPE]->(b)
        RETURN r
        """
        return n

    def on_data(self, data):
        data = json.loads(data)
        #print(data['text'])
        if data['retweeted']:
            return fail
        text = data['text']
        text = text.encode('utf-8') # lowercase the text
        #print dic
        for key in dic.keys():
            if key=='cCategory':
                break
            for pattern in dic.get(key):
                #print ("pattern :%s",pattern)
                if re.search(pattern,text,re.I|re.L):
                   data[unicode('typesh')]=key
                   #print text
                   #print key
                   catList= self.categoryMaterialize(text)
                   area_place= self.locationAreas(text)
                   print (catList,area_place)
                   data[unicode('category')]=catList
                   data[unicode('area_place')]=area_place
                   print "satheesh"
                   self.creatNode(data)
                   #print data
                   return 0


    def on_error(self, status):
        print status

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#chennaiRainsHelp","#Chennaivolunteer","#chennairescue"])
