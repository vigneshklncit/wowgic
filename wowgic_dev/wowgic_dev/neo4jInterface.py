#! /usr/bin/python
#===============================================================================
# File Name      : .py
# Date           : 12-02-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Description    : This file just interfaces to neo4J and brings you the handle so that multiple files can
#
#===============================================================================
import loggerRecord
logger =  loggerRecord.get_logger()
####
# Get neo4j set up
#import py2neo
from py2neo import *

class neo4jInterface:
    ''' bla bla
    '''
    logger.debug('who invoked me ? hey u - %s',__name__)
    #REST server credentials
    #default Remember to change these credentials User/Pass.
    userName = 'Wowgic'
    passWord = 'GcpXosEMPJV5pLR0QJQ3'
    #Rest server uri
    #connectUri='neo-graciela-stracke-cornsilk-564c5f886175e.do-stories.graphstory.com:7473'
    connectUri='wowgic.sb02.stations.graphenedb.com:24789/db/data/'


    #optional authentication for database servers, enabled by default
    #authenticate(connectUri,userName,passWord)

    ############################################################################
    #Function Name  : connect                                                  #
    #Input          : IP -> IP of the machine to connect                       #
    #               : Username & password to connect with                      #
    #Return Value   : object to interact withe neo4j                           #
    ############################################################################
    def connect(self,c=connectUri,u=userName,p=passWord):
        '''The Graph class provides a wrapper around the REST API exposed by a running Neo4j database server and is
        identified by the base URI of the graph database'''
        #secure_graph frame the credentials
        secureUri = 'http://'+u+':'+p+'@'+c
        #secureUri = u+'/db/data/'
        logger.debug('who invoked me ? hey u - %s',secureUri)
        #return Graph(secureUri)
        return Graph(secureUri)

################################################################################
