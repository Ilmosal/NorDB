from datetime import date
import pytest
from nordb.core.nordic import *

DUMMY_NORDIC_FILE = ([
    " 2013 0103 0614 00.0 LE 63.635  22.913  0.0F HEL 15 0.3 1.6LHEL 1.4LUPP        1\n",
    " GAP= 80         0.1     0.391   0.477                  0.0                    5\n",
    " CSS:2013003061203.WFDISC  (DET3C)                                             6\n",
    " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE CHECKED (NIH)              3\n",
    " MINING AREA & TIME WINDOW: PEDERSORE  3KM                                     3\n",
    " FINLAND                                                                       3\n",
    " 2013 0103 0613 04.0 LE 63.650  22.942  0.0FFHEL 11 0.4 1.6LHEL                1\n",
    " GAP= 92         0.3     0.291   0.427                  0.1                    5\n",
    " 2013 0103 0613 05.2 LP 63.680  22.728  0.1F UPP  7 0.3 1.4LUPP                1\n",
    "                            2 MM                                        BER    2\n",
    " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n",
    " VAF  BZ EP       0613 15.30                    7.0              0.210   67 191 \n",
    " VAF  BZ ES       0613 23.10                                     0.4 4          \n",
    " UMAU BZ EP       0613 22.64                                    -0.010  114 285 \n",
    " BURU BZ EPB      0613 25.38                  141.0             -0.1 9  130 325 \n",
    " BURU BZ ES       0613 39.82                                    -0.3 4          \n",
    " ODEU BZ EP       0613 26.31                                    -0.2 9  138 310 \n",
    " SVAU BZ EP       0613 34.71                                     0.3 8  189 302 \n",
    " KEF  BZ EPN      0613 35.36                                     0.0 4  192 148 \n",
    " KEF  BZ ESN      0613 58.10                                    -0.0 8          \n",
    " SUF  BZ EPG      0613 35.20                                    -0.1 8  193 121 \n",
    " SUF  BZ  MSG     0613 55.58         3.6 0.20                                   \n",
    " SUF  BZ ESN      0613 58.00                                    -0.3 9          \n",
    " OUL  BZ EPG      0613 39.06                  224.0             -0.2 4  217  40 \n",
    " OUL  BZ ESG      0614 04.50                                     0.3 5          \n",
    " SJUU BZ EP       0613 38.75                                     0.1 8  218 344 \n",
    " LILU BZ EP       0613 41.40                                     0.5 8  236 323 \n",
    " KAF  BZ EPB      0613 42.50                  314.0              0.2 4  243 133 \n",
    " KAF  BZ  MSG     0614 08.53         2.7 0.20                                   \n",
    " KAF  BZ ESG      0614 11.10                                    -0.2 0          \n",
    " KALU BZ EPB      0613 43.50                                     0.2 6  249   5 \n",
    " KALU BZ ESB      0614 12.34                                     0.4 4          \n",
    " HEMU BZ EPB      0613 45.78                   61.0             -0.4 8  268 249 \n",
    " HEMU BZ ESG      0614 18.14                                    -0.3 4          \n",
    " TOF  BZ EPB      0613 48.10                                     0.0 3  281  13 \n",
    " TOF  BZ  MSG     0614 18.11         2.2 0.20                                   \n",
    " TOF  BZ ESB      0614 20.10                                    -0.1 0          \n",
    " ERTU BZ ES       0614 27.84                                     0.4 0  328 354 \n",
                                ])

DUMMY_NORDIC_FAULTY_FILE = ([
    " 2013 0103 0613 60.0 LE 63.635  22.913  0.0F HEL 15 0.3 1.6LHEL 1.4LUPP        1\n",
    " GAP= 80         0.1     0.391   0.477                  0.0                    5\n",
    " CSS:2013003061203.WFDISC  (DET3C)                                             6\n",
    " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE CHECKED (NIH)              3\n",
    " MINING AREA & TIME WINDOW: PEDERSORE  3KM                                     3\n",
    " FINLAND                                                                       3\n",
    " 2013 0103 0613 04.0 LE 63.650  22.942  0.0FFHEL 11 0.4 1.6LHEL                1\n",
    " GAP= 92         0.3     0.291   0.427                  0.1                    5\n",
    " 2013 0103 0613 05.2 LP 63.680  22.728  0.1F UPP  7 0.3 1.4LUPP                1\n",
    "                            2 MM                                        BER    2\n",
    " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n",
    " VAF  BZ EP       0613 15.30                    7.0              0.210   67 191 \n",
    " VAF  BZ ES       0613 23.10                                     0.4 4          \n",
    " UMAU BZ EP       0613 22.64                                    -0.010  114 285 \n",
    " BURU BZ EPB      0613 25.38                  141.0             -0.1 9  130 325 \n",
    " BURU BZ ES       0613 39.82                                    -0.3 4          \n",
    " ODEU BZ EP       0613 26.31                                    -0.2 9  138 310 \n",
    " SVAU BZ EP       0613 34.71                                     0.3 8  189 302 \n",
    " KEF  BZ EPN      0613 35.36                                     0.0 4  192 148 \n",
    " KEF  BZ ESN      0613 58.10                                    -0.0 8          \n",
    " SUF  BZ EPG      0613 35.20                                    -0.1 8  193 121 \n",
    " SUF  BZ  MSG     0613 55.58         3.6 0.20                                   \n",
    " SUF  BZ ESN      0613 58.00                                    -0.3 9          \n",
    " OUL  BZ EPG      0613 39.06                  224.0             -0.2 4  217  40 \n",
    " OUL  BZ ESG      0614 04.50                                     0.3 5          \n",
    " SJUU BZ EP       0613 38.75                                     0.1 8  218 344 \n",
    " LILU BZ EP       0613 41.40                                     0.5 8  236 323 \n",
    " KAF  BZ EPB      0613 42.50                  314.0              0.2 4  243 133 \n",
    " KAF  BZ  MSG     0614 08.53         2.7 0.20                                   \n",
    " KAF  BZ ESG      0614 11.10                                    -0.2 0          \n",
    " KALU BZ EPB      0613 43.50                                     0.2 6  249   5 \n",
    " KALU BZ ESB      0614 12.34                                     0.4 4          \n",
    " HEMU BZ EPB      0613 45.78                   61.0             -0.4 8  268 249 \n",
    " HEMU BZ ESG      0614 18.14                                    -0.3 4          \n",
    " TOF  BZ EPB      0613 48.10                                     0.0 3  281  13 \n",
    " TOF  BZ  MSG     0614 18.11         2.2 0.20                                   \n",
    " TOF  BZ ESB      0614 20.10                                    -0.1 0          \n",
    " ERTU BZ ES       0614 27.84                                     0.4 0  328 354 \n",
                                ])
class TestReadNordic(object):
    def testReadNordic(self):
        nordic_event = createNordicEvent(DUMMY_NORDIC_FILE, False)
        assert str(nordic_event) == "".join(DUMMY_NORDIC_FILE)

    def testFaultyReadNordic(self):
        with pytest.raises(Exception):
            nordic_event = createNordicEvent(DUMMY_NORDIC_FAULTY_FILE, False)

    def testFixNordic(self):
        nordic_event = createNordicEvent(DUMMY_NORDIC_FAULTY_FILE, True)
        assert str(nordic_event) == "".join(DUMMY_NORDIC_FILE)

