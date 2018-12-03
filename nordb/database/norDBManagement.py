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

def databaseIsRunning():
    """
    Function for checking out if database is running and can be connected to

    :returns: True if database is running
    """
    try:
        conn = usernameUtilities.log2nordb()
    except:
        return False
    return True

def checkPermissions(required_role, db_conn = None):
    """
    Function that checks the owner level of the current user and returns this.

    :param required_role str: the required role level of the user
    :returns: boolean value if the current_user has access rights of the required role
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()
    cur.execute("SELECT role FROM nordb_user WHERE username = CURRENT_USER")
    user_role = cur.fetchone()[0]

    if db_conn is None:
        conn.close()
    return (getRoleLevel(required_role) <= getRoleLevel(user_role))

def getRoleLevel(role_str):
    """
    Helper function to calculate role level from the role string
    :param role_str str: The role level string
    :returns: the level of the role as a integer 
    """
    role_level = 0
    if role_str == 'quests':
        role_level = 1
    elif role_str == 'default_users':
        role_level = 2
    elif role_str == 'station_managers':
        role_level = 3
    elif role_str == 'admins':
        role_level = 4
    elif role_str == 'owner':
        role_level = 5
    else:
        raise Exception("No such role in the system! ({0})".format(role_str))

    return role_level

def countEvents(solution_type = None, db_conn = None):
    """
    Function for returning the number of all events in the database.

    :param solution_type str: If solution_type is defined, countEvents will only count all events of the chosen type. Otherwise it will return the amount of all events in the database.
    :returns: The number of events of the chosen type or number of all events
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    if solution_type is None:
        cur.execute("SELECT COUNT(*) FROM nordic_event")
    elif len(solution_type) <= 6:
        cur.execute("SELECT COUNT(*) FROM nordic_event WHERE solution_type = %s", (solution_type,))
    else:
        if db_conn is None:
            conn.close()
        raise Exception("Solution type too long")

    ans = cur.fetchone()[0]

    if db_conn is None:
        conn.close()

    return ans

def countStations(network = None, db_conn = None):
    """
    Function for returning the number of all stations in the database

    :param network str: If network is given, the function will only return the amount of stations in the given network.
    :returns: The number of stations in given network or number of all stations.
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    if network is None:
        cur.execute("SELECT COUNT(*) FROM station")
    else:
        cur.execute("SELECT COUNT(*) FROM station WHERE network = %s", (network,))

    num_stations = cur.fetchone()[0]

    if db_conn is None:
        conn.close()

    return num_stations

def createDatabase():
    """
    Method for creating the database if the database doesn't exist. Postgres createdb rights required. You will be automatically the owner of the database.
    """
    if not settings.test:
        params = {
            "dbname":"postgres",
            "user":settings.database_settings[settings.active_database]["user"],
            "password":settings.database_settings[settings.active_database]["password"]
        }
    else:
        params = {
            "dbname":"postgres",
            "user":settings.database_settings['test database']["user"],
            "password":settings.database_settings['test database']["password"]
        }
    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    if settings.test:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'test_nordb'")
    else:
        cur.execute("SELECT 1 FROM pg_database WHERE datname='{0}'".format(settings.getDBName()))

    if cur.fetchall():
        conn.close()
        raise Exception("Database already exists")

    if settings.test:
        cur.execute("CREATE DATABASE test_nordb")
    else:
        cur.execute("CREATE DATABASE {0}".format(settings.getDBName()))

    conn.commit()
    conn.close()

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute(open(MODULE_PATH + "sql/create_roles.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordb_user.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/creation_info.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_event_root.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_file.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/solution_type.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_event.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_main.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_error.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_comment.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_macroseismic.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_waveform.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_phase_data.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/network.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/station.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/sitechan.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/response.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/fap_response.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/paz_response.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/instrument.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/sensor.sql", "r").read())

    cur.execute(open(MODULE_PATH + "sql/nordb_user_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/creation_info_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_event_root_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_file_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/solution_type_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_event_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_main_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_error_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_comment_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_macroseismic_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_header_waveform_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/nordic_phase_data_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/network_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/station_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/sitechan_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/instrument_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/sensor_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/response_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/fap_response_policies.sql", "r").read())
    cur.execute(open(MODULE_PATH + "sql/paz_response_policies.sql", "r").read())

    cur.execute(open(MODULE_PATH + "sql/grant_access.sql", "r").read())

    conn.commit()
    conn.close()

def createUser(username, user_role, password, db_conn = None):
    """
    Creates a new user to the database. Admin rights required.
    :param username str: the username of the new user
    :param user_role str: the role of the new user
    :param password str: the password of the new user
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    if not checkPermissions('admins', conn):
        raise Exception('You are not an admin in the database so you cannot run this command')

    cur = conn.cursor()

    try:
        if user_role not in ['guests', 'default_users', 'station_managers', 'admins']:
            raise Exception("User role not a valid user role ({0})".format(user_role))

        cur.execute("SELECT * FROM pg_roles WHERE rolname = %s", (username,))
        if cur.fetchone() is not None:
            raise Exception("The user already exists! Chooose another username. ({0})".format(username))

        if len(username) > 32:
            raise Exception('Username too long!')

        cur.execute("CREATE USER {0} IN ROLE {1} PASSWORD %s".format(username,
                                                                     user_role),
                    (password,))
        cur.execute("INSERT INTO nordb_user (username, role) VALUES (%s, %s)",
                    (username, user_role))
        if user_role == 'admins':
            cur.execute("ALTER USER {0} WITH CREATEROLE".format(username))
    except Exception as e:
        if db_conn is None:
            conn.close()
        raise e

    conn.commit()
    if db_conn is None:
        conn.close()

def removeUser(username, db_conn = None):
    """
    Removes a user from the database and postgres system. Admin rights required.
    :param username str:
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    if not checkPermissions('admin', conn):
        raise Exception('You are not an admin in the database so you cannot run this command')

    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM pg_roles WHERE rolname = %s", (username,))
        if cur.fetchone() is None:
            raise Exception("The user does not exist! Chooose another username. ({0})".format(username))

        cur.execute("DELETE FROM nordb_user WHERE username = %s", (username, ))
        cur.execute("DROP ROLE {0}".format(username))
    except Exception as e:
        if db_conn is None:
            conn.close()
        raise e

    conn.commit()
    if db_conn is None:
        conn.close()

def alterUser(username, new_username = None, new_user_role = None, new_password = None, db_conn = None):
    """
    Alters user in the database. If you modify your own user, this is allowed for default_users, otherwise admin rights required. NOT DONE YET!
    :param username str: the username of the user which will be modified
    :param new_username str: The username which will be the new username of the user
    :param new_user_role str: The role which will be the new role of the user. Options: guests, default_users, station_managers and admins
    :param new_password str: The new password to the database
    """

    if username == settings.database_settings[settings.active_database]["user"]:
        if not checkPermissions('default_user'):
            raise Exception('You are not a user in the database so you cannot modify yourself')
    else:
        if not checkPermissions('admin'):
            raise Exception('You are not an admin in the database so you cannot alter other users')

    if len(new_username) > 32:
        raise Exception("New username is too long! Maximum lenght of 32 characters")

    if new_user_role not in ['guests', 'default_users', 'station_managers', 'admins']:
        raise Exception("User role not a valid user role ({0})".format(new_user_role))

    pass

def destroyDatabase():
    """
    Method for destroying the database if the database exists
    """
    if not checkPermissions('owner'):
        raise Exception('You are not the owner of the database so you cannot run this command')

    if not settings.test:
        params = {
            "dbname":"postgres",
            "user":settings.database_settings[settings.active_database]["user"],
            "password":settings.database_settings[settings.active_database]["password"]
        }
    else:
        params = {
            "dbname":"postgres",
            "user":settings.database_settings['test database']["user"],
            "password":settings.database_settings['test database']["password"]
        }

    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    if settings.test:
        cur.execute("SELECT 1 FROM pg_database WHERE datname='test_nordb'")
    else:
        cur.execute("SELECT 1 FROM pg_database WHERE datname='{0}'".format(settings.getDBName()))

    if not cur.fetchall():
        conn.close()
        raise Exception("Database does not exist")

    conn.close()

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("DROP SCHEMA public CASCADE")

    conn.commit()
    conn.close()

    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    if settings.test:
        cur.execute("DROP DATABASE test_nordb")
    else:
        cur.execute("DROP DATABASE {0}".format(settings.getDBName()))

    conn.commit()
    conn.close()

def createBackup():
    """
    Function that creates a backup of the database in its current form and saves it to the backups folder.
    """
    backup_name = BACKUP_PATH + "backup_" + datetime.datetime.now().strftime("%Y%jT%H%M%S")
    call(["pg_dump","-Fc", "nordb", "-f", backup_name])

def loadBackup(backup_path):
    """
    Function that destroys the database and loads a backup of the database into a new one.

    :param str backup_path: path to the database backup
    """
    destroyDatabase()

    params = {
        "dbname":"postgres",
        "user":settings.database_settings[settings.active_database]["user"],
        "password":settings.database_settings[settings.active_database]["password"]
    }
    conn = psycopg2.connect(**params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    if settings.test:
        cur.execute("CREATE DATABASE test_nordb")
    else:
        cur.execute("CREATE DATABASE {0}".format(settings.getDBName()))

    conn.commit()
    conn.close()

    call(["pg_restore", "-d", "nordb", BACKUP_PATH+backup_path])
