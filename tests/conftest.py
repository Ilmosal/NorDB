import os
import pytest
from nordb.database import norDBManagement
from nordb.core import usernameUtilities
from nordb.core import nordic
from nordb import settings

@pytest.fixture(scope="function")
def setupdb():
    settings.setTest()
    username = settings.username
    norDBManagement.createDatabase()
    yield None
    usernameUtilities.confUser(username)
    norDBManagement.destroyDatabase()

@pytest.fixture(scope="module")
def nordicEvents():
    nordic_events = [
                        [
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
                        ],
                        [
                        " 2017 0110 1225 38.9 LE 63.889  24.821 28.8FFHEL  9 0.3 1.1LHEL                1\n",
                        " GAP=291         0.7     5.200   6.200                  0.1                    5\n",
                        " CSS:2017010122438.WFDISC  (det3c)                                             6\n",
                        " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                        " FINLAND                                                                       3\n",
                        " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n",
                        " OBF6 BZ  Pb      1225 44.02                                    -1.1 0   30 337 \n",
                        " OBF6 BZ  MSG     1225 46.45         5.7 0.10                                   \n",  
                        " OBF6 BZ  Sb      1225 47.89                                    -1.8 0   30 337 \n",
                        " OBF7 BZ  Pb      1225 47.55                                     0.010   49 311 \n",
                        " OBF7 BZ  MSG     1225 51.87         2.6 0.10                                   \n",  
                        " OBF7 BZ  Sb      1225 53.77                                    -0.110   49 311 \n",
                        " OUF  BZ  Pb      1225 48.07                                    -0.110   54 356 \n",
                        " OUF  BZ  Sb      1225 55.08                                     0.210   54 356 \n",
                        " OBF5 BZ  Pb      1225 49.80                                    -0.010   66  20 \n",
                        " OBF5 BZ  Sb      1225 57.95                                     0.110   66  20 \n",
                        " OBF1 BZ  Pb      1225 51.15                                     0.8 0   69 328 \n",
                        " OBF1 BZ  Sb      1225 59.26                                     0.5 0   69 328 \n",
                        " OBF0 BZ  Pb      1225 52.10                                     1.1 0   74 338 \n",
                        " OBF0 BZ  Sb      1226 00.59                                     0.8 0   74 338 \n",
                        " OBF2 BZ  Pn      1225 53.64                                    -0.4 0   84 347 \n",
                        " OBF3 BZ  Pn      1225 56.44                                    -0.110  104 357 \n",
                        " OBF4 BZ  Pn      1225 56.55                                     0.010  104   8 \n",
                        " OBF4 BZ  Sn      1226 10.62                                     1.1 0  104   8 \n", 
                        ],
                        [
                        " 2017 0801 1200 34.4 LE 64.812  25.066  0.0FFHEL  7 1.6 0.8LHEL                1\n",
                        " GAP=171         0.8     7.100  10.400                  0.2                    5\n",
                        " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                        " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n",
                        " OBF4 BZ  Pg      1200 34.67                  293.9          31 -0.010    2  83 \n",
                        " OBF4 BZ  Sg      1200 35.91                                     1.010    2  83 \n", 
                        " OBF3 BZ  Pg      1200 39.21                                     2.010   17 272 \n",
                        ],
                    ]
    return nordic_events

@pytest.fixture(scope="module")
def fixableNordicEvent():
    fixable_nordic_event =  [
                                [
                                " 2017  8 1 2259 60.0 LE 64.812  25.066  0.0FFHEL  7 1.6 nAnLHEL nan     nan    1\n",
                                " GAP=171         0.8     7.1    10.4                    nAn                    5\n",
                                " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                                " OBF4 BZ  Pg      2359 60.00                  360.0          31 -0.010  1.2  83 \n",
                                " OBF4 BZ  Sg      2302 35.91                                     1.010    2  83 \n", 
                                " OBF3 BZ  Pg       200 39.21                                     2.010   17 360 \n",
                                ],
                                [
                                " 2017 0801 2300 00.0 LE 64.812  25.066  0.0FFHEL  7 1.6    LHEL                1\n",
                                " GAP=171         0.8     7.100  10.400                                         5\n",
                                " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                                " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n",
                                " OBF4 BZ  Pg     +0000 00.00                    0.0          31 -0.010    1  83 \n",
                                " OBF4 BZ  Sg      2302 35.91                                     1.010    2  83 \n", 
                                " OBF3 BZ  Pg     +0200 39.21                                     2.010   17   0 \n",

                                ],
                                [
                                " 2017  8 1 2259 60.0 LE 64.812  25.066  0.0FFHEL  7 1.6 asdLHEL asdasdadsasdasd1\n",
                                " GAP=171         0.8     7.1    10.4                    vidu                   5\n",
                                " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                                " OBF4 BZ  Pg      23as 60.00                  293.9          31 -0.010  juu  83 \n",
                                " OBF4 BZ  Sg      as00 35.91                                     1.010    2  83 \n", 
                                " OBF3 BZ  Pg       200 39.21                                     2.010   17 272 \n",
                                ],
                                [
                                " 2017  8 1 2359 60.0 LE 64.812  25.066  0.0FFHEL  7 1.6 asdLHEL asd     asd    1\n",
                                " GAP=171         0.8     7.1    10.4                    asd                    5\n",
                                " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                                " OBF4 BZ  Pg      23as 60.00                  293.9          31 -0.010  juu  83 \n",
                                " OBF4 BZ  Sg      as00 35.91                                     1.010    2  83 \n", 
                                " OBF3 BZ  Pg       200 39.21                                     2.010   17 272 \n",
                                ],

                            ]

    return fixable_nordic_event

@pytest.fixture(scope="module")
def faultyNordicEvents():
    faulty_nordic_events = [
                        [
                        " 2013 01AR 0613 60.0 LE 63RAwa  22.913  0.0F HEL 15 0.3 1.6LHEL 1.4LUPP        1\n",
                        " GAP= 80         0.1     0.391   0.477                  0.0                    5\n",
                        " CSS:2013003061203.WFDISC  (DET3C)                                             6\n",
                        " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE CHECKED (NIH)              3\n",
                        " MINING AREA & TIME WINDOW: PEDERSORE  3KM                                     3\n",
                        " FINLAND                                                                       3\n",
                        " 2013 0103 0613 04.0 LE 63.650  22.942  0.0FFHEL 11 0.4 1.6LHEL                1\n",
                        " GAP= 92         0.3     0.291   0.427                  0.1                    5\n",
                        " 2013 0103 0613 05.2 LP 63.680  22Rasd  0.1F UPP  7 0.3 1.4LUPP                1\n",
                        "                            2 MM                                        BER    2\n",
                        " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n",
                        " VAF  BZ EP       0613 15.30                    7.0              0.210   67 191 \n",
                        " VAF  BZ ES       0613 23.10                                     0.4 4          \n",
                        " UMAU BZ EP       0613 22.64                                    -0RAr0  114 285 \n",
                        " BURU BZ EPB      0613 25.38                  141.0             -0.1 9  130 325 \n",
                        " BURU BZ ES       Rar3 39.82                                    -0.3 4          \n",
                        " ODEU BZ EP       0613 26.31                                    -0.2 9  138 310 \n",
                        " SVAU ad EP       0613Rasdr1                                     0.3 8  189 302 \n",
                        " KEF  BZ EPN      0613 35.36                                     0.0 4  192 148 \n",
                        " KEF  BZ ESN      0613 58.10                                    -0.0 8          \n",
                        " SUF  BZ EPG      0613 35.20                                    -0.1 8  193 121 \n",
                        " SUF  BZ  MSG     0613 55.58         3.6 0.20                                   \n",
                        " SUF  BZ ESN      0613 58.00                                    -0Ra 9          \n",
                        " OUL  BZ EPG      0613 39.06                  224.0             -0.2 4  217  40 \n",
                        " OUL  BZ ESG      0614 04.50                                     0.3 5          \n",
                        " SJUU BZ EP       0613 38.75                                     0.1 8  218 344 \n",
                        " LILU BZ EP       0613 41RA0                                     0.5 8  236 323 \n",
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
                        ],
                        [
                        " 2017 0110 1225 38.9 LE 63.889  24.821 28.8FFHEL  9 0.3 1.1LHEL                1\n",
                        " GAP=291         0.7     5.2     6.2                    0.1                    5\n",
                        " OBF7 BZ  MSG     1225 51.87         2.6 0.10                                   \n",  
                        " OBF7 BZ  Sb      1225 53.77                                    -0.110   49 311 \n",
                        " OUF  BZ  Pb      1225 48.07                                    -0.110   54 356 \n",
                        " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                        " CSS:2017010122438.WFDISC  (det3c)                                             6\n",
                        " FINLAND                                                                       3\n",
                        " OBF6 BZ  Pb      1225 44.02                                    -1.1 0   30 337 \n",
                        " OBF6 BZ  MSG     1225 46.45         5.7 0.10                                   \n",  
                        " OBF6 BZ  Sb      1225 47.89                                    -1.8 0   30 337 \n",
                        " OBF7 BZ  Pb      1225 47.55                                     0.010   49 311 \n",
                        " OUF  BZ  Sb      1225 55.08                                     0.210   54 356 \n",
                        " OBF5 BZ  Pb      1225 49.80                                    -0.010   66  20 \n",
                        " FINLAND                                                                       3\n",
                        " OBF5 BZ  Sb      1225 57.95                                     0.110   66  20 \n",
                        " OBF1 BZ  Pb      1225 51.15                                     0.8 0   69 328 \n",
                        " OBF1 BZ  Sb      1225 59.26                                     0.5 0   69 328 \n",
                        " OBF0 BZ  Pb      1225 52.10                                     1.1 0   74 338 \n",
                        " OBF0 BZ  Sb      1226 00.59                                     0.8 0   74 338 \n",
                        " OBF2 BZ  Pn      1225 53.64                                    -0.4 0   84 347 \n",
                        " OBF3 BZ  Pn      1225 56.44                                    -0.110  104 357 \n",
                        " OBF4 BZ  Pn      1225 56.55                                     0.010  104   8 \n",
                        " OBF4 BZ  Sn      1226 10.62                                     1.1 0  104   8 \n", 
                        " GAP=291         0.7     5.2     6.2                    0.1                    5\n",

                        ],
                        [
                        " 0017 7821 12-1 34.4 LE 64.812  -5.066  0.0FFHEL  7 1.6 0.8LHEL                1\n",
                        " GAP=171         0.8     7.1    10.4                    0.2                    5\n",
                        " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE UNCHECKED                  3\n",
                        " OBF4 BZ  Pg      1200 34.67                  293.9          31 -0.010   -2  83 \n"  
                        " OBF4 BZ  Sg      4200 35.91                                     1.010    2  83 \n"  
                        " OBF3 BZ  Pg      1200 79.21                                     2.010   17 272 \n"
                        ]
                    ]
    return faulty_nordic_events

@pytest.fixture(scope="module")
def stationFiles():
    station_files =     [
                        "AFI     2004334       -1  -13.9093 -171.7773    0.7060 AFIAMALU, SAMOA                                    ar   AFI       0.0000    0.0000       2004-Nov-29\n",
                        "AK01    2006257       -1   50.6911   29.2131    0.1600 Malin Array element AK01                           ss   AKBB     -1.1480   -0.7590       2006-Sep-14\n",
                        "AK02    2006257       -1   50.6573   29.2057    0.1700 Malin Array element AK02                           ss   AKBB     -4.9220   -1.1640       2006-Sep-14\n",
                        "AK03    2006257       -1   50.7263   29.2217    0.1600 Malin Array element AK03                           ss   AKBB      2.7770   -0.2640       2006-Sep-14\n",
                        "AKTO    2005256       -1   50.4348   58.0164    0.3790 AKTYUBINSK, KAZAKHSTAN                             bb   AKTO      0.0000    0.0000       2005-Sep-13\n",
                        "AL31    1977149  2005256   65.0649 -147.5668    0.2980 EIELSON, AK ARRAY, United States of America        ss   -         0.0000    0.0000       2008-Jun-04\n"
                        ]

    return station_files

@pytest.fixture(scope="module")
def faultyStationFiles():
    faulty_files =      [
                        "AFI     2004334       -1  -13.9093 -371.7773    0.7060 AFIAMALU, SAMOA                                    ar   AFI       0.0000    0.0000       2004-Nov-29\n",
                        "AK01    2006257       -1   50.6911       nAn    0.1600 Malin Array element AK01                           ss   AKBB     -1.1480   -0.7590       2006-Sep-14\n",
                        "AK02    2006257       -1   50.6573   29.2057  -99.1700 Malin Array element AK02                           ss   AKBB     -4.9220   -1.1640       2006-Sep-14\n",
                        "AK03    2006257       -1  650.7263   29.2217    0.1600 Malin Array element AK03                           ss   AKBB      2.7770   -0.2640       2006-Sep-14\n",
                        "AKTO    2005256       -1   50.4348   58.0164    0.3790 AKTYUBINSK, KAZAKHSTAN                             bb   AKTO      0.0000       inf       2005-Sep-13\n",
                        "AL31    asdasdd  2005256   65.0649 -147.5668    0.2980 EIELSON, AK ARRAY, United States of America        gg   -         0.0000    0.0000       2008-Jun-04\n"
                        ]
    return faulty_files

@pytest.fixture(scope="module")
def siteChanFiles():
    sitechan_files =    [
                        "AFI    BHE       2004335  1116650       -1 n     0.000000 90.000 90.000 broad band east                                          2004-Nov-29\n",
                        "AFI    BHN       2004334  1116651       -1 n     0.000000 0.0000 90.000 broad band north                                         2004-Nov-29\n",
                        "AFI    BHZ       2004334  1116652       -1 n     0.000000 -1.000 0.0000 broad band vertical                                      2004-Nov-29\n",
                        "AK01   BHZ       2006257  1117200       -1 n     0.037000 -1.000 0.0000 broad-band vertical                                      2006-Sep-14\n",
                        "AK02   BHZ       2006257  1117201       -1 n     0.073000 -1.000 0.0000 broad-band vertical                                      2006-Sep-14\n"
                        ]

    return sitechan_files

@pytest.fixture(scope="module")
def faultySitechanFiles():
    faulty_files =      [
                        "ASD    BHE       2004335  1116650       -1 n     0.000000 90.000 90.000 broad band east                                          2004-Nov-29\n",
                        "AFI    BHN       2004334  -116651       -1 n     0.000000 0.0000 90.000 broad band north                                         2004-Nov-29\n",
                        "AFI    BHZ       adssada  1116652       -1 n     0.000000 -1.000 0.0000 broad band vertical                                      2004-Nov-29\n",
                        "AK01   BHZ       2006257  1117200       -1 g     0.037000 -1.000 0.0000 broad-band vertical                                      2006-Sep-14\n",
                        ]
    return faulty_files

@pytest.fixture(scope="module")
def sensorFiles():
    sensor_files =  [
                        "AFI    BHE       1101746937.00000  1266943736.99900  1116211  1116650  2004334         1.000000         1.000000 0.0000 y       2004-Nov-29\n",
                        "AFI    BHN       1101746937.00000  1266943736.99900  1116212  1116651  2004334         1.000000         1.000000 0.0000 y       2004-Nov-29\n",
                        "AFI    BHZ       1101746937.00000  1266943736.99900  1116213  1116652  2004334         1.000000         1.000000 0.0000 y       2004-Nov-29\n",
                        "AFI    BHE       1266943737.00000  9999999999.99900  1117422  1116650  2010054         1.000000         1.000000 0.0000 y       2010-May-17\n",
                        "AFI    BHN       1266943737.00000  9999999999.99900  1117423  1116651  2010054         1.000000         1.000000 0.0000 y       2010-May-17\n",
                        "AFI    BHZ       1266943737.00000  9999999999.99900  1117424  1116652  2010054         1.000000         1.000000 0.0000 y       2010-May-17\n"
                    ]

    return sensor_files

@pytest.fixture(scope="module")
def faultySensorFiles():
    faulty_files =   [
                        "FAL    BHE       1101746937.00000  1266943736.99900  1116211  1116650  2004334         1.000000         1.000000 0.0000 y       2004-Nov-29\n",
                        "AFI    ASD       1101746937.00000  1266943736.99900  1116212  1116651  2004334         1.000000         1.000000 0.0000 y       2004-Nov-29\n",
                        "AFI    BHZ       WHAT746937.00000  1266943736.99900  1116213  1116652  2004334         1.000000         1.000000 0.0000 y       2004-Nov-29\n",
                        "AFI    BHE       1266943737.00000 -9999999999.99900  1117422    12310  2010054         1.000000         1.000000 0.0000 y       2010-May-17\n",
                        "AFI    BHN       1266943737.00000  9999999999.99900  1117423  1116651  2010054         1.000000         1.000000 0.0000 a       2010-May-17\n",
                        "AFI    BHZ       1266943737.00000  9999999999.99900  1117424  1116652  2010054         1.000000      -999.000000 0.0000 y       2010-May-17\n"
                    ]
    return faulty_files

@pytest.fixture(scope="module")
def instrumentFiles():
    instrument_files =  [
                            " 1116211 Streckeisen STS-2/VBB + Quanterra Q680             STS-2  b d   40.000000         0.019000         1.000000 ../response                                                      AFI_bb_response_20041107         pazfir       2004-Nov-29\n",
                            " 1116212 Streckeisen STS-2/VBB + Quanterra Q680             STS-2  b d   40.000000         0.019000         1.000000 ../response                                                      AFI_bb_response_20041107         pazfir       2004-Nov-29\n",
                            " 1116213 Streckeisen STS-2/VBB + Quanterra Q680             STS-2  b d   40.000000         0.019000         1.000000 ../response                                                      AFI_bb_response_20041107         pazfir       2004-Nov-29\n",
                            " 1116214 Streckeisen STS-2/VBB + IDA Mark 8                 STS-2  b d   40.000000         0.215000         1.000000 ../response                                                      RPN_bb_response_20040902         pazfir       2004-Nov-30\n",
                            " 1116215 Streckeisen STS-2/VBB + IDA Mark 8                 STS-2  b d   40.000000         0.215000         1.000000 ../response                                                      RPN_bb_response_20040902         pazfir       2004-Nov-30\n",
                            " 1116216 Streckeisen STS-2/VBB + IDA Mark 8                 STS-2  b d   40.000000         0.215000         1.000000 ../response                                                      RPN_bb_response_20040902         pazfir       2004-Nov-30\n",
                    ]

    return instrument_files

@pytest.fixture(scope="module")
def faultyInstrumentFiles():
    faulty_files =   [
                            "    ads1 Streckeisen STS-2/VBB + Quanterra Q680             STS-2  b d   40.000000         0.019000         1.000000 ../response                                                      AFI_bb_response_20041107         pazfir       2004-Nov-29\n",
                            " 1116212 Streckeisen STS-2/VBB + Quanterra Q680             STasdadsasd  40.000000         0.019000         1.000000 ../response                                                      AFI_bb_response_20041107         pazfir       2004-Nov-29\n",
                            " 1116213 Streckeisen STS-2/VBB + Quanterra Q680             STS-2  b d   40.000000         0.019000         1.000000 ../response                                                      AFI_bb_response_20041107         pazfir       2004-Nov-29\n",
                    ]
    return faulty_files


