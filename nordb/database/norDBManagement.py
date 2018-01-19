"""
This module contains all functions for creating or destroying the database.

Functions and Classes
---------------------
"""

import sys
import os
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

MODULE_PATH = os.path.realpath(__file__)[:-len("norDBManagement.py")]

from nordb.core import usernameUtilities
from nordb import settings

def createDatabase():
    """
    Method for creating the database if the database doesn't exist.
    """
    conn = psycopg2.connect("dbname = postgres user={0}".format(settings.username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname='{0}'".format(settings.dbname))
    if cur.fetchall():
        logging.error("Database already exists. Destroy the database with destroy and try again!")
        conn.close()
        sys.exit()

    cur.execute("CREATE DATABASE {0}".format(settings.dbname))

    conn.commit()
    conn.close()
    
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    
    cur.execute(open(MODULE_PATH + "../sql/nordic_event_root.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_file.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/creation_info.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_event.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/scandia_header.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_modified.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_header_main.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_header_comment.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_header_error.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_header_macroseismic.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_header_waveform.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/network.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/station.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/sitechan.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/instrument.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/sensor.sql", "r").read())
    cur.execute(open(MODULE_PATH + "../sql/nordic_phase_data.sql", "r").read())

    conn.commit()
    conn.close()

def destroyDatabase():
    """
    Method for destroying the database if the database exists
    """
    conn = psycopg2.connect("dbname = postgres user={0}".format(settings.username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname='{0}'".format(settings.dbname))
    if not cur.fetchall():
        logging.error("Database doesn't exists. Exiting program.")
        conn.close()
        sys.exit()

    conn.close()

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("DROP SCHEMA public CASCADE")

    conn.commit()
    conn.close()

    conn = psycopg2.connect("dbname = postgres user={0}".format(settings.username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("DROP DATABASE {0}".format(settings.dbname))

    conn.commit()
    conn.close()
