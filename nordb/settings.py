"""
This module contains all settings needed by the program. It supplies all other modules with the username and database name.
"""
import os

def init():
    global dbname 
    dbname = "nordb"
    global username
    username = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + ".user.config").read().strip()

def updateUsername():
    username = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + ".user.config").read().strip()

init()
