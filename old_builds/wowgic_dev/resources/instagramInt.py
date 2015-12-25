#! /usr/bin/python
#===============================================================================
# File Name      : .py
# Date           : 12-21-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
from instagram.client import InstagramAPI
from random import randint
import sys
from collections import OrderedDict

client_id = '081ccf9e86164090af417c8ce91cc2e4'
client_secret = '5b623638585b46cd9d35a203e84114e0'
access_token = 'XXXXXXXX'
client_ip = 'XX.XX.XX.XX'

class twitterInt:
    ''' bla bla
    '''
    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        #authenticate twitter app
        api = InstagramAPI(client_id=client_id, client_secret=client_secret, client_ips= client_ip,access_token= access_token)

    def retrieveTweetsBasedHashtag(self):
        feeds =[]

media_all_ids=[]

#get recent media ids with the tag "instadogs", only get the most recent 80
#tag_recent_media returns 2 variables, the media ID in an array and the next
#url for the next page
media_ids,next = api.tag_recent_media(tag_name='madurai', count=1)

#obtain the max_tag_id to use to get the next page of results
temp,max_tag=next.split('max_tag_id=')
max_tag=str(max_tag)

for media_id in media_ids:
        media_all_ids.append(media_id.id)

counter = 1

#the while loop will go through the first 3 pages of resutls, you can increase this
# but you also need to increase the count above.
while next and counter < 3 :
        more_media, next = api.tag_recent_media(tag_name='instadogs', max_tag_id=max_tag)
        temp,max_tag=next.split('max_tag_id=')
        max_tag=str(max_tag)
        for media_id2 in more_media:
                media_all_ids.append(media_id2.id)
        print len(media_all_ids)
        counter+=1

#remove dublictes if any.
media_all_ids=list(OrderedDict.fromkeys(media_all_ids))

print len(media_all_ids)
