"""
This module contains all settings needed by the program. It supplies all other modules with the username and database name.
"""
import os

def init():
    global dbname 
    dbname = "nordb"
    global username
    try:
        username = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + ".user.config").read().strip()
    except FileNotFoundError:
        username = None

def updateUsername():
    username = open(os.path.dirname(os.path.realpath(__file__)) + os.sep + ".user.config").read().strip()

init()
