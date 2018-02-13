import pytest
from nordb.core import usernameUtilities
from nordb.database import norDBManagement

@pytest.mark.usefixture("setupdb")
class TestNorDNManagment(object):
    def testCreateDatabaseDoesntWorkIfThereIsDatabase(self, setupdb):
        with pytest.raises(Exception):
            norDBManagement.createDatabase()

    def testDestroyDatabaseDoesntWorkTwice(self, setupdb):
        norDBManagement.destroyDatabase()
        with pytest.raises(Exception):
            norDBManagement.destroyDatabase()
            
