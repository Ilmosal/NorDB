import pytest
from nordb.database import nordic2sql
from nordb.database import creationInfo
from nordb.database import sql2nordic
from nordb.core import nordic
from nordb.core import usernameUtilities

@pytest.mark.usefixtures("setupdb", "nordicEvents")
class TestNordic2SQL(object):
    def testSuccesfulNordic(self, setupdb, nordicEvents):
        events = []
        for e in nordicEvents:
            events.append(nordic.readNordic(e, False))

        creation_id = creationInfo.createCreationInfo('public')

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
        event = nordic.readNordic(nordicEvents[0], False) 
        creation_id = creationInfo.createCreationInfo('public')

        nordic2sql.event2Database(event, "F", "dummy", creation_id, -1)
        nordic2sql.event2Database(event, "F", "dummy", creation_id, event.event_id)

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
        cur.execute("SELECT root_id, solution_type FROM nordic_event")
        ans = cur.fetchall()
        conn.close()

        assert ans[0][0] == ans[1][0]
        assert ans[0][1] != ans[1][1]
        
    def testAttachToNonExistingEvent(self, setupdb, nordicEvents):
        event = nordic.readNordic(nordicEvents[0], False) 
        creation_id = creationInfo.createCreationInfo('public')

        with pytest.raises(Exception): 
            nordic2sql.event2Database(event, "F", "dummy", creation_id, 3)
   

