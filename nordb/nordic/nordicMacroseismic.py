"""
This module contains all class information related to NordicMacroseismic header

Functions and Classes
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

class NordicMacroseismic:
    """
    A class that functions as a collection of enums. Contains the information of the macroseismic header line of a nordic file. 

    :param list header: The header of a nordic macroseismic in a list where each index of a value corresponds to NordicMacroseismic's pseudo-enum.
    :ivar string description: Description of the macroseismic event. Maximum of 15 characters
    :ivar string diastrophism_code: Diastrophism code - PDE type (F, U, D)
    :ivar string tsunami_code: Tsunami code - PDE type (T, Q)
    :ivar string seiche_code: Seiche code - PDE type (S, Q)
    :ivar string cultural_effects: Cultural effects - PDE type (C, D, F, H)
    :ivar string unusual_effects: Unsusual effects - PDE type (L, G, S, B, C, V, O, M)
    :ivar int maximum_observed_intensity: Maximum of the observed intesity
    :ivar string maximum_intensity_qualifier: Maximum intensity qualifier (+/- indicating more precisely)
    :ivar string intensity_scale: Intesity Scale - ISC scale (MM, RF, CS, SK)
    :ivar float macroseismic_latitude: Latitude of the event
    :ivar float macroseismic_longitude: Longitude of the event
    :ivar float macroseismic_magnitude: Magnitude of the event
    :ivar string type_of_magnitude: Type of the magnitude (I, A, R, *)
    :ivar float logarithm_of_radius: Logarithm (base 10) of the radius(km) of felt area
    :ivar float logarithm_of_area_1: Logarithm (base 10) of area(km**2) number 1 where earthquake was felt exceeding a given intensity
    :ivar int bordering_intensity_1: Intensity bordering the area number 1
    :ivar float logarithm_of_area_2: Logarithm (base 10) of area(km**2) number 2 where earthquake was felt exceeding a given intensity
    :ivar int bordering_intensity_2: Intensity bordering the area number 2
    :ivar string quality_rank: Quality rank of the report (A, B, C, D)
    :ivar string reporting_agency: Reporting agency
    :ivar int event_id: Id of the event of the Macroseismic header
    :ivar int h_id: Id of the NordicMacroseismic header in the database
    :ivar int header_type: This value tells that this is a NordicMacroseismic object. Value of 2
    :ivar int DESCRIPTION: Location of the description in a array. Value of 0
    :ivar int DIASTROPHISM_CODE: Location of the diastrophism_code in a array. Value of 1
    :ivar int TSUNAMI_CODE: Location of the tsunami_code in a array. Value of 2
    :ivar int SEICHE_CODE: Location of the seiche_code in a array. Value of 3 
    :ivar int CULTURAL_EFFECTS: Location of the cultural_effects in a array. Value of 4
    :ivar int UNUSUAL_EFFECTS: Location of the unusual_effects in a array. Value of 5
    :ivar int MAXIMUM_OBSERVED_INTENSITY: Location of the maximum_observed_intensity in a array. Value of 6
    :ivar int MAXIMUM_INTENSITY_QUALIFIER: Location of the maximum_intensity_qualifier in a array. Value of 7
    :ivar int INTENSITY_SCALE: Location of the intensity_scale in a array. Value of 8
    :ivar int MACROSEISMIC_LATITUDE: Location of the macroseismic_latitude in a array. Value of 9
    :ivar int MACROSEISMIC_LONGITUDE: Location of the macroseismic_longitude in a array. Value of 10
    :ivar int MACROSEISMIC_MAGNITUDE: Location of the macroseismic_magnitude in a array. Value of 11
    :ivar int TYPE_OF_MAGNITUDE: Location of the type_of_magnitude in a array. Value of 12
    :ivar int LOGARITHM_OF_RADIUS: Location of the logarithm_of_radius in a array. Value of 13
    :ivar int LOGARITHM_OF_AREA_1: Location of the logarithm_of_area_1 in a array. Value of 14
    :ivar int BORDERING_INTENSITY_1: Location of the bordering_intensity_1 in a array. Value of 15
    :ivar int LOGARITHM_OF_AREA_2: Location of the logarithm_of_area_2 in a array. Value of 16
    :ivar int BORDERING_INTENSITY_2: Location of the bordering_intensity_2 in a array. Value of 17
    :ivar int QUALITY_RANK: Location of the quality_rank in a array. Value of 18
    :ivar int REPORTING_AGENCY: Location of the reporting_agency in a array. Value of 19
    :ivar int EVENT_ID: Location of the event_id in a array. Value of 20
    :ivar int ID: Location of the id in a array. Value of 21
    """
    header_type = 2
    DESCRIPTION = 0
    DIASTROPHISM_CODE = 1
    TSUNAMI_CODE = 2
    SEICHE_CODE = 3
    CULTURAL_EFFECTS = 4
    UNUSUAL_EFFECTS = 5
    MAXIMUM_OBSERVED_INTENSITY = 6
    MAXIMUM_INTENSITY_QUALIFIER = 7
    INTENSITY_SCALE = 8
    MACROSEISMIC_LATITUDE = 9
    MACROSEISMIC_LONGITUDE = 10
    MACROSEISMIC_MAGNITUDE = 11
    TYPE_OF_MAGNITUDE = 12
    LOGARITHM_OF_RADIUS = 13
    LOGARITHM_OF_AREA_1 = 14
    BORDERING_INTENSITY_1 = 15
    LOGARITHM_OF_AREA_2 = 16
    BORDERING_INTENSITY_2 = 17
    QUALITY_RANK = 18
    REPORTING_AGENCY = 19
    EVENT_ID = 20
    H_ID = 21

    def __init__(self, header = None):
        if header is None:
            self.description = None
            self.diastrophism_code = None
            self.tsunami_code = None
            self.seiche_code = None
            self.cultural_effects = None
            self.unusual_effects = None
            self.maximum_observed_intensity = None
            self.maximum_intensity_qualifier = None
            self.intensity_scale = None
            self.macroseismic_latitude = None
            self.macroseismic_longitude = None
            self.macroseismic_magnitude = None
            self.type_of_magnitude = None
            self.logarithm_of_radius = None
            self.logarithm_of_area_1 = None
            self.bordering_intensity_1 = None
            self.logarithm_of_area_2 = None
            self.bordering_intensity_2 = None
            self.quality_rank = None
            self.reporting_agency = None
            self.event_id = -1
            self.h_id = -1
        else:
            self.description = header[self.DESCRIPTION]
            self.diastrophism_code = header[self.DIASTROPHISM_CODE]
            self.tsunami_code = header[self.TSUNAMI_CODE]
            self.seiche_code = header[self.SEICHE_CODE]
            self.cultural_effects = header[self.CULTURAL_EFFECTS]
            self.unusual_effects = header[self.UNUSUAL_EFFECTS]
            self.maximum_observed_intensity = header[self.MAXIMUM_OBSERVED_INTENSITY]
            self.maximum_intensity_qualifier = header[self.MAXIMUM_INTENSITY_QUALIFIER]
            self.intensity_scale = header[self.INTENSITY_SCALE]
            self.macroseismic_latitude = header[self.MACROSEISMIC_LATITUDE]
            self.macroseismic_longitude = header[self.MACROSEISMIC_LONGITUDE]
            self.macroseismic_magnitude = header[self.MACROSEISMIC_MAGNITUDE]
            self.type_of_magnitude = header[self.TYPE_OF_MAGNITUDE]
            self.logarithm_of_radius = header[self.LOGARITHM_OF_RADIUS]
            self.logarithm_of_area_1 = header[self.LOGARITHM_OF_AREA_1]
            self.bordering_intensity_1 = header[self.BORDERING_INTENSITY_1]
            self.logarithm_of_area_2 = header[self.LOGARITHM_OF_AREA_2]
            self.bordering_intensity_2 = header[self.BORDERING_INTENSITY_2]
            self.quality_rank = header[self.QUALITY_RANK]
            self.reporting_agency = header[self.REPORTING_AGENCY]
            self.event_id = header[self.EVENT_ID]
            self.h_id = header[self.H_ID]

    description = property(operator.attrgetter('_description'), doc="")

    @description.setter
    def description(self, val):
        val_description = validateString(val, "description", 0, 15, None, self.header_type)
        self._description = val_description

    diastrophism_code = property(operator.attrgetter('_diastrophism_code'), doc="")

    @diastrophism_code.setter
    def diastrophism_code(self, val):
        val_diastrophism_code = validateString(val, "diastrophism_code", 0, 1, "FUD ", self.header_type)
        self._diastrophism_code = val_diastrophism_code

    tsunami_code = property(operator.attrgetter('_tsunami_code'), doc="")

    @tsunami_code.setter
    def tsunami_code(self, val):
        val_tsunami_code = validateString(val, "tsunami_code", 0, 1, "TQ ", self.header_type)
        self._tsunami_code = val_tsunami_code

    seiche_code = property(operator.attrgetter('_seiche_code'), doc="")

    @seiche_code.setter
    def seiche_code(self, val):
        val_seiche_code = validateString(val, "seiche_code", 0, 1, "SFQ ", self.header_type)
        self._seiche_code = val_seiche_code

    cultural_effects = property(operator.attrgetter('_cultural_effects'), doc="")

    @cultural_effects.setter
    def cultural_effects(self, val):
        val_cultural_effects = validateString(val, "cultural_effects", 0, 1, "CDFH ", self.header_type)
        self._cultural_effects = val_cultural_effects

    unusual_effects = property(operator.attrgetter('_unusual_effects'), doc="")

    @unusual_effects.setter
    def unusual_effects(self, val):
        val_unusual_effects = validateString(val, "unusual_effects", 0, 1, "LGSBCVOM", self.header_type)
        self._unusual_effects = val_unusual_effects

    maximum_observed_intensity = property(operator.attrgetter('_maximum_observed_intensity'), doc="")

    @maximum_observed_intensity.setter
    def maximum_observed_intensity(self, val):
        val_maximum_observed_intensity = validateInteger(val, "maximum_observed_intensity", 0, 20, self.header_type)
        self._maximum_observed_intensity = val_maximum_observed_intensity

    maximum_intensity_qualifier = property(operator.attrgetter('_maximum_intensity_qualifier'), doc="")

    @maximum_intensity_qualifier.setter
    def maximum_intensity_qualifier(self, val):
        val_maximum_intensity_qualifier = validateString(val, "maximum_intensity_qualifier", 0, 1, "+- ", self.header_type)
        self._maximum_intensity_qualifier = val_maximum_intensity_qualifier

    intensity_scale = property(operator.attrgetter('_intensity_scale'), doc="")

    @intensity_scale.setter
    def intensity_scale(self, val):
        val_intensity_scale = validateString(val, "intensity_scale", 0, 2, ["MM", "RF", "CS", "SK", "M", "R", "C", "S"], self.header_type)
        self._intensity_scale = val_intensity_scale

    macroseismic_latitude = property(operator.attrgetter('_macroseismic_latitude'), doc="")

    @macroseismic_latitude.setter
    def macroseismic_latitude(self, val):
        val_macroseismic_latitude = validateFloat(val, "macroseismic_latitude", -90.0, 90.0, self.header_type)
        self._macroseismic_latitude = val_macroseismic_latitude

    macroseismic_longitude = property(operator.attrgetter('_macroseismic_longitude'), doc="")

    @macroseismic_longitude.setter
    def macroseismic_longitude(self, val):
        val_macroseismic_longitude = validateFloat(val, "macroseismic_longitude", -180.0, 180.0, self.header_type)
        self._macroseismic_longitude = val_macroseismic_longitude

    macroseismic_magnitude = property(operator.attrgetter('_macroseismic_magnitude'), doc="")

    @macroseismic_magnitude.setter
    def macroseismic_magnitude(self, val):
        val_macroseismic_magnitude = validateFloat(val, "macroseismic_magnitude", 0.0, 20.0, self.header_type)
        self._macroseismic_magnitude = val_macroseismic_magnitude

    type_of_magnitude = property(operator.attrgetter('_type_of_magnitude'), doc="")

    @type_of_magnitude.setter
    def type_of_magnitude(self, val):
        val_type_of_magnitude = validateString(val, "type_of_magnitude", 0, 1, "IAR*", self.header_type)
        self._type_of_magnitude = val_type_of_magnitude

    logarithm_of_radius = property(operator.attrgetter('_logarithm_of_radius'), doc="")

    @logarithm_of_radius.setter
    def logarithm_of_radius(self, val):
        val_logarithm_of_radius = validateFloat(val, "logarithm_of_radius", 0.0, 99.99, self.header_type)
        self._logarithm_of_radius = val_logarithm_of_radius

    logarithm_of_area_1 = property(operator.attrgetter('_logarithm_of_area_1'), doc="")

    @logarithm_of_area_1.setter
    def logarithm_of_area_1(self, val):
        val_logarithm_of_area_1 = validateFloat(val, "logarithm_of_area_1", 0.0, 99.99, self.header_type)
        self._logarithm_of_area_1 = val_logarithm_of_area_1

    bordering_intensity_1 = property(operator.attrgetter('_bordering_intensity_1'), doc="")

    @bordering_intensity_1.setter
    def bordering_intensity_1(self, val):
        val_bordering_intensity_1 = validateInteger(val, "bordering_intensity_1", 0, 99, self.header_type)
        self._bordering_intensity_1 = val_bordering_intensity_1

    logarithm_of_area_2 = property(operator.attrgetter('_logarithm_of_area_2'), doc="")

    @logarithm_of_area_2.setter
    def logarithm_of_area_2(self, val):
        val_logarithm_of_area_2 = validateFloat(val, "logarithm_of_area_2", 0.0, 99.99, self.header_type)
        self._logarithm_of_area_2 = val_logarithm_of_area_2

    bordering_intensity_2 = property(operator.attrgetter('_bordering_intensity_2'), doc="")

    @bordering_intensity_2.setter
    def bordering_intensity_2(self, val):
        val_bordering_intensity_2 = validateInteger(val, "bordering_intensity_2", 0, 99, self.header_type)
        self._bordering_intensity_2 = val_bordering_intensity_2

    quality_rank = property(operator.attrgetter('_quality_rank'), doc="")

    @quality_rank.setter
    def quality_rank(self, val):
        val_quality_rank = validateString(val, "quality_rank", 0, 1, "ABCD", self.header_type)
        self._quality_rank = val_quality_rank

    reporting_agency = property(operator.attrgetter('_reporting_agency'), doc="")

    @reporting_agency.setter
    def reporting_agency(self, val):
        val_reporting_agency = validateString(val, "reporting_agency", 3, 3, None, self.header_type)
        self._reporting_agency = val_reporting_agency

    def __str__(self):
        h_string = "     "

        h_string += addString2String(self.description, 15, '<')
        h_string += " "
        h_string += addString2String(self.diastrophism_code, 1, '>')
        h_string += addString2String(self.tsunami_code, 1, '>')
        h_string += addString2String(self.seiche_code, 1, '>')
        h_string += addString2String(self.cultural_effects, 1, '>')
        h_string += addString2String(self.unusual_effects, 1, '>')
        h_string += " "
        h_string += addInteger2String(self.maximum_observed_intensity, 2, '>')
        h_string += addString2String(self.maximum_intensity_qualifier, 1, '>')
        h_string += addString2String(self.intensity_scale, 2, '>')
        h_string += " "
        h_string += addFloat2String(self.macroseismic_latitude, 6, 2, '>')
        h_string += " "
        h_string += addFloat2String(self.macroseismic_longitude, 7, 2, '>')
        h_string += " "
        h_string += addFloat2String(self.macroseismic_magnitude, 3, 1, '>')
        h_string += addString2String(self.type_of_magnitude, 1, '>')
        h_string += addFloat2String(self.logarithm_of_radius, 4, 2, '>')
        h_string += addFloat2String(self.logarithm_of_area_1, 5, 2, '>')
        h_string += addInteger2String(self.bordering_intensity_1, 2, '>')
        h_string += addFloat2String(self.logarithm_of_area_2, 5 ,2 , '>')
        h_string += addInteger2String(self.bordering_intensity_2, 2, '>')
        h_string += " "
        h_string += addString2String(self.quality_rank, 1, '>')
        h_string += addString2String(self.reporting_agency, 3, '>')
        h_string += "    2"

        return h_string

    def getAsList(self):
        header_list = []
        header_list.append(self.description)
        header_list.append(self.diastrophism_code)
        header_list.append(self.tsunami_code)
        header_list.append(self.seiche_code)
        header_list.append(self.cultural_effects)
        header_list.append(self.unusual_effects)
        header_list.append(self.maximum_observed_intensity)
        header_list.append(self.maximum_intensity_qualifier)
        header_list.append(self.intensity_scale)
        header_list.append(self.macroseismic_latitude)
        header_list.append(self.macroseismic_longitude)
        header_list.append(self.macroseismic_magnitude)
        header_list.append(self.type_of_magnitude)
        header_list.append(self.logarithm_of_radius)
        header_list.append(self.logarithm_of_area_1)
        header_list.append(self.bordering_intensity_1)
        header_list.append(self.logarithm_of_area_2)
        header_list.append(self.bordering_intensity_2)
        header_list.append(self.quality_rank)
        header_list.append(self.reporting_agency)
        header_list.append(self.event_id)

        return header_list
