import pytest
from nordb.database import undoRead
from nordb.database import nordic2sql
from nordb.core import nordic
from nordb.core import usernameUtilities

@pytest.mark.usefixture("setupdb", "nordicEvents")
class TestUndoRead(object):
    def testUndoWithoutEvents(self, setupdb):
        with pytest.raises(Exception):
            undoRead.undoMostRecent()
    
    def testUndoWithEvents(self, setupdb, nordicEvents):
        events = []
        for e in nordicEvents:
            events.append(nordic.createNordicEvent(e, False))

        creation_id = nordic2sql.createCreationInfo()

        for e in events:
            nordic2sql.event2Database(e, "S", "dummy_name", creation_id, -1)

        undoRead.undoMostRecent() 
        
        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
    
        cur.execute("SELECT COUNT(*) FROM nordic_event;") 
        ans = cur.fetchone()[0]

        assert ans == 0
    
    def testRemoveWithCreationId(self, setupdb, nordicEvents):
        events = []
        for e in nordicEvents:
            events.append(nordic.createNordicEvent(e, False))

        for e in events:
            creation_id = nordic2sql.createCreationInfo()
            nordic2sql.event2Database(e, "S", "dummy_name", creation_id, -1)

        undoRead.removeEventsWithCreationId(2)
        
        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()
    
        cur.execute("SELECT COUNT(*) FROM nordic_event;") 
        ans = cur.fetchone()[0]

        assert ans == len(nordicEvents)-1
 
