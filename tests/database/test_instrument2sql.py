import pytest
from nordb.database import response2sql
from nordb.database import instrument2sql
from nordb.core import usernameUtilities
from nordb.nordic import response
from nordb.nordic import instrument

@pytest.mark.userfixtures("setupdb", "instrumentFiles", "responseFiles")
class TestInsertInstrument2Database(object):
    def testInsertIsSuccesfull(self, setupdb, instrumentFiles, responseFiles):
        instruments = []

        for resp in responseFiles:
            response2sql.insertResponse2Database(response.readResponseArrayToResponse(resp[0], resp[1]))

        for ins in instrumentFiles:
            instruments.append(instrument.readInstrumentStringToInstrument(ins))

        for ins in instruments:
            instrument2sql.insertInstrument2Database(ins)

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM instrument")
        ans = cur.fetchone()

        conn.close()
