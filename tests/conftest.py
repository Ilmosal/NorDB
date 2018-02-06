import os
import pytest
from nordb.database import norDBManagement
from nordb.core import usernameUtilities
from nordb import settings

@pytest.fixture()
def setupdb():
    print("Setup!")
    username = settings.username
    norDBManagement.createDatabase(True)
    yield None
    print("teardown")
    usernameUtilities.confUser(username)
    norDBManagement.destroyDatabase(True)

