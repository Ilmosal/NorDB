import pytest
from nordb.database import nordicSearch
from nordb.database import nordic2sql
from nordb.core import usernameUtilities
from nordb.core import nordic

@pytest.mark.usefixtures("setupdbWithEvents")
class TestNordicSearchWithCriteria(object):
    def testFindAllEventsWithoutCriteria(self, setupdbWithEvents):
        foundEvents = nordicSearch.searchWithCriteria({})

        assert len(foundEvents) == 3

    def testFindEventsWithDate(self, setupdbWithEvents):
        criteria = {"date":"03.01.2013"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithHour(self, setupdbWithEvents):
        criteria = {"hour":"6"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithMinute(self, setupdbWithEvents):
        criteria = {"minute":"14"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithSecond(self, setupdbWithEvents):
        criteria = {"second":"4.0"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithMagnitude(self, setupdbWithEvents):
        criteria = {"magnitude":"1.6"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithLatitude(self, setupdbWithEvents):
        criteria = {"latitude":"63.635"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithLatitudeRange(self, setupdbWithEvents):
        criteria = {"latitude":"63.632-63.637"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1

    def testFindEventsWithLatitudeLower(self, setupdbWithEvents):
        criteria = {"latitude":"63.637-"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1

    def testFindEventsWithLatitudeUpper(self, setupdbWithEvents):
        criteria = {"latitude":"63.632+"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 3

    def testFindEventsWithLongitude(self, setupdbWithEvents):
        criteria = {"longitude":"22.913"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithDepth(self, setupdbWithEvents):
        criteria = {"depth":"0.1"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithEventType(self, setupdbWithEvents):
        criteria = {"event_type":"F"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 3

    def testFindEventsWithEventTypeRange(self, setupdbWithEvents):
        criteria = {"event_type":"F-S"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 3

    def testFindEventsWithEventTypeLower(self, setupdbWithEvents):
        criteria = {"event_type":"F-"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 3

    def testFindEventsWithEventTypeUpper(self, setupdbWithEvents):
        criteria = {"event_type":"P+"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 3

    def testFindEventsWithDistanceIndicator(self, setupdbWithEvents):
        criteria = {"distance_indicator":"L"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 3

    def testFindEventsWithEventID(self, setupdbWithEvents):
        criteria = {"event_id":"1"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testFindEventsWithEventDescID(self, setupdbWithEvents):
        criteria = {"event_desc_id":"P"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 1
        assert foundEvents[0].event_id == 1

    def testSearchWithWrongTypeCrieria(self, setupdbWithEvents):
        criteria = {"latitude":"12"}
        with pytest.raises(Exception):
            nordicSearch.searchWithCriteria(criteria)

    def testNoEventsWithNonexistingDate(self, setupdbWithEvents):
        criteria = {"date":"03.11.2012"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingHour(self, setupdbWithEvents):
        criteria = {"hour":"19"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingMinute(self, setupdbWithEvents):
        criteria = {"minute":"44"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingSecond(self, setupdbWithEvents):
        criteria = {"second":"7.1"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingMagnitude(self, setupdbWithEvents):
        criteria = {"magnitude":"5.6"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingLatitude(self, setupdbWithEvents):
        criteria = {"latitude":"23.635"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingLongitude(self, setupdbWithEvents):
        criteria = {"longitude":"12.913"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingDepth(self, setupdbWithEvents):
        criteria = {"depth":"13.1"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingEventType(self, setupdbWithEvents):
        criteria = {"event_type":"S"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingDistanceIndicator(self, setupdbWithEvents):
        criteria = {"distance_indicator":"R"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingEventID(self, setupdbWithEvents):
        criteria = {"event_id":"123"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testNoEventsWithNonexistingEventDescID(self, setupdbWithEvents):
        criteria = {"event_desc_id":"Q"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 0

    def testSearchFailsWithInvalidDate(self, setupdbWithEvents):
        criteria = {"date":"03ad1.20as"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithCriteria(criteria)

    def testSearchFailsWithInvalidHour(self, setupdbWithEvents):
        criteria = {"hour":"4s"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithCriteria(criteria)

    def testSearchFailsWithInvalidMinute(self, setupdbWithEvents):
        criteria = {"minute":"1f00"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithCriteria(criteria)

    def testSearchFailsWithSecond(self, setupdbWithEvents):
        criteria = {"second":"10sa00.0"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithCriteria(criteria)

    def testSearchFailsWithFaultyMagnitude(self, setupdbWithEvents):
        criteria = {"magnitude":"-a213.0"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithFaultyCriteria(criteria)

    def testSearchFailsWithFaultyLatitude(self, setupdbWithEvents):
        criteria = {"latitude":"100ad0000"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithFaultyCriteria(criteria)

    def testSearchFailsWithFaultyLongitude(self, setupdbWithEvents):
        criteria = {"longitude":"1000da000"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithFaultyCriteria(criteria)

    def testSearchFailsWithFaultyDepth(self, setupdbWithEvents):
        criteria = {"depth":"-130d0.1"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithFaultyCriteria(criteria)

    def testSearchFailsWithFaultyEventType(self, setupdbWithEvents):
        criteria = {"event_type":"a21G"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithFaultyCriteria(criteria)

    def testSearchFailsWithFaultyDistanceIndicator(self, setupdbWithEvents):
        criteria = {"distance_indicator":"Cad2"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithFaultyCriteria(criteria)

    def testSearchFailsWithFaultyEventID(self, setupdbWithEvents):
        criteria = {"event_id":"jooh"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithFaultyCriteria(criteria)

    def testSearchFailsWithFaultyEventDescID(self, setupdbWithEvents):
        criteria = {"event_desc_id":"123sad"}
        with pytest.raises(Exception):
            foundEvents = nordicSearch.searchWithCriteria(criteria)

    def testSearchWithRange(self, setupdbWithEvents):
        criteria = {"date":"01.01.2017-12.12.2017"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 2

    def testSearchWithPositiveRange(self, setupdbWithEvents):
        criteria = {"date":"01.01.2017+"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 2
    
    def testSearchWithNegativeRange(self, setupdbWithEvents):
        criteria = {"date":"11.02.2017-"}
        foundEvents = nordicSearch.searchWithCriteria(criteria)
        assert len(foundEvents) == 2
    
    def testSearchUnderInvalidValue(self, setupdbWithEvents):
        criteria = {"depth":"asd-"}
        with pytest.raises(Exception):
            nordicSearch.searchWithCriteria(criteria)

    def testSearchOverInvalidValue(self, setupdbWithEvents):
        criteria = {"depth":"asd+"}
        with pytest.raises(Exception):
            nordicSearch.searchWithCriteria(criteria)

    def testSearchBetweenInvalidValue(self, setupdbWithEvents):
        criteria = {"depth":"asd-jeeh"}
        with pytest.raises(Exception):
            nordicSearch.searchWithCriteria(criteria)

@pytest.mark.usefixtures("setupdbWithEvents", "nordicEvents")
class TestSearchSameEvents(object):
    def testSearchSameEvent(self, setupdbWithEvents, nordicEvents):
        e = nordic.createNordicEvent(nordicEvents[0], False)
        assert len(nordicSearch.searchSameEvents(e)) == 1
       
@pytest.mark.usefixtures("setupdbWithEvents", "nordicEvents")
class TestSearchSimilarEvents(object):
    def testSearchSimilarEvent(self, setupdbWithEvents, nordicEvents):
        e = nordic.createNordicEvent(nordicEvents[0], False)
        events = nordicSearch.searchSimilarEvents(e)
        assert len(events) == 1
 
