"""
This file contains all functions for handling the .user.config file in the nordb folder that contains the name of the user handling all postgres operations. 

Functions and Classes
---------------------
"""

import os
import logging

import psycopg2
from nordb import settings

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def confUser(username):
    """
    Method for configuring the .user.config to the format user wants it to be.

    :param str username: the username given by user
    """
    print(MODULE_PATH + os.sep + ".user.config")
    f = open(MODULE_PATH + os.sep + ".user.config", "w")
    f.write(username)
    f.close()
    settings.updateUsername()

def log2nordb():
    """
    Function that logs to database and returns a psycopg2 Connect object.
    
    :return: psycopg2.Connect object
    """
    conn = psycopg2.connect("dbname = {0} user = {1}".format(settings.dbname, settings.username))

    return conn
