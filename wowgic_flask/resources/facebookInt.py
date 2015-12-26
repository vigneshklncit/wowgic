#! /usr/bin/python
#===============================================================================
# File Name      : facebookInt.py
# Date           : 12-22-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
from flask_oauth import OAuth
from flask import url_for, request
import sys
sys.path.append('../common')
import loggerRecord, globalS

FACEBOOK_APP_ID = '575443062564498'
FACEBOOK_APP_SECRET = '3112a499e27dcd991b9869a5dd5524c0'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

class facebookInt:
    ''' bla bla
    '''
    def facebook_login(self):
        fbCallback= facebook.authorize(callback=url_for('facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))
        logger.debug("fb callback url %s",fbCallback)
        return facebook.authorize(callback=url_for('facebook_authorized',
            next=request.args.get('next') or request.referrer or None,
            _external=True))

    @facebook.authorized_handler
    def facebook_authorized(self,resp):
        logger.debug("fb rcvd Response url %s",resp)
        if resp is None:
            return 'Access denied: reason=%s error=%s' % (
                request.args['error_reason'],
                request.args['error_description']
            )
        globalS.dictDb['logged_in'] = True
        globalS.dictDb['facebook_access_token'] = (resp['access_token'], '')
        #globalS.dictDb['facebook_access_token'] = session['facebook_token']
        me = facebook.get('/me')
        return me

    def get_facebook_oauth_token(self):
        globalS.dictDb['fbToken'] = session.get('facebook_token')
        return globalS.dictDb['fbToken']