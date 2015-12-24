#! /usr/bin/python
#===============================================================================
# File Name      : wowgic_dev_tests.py
# Date           : 12-02-2015
# Input Files    : Nil
# Author         : Satheesh <sathishsms@gmail.com>
# Contributors   : Vivek , chelladurai
# Description    : To test the environment so that wowgic is ready to be fired. Check neo4J is installed up & running.
#                  setup.py has installed properly the required packages, IP and port are availble to take over, no critical envt
#                  alarms in the system etc
#===============================================================================
from nose.tools import *
import wowgic_dev

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I CAN BE RAN! Be Healthy Use wowgic"
