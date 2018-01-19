import pytest

@pytest.fixture
def dummyDB():
    import nordb.settings
    from nordb.database import norDBManagement
    nordb.settings.username = "dummyname"
    nordb.settings.dbname = "dummyDB"
    norDBManagement.createDatabase()
    yield dummyDB
    norDBManagement.destroyDatabase()

    
    
    
