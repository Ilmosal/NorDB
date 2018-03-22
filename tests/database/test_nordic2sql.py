import pytest
from nordb.database import nordic2sql
from nordb.database import sql2nordic
from nordb.core import nordic
from nordb.core import usernameUtilities

@pytest.mark.usefixtures("setupdb", "nordicEvents")
class TestNordic2SQL(object):
    def testSuccesfulNordic(self, setupdb, nordicEvents):
        events = []
        for e in nordicEvents:
            events.append(nordic.createNordicEvent(e, False))

        creation_id = nordic2sql.createCreationInfo()

        for e in events:
            nordic2sql.event2Database(e, "F", "dummy_name", creation_id, -1)

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
        cur.execute("SELECT id FROM nordic_event")
        e_ids = cur.fetchall()
        conn.close()

        i = 0
        for e_id in e_ids:
            #assert str(sql2nordic.getNordicFromDB(e_id[0])) == str(events[i])
            i += 1
        
            
    def testPutSameEventTwice(self, setupdb, nordicEvents):
        event = nordic.createNordicEvent(nordicEvents[0], False) 
        creation_id = nordic2sql.createCreationInfo()

        nordic2sql.event2Database(event, "F", "dummy", creation_id, -1)
        nordic2sql.event2Database(event, "F", "dummy", creation_id, event.event_id)

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
        cur.execute("SELECT root_id, event_type FROM nordic_event")
        ans = cur.fetchall()
        conn.close()

        assert ans[0][0] == ans[1][0]
        assert ans[0][1] != ans[1][1]
        
    def testAttachToNonExistingEvent(self, setupdb, nordicEvents):
        event = nordic.createNordicEvent(nordicEvents[0], False) 
        creation_id = nordic2sql.createCreationInfo()

        with pytest.raises(Exception): 
            nordic2sql.event2Database(event, "F", "dummy", creation_id, 3)
   
@pytest.mark.usefixtures("setupdb")
class TestCreationInfo(object):
    def testCreationInfo(self, setupdb):
        c_id = nordic2sql.createCreationInfo()
        nordic2sql.deleteCreationInfoIfUnnecessary(c_id)
  
        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
        cur.execute("SELECT * FROM creation_info")
        ans = cur.fetchall()
        conn.close() 
        assert not ans

@pytest.mark.usefixtures("setupdb")
class TestExecuteCommand(object):
    def testExecuteCommandNoReturn(self, setupdb):
        conn = usernameUtilities.log2nordb()
        assert nordic2sql.executeCommand(conn.cursor(), "SELECT * FROM nordic_event", None, False) is None

    def testExecuteCommandReturn(self, setupdb):
        conn = usernameUtilities.log2nordb()
        assert not nordic2sql.executeCommand(conn.cursor(), "SELECT * FROM nordic_event", None, True)

