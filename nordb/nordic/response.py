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

class PazResponse(Response):
    """
    Class for poles and zeros type of response. Inherits Response class.
    """
    def __init__(self, response_data, scale_factor, poles, zeros):
        Response.__init__(response_data)
        self.scale_factor = scale_factor
        self.poles = poles
        self.zeros = zeros

    scale_factor = property(operator.attrgetter('_scale_factor'), doc="")
    
    @scale_factor.setter
    def scale_factor(self, val):
        val_scale_factor = validateString(val, "scale_factor", 0, 32, None, self.header_type)
        self._scale_factor = val_scale_factor

    def getAsList(self):
        paz_response_list = self.Response.getAsList()
        paz_response_list += [self.scale_factor]        

        return raz_response_list

class FapResponse(Response):
    """
    Class for frequency, amplitude and phase type response. Inherits Response class.
    """
    def __init__(self, response_data, fap):
        Response.__init__(response_data)
        self.fap = fap

class Response(object):
    """
    Class for response information. Always use eihter PazResponse or FapResponse instead of this class.

    :param array data: all the relevant data for response in an array. These values are accessed by its numerations. 
    :ivar int SOURCE: Source of the response
    :ivar int STAGE: Stage of the response
    :ivar int DESCRIPTION: Description of the response
    :ivar int FORMAT: Format of the reposse. Either paz or fap
    :ivar int AUTHOR: Author of the reponse
    :ivar int INTRUMENT_ID: id of the instrument to which the response refers to. 
    :ivar int ID: id of the response
    """
    header_type = 14
    SOURCE = 0
    STAGE = 1
    DESCRIPTION = 2
    RESPONSE_FORMAT = 3
    AUTHOR = 4
    INSTRUMENT_ID = 5
    ID = 6

    def __init__(self, data):
        self.source = data[self.SOURCE]
        self.stage = data[self.STAGE]
        self.description = data[self.DESCRIPTION]
        self.response_format = data[self.RESPONSE_FORMAT]
        self.author = data[self.AUTHOR]
        self.instrument_id = data[self.INSTRUMENT_ID]
        self.id = data[self.ID]

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

    instrument_id = property(operator.attrgetter('_instrument_id'), doc="")
    
    @instrument_id.setter
    def instrument_id(self, val):
        val_instrument_id = validateInteger(val, "instrument_id", None, None, self.header_type)
        self._instrument_id = val_instrument_id

    def __str__(self):
        response_string = ""

        return sensorString
  
    def getAsList(self):
        response_list = [
                        self.source,
                        self.stage,
                        self.description,
                        self.response_format,
                        self.author,
                        self.instrument_id,
                        self.id
                        ]

        return response_list

def readResponseArrayToResponse(resp):
    """
    Function for reading response string array into a Response object

    :param Array resp: response string
    :return: Response object
    """
    response = [None]*15

    return Response(resp)

