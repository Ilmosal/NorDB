"""
This file contains all functions for configuring the .nordb.config file.

Functions and Classes
---------------------
"""

import os
from nordb import settings

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def confExists():
    """
    Method for checking whether .nordb.config file exists
    """
    config_file = ".nordb.config"

    return os.path.isfile(MODULE_PATH + os.sep + config_file)

def getActiveDatabase():
    """
    This function returns the current active database configuration name to the user

    :returns: database configuration name as a string
    """
    return settings.active_database

def getDabaseConfiguration(conf_name):
    """
    Function for returning a database configuration to the user

    :returns: the database configuration dict
    """
    if conf_name not in settings.database_settings.keys():
        raise Exception("No such configuration in the database")
    return settings.database_settings[conf_name]

def changeActiveDatabase(conf_name):
    """
    Function for changing the current active database

    :param str conf_name: name of the configuration that will be the new active database
    """
    if conf_name not in settings.database_settings.keys():
        raise Exception("Configuration name not listed in your configuration file! Does database with configuration name {0} exist?".format(conf_name))

    writeDBConf(settings.database_settings, conf_name)

def listConfigurations():
    """
    Function for listing all database settings
    """
    return settings.database_settings

def alterDBConf(old_conf_name, new_conf_name, db_name, db_username, db_password, db_location='local', host_ip = None, host_port = None):
    """
    Function for altering a single database configuration.

    :param str old_conf_name: name of the old configuration
    :param str new_conf_name: new name for the configuration
    :param str db_name: name for the database
    :param str db_username: username in the database
    :param str db_password: password of the user
    :param str db_location: 'remote' or 'local'
    :param str host_ip: ip of the remote machine
    :param str host_port: port to which nordb will accept
    """
    if db_location not in ['remote', 'local']:
        raise Exception('db_location is not remote or local. ({0})'.format(db_location))

    removeDBFromConf(old_conf_name)
    addDBToConf(new_conf_name, db_name, db_username, db_password, db_location, host_ip, host_port)

    if settings.active_database == old_conf_name:
        changeActiveDatabase(new_conf_name)

def removeDBFromConf(conf_name):
    """
    Method for removing a database from your configuration.
    """
    db_settings = settings.database_settings

    if conf_name not in db_settings.keys():
        raise Exception("Database with conf_name {0} does not exist!".format(conf_name))
    if conf_name is 'test database':
        raise Exception("Do not remove test database!")

    del db_settings[conf_name]
    writeDBConf(db_settings, settings.active_database)

def addDBToConf(conf_name, db_name, db_username, db_password, db_location = 'local', host_ip = None, host_port = None):
    """
    Method for adding a database configuration to the your own database configuration.

    :param str username: the username given by user
    """
    db_settings = settings.database_settings
    if conf_name in db_settings.keys():
        raise Exception('database with conf_name {0} already exists! Please use another name or alter the existing configuration'.format(conf_name))

    if db_location not in ['local', 'remote']:
        raise Exception('db_location is not remote or local. ({0})'.format(db_location))

    db_settings[conf_name] = {  'dbname':db_name,
                                'user':db_username,
                                'password':db_username,
                                'location':db_location,
                                'host':host_ip,
                                'port':host_port}

    writeDBConf(db_settings, settings.active_database)

def writeDBConf(db_settings, active_database):
    """
    Function for writing the database config file out

    :param Dict db_settings: settings that will be written as the config
    """
    config_file = ".nordb.config"

    conf_string = "Active database: {0}\n\n".format(active_database)
    for conf_name in db_settings.keys():
        conf_string += "-{0}-\n".format(conf_name)
        conf_string += "name: {0}\n".format(db_settings[conf_name]['dbname'])
        conf_string += "username: {0}\n".format(db_settings[conf_name]['user'])
        conf_string += "password: {0}\n".format(db_settings[conf_name]['password'])
        conf_string += "location: {0}\n".format(db_settings[conf_name]['location'])

        if db_settings[conf_name]['location'] == 'remote':
            conf_string += "host_ip: {0}\n".format(db_settings[conf_name]['host'])
            conf_string += "host_port: {0}\n".format(db_settings[conf_name]['port'])

        conf_string += "\n"

    f = open(MODULE_PATH + os.sep + config_file, "w")
    f.write(conf_string)
    f.close()
    settings.updateUsername()
