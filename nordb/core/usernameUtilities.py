import os
import logging

import psycopg2

MODULE_PATH = os.path.realpath(__file__)[:-len("core/usernameUtilities.py")]

def confUser(username):
    """
    Method for configuring the .user.config to the format user wants it to be.

    Args:
        username(str): the username given by user
    """
    f = open(MODULE_PATH + ".user.config", "w")
    f.write(username)
    f.close()

def readUsername():
    """
    Method for reading the .user.config file and loading it on the module that requires it.
    
    Returns:
        The username as a string
    """
    try:
        f_user = open(MODULE_PATH + ".user.config")
        username = f_user.readline().strip()
        f_user.close()
    except:
        logging.error("No .user.config file!! Run the program with conf command to initialize the .user.config")
        sys.exit(-1)
    return username

def log2nordb():
    """
    Function that logs to database and returns a psycopg2 cur object.

    Returns:
        cur object.
    """
    username = readUsername()

    try:
        conn = psycopg2.connect("dbname = nordb user = {0}".format(username))
    except psycopg2.Error as e:
        logging.error("Program couldn't connect to the database!\nError: {0}".format(e))
        print("Problem with connecting! See error messages in error logs")
        sys.exit()

    cur = conn.cursor()

    return conn.cursor()
