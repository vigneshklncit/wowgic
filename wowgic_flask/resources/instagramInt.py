#! /usr/bin/python
#===============================================================================
# File Name      : .py
# Date           : 12-21-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
from instagram import client
from flask import url_for, redirect, request
import sys,json
sys.path.append('../common')
import loggerRecord, globalS
logger =  loggerRecord.get_logger()

from collections import OrderedDict

client_id = '081ccf9e86164090af417c8ce91cc2e4'
client_secret = '5b623638585b46cd9d35a203e84114e0'
access_token = '2300510664.081ccf9.545afdfe23b441dd9cfb3d8341c83ca7'
client_ip = 'XX.XX.XX.XX'
api=''

class instagramInt:
    ''' bla bla
    '''
    def __init__(self):
        logger.debug('who invoked me ? hey u - %s',__name__)
        #authenticate twitter app

    def instagram_login(self):

        redirect_uri = ('http://'+globalS.dictDb['HOST_NAME'] + url_for('handle_instagram_authorization'))
        instagram_client = client.InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
        return redirect(instagram_client.get_authorize_url(scope=['basic']))

    def handle_instagram_authorization(self):

        redirect_uri = ('http://'+globalS.dictDb['HOST_NAME'] + url_for('handle_instagram_authorization'))
        code = request.values.get('code')
        if not code:
            return error_response('Missing code')
        try:
            instagram_client = client.InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
            access_token, instagram_user = instagram_client.exchange_code_for_access_token(code)
            if not access_token:
                return 'Could not get access token'
            #update access_token to the instagram_user
            instagram_user['access_token'] = access_token
            globalS.dictDb['instagram_userid'] = instagram_user['id']
            globalS.dictDb['instagram_access_token']   = access_token
            logger.debug('access_token#%s, instagram_user#%s',access_token, instagram_user)
            #deferred.defer(fetch_instagram_for_user, g.user.get_id(), count=20, _queue='instagram')
        except Exception, e:
            return ('Error while handle_instagram_authorization')
        #return redirect(url_for('settings_data') + '?after_instagram_auth=True')
        #return globalS.dictDb
        return instagram_user

    def retrieveMediaBasedTags(self):
        '''get recent media ids with the tag "instadogs", only get the most recent 80
        tag_recent_media returns 2 variables, the media ID in an array and the next
        url for the next page'''
        api = client.InstagramAPI(client_id=client_id, client_secret=client_secret,access_token= access_token)
        media_ids,next = api.tag_recent_media(tag_name='madurai', count=1,return_json=True)
        for mid in media_ids:
            pass
            #mediaF=api.media(mid.id,return_json=True)
            #logger.debug('INstagram mediaIds:%s full_media:%s',mid,media_ids)
        #logger.debug('jsonify error:\n %s', mid)
        return media_ids

