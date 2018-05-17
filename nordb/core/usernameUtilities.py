"""
This file contains all functions for handling the .nordb.config file in the nordb folder that contains the name of the user handling all postgres operations. 

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
    Method for configuring the .nordb.config to the format user wants it to be.

    :param str username: the username given by user
    """
    #this needs to be rewritten
#    config_file = ".nordb.config"
#    f = open(MODULE_PATH + os.sep + config_file, "w")
#    f.write(username)
#    f.close()
#    settings.updateUsername()

def log2nordb(password = None):
    """
    Function that logs to database and returns a psycopg2 Connect object.
    
    :return: psycopg2.Connect object
    """
    if password is not None:
        settings.database_settings[settings.active_database]["password"] = password

    if settings.test:
        return psycopg2.connect(**settings.database_settings["test database"])
    else:
        return psycopg2.connect(**settings.database_settings[settings.active_database])

