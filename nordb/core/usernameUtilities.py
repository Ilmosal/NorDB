import os

MODULE_PATH = os.path.realpath(__file__)[:-len("core/usernameUtilities.py")]

def confUser(username):
    f = open(MODULE_PATH + ".user.config", "w")
    f.write(username)
    f.close()
    return True

def readUsername():
    try:
        f_user = open(MODULE_PATH + ".user.config")
        username = f_user.readline().strip()
        f_user.close()
    except:
        logging.error("No .user.config file!! Run the program with conf command to initialize the .user.config")
        sys.exit(-1)
    return username
