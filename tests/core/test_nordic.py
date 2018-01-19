import io
from datetime import date
import pytest
from nordb.core.nordic import *
from nordb.validation import nordicValidation

DUMMY_NORDIC_FILE =  io.StringIO(
    " 2013 0103 0613 04.3 LE 63.635  22.913  0.0F HEL 15 0.3 1.6LHEL 1.4LUPP        1\n"
    " GAP= 80         0.1     0.391   0.477                  0.0                    5\n"
    " CSS:2013003061203.WFDISC  (DET3C)                                             6\n"
    " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE CHECKED (NIH)              3\n"
    " MINING AREA & TIME WINDOW: PEDERSORE  3KM                                     3\n"
    " FINLAND                                                                       3\n"
    " 2013 0103 0613 04.0 LE 63.650  22.942  0.0FFHEL 11 0.4 1.6LHEL                1\n"
    " GAP= 92         0.3     0.291   0.427                  0.1                    5\n"
    " 2013 0103 0613 05.2 LP 63.680  22.728  0.1F UPP  7 0.3 1.4LUPP                1\n"
    "                            2 MM                                        BER    2\n"
    " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n"
    " VAF  BZ EP       0613 15.30                    7.0              0.210   67 191 \n"
    " VAF  BZ ES       0613 23.10                                     0.4 4          \n"
    " UMAU BZ EP       0613 22.64                                    -0.010  114 285 \n"
    " BURU BZ EPB      0613 25.38                  141.0             -0.1 9  130 325 \n"
    " BURU BZ ES       0613 39.82                                    -0.3 4          \n"
    " ODEU BZ EP       0613 26.31                                    -0.2 9  138 310 \n"
    " SVAU BZ EP       0613 34.71                                     0.3 8  189 302 \n"
    " KEF  BZ EPN      0613 35.36                                     0.0 4  192 148 \n"
    " KEF  BZ ESN      0613 58.10                                    -0.0 8          \n"
    " SUF  BZ EPG      0613 35.20                                    -0.1 8  193 121 \n"
    " SUF  BZ  MSG     0613 55.58         3.6 0.20                                   \n"
    " SUF  BZ ESN      0613 58.00                                    -0.3 9          \n"
    " OUL  BZ EPG      0613 39.06                  224.0             -0.2 4  217  40 \n"
    " OUL  BZ ESG      0614 04.50                                     0.3 5          \n"
    " SJUU BZ EP       0613 38.75                                     0.1 8  218 344 \n"
    " LILU BZ EP       0613 41.40                                     0.5 8  236 323 \n"
    " KAF  BZ EPB      0613 42.50                  314.0              0.2 4  243 133 \n"
    " KAF  BZ  MSG     0614 08.53         2.7 0.20                                   \n"
    " KAF  BZ ESG      0614 11.10                                    -0.2 0          \n"
    " KALU BZ EPB      0613 43.50                                     0.2 6  249   5 \n"
    " KALU BZ ESB      0614 12.34                                     0.4 4          \n"
    " HEMU BZ EPB      0613 45.78                   61.0             -0.4 8  268 249 \n"
    " HEMU BZ ESG      0614 18.14                                    -0.3 4          \n"
    " TOF  BZ EPB      0613 48.10                                     0.0 3  281  13 \n"
    " TOF  BZ  MSG     0614 18.11         2.2 0.20                                   \n"
    " TOF  BZ ESB      0614 20.10                                    -0.1 0          \n"
    " ERTU BZ ES       0614 27.84                                     0.4 0  328 354 \n"
    "                                                                                \n"
                                )

DUMMY_NORDIC_FAULTY_FILE =  io.StringIO(
    " 2013  103  613 60.0 LE 63.635  22.913  0.0F HEL 15 0.3 1.6LHEL 1.4LUPP        1\n"
    " GAP= 80         0.1     0.391   0.477                  0.0                    5\n"
    " CSS:2013003061203.WFDISC  (DET3C)                                             6\n"
    " FULLY AUTOMATIC, EVENT TYPE & LOCATION & MAGNITUDE CHECKED (NIH)              3\n"
    " MINING AREA & TIME WINDOW: PEDERSORE  3KM                                     3\n"
    " FINLAND                                                                       3\n"
    " 2013 0103 0613  4.0 LE 63.650  22.942  0.0FFHEL 11 0.4 1.6LHEL                1\n"
    " GAP= 92         0.3     0.291   0.427                  0.1                    5\n"
    " 2013 0103 0613  5.2 LP 63.680  22.728  0.1F UPP  7 0.3 1.4LUPP                1\n"
    " STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO SNR AR TRES W  DIS CAZ7\n"
    " VAF  BZ EP        613 15.30                    7.0              0.210   67 191 \n"
    " VAF  BZ ES        613 23.10                                     0.4 4          \n"
    " UMAU BZ EP        613 22.64                                    -0.010  114 285 \n"
    " BURU BZ EPB       613 25.38                  141.0             -0.1 9  130 325 \n"
    " BURU BZ ES        613 39.82                                    -0.3 4          \n"
    " ODEU BZ EP        613 26.31                                    -0.2 9  138 310 \n"
    " SVAU BZ EP        613 34.71                                     0.3 8  189 302 \n"
    " KEF  BZ EPN       613 35.36                                     0.0 4  192 148 \n"
    " KEF  BZ ESN       613 58.10                                    -0.0 8          \n"
    " SUF  BZ EPG       613 35.20                                    -0.1 8  193 121 \n"
    " SUF  BZ  MSG      613 55.58         3.6 0.20                                   \n"
    " SUF  BZ ESN       613 58.00                                    -0.3 9          \n"
    " OUL  BZ EPG       613 39.06                  224.0             -0.2 4  217  40 \n"
    " OUL  BZ ESG       614 04.50                                     0.3 5          \n"
    " SJUU BZ EP        613 38.75                                     0.1 8  218 344 \n"
    " LILU BZ EP        613 41.40                                     0.5 8  236 323 \n"
    " KAF  BZ EPB       613 42.50                  314.0              0.2 4  243 133 \n"
    " KAF  BZ  MSG      614  8.53         2.7 0.20                                   \n"
    " KAF  BZ ESG       614 11.10                                    -0.2 0          \n"
    " KALU BZ EPB       613 43.50                                     0.2 6  249   5 \n"
    " KALU BZ ESB       614 12.34                                     0.4 4          \n"
    " HEMU BZ EPB       613 45.78                   61.0             -0.4 8  268 249 \n"
    " HEMU BZ ESG       614 18.14                                    -0.3 4          \n"
    " TOF  BZ EPB       613 48.10                                     0.0 3  281  13 \n"
    " TOF  BZ  MSG      614 18.11         2.2 0.20                                   \n"
    " TOF  BZ ESB       614 20.10                                    -0.1 0          \n"
    " ERTU BZ ES        614 27.84                                     0.4 0  328 354 \n"
    "                                                                                \n"
                                )

class TestReadNordic(object):
    def testReadNordic(self):
        nordics, nordics_fail = readNordic(DUMMY_NORDIC_FILE, False)
        DUMMY_NORDIC_FILE.seek(0)
        assert len(nordics) == 1
        assert len(nordics_fail) == 0
        assert str(nordics[0]) == DUMMY_NORDIC_FILE.read()[:-81]

    def testFaultyReadNordic(self):
        nordics, nordics_fail = readNordic(DUMMY_NORDIC_FAULTY_FILE, False)
        DUMMY_NORDIC_FAULTY_FILE.seek(0)
        assert len(nordics) == 0
        assert len(nordics_fail) == 1

    def testFixNordic(self):
        nordics, nordics_fail = readNordic(DUMMY_NORDIC_FAULTY_FILE, True)
        DUMMY_NORDIC_FAULTY_FILE.seek(0)
        assert len(nordics) == 1
        assert len(nordics_fail) == 0

class TestNordicData(object):
    def testCorrectLine(self):
        line = " VAFB BZ EAML0  C+0613 15.30    5 1233.1 0.20 122.1 12.112.2312123.0 9   67 191 \n"
        assert str(dataString2Data(createStringPhaseData(line), -1)) == line[:-1]

class TestNordicMain(object):
    def testCorrectLine(self):
        line = " 2013 0103 0613 04.3ALE 63.635  22.913  0.0FFHEL 15 0.3 1.6LHEL 1.4CUPP 1.3CBER1\n"
        assert str(mainString2Main(createStringMainHeader(line), -1)) == line[:-1]

class TestNordicMacroseismic(object):
    def testCorrectLine(self):
        line = "     ANY_DESCRIPTIVE FTSCL 12+MM  63.12   22.31 5.2I4.1212.123112.3231 ABER    2\n"
        assert str(macroseismicString2Macroseismic(createStringMacroseismicHeader(line), -1)) == line[:-1]

class TestNordicComment(object):
    def testCorrectLine(self):
        line = " ASDSADASDASDASDASDASDASDASDSADASDsadsadaDSADSASDSADdadsasdsasdasdASDASdaadssad3\n"
        assert str(commentString2Comment(createStringCommentHeader(line), -1)) == line[:-1]

class TestErrorHeader(object):
    def testCorrectLine(self):
        line = " GAP= 92         0.3     0.291   0.427  0.1             0.1                    5\n"
        assert str(errorString2Error(createStringErrorHeader(line, 1), -1)) == line[:-1]

class TestWaveformHeader(object):
    def testCorrectLine(self):
        line = " ASDASDASDSADSADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD6\n"
        assert str(waveformString2Waveform(createStringWaveformHeader(line), -1)) == line[:-1]

class TestReturnInt(object):
    def testCorrectPlainInt(self):
        assert returnInt("12") == 12

    def testCorrectEmptyString(self):
        assert returnInt("  ") is None

    def testCorrectIntWithZero(self):
        assert returnInt("02") == 2

    def testCorrectNegativeInt(self):
        assert returnInt("-12") == -12

    def testStringReturnsError(self):
        with pytest.raises(ValueError):
            returnInt("error")

class TestReturnFloat(object):
    def testCorrectPlainFloat(self):
        assert returnFloat("12.12") == 12.12

    def testCorrectEmptyString(self):
        assert returnFloat("  ") is None

    def testCorrectFloatWithZero(self):
        assert returnFloat("02.12") == 2.12

    def testCorrectNegativeFloat(self):
        assert returnFloat("-12.31") == -12.31

    def testStringReturnsError(self):
        with pytest.raises(ValueError):
            returnFloat("error")

class TestReturnDate(object):
    def testCorrectDate(self):
        assert returnDate("2015 03 12") == date(year=2015, month=3, day=12)

    def testEmptyDate(self):
        assert returnDate("   ") is None

    def testDateWithWrongValues(self):
        with pytest.raises(ValueError):
            returnDate("2014 15 58")

    def testDateWithWrongString(self):
        with pytest.raises(ValueError):
            returnDate("asdasdasda")

class TestReturnString(object):
    def testCorrectString(self):
        assert returnString("asd ") == "asd"

    def testEmptyString(self):
        assert returnString("  ") == None
