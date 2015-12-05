#! /usr/bin/python
#===============================================================================
# File Name      : .py
# Date           : 12-02-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    :
#
#===============================================================================
import time
import sys
import argparse
import json
sys.path.append('../wowgic_dev')

import globalS
import generic
import loggerRecord
import neo4jInterface

####
# Get tweepy set up
import tweepy
from tweepy import Cursor

#parse the run-time args passed
parser = argparse.ArgumentParser(description='  To get the mra.log,rc.log,\
        qpTraces & tcpdump to the log viewer machine or any user defined server\
        all in one place with a single click. Works among multiple Active Pairs \
        (MPE\'s, MRA\'s)..................................................\
        Example: ./loggy CAM-92410 -c serverRack_C6GRsetup.cfg or ./loggy \
        CAM-92410 or ./loggy -v ',add_help=True)
#parser.add_argument('testName',help='Name suffixed to log file name generated')
#if the def file is not passed as arg thn take the default file.
parser.add_argument('-c', '--config',default='serverRack.def',help='definition file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.3')
parser.add_argument("-l", "--logLevel",default='error',help="Enable standard output verbosity")
args = parser.parse_args()


############################################################################
#Function Name  : compileFileName                                          #
#Input          : Nil                                                      #
#Return Value   : just sets the suffix fileName for logs                   #
############################################################################
def compileFileName():
    dayTime      = generic.dateTimeFields()
    dayTime     += '_'+'wowgic'
    return dayTime
############################################################################

globalS.init()#intialize the global variables
generic      = generic.generic()

#==============================================================================#
#           Opening log file to record all the cli outputs                     #
#==============================================================================#
sufFileName = compileFileName()
logFileName  = "/tmp/" + sufFileName + ".log"
logger       = loggerRecord.loggerInit(logFileName,args.logLevel)
logger.debug('Log file# %s & TestBed file ',logFileName)

#keys from twitter is stored here temp will be removed once we access the user credentials
#chella's credentials
consumer_key= 'HwvpHtsPt3LmOZocZXwtn72Zv';
consumer_secret = 'afVEAR0Ri3ZluVItqbDi0kfm7BHSxjwRXbpw9m9kFhXGjnzHKh';
access_token = '419412786-cpS2hDmR6cuIf8BD2kSSri0BAWAmXBA3pzcB56Pw';
access_secret = 'pRx5MNKkmxyImwuhUFMNVOr1NrAWcRmOGUgGTLVYFAjsJ';


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

neo4jInt = neo4jInterface.neo4jInterface()
graphDB=neo4jInt.connect()
####
# End of boilerplate, interesting code starts here:

try:
    logger.info('i:creating a constraint')
    graphDB.cypher.execute("""CREATE CONSTRAINT ON (n:name) ASSERT n.id IS UNIQUE """)
except:
    pass


#facbook
json_input = '{"id":"1240560189303114","name":"Mari Satheesh","hometown":{"id":"106076206097781","name":"Madurai, India"},"location":{"id":"106377336067638","name":"Bangalore, India"},"education":[{"school":{"id":"135521326484377","name":"Cathy Matriculationn Higher Secondary School"},"type":"High School"},{"school":{"id":"131854716845812","name":"KLN College of Engineering"},"type":"College"},{"school":{"id":"112188602140934","name":"kln"},"type":"College"}],"work":[{"employer":{"id":"114041451939962","name":"Sonus Networks"}}]}'
try:
    decoded = json.loads(json_input)

    # pretty printing of json-formatted string
    logger.info("%s", json.dumps(decoded, sort_keys=True, indent=4))

    logger.info ("JSON parsing example:%s ", decoded['id'])
    #print "Complex JSON parsing example: ", decoded['two']['list'][1]['item']

except (ValueError, KeyError, TypeError):
    logger.error("JSON format error")


    ############################################################################
    #Function Name  : exeCmd                                                   #
    #Input          : k--> ssh key                                             #
    #               : cmd --> cmd to send to the terminal                      #
    #Return Value   : string -->output content before the prompt               #
    ############################################################################
def create_or_get_node(twitter_user,labels=[]):
    data = {'id': twitter_user.id,
        'name': twitter_user.name,
        'description': twitter_user.description,
        #'url': twitter_user.url,
        #'followers_count': twitter_user.followers_count,
        #'friends_count': twitter_user.friends_count,
        #'listed_count': twitter_user.listed_count,
        #'statuses_count': twitter_user.statuses_count,
        #'favourites_count': twitter_user.favourites_count,
        #'location': twitter_user.location,
        #'time_zone': twitter_user.time_zone,
        #'utc_offset': twitter_user.utc_offset,
        #'lang': twitter_user.lang,
        #'profile_image_url': twitter_user.profile_image_url,
        #'geo_enabled': twitter_user.geo_enabled,
        #'verified': twitter_user.verified,
        #'notifications': twitter_user.notifications,
    }
    query_string = """
        MERGE (u:User {id:{id}})
        ON CREATE SET
"""+   (('u:'+',u:'.join(labels)+",") if labels else '') +"""
            u.name={name},
            #u.screen_name={screen_name},
            #u.description={description},
            #u.url={url},
            #u.followers_count={followers_count},
            #u.friends_count={friends_count},
            #u.listed_count={listed_count},
            #u.statuses_count={statuses_count},
            #u.favourites_count={favourites_count},
            #u.location={location},
            #u.time_zone={time_zone},
            #u.utc_offset={utc_offset},
            #u.lang={lang},
            #u.profile_image_url={profile_image_url},
            #u.geo_enabled={geo_enabled},
            #u.verified={verified},
            #u.notifications={notifications}
""" +   (("ON MATCH SET\n  u:"+',u:'.join(labels)) if labels else '') +"""
        RETURN u
    """
    logger.debug("quer string is %s",query_string)
    n=graphDB.cypher.execute_one(query_string, parameters=None, **data)
    return n


def insert_user_with_friends(twitter_user,user_labels=[]):
    user_labels.append("user")
    #if isinstance(twitter_user, str):
    #    try:
    #        twitter_user = api.get_user(twitter_user)
    #    except:
    #        time.sleep(60 * 16)
    #        friend = friends.next()
    #create_or_get_node(twitter_user,user_labels)
    #friend_count = 0
    #print(u"\nINSERTING FOR: {}".format(twitter_user.name))
    #friends = Cursor(api.friends, user_id=twitter_user.id_str, count=200).items()
    #try:
    #    while True:
    #        try:
    #            friend = friends.next()
    #        except tweepy.TweepError:
    #            print("exceeded rate limit. waiting")
    #            time.sleep(60 * 16)
    #            friend = friends.next()
    #
    #        #print u"    INSERTING: {}".format(friend.name)
    #        friend_count += 1
    #        sys.stdout.write('.')
    #        if(friend_count%10 == 0): sys.stdout.write(' ')
    #        if(friend_count%50 == 0): sys.stdout.write('| ')
    #        if(friend_count%100 == 0): print


        #create_or_get_node(friend)
        #n=graphDB.cypher.execute_one("""
        #MATCH (user:User {id:{user_id_str}}),(friend:User {id_str:{friend_id_str}})
        #CREATE UNIQUE (user)-[:FOLLOWS]->(friend)
        #""", parameters=None, user_id_str=twitter_user.id)
        ##except StopIteration:
        ##    print(u"\n    Total Friend Count = {}".format(friend_count))




# Add me and all my colleagues to the db along with all of our friends.
#insert_user_with_friends('swtit',["Neo"])
insert_user_with_friends('satheesh',["wowgic_test"])

#Now you add yourself and add those that you find interesting.
