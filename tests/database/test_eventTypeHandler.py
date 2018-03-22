import pytest
from nordb.database import eventTypeHandler
from nordb.database import nordicSearch
from nordb.core import usernameUtilities

@pytest.mark.usefixture("setupdb")
class TestAddEventType(object):
    def testAddNewEventType(self, setupdb):
        eventTypeHandler.addEventType("T", "Test", True)
    
    def testAddTooLongEventId(self, setupdb):
        with pytest.raises(Exception):
            eventTypeHandler.addEventType("TESTING", "Test value", True)

    def testAddTooLongEventDesc(self, setupdb):
        with pytest.raises(Exception):
            eventTypeHandler.addEventType("T", "Test valueTest valueTest valueTest valueTest valueTest valueTest valueTest valueTest valueTest valueTest value", True)

    def testAddAlreadyExistingEventId(self, setupdb):
        eventTypeHandler.addEventType("T", "Test", True)

        with pytest.raises(Exception):
            eventTypeHandler.addEventType("T", "Test", True)

@pytest.mark.usefixture("setupdb")
class TestGetEventTypes(object):
    def testGetEventTypes(self, setupdb):
        assert len(eventTypeHandler.getEventTypes()) == 3
        eventTypeHandler.addEventType("T", "Test", True)
        assert len(eventTypeHandler.getEventTypes()) == 4

@pytest.mark.usefixture("setupdbWithEvents")
class TestRemoveEventTypes(object):
    def testGetEventTypes(self, setupdbWithEvents):
        eventTypeHandler.removeEventType("F", "O")
        assert len(eventTypeHandler.getEventTypes()) == 2
        search = nordicSearch.NordicSearch()
        search.addSearchExactly("event_type", "O")
        assert len(search.searchEvents()) == 3
        search.clear()
        search = nordicSearch.NordicSearch()
        search.addSearchExactly("event_type", "F")
        assert len(search.searchEvents()) == 0


