import os
import pytest
import psycopg2
from nordb.core import usernameUtilities
from nordb.database import norDBManagement
from nordb import settings

@pytest.mark.usefixtures("setupdb")
class TestConfUser(object):
    def testConfUserWritesUsername(setupdb):
        TEST_USER = "test"
        usernameUtilities.confUser(TEST_USER)
        f = open(usernameUtilities.MODULE_PATH + "/.user.config")
        s_username = f.readline().strip()
        f.close()
        assert s_username == TEST_USER

@pytest.mark.usefixtures("setupdb")
class TestLog2NorDB(object):
    def testLogSuccesful(setupdb):
        conn = usernameUtilities.log2nordb()
        assert type(conn), psycopg2.Connect

    def testLogFailWithWrongUser(setupdb):
        usernameUtilities.confUser("wrong")
        with pytest.raises(psycopg2.OperationalError):
            usernameUtilities.log2nordb()
