import pytest
from nordb.core.nordic import *
from nordb.database.nordicModify import *
from nordb.database import nordic2sql
from nordb.database import sql2nordic

@pytest.mark.usefixtures("setupdb", "nordicEvents")
class TestNordicChangeType(object):
    def testNordicChangeTypeWorks(self, setupdb, nordicEvents):
        event = createNordicEvent(nordicEvents[0], False)
        creation_id = nordic2sql.createCreationInfo()
        nordic2sql.event2Database(event, "S", "dummy_name", False, True, creation_id, -1)
    
        changeEventType(1, "F")

        assert "F" == sql2nordic.getNordicFromDB(1).event_type

    def testNordicChangeTypeWithNoEvent(self, setupdb):
        with pytest.raises(Exception):
            changeEventType(1, "O")

    def testNordicChangeTypeWithSameType(self, setupdb, nordicEvents):
        event = createNordicEvent(nordicEvents[0], False)
        creation_id = nordic2sql.createCreationInfo()
        nordic2sql.event2Database(event, "F", "dummy_name", False, True, creation_id, -1)

        with pytest.raises(Exception):    
            changeEventType(1, "F") 

@pytest.mark.usefixtures("setupdb", "nordicEvents")
class TestNordicChangeRoot(object):
    def testNordicChangeRootWorks(self, setupdb, nordicEvents):
        event = createNordicEvent(nordicEvents[0], False)
        creation_id = nordic2sql.createCreationInfo()
        nordic2sql.event2Database(event, "S", "dummy_name", False, True, creation_id, -1)
        nordic2sql.event2Database(event, "S", "dummy_name", False, True, creation_id, -1)

        changeEventRoot(2, 1)

        assert sql2nordic.getNordicFromDB(1).root_id == sql2nordic.getNordicFromDB(2).root_id


    def testNordicChangeRootWorksWithNonExistingRoot(self, setupdb, nordicEvents):
        event = createNordicEvent(nordicEvents[0], False)
        creation_id = nordic2sql.createCreationInfo()
        nordic2sql.event2Database(event, "S", "dummy_name", False, True, creation_id, -1)

        changeEventRoot(1, -999)

        assert sql2nordic.getNordicFromDB(1).root_id == 2

    def testNordicChangeRootFailsWithNonExisting(self, setupdb, nordicEvents):
        event = createNordicEvent(nordicEvents[0], False)
        creation_id = nordic2sql.createCreationInfo()
        nordic2sql.event2Database(event, "S", "dummy_name", False, True, creation_id, -1)

        with pytest.raises(Exception):
            changeEventRoot(1, 12)

    def testNordicChangeRootFailsWithoutEvent(self, setupdb, nordicEvents):
        event = createNordicEvent(nordicEvents[0], False)
        creation_id = nordic2sql.createCreationInfo()

        with pytest.raises(Exception):
            changeEventRoot(1, 12)



