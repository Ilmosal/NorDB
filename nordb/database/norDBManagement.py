"""
This module contains all basic functions of the database which do not fit quite to the other modules.

Functions and Classes
---------------------
"""

import sys
import os
import datetime
import psycopg2
from subprocess import call
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep

BACKUP_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + os.sep + "backups" + os.sep

from nordb.core import usernameUtilities
from nordb import settings

def countEvents(solution_type = None):
    """
    Function for returning the number of all events in the database.

    :param solution_type str: If solution_type is defined, countEvents will only count all events of the chosen type. Otherwise it will return the amount of all events in the database. 
    :returns: The number of events of the chosen type or number of all events
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    if solution_type is None:
        cur.execute("SELECT COUNT(*) FROM nordic_event")
    elif solution_type in "OAPRFS":
        cur.execute("SELECT COUNT(*) FROM nordic_event WHERE solution_type = %s", (solution_type,))
    else:
        raise Exception("Solution type not a valid solution type: ({0})".format(solution_type))

    return cur.fetchone()[0]

def countStations(network = None):
    """
    Function for returning the number of all stations in the database

    :param network str: If network is given, the function will only return the amount of stations in the given network.
    :returns: The number of stations in given network or number of all stations.
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    if network is None:
        cur.execute("SELECT COUNT(*) FROM station")
    else:
        cur.execute("SELECT COUNT(*) FROM station WHERE network = %s", (network,))

    return cur.fetchone()[0]

def createDatabase():
    """
    Method for creating the database if the database doesn't exist.
    """
    conn = psycopg2.connect("dbname = postgres user={0}".format(settings.username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    if settings.test:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'test_nordb'")
    else:
        cur.execute("SELECT 1 FROM pg_database WHERE datname='{0}'".format(settings.dbname))

    if cur.fetchall():
        conn.close()
        raise Exception("Database already exists")

    if settings.test:
        cur.execute("CREATE DATABASE test_nordb")
    else:
        cur.execute("CREATE DATABASE {0}".format(settings.dbname))
    
    conn.commit()
    conn.close()
    
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    
    cur.execute(open(MODULE_PATH + "sql/nordic_event_root.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_file.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/creation_info.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_event.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/scandia_header.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_modified.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_main.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_comment.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_error.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_macroseismic.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_waveform.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/network.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/station.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/sitechan.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/instrument.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/sensor.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_phase_data.sql", "r").read())

    conn.commit()
    conn.close()

def destroyDatabase():
    """
    Method for destroying the database if the database exists
    """
    conn = psycopg2.connect("dbname = postgres user={0}".format(settings.username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    if settings.test:
        cur.execute("SELECT 1 FROM pg_database WHERE datname='test_nordb'")
    else:
        cur.execute("SELECT 1 FROM pg_database WHERE datname='{0}'".format(settings.dbname))
    if not cur.fetchall():
        conn.close()
        raise Exception("Database does not exist")

    conn.close()

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("DROP SCHEMA public CASCADE")

    conn.commit()
    conn.close()

    conn = psycopg2.connect("dbname = postgres user={0}".format(settings.username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    if settings.test:
        cur.execute("DROP DATABASE test_nordb")
    else:
        cur.execute("DROP DATABASE {0}".format(settings.dbname))

    conn.commit()
    conn.close()

def createBackup():
    """
    """
    backup_name = BACKUP_PATH + "backup_" + datetime.datetime.now().strftime("%Y%jT%H%M%S")
    call(["pg_dump","-Fc", "nordb", "-f", backup_name])

def loadBackup(backup_path):
    """
    """
    destroyDatabase()
    
    conn = psycopg2.connect("dbname = postgres user={0}".format(settings.username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    if settings.test:
        cur.execute("CREATE DATABASE test_nordb")
    else:
        cur.execute("CREATE DATABASE {0}".format(settings.dbname))
    
    conn.commit()
    conn.close()
    
    call(["pg_restore", "-d", "nordb", backup_path])

