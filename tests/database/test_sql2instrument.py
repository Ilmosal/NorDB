import pytest
from nordb.database import instrument2sql
from nordb.core import usernameUtilities
from nordb.nordic import instrument
from nordb.database import sql2instrument

@pytest.mark.userfixtures("setupdb", "instrumentFiles")
class TestSQL2Instrument(object):
    def testGetAllInstruments(self, setupdb, instrumentFiles):
        instruments = []
        for ins in instrumentFiles:
            instruments.append(instrument.readInstrumentStringToInstrument(ins))

        for ins in instruments:
            instrument2sql.insertInstrument2Database(ins)

        instruments = sql2instrument.getAllInstruments()

        assert len(instrumentFiles) == len(instruments)

    def testGetOneInstruments(self, setupdb, instrumentFiles):
        instruments = []
        for ins in instrumentFiles:
            instruments.append(instrument.readInstrumentStringToInstrument(ins))

        for ins in instruments:
            instrument2sql.insertInstrument2Database(ins)

        ins = sql2instrument.getInstrument(1)

        assert str(ins).strip() == instrumentFiles[0].strip()

