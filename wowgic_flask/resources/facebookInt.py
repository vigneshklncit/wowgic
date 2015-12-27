#! /usr/bin/python
#===============================================================================
# File Name      : facebookInt.py
# Date           : 12-22-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
import sys
sys.path.append('../common')
import loggerRecord, globalS
logger =  loggerRecord.get_logger()



class facebookInt:
    ''' bla bla
    '''
    def get_facebook_oauth_token(self):
        globalS.dictDb['fbToken'] = session.get('facebook_token')
        return globalS.dictDb['fbToken']