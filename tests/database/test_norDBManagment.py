import pytest
from nordb.core import usernameUtilities
from nordb.database import norDBManagement
from nordb import settings

@pytest.mark.usefixtures("setupdb")
class TestNorDBManagment(object):
    def testCreateDatabaseDoesntWorkIfThereIsDatabase(self, setupdb):
        with pytest.raises(Exception):
            norDBManagement.createDatabase()

    def testDestroyDatabaseDoesntWorkTwice(self, setupdb):
        norDBManagement.destroyDatabase()
        with pytest.raises(Exception):
            norDBManagement.destroyDatabase()
            
