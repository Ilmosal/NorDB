import os

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
    
    Returning:
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
