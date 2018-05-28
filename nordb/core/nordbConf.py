"""
This file contains all functions for configuring the .nordb.config file. 

Functions and Classes
---------------------
"""

import os

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def confExists():
    """
    Method for checking whether .nordb.config file exists
    """
    config_file = ".nordb.config"

    return os.path.isfile(MODULE_PATH + os.sep + config_file)

def confUser():
    """
    Method for configuring the .nordb.config to the format user wants it to be.

    :param str username: the username given by user
    """
    #this needs to be rewritten
    config_file = ".nordb.config"
    config_string = "Active database: local nordb\n"
    config_string = "\n"
    config_string = "-local nordb-\n"
    config_string = "name: nordb\n"
    config_string = "username: \n"
    config_string = "password: \n"
    config_string = "location: local\n"
    config_string = "\n"
    config_string = "-remote nordb-\n"
    config_string = "name: nordb\n"
    config_string = "username: \n"
    config_string = "password: \n"
    config_string = "location: \n"
    config_string = "host_ip: \n"
    config_string = "host_port: 5432\n"
    config_string = "\n"
    config_string = "-test database-\n"
    config_string = "name: test_nordb\n"
    config_string = "username: postgres\n"
    config_string = "password: \n"
    config_string = "location: local\n"

    f = open(MODULE_PATH + os.sep + config_file, "w")
    f.write(config_string)
    f.close()
    settings.updateUsername()
