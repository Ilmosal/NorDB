import pytest
from nordb.database import solutionTypeHandler
from nordb.database import nordicSearch
from nordb.core import usernameUtilities

@pytest.mark.usefixture("setupdb")
class TestAddSolutionType(object):
    def testAddNewSolutionType(self, setupdb):
        solutionTypeHandler.addSolutionType("T", "Test", True)
    
    def testAddTooLongEventId(self, setupdb):
        with pytest.raises(Exception):
            solutionTypeHandler.addSolutionType("TESTING", "Test value", True)

    def testAddTooLongEventDesc(self, setupdb):
        with pytest.raises(Exception):
            solutionTypeHandler.addSolutionType("T", "Test valueTest valueTest valueTest valueTest valueTest valueTest valueTest valueTest valueTest valueTest value", True)

    def testAddAlreadyExistingEventId(self, setupdb):
        solutionTypeHandler.addSolutionType("T", "Test", True)

        with pytest.raises(Exception):
            solutionTypeHandler.addSolutionType("T", "Test", True)

@pytest.mark.usefixture("setupdb")
class TestGetSolutionTypes(object):
    def testGetSolutionTypes(self, setupdb):
        assert len(solutionTypeHandler.getSolutionTypes()) == 3
        solutionTypeHandler.addSolutionType("T", "Test", True)
        assert len(solutionTypeHandler.getSolutionTypes()) == 4

@pytest.mark.usefixture("setupdbWithEvents")
class TestRemoveSolutionTypes(object):
    def testGetSolutionTypes(self, setupdbWithEvents):
        solutionTypeHandler.removeSolutionType("F", "O")
        assert len(solutionTypeHandler.getSolutionTypes()) == 2
        search = nordicSearch.NordicSearch()
        search.addSearchExactly("solution_type", "O")
        assert len(search.searchEvents()) == 3
        search.clear()
        search = nordicSearch.NordicSearch()
        search.addSearchExactly("solution_type", "F")
        assert len(search.searchEvents()) == 0


