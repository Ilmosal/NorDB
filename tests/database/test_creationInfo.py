import pytest
from nordb.database import nordic2sql
from nordb.database import creationInfo
from nordb.database import sql2nordic
from nordb.core import nordic
from nordb.core import usernameUtilities

@pytest.mark.usefixtures("setupdb")
class TestCreationInfo(object):
    def testCreationInfo(self, setupdb):
        c_id = creationInfo.createCreationInfo('secure')
        creationInfo.deleteCreationInfoIfUnnecessary(c_id)
  
        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
        cur.execute("SELECT * FROM creation_info WHERE id = %s", (c_id, ))
        ans = cur.fetchall()
        conn.close() 
        assert not ans

@pytest.mark.usefixtures("setupdb")
class TestExecuteCommand(object):
    def testExecuteCommandNoReturn(self, setupdb):
        conn = usernameUtilities.log2nordb()
        assert nordic2sql.executeCommand(conn.cursor(), "SELECT * FROM nordic_event", None, False) is None
        conn.close()

    def testExecuteCommandReturn(self, setupdb):
        conn = usernameUtilities.log2nordb()
        assert not nordic2sql.executeCommand(conn.cursor(), "SELECT * FROM nordic_event", None, True)
        conn.close()

