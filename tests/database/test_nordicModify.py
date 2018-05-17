import pytest
from nordb.core.nordic import *
from nordb.database.nordicModify import *
from nordb.database import nordic2sql
from nordb.database import creationInfo
from nordb.database import sql2nordic

@pytest.mark.usefixtures("setupdb", "nordicEvents")
class TestNordicChangeType(object):
    def testNordicChangeTypeWorks(self, setupdb, nordicEvents):
        event = readNordic(nordicEvents[0], False)
        creation_id = creationInfo.createCreationInfo('public')
        nordic2sql.event2Database(event, "A", "dummy_name", creation_id, -1)
    
        changeSolutionType(1, "F")

        assert "F" == sql2nordic.getNordic(1).solution_type

    def testNordicChangeTypeWithNoEvent(self, setupdb):
        with pytest.raises(Exception):
            changeSolutionType(1, "O")

    def testNordicChangeTypeWithSameType(self, setupdb, nordicEvents):
        event = readNordic(nordicEvents[0], False)
        creation_id = creationInfo.createCreationInfo('public')
        nordic2sql.event2Database(event, "F", "dummy_name", creation_id, -1)

        with pytest.raises(Exception):    
            changeSolutionType(1, "F") 

@pytest.mark.usefixtures("setupdb", "nordicEvents")
class TestNordicChangeRoot(object):
    def testNordicChangeRootWorks(self, setupdb, nordicEvents):
        event = readNordic(nordicEvents[0], False)
        creation_id = creationInfo.createCreationInfo('public')
        nordic2sql.event2Database(event, "F", "dummy_name", creation_id, -1)
        nordic2sql.event2Database(event, "F", "dummy_name", creation_id, -1)

        changeEventRoot(2, 1)

        assert sql2nordic.getNordic(1).root_id == sql2nordic.getNordic(2).root_id

    def testNordicChangeRootWorksWithNonExistingRoot(self, setupdb, nordicEvents):
        event = readNordic(nordicEvents[0], False)
        creation_id = creationInfo.createCreationInfo('public')
        nordic2sql.event2Database(event, "F", "dummy_name", creation_id, -1)

        changeEventRoot(1, -9)

        assert sql2nordic.getNordic(1).root_id == 2

    def testNordicChangeRootFailsWithNonExisting(self, setupdb, nordicEvents):
        event = readNordic(nordicEvents[0], False)
        creation_id = creationInfo.createCreationInfo('public')
        nordic2sql.event2Database(event, "F", "dummy_name", creation_id, -1)

        with pytest.raises(Exception):
            changeEventRoot(1, 12)

    def testNordicChangeRootFailsWithoutEvent(self, setupdb, nordicEvents):
        event = readNordic(nordicEvents[0], False)
        creation_id = creationInfo.createCreationInfo('public')

        with pytest.raises(Exception):
            changeEventRoot(1, 12)

