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

