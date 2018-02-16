import pytest
from nordb.database import station2sql
from nordb.database import sitechan2sql
from nordb.database import sensor2sql
from nordb.database import instrument2sql
from nordb.core import usernameUtilities
from nordb.nordic import station
from nordb.nordic import sitechan
from nordb.nordic import sensor
from nordb.nordic import instrument

@pytest.mark.userfixtures("setupdb", "instrumentFiles")
class TestInsertInstrument2Database(object):
    def testInsertIsSuccesfull(self, setupdb, instrumentFiles):
        instruments = []
        for ins in instrumentFiles:
            instruments.append(instrument.readInstrumentStringToInstrument(ins))

        for ins in instruments:
            instrument2sql.insertInstrument2Database(ins)

        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM instrument") 
        ans = cur.fetchone()
 
        conn.close()
   
