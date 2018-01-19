import os
import pytest
import psycopg2
from nordb.core import usernameUtilities

class TestConfUser(object):
    @pytest.mark.skip(reason="no way of currently testing this")
    def testConfUserWritesUsername(dummyDB):
        usernameUtilities.confUser(TEST_USER)
        f = open(usernameUtilities.MODULE_PATH + ".user.config")
        username = f.readline().strip()
        assert username == TEST_USER

class TestLog2NorDB(object):
    def testLogSuccesful(self):
        conn = usernameUtilities.log2nordb()
        assert type(conn), psycopg2.Connect

    @pytest.mark.skip(reason="no way of currently testing this")
    def testLogFailWithWrongUser(dummyDB):
        usernameUtilities.confUser("wrong")
        with pytest.raises(psycopg2.OperationalError):
            usernameUtilities.log2nordb()
