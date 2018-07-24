"""
This module contains function for logging into the database
Functions and Classes
---------------------
"""

import os
import logging

import psycopg2

from nordb import settings

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def databaseSettingsDict(db_dict):
    """
    Function for transfroming the database setting dict into a one that psycopg2 accepts.

    :param dict db_dict: Dict of from the database configuration file
    :returns: dict fitted for psycopg2.connect function
    """
    newdict = dict(db_dict)
    del newdict['location']
    return newdict

def log2nordb(password = None):
    """
    Function that logs to database and returns a psycopg2 Connect object.

    :return: psycopg2.Connect object
    """
    if password is not None:
        settings.database_settings[settings.active_database]["password"] = password

    if settings.test:
        return psycopg2.connect(**databaseSettingsDict(settings.database_settings["test database"]))
    else:
        return psycopg2.connect(**databaseSettingsDict(settings.database_settings[settings.active_database]))

