"""
This module contains all settings needed by the program. It supplies all other modules with the username and database name.
"""
import os

test = False

def init():
    global dbname 
    global username
#    global test
    dbname = "nordb"
    conf_name = ".user.config"
#    test = False
    try:
        username = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + conf_name).read().strip()
    except FileNotFoundError:
        username = None

def updateUsername():
    conf_name = ".user.config"
    global username
    username = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + conf_name).read().strip()

def setTest():
    global test
    test = True

init()
