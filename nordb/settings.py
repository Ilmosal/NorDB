"""
This module contains all settings needed by the program. It supplies all other modules with the username and database name.
"""
import os

test = False
config_file_name = os.path.dirname(os.path.realpath(__file__)) + os.sep + ".nordb.config"

def init():
    global database_settings
    database_settings = {}
    global active_database
    try:
        config_file = open(config_file_name, 'r').readlines()
    except:
        raise Exception("No config file for the database! Run nordb conf to create the config file")
    read_info = -1
    database_config = {}
    read_name = None

    for line in config_file:
        if line[0] == "#":
            continue
        if line[:len("Active database:")] == "Active database:":
            active_database = line[len("Active database:"):].strip()

        elif read_info == 5:
            if line[:len("host_port:")] == "host_port:":
                database_config["port"] = line[len("host_port:"):].strip()
                read_info = -1
            else:
                raise Exception("host_ip not in correct format or in right place")

        elif read_info == 4:
            if line[:len("host_ip:")] == "host_ip:":
                database_config["host"] = line[len("host_ip:"):].strip()
                read_info += 1
            else:
                raise Exception("host_ip not in correct format or in right place")

        elif read_info == 3:
            if line[:len("location:")] == "location:":
                if line[len("location:"):].strip() == "local":
                    database_config['location'] = 'local'
                    read_info = -1
                elif line[len("location:"):].strip() == "remote":
                    read_info += 1
                    database_config['location'] = 'remote'
            else:
                raise Exception("database location not in correct format or in right place")

        elif read_info == 2:
            if line[:len("password:")] == "password:":
                database_config["password"] = line[len("password:"):].strip()
                read_info += 1
            else:
                raise Exception("password not in correct format or in right place")

        elif read_info == 1:
            if line[:len("username:")] == "username:":
                database_config["user"] = line[len("username:"):].strip()
                read_info += 1
            else:
                raise Exception("username not in correct format or in right place")

        elif read_info == 0:
            if line[:len("name:")] == "name:":
                database_config["dbname"] = line[len("name:"):].strip()
                read_info += 1
            else:
                raise Exception("dbname not in correct format or in right place")

        elif line[0] == '-' and read_info == -1:
            read_name = line.strip()[1:-1]
            read_info = 0

        if read_name is not None and read_info == -1:
            database_settings[read_name] = database_config
            read_name = None
            database_config = {}

def updateUsername():
    init()

def setTest():
    global test
    test = True

def getDBName():
    return database_settings[active_database]["dbname"]

def getUsername():
    return database_settings[active_database]["user"]

init()
