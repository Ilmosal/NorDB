import os
import pytest
import psycopg2
from nordb.core import usernameUtilities

TEST_USER = "testname"

def setup_module(test_usernameUtilities):
    if os.path.isfile(usernameUtilities.MODULE_PATH + ".user.config"):
        f = open(usernameUtilities.MODULE_PATH + ".user.config", "r")
        f_temp = open(".temp.usrname", "w")
        f_temp.write(f.read().strip())
        f.close()
        f_temp.close()

def teardown_module(test_usernameUtilities):
    if os.path.isfile(".temp.usrname"):
        f = open(usernameUtilities.MODULE_PATH + ".user.config", 'w')
        f_temp = open(".temp.usrname", "r")
        f.write(f_temp.read().strip())
        f_temp.close()
        f.close()
        os.remove(".temp.usrname")

class TestConfUser(object):

    def testConfUserWritesUsername(self):
        usernameUtilities.confUser(TEST_USER)
        f = open(usernameUtilities.MODULE_PATH + ".user.config")
        username = f.readline().strip()
        assert username == TEST_USER

class TestReadUsername(object):
   
    def testReadSuccessful(self):
        open(usernameUtilities.MODULE_PATH + ".user.config", 'w').write(TEST_USER)
        username = usernameUtilities.readUsername()
        assert username == TEST_USER

    def testReadFail(self):
        if os.path.isfile(usernameUtilities.MODULE_PATH + ".user.config"):
            os.remove(usernameUtilities.MODULE_PATH + ".user.config")
        with pytest.raises(FileNotFoundError):
            usernameUtilities.readUsername()

class TestLog2NorDB(object):
    
    def testLogSuccesful(self):
        if not os.path.isfile(".temp.usrname"):
            pytest.skip("No username configured for the program")
        usernameUtilities.confUser(open(".temp.usrname").read().strip())
        conn = usernameUtilities.log2nordb()
        assert type(conn), psycopg2.Connect
   
    def testLogFailWithWrongUser(self):
        usernameUtilities.confUser("wrong")
        with pytest.raises(psycopg2.OperationalError):
            usernameUtilities.log2nordb()


