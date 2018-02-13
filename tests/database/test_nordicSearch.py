import pytest
from nordb.database import nordicSearch
from nordb.database import nordic2sql
from nordb.core import usernameUtilities
from nordb.core import nordic

@pytest.mark.usefixtures("nordicEvents","setupdb")
class TestNordicSearch(object):
    def testFindAllEventsWithoutCriteria(self, nordicEvents, setupdb):
        events = []
        for e in nordicEvents:
           events.append(nordic.createNordicEvent(e, False)) 

        creation_id = nordic2sql.createCreationInfo()
        for e in events:
            nordic2sql.event2Database(e, "F", "dummy_name", creation_id, -1)

        foundEvents = nordicSearch.searchWithCriteria({})

        assert len(foundEvents) == len(nordicEvents)


