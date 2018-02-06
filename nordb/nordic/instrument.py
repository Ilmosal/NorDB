"""
Contains information relevant to Instrument object

Classes and Functions
---------------------
"""
import operator

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String

class Instrument:
    """
    Class for instrument information. Comes from css instrument format.

    :param array data: all the relevant data for Sensor in an array. These values are accessed by its numerations. 
    :ivar int header_type: 12
    :ivar string band: Frequency band. Maximum of 1 character
    :ivar string instrument_name: Name of the instrument. Maximum of 50 characters
    :ivar string instrument_type: Type of the instrument. Maximum of 6 characters
    :ivar string digital: data type: d - digital a - analog. Maximum of 1 characters
    :ivar float samprate: sampling rate in samples/sec
    :ivar float ncalib: nominal calibration (nn/count)
    :ivar flaot ncalper: nominal calibration period (sec)
    :ivar string resp_dir: Directory for instrument response file. Maximum of 64 characters
    :ivar string dfile: Maximum of 32 characters
    :ivar string rsptype: response type. Maximum of 6 characters
    :ivar date lddate: load date
    :ivar int I_ID: id of the instrument in the database
    :ivar int CSS_ID: css_id of the instrument in the database
    :ivar int INSTRUMENT_NAME: Location of the instrument_name in a array. Value of 0
    :ivar int INSTRUMENT_TYPE: Location of the instrument_type in a array. Value of 1
    :ivar int BAND: Location of the band in a array. Value of 2
    :ivar int DIGITAL: Location of the digital in a array. Value of 3
    :ivar int SAMPRATE: Location of the samprate in a array. Value of 4
    :ivar int NCALIB: Location of the ncalib in a array. Value of 5
    :ivar int NCALPER: Location of the ncalper in a array. Value of 6
    :ivar int RESP_DIR: Location of the resp_dir in a array. Value of 7
    :ivar int DFILE: Location of the dfile in a array. Value of 8
    :ivar int RSPTYPE: Location of the rsptype in a array. Value of 9
    :ivar int LDDATE: Location of the lddate in a array. Value of 10
    :ivar int ID: Location of the id in a array. Value of 11
    :ivar int CSS_ID: Location of the css_id in a array. Value of 12
    """
    header_type = 12
    INSTRUMENT_NAME = 0
    INSTRUMENT_TYPE = 1
    BAND = 2 
    DIGITAL = 3
    SAMPRATE = 4
    NCALIB = 5
    NCALPER = 6
    RESP_DIR = 7
    DFILE = 8
    RSPTYPE = 9
    LDDATE = 10
    I_ID = 11
    CSS_ID = 12

    def __init__(self, data):
        self.instrument_name = data[self.INSTRUMENT_NAME]
        self.instrument_type = data[self.INSTRUMENT_TYPE]
        self.band = data[self.BAND]
        self.digital = data[self.DIGITAL]
        self.samprate = data[self.SAMPRATE]
        self.ncalib = data[self.NCALIB]
        self.ncalper = data[self.NCALPER]
        self.resp_dir = data[self.RESP_DIR]
        self.dfile = data[self.DFILE]
        self.rsptype = data[self.RSPTYPE]
        self.lddate = data[self.LDDATE]
        self.i_id = data[self.I_ID]
        self.css_id = data[self.CSS_ID]

    instrument_name = property(operator.attrgetter('_instrument_name'), doc="")
    
    @instrument_name.setter
    def instrument_name(self, val):
        val_instrument_name = validateString(val, "instrument_name", 0, 50, None, False, self.header_type)
        self._instrument_name = val_instrument_name

    instrument_type = property(operator.attrgetter('_instrument_type'), doc="")
    
    @instrument_type.setter
    def instrument_type(self, val):
        val_instrument_type = validateString(val, "instrument_type", 0, 6, None, False, self.header_type)
        self._instrument_type = val_instrument_type

    band = property(operator.attrgetter('_band'), doc="")
    
    @band.setter
    def band(self, val):
        val_band = validateString(val, "band", 0, 1, None, False, self.header_type)
        self._band = val_band

    digital = property(operator.attrgetter('_digital'), doc="")
    
    @digital.setter
    def digital(self, val):
        val_digital = validateString(val, "digital", 0, 1, None, False, self.header_type)
        self._digital = val_digital

    samprate = property(operator.attrgetter('_samprate'), doc="")
    
    @samprate.setter
    def samprate(self, val):
        val_samprate = validateFloat(val, "samprate", 0.0, 1000.0, True, self.header_type)
        self._samprate = val_samprate

    ncalib = property(operator.attrgetter('_ncalib'), doc="")
    
    @ncalib.setter
    def ncalib(self, val):
        val_ncalib = validateFloat(val, "ncalib", -1.0, 10000.0, True, self.header_type)
        self._ncalib = val_ncalib

    ncalper = property(operator.attrgetter('_ncalper'), doc="")
    
    @ncalper.setter
    def ncalper(self, val):
        val_ncalper = validateFloat(val, "ncalper", -1.0, 10000.0, True, self.header_type)
        self._ncalper = val_ncalper

    resp_dir = property(operator.attrgetter('_resp_dir'), doc="")
    
    @resp_dir.setter
    def resp_dir(self, val):
        val_resp_dir = validateString(val, "resp_dir", 0, 64, None, False, self.header_type)
        self._resp_dir = val_resp_dir

    dfile = property(operator.attrgetter('_dfile'), doc="")
    
    @dfile.setter
    def dfile(self, val):
        val_dfile = validateString(val, "dfile", 0, 32, None, False, self.header_type)
        self._dfile = val_dfile

    rsptype = property(operator.attrgetter('_rsptype'), doc="")
    
    @rsptype.setter
    def rsptype(self, val):
        val_rsptype = validateString(val, "rsptype", 0, 6, None, False, self.header_type)
        self._rsptype = val_rsptype

    lddate = property(operator.attrgetter('_lddate'), doc="")
    
    @lddate.setter
    def lddate(self, val):
        val_lddate = validateDate(val, "lddate", self.header_type)
        self._lddate = val_lddate

    css_id = property(operator.attrgetter('_css_id'), doc="")

    @css_id.setter
    def css_id(self, val):
        val_css_id = validateInteger(val, "css_id", None, None, False, self.header_type)
        self._css_id = val_css_id

    def __str__(self):
        instrumentString = ""
    
        instrumentString += addInteger2String(self.css_id, 8, '>')
        
        instrumentString += " "

        instrumentString += addString2String(self.instrument_name, 50, '<')

        instrumentString += " "
        
        instrumentString += addString2String(self.instrument_type, 6, '<')

        instrumentString += " "

        instrumentString += addString2String(self.band, 2, '<')
        instrumentString += addString2String(self.digital, 2, '<')
        instrumentString += addFloat2String (self.samprate, 11, 7, '>')

        instrumentString += "    "
        
        instrumentString += addFloat2String (self.ncalib, 13, 6, '>')
        
        instrumentString += "    "
        
        instrumentString += addFloat2String(self.ncalper, 13, 6, '>')

        instrumentString += " "

        instrumentString += addString2String(self.resp_dir, 64, '<')
            
        instrumentString += " "
        
        instrumentString += addString2String(self.dfile, 32, '<')

        instrumentString += " "

        instrumentString += addString2String(self.rsptype, 6, '<')
    
        instrumentString += "       "

        instrumentString += addString2String(self.lddate.strftime("%Y-%b-%d"), 11, '<')

        return instrumentString

    def getAsList(self):
        instrument_list = [ self.instrument_name,
                            self.instrument_type,
                            self.band,
                            self.digital,
                            self.samprate,
                            self.ncalib,
                            self.ncalper,
                            self.resp_dir,
                            self.dfile,
                            self.rsptype,
                            self.lddate]

        return instrument_list
