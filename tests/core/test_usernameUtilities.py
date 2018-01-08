import os
import pytest
import psycopg2
from nordb.core import usernameUtilities

TEST_USER = "testname"

class TestConfUser(object):
    
    def testConfUserWritesUsername(self):
        dummy = usernameUtilities.MODULE_PATH
        usernameUtilities.MODULE_PATH = ""
        usernameUtilities.confUser(TEST_USER)
        usernameUtilities.MODULE_PATH = dummy
        f = open(".user.config")
        os.remove(".user.config")
        username = f.readline().strip()
        assert username == TEST_USER

class TestReadUsername(object):
   
    def testReadSuccessful(self):
        dummy = usernameUtilities.MODULE_PATH
        usernameUtilities.MODULE_PATH = ""
        usernameUtilities.confUser(TEST_USER)
        username = usernameUtilities.readUsername()
        usernameUtilities.MODULE_PATH = dummy
        os.remove(".user.config")
        assert username == TEST_USER

    def testReadFail(self):
        dummy = usernameUtilities.MODULE_PATH
        usernameUtilities.MODULE_PATH = ""
        with pytest.raises(FileNotFoundError):
            usernameUtilities.readUsername()
        usernameUtilities.MODULE_PATH = dummy

class TestLog2NorDB(object):
    
    def testLogSuccesful(self):
        conn = usernameUtilities.log2nordb()
        assert type(conn), psycopg2.Connect
   
    def testLogFailWithWrongUser(self):
        usr = usernameUtilities.readUsername()
        usernameUtilities.confUser("wrong")
        with pytest.raises(psycopg2.OperationalError):
            usernameUtilities.log2nordb()
        usernameUtilities.confUser(usr)
    
