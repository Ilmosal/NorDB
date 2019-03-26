"""
Contains information relevant to Responses.
"""

import operator
import unidecode

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String
from nordb.core.utils import stringToDate

class Response(object):
    """
    Class for response information. Always use eihter PazResponse or FapResponse instead of this class.

    :param array data: all the relevant data for response in an array. These values are accessed by its numerations.
    :ivar int c_id: Creation id of the response in the database
    :ivar string file_name: Name of the response file from which this object was read from
    :ivar string source: Source of the response
    :ivar string stage: stage of the response
    :ivar string description: description of the response
    :ivar string response_format: format of this response file. Either paz or fap
    :ivar string author: author of the response
    :ivar int response_id: id of the response in the database
    :ivar int FILE_NAME: Enumeration of the data list. Value of 0
    :ivar int SOURCE: Enumeration of the data list. Value of 1
    :ivar int STAGE: Enumeration of the data list. Value of 2
    :ivar int DESCRIPTION: Enumeration of the data list. Value of 3
    :ivar int RESPONSE_FORMAT: Enumeration of the data list. Value of 4
    :ivar int AUTHOR: Enumeration of the data list. Value of 5
    :ivar int ID: Enumeration of the data list. Value of 6
    """
    header_type = 14
    FILE_NAME = 0
    SOURCE = 1
    STAGE = 2
    DESCRIPTION = 3
    RESPONSE_FORMAT = 4
    AUTHOR = 5
    ID = 6

    def __init__(self, data = None):
        if data is None:
            self.c_id = -1
            self.file_name = None
            self.source = None
            self.stage = None
            self.description = None
            self.response_format = None
            self.author = None
            self.response_id = -1
        else:
            self.c_id = -1
            self.file_name = data[self.FILE_NAME]
            self.source = data[self.SOURCE]
            self.stage = data[self.STAGE]
            self.description = data[self.DESCRIPTION]
            self.response_format = data[self.RESPONSE_FORMAT]
            self.author = data[self.AUTHOR]
            self.response_id = data[self.ID]

    file_name = property(operator.attrgetter('_file_name'), doc="")

    @file_name.setter
    def file_name(self, val):
        val_file_name = validateString(val, "file_name", 0, 32, None, self.header_type)
        self._file_name = val_file_name

    source = property(operator.attrgetter('_source'), doc="")

    @source.setter
    def source(self, val):
        val_source = validateString(val, "source", 0, 32, None, self.header_type)
        self._source = val_source

    stage = property(operator.attrgetter('_stage'), doc="")

    @stage.setter
    def stage(self, val):
        val_stage = validateInteger(val, "stage", 0, 10, self.header_type)
        self._stage = val_stage

    description = property(operator.attrgetter('_description'), doc="")

    @description.setter
    def description(self, val):
        val_description = validateString(val, "description", 0, 32, None, self.header_type)
        self._description = val_description

    response_format = property(operator.attrgetter('_response_format'), doc="")

    @response_format.setter
    def response_format(self, val):
        val_response_format = validateString(val, "response_format", 3, 3, ["paz", "fap"], self.header_type)
        self._response_format = val_response_format

    author = property(operator.attrgetter('_author'), doc="")

    @author.setter
    def author(self, val):
        val_author = validateString(val, "author", 0, 32, None, self.header_type)
        self._author = val_author

    def __str__(self):
        response_string = "{0} {1} {2} {3} {4}\n".format(self.source, self.stage, self.description, self.response_format, self.author)

        return response_string

    def getAsList(self):
        response_list = [
                        self.c_id,
                        self.file_name,
                        self.source,
                        self.stage,
                        self.description,
                        self.response_format,
                        self.author,
                        ]

        return response_list


class PazResponse(Response):
    """
    Class for poles and zeros type of response. Inherits Response class.

    :ivar float scale_factor: scale factor of the response
    :ivar Array poles: array of all the poles in the response. Poles are arrays of floats and contain the imaginary value of the pole and the error of the pole
    :ivar Array zeros: array of all the zeros in the response. Poles are arrays of floats and contain the imaginary value of the zero and the error of the zero
    """
    def __init__(self, response_data = None, scale_factor=None, poles=[], zeros=[]):
        Response.__init__(self, response_data)
        self.scale_factor = scale_factor
        self.poles = poles
        self.zeros = zeros

    scale_factor = property(operator.attrgetter('_scale_factor'), doc="")

    @scale_factor.setter
    def scale_factor(self, val):
        val_scale_factor = validateFloat(val, "scale_factor", None, None, self.header_type)
        self._scale_factor = val_scale_factor

    def getObspyResponse(self, mode="dis"):
        """
        Method for getting the response in a format suited for obspy.

        :param string mode: dis, vel or acc depending on which derivative of paz file you want
        :returns: response in a format fitting to obspy
        """
        if mode not in ["dis", "acc", "vel"]:
            raise Exception("{0} not a valid mode!".format(mode))

        obspy_resp = {'poles':[], 'zeros':[], 'sensitivity':self.scale_factor, 'gain':1.0}
        for p in self.poles:
            obspy_resp['poles'].append(complex(p[0], p[1]))

        ceil = len(self.zeros)
        if (mode == "vel"):
            ceil -= 1
        elif (mode == "acc"):
            ceil -= 2

        zero_list = []

        for i in range(0, ceil):
            obspy_resp['zeros'].append(complex(self.zeros[i][0],
                                               self.zeros[i][1]))

        return obspy_resp

    def __str__(self):
        paz_string = "{0} {1} {2} {3} {4}\n".format(self.source, self.stage, self.description, self.response_format, self.author)
        paz_string += "{0}\n".format(self.scale_factor)
        paz_string += "{0}\n".format(len(self.poles))
        for pole in self.poles:
            paz_string += "{0:10.4f} {1:10.4f} {2:10.4f} {3:10.4f}\n".format(pole[0], pole[1], pole[2], pole[3])
        paz_string += "{0}\n".format(len(self.zeros))
        for zero in self.zeros:
            paz_string += "{0:10.4f} {1:10.4f} {2:10.4f} {3:10.4f}\n".format(zero[0], zero[1], zero[2], zero[3])

        return paz_string

class FapResponse(Response):
    """
    Class for frequency, amplitude and phase type response. Inherits Response class.

    :ivar Array fap: an array of five float values which contain the frequency, amplitude, phase, amplitude_error, phase_error in that order
    """
    def __init__(self, response_data = None, fap = []):
        Response.__init__(self, response_data)
        self.fap = fap

    def __str__(self):
        fap_string = "{0} {1} {2} {3} {4}\n".format(self.source, self.stage, self.description, self.response_format, self.author)
        fap_string += "{0}\n".format(len(self.fap))
        for f in self.fap:
            fap_string += "{0:9.4f}   {1:9.4f}   {2:9.4f}   {3:9.4f}   {4:9.4f}\n".format(f[0], f[1], f[2], f[3], f[4])

        return fap_string

def readResponseArrayToResponse(resp, file_name):
    """
    Function for reading response string array into a Response object

    :param Array resp: response string
    :return: PazResponse object or FapResponse object
    """
    row_num = 0

    while resp[row_num][0] == '#':
        row_num += 1
    resp_data = [file_name]
    resp_data += resp[row_num].split()
    if len(resp_data) == 5:
        resp_data += [None]
    resp_data += [-1]
    if resp_data[4] == 'fap':
        fap = []
        fap_amount = int(resp[row_num+1])

        for i in range(row_num+2, row_num+2+fap_amount):
            fl = resp[i].split()
            fap.append([float(fl[0]), float(fl[1]), float(fl[2]), float(fl[3]), float(fl[4])])

        return FapResponse(resp_data, fap)

    elif resp_data[4] == 'paz':
        poles = []
        zeros = []
        scale_factor = float(resp[row_num+1].strip())
        pole_amount = int(resp[row_num+2])

        for i in range(row_num+3, row_num+3+pole_amount):
            poles.append([float(x) for x in resp[i].split()])

        zero_amount = int(resp[row_num+3+pole_amount])

        for i in range(row_num+4+pole_amount, row_num+4+pole_amount+zero_amount):
            zeros.append([float(x) for x in resp[i].split()])

        return PazResponse(resp_data, scale_factor, poles, zeros)
    else:
        raise Exception("Response is not a paz or fap response")

    return None
