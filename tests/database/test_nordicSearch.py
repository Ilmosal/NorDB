import pytest
from nordb.database.nordicSearch import *
from nordb.database import nordic2sql
from datetime import date
from nordb.core import usernameUtilities
from nordb.core import nordic

@pytest.mark.usefixtures("setupdbWithEvents")
class TestNordicSearchWithCriteria(object):
    def testFindAllEventsWithoutCriteria(self, setupdbWithEvents):
        search = NordicSearch()
        foundEvents = search.searchEvents()

        assert len(foundEvents) == 3

    def testFindEventsWithDate(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("origin_time", date(2013, 1, 3))
        foundEvents = search.searchEvents()
        for e in foundEvents:
            print(e)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithMagnitude(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("magnitude_1", 1.6)
        foundEvents = search.searchEvents()

        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithLatitude(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("epicenter_latitude", 63.635)
        foundEvents = search.searchEvents()

        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithLatitudeRange(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchBetween("epicenter_latitude", 63.632, 63.637)
        foundEvents = search.searchEvents()

        assert len(foundEvents) == 1

    def testFindEventsWithLatitudeUnder(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchUnder("epicenter_latitude", 63.637)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 1

    def testFindEventsWithLatitudeOver(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchOver("epicenter_latitude", 63.632)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 3

    def testFindEventsWithLongitude(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("epicenter_longitude", 22.913)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithDepth(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("depth", 0.1)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithEventType(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("solution_type", "F")
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 3

    def testFindEventsWithDistanceIndicator(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("distance_indicator", "L")
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 3

    def testFindEventsWithEventID(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("event_id", 1)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithEventDescID(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("event_desc_id", "P")
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testSearchWithWrongTypeCriteria(self, setupdbWithEvents):
        search = NordicSearch()
        with pytest.raises(Exception):
            search.addSearchExactly("epicenter_latitude", "P")
            foundEvents = search.searchEvents()

    def testNoEventsWithNonexistingDate(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("origin_time", date(2012,11,3))
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingMagnitude(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("magnitude_1", 5.6)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingLatitude(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("epicenter_latitude", 23.635)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingLongitude(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("epicenter_longitude", 12.913)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingDepth(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("depth", 12.91)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingEventType(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("solution_type", "S")
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingDistanceIndicator(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("distance_indicator", "R")
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingEventID(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("event_id", 123)
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingEventDescID(self, setupdbWithEvents):
        search = NordicSearch()
        search.addSearchExactly("event_desc_id", "Q")
        foundEvents = search.searchEvents()
        assert len(foundEvents) == 0

@pytest.mark.usefixtures("setupdbWithEvents", "nordicEvents")
class TestSearchSameEvents(object):
    def testSearchSameEvent(self, setupdbWithEvents, nordicEvents):
        e = nordic.readNordic(nordicEvents[0], False)
        assert len(searchSameEvents(e)) == 1
       
@pytest.mark.usefixtures("setupdbWithEvents", "nordicEvents")
class TestSearchSimilarEvents(object):
    def testSearchSimilarEvent(self, setupdbWithEvents, nordicEvents):
        e = nordic.readNordic(nordicEvents[0], False)
        events = searchSimilarEvents(e)
        assert len(events) == 1
 
