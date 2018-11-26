"""
Contains information relevant to NordicData header
"""

import operator

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDatetime
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String

class NordicData:
    """
    A class that functions as a collection of enums. Contains the information of the phase data line of a nordic file.

    :param list data: The data of a nordic phase in a list where each index of a value corresponds to NordicData's pseudo-enum. The data easily accessed with the enums provided by the class
    :ivar string station_code: Code of the station. Maximum of 4 characters
    :ivar string sp_instrument_type: instrument type(S, B or L)
    :ivar string sp_component: Component of the observation(Z, N or E)
    :ivar string quality_indicator: Quality of the observation(I, E, etc.)
    :ivar string phase_type: Phase type. (PG, SG, PN, etc). Maximum of 4 characters
    :ivar int weight: Weighting indicator(1-4). 0=full weight as Hypocenter program, 9=timing error
    :ivar string first_motion: First motion of the observation(C/D for clear compression/dilatation, +/- for unclear compression/dilatation).
    :ivar observation_time datetime: Datetime of the pick
    :ivar int signal_duration:  duration of the signal from phase onset to noise as seconds
    :ivar float max_amplitude: Maximum amplitude from zero to peak ground motion amplitude.
    :ivar float max_amplitude_period: Period of the maximum amplitude
    :ivar float back_azimuth: back azimuth of the observation as degrees
    :ivar float apparent_velocity: Apparent velocity of the observation  (km/s)
    :ivar float signal_to_noise: signal to noise ration of the observation
    :ivar int azimuth_residual: Azimuth residual of the observation in deg
    :ivar float travel_time_residual: travel time residual of the observation in sec
    :ivar int location_weight: Actual weight used for location
    :ivar int epicenter_distance: Distance from epicenter to observation in km
    :ivar int epicenter_to_station_azimuth: Epicenter-to-station azimuth as deg
    :ivar int event_id: id of the event to which this nordic Data is related to
    :ivar int d_id: id of the NordicData in the database
    :ivar int header_type: This value tells that this is a NordicData object. Value of 7
    :ivar int STATION_CODE: Location of the station_code in a array. Value of 0
    :ivar int SP_INSTRUMENT_TYPE: Location of the sp_instrument_type in a array. Value of 1
    :ivar int SP_COMPONENT: Location of the sp_component in a array. Value of 2
    :ivar int QUALITY_INDICATOR: Location of the quality_indicator in a array. Value of 3
    :ivar int PHASE_TYPE: Location of the phase_type in a array. Value of 4
    :ivar int WEIGHT: Location of the weight in a array. Value of 5
    :ivar int FIRST_MOTION: Location of the first_motion in a array. Value of 6
    :ivar int OBSEVATION_TIME: Location of the observation_time in a array. Value of 7
    :ivar int SIGNAL_DURATION: Location of the signal_duration in a array. Value of 8
    :ivar int MAX_AMPLITUDE: Location of the max_amplitude in a array. Value of 9
    :ivar int MAX_AMPLITUDE_PERIOD: Location of the max_amplitude_period in a array. Value of 10
    :ivar int BACK_AZIMUTH: Location of the back_azimuth in a array. Value of 11
    :ivar int APPARENT_VELOCITY: Location of the apparent_velocity in a array. Value of 12
    :ivar int SIGNAL_TO_NOISE: Location of the signal_to_noise in a array. Value of 13
    :ivar int AZIMUTH_RESIDUAL: Location of the azimuth_residual in a array. Value of 14
    :ivar int TRAVEL_TIME_RESIDUAL: Location of the travel_time_residual in a array. Value of 15
    :ivar int LOCATION_WEIGHT: Location of the location_weight in a array. Value of 16
    :ivar int EPICENTER_DISTANCE: Location of the epicenter_distance in a array. Value of 17
    :ivar int EPICENTER_TO_STATION_AZIMUTH: Location of the epicenter_to_station_azimuth in a array. Value of 18
    :ivar int EVENT_ID: Location of the event_id in a array. Value of 19
    :ivar int D_ID: Location of the d_id in a array. Value of 20
    """
    header_type = 8
    STATION_CODE = 0
    SP_INSTRUMENT_TYPE = 1
    SP_COMPONENT = 2
    QUALITY_INDICATOR = 3
    PHASE_TYPE = 4
    WEIGHT = 5
    FIRST_MOTION = 6
    OBSERVATION_TIME = 7
    SIGNAL_DURATION = 8
    MAX_AMPLITUDE = 9
    MAX_AMPLITUDE_PERIOD = 10
    BACK_AZIMUTH = 11
    APPARENT_VELOCITY = 12
    SIGNAL_TO_NOISE = 13
    AZIMUTH_RESIDUAL = 14
    TRAVEL_TIME_RESIDUAL = 15
    LOCATION_WEIGHT = 16
    EPICENTER_DISTANCE = 17
    EPICENTER_TO_STATION_AZIMUTH = 18
    EVENT_ID = 19
    D_ID = 20

    def __init__(self, data=None):
        if data is None:
            self.station_code = None
            self.sp_instrument_type = None
            self.sp_component = None
            self.quality_indicator = None
            self.phase_type = None
            self.weight = None
            self.first_motion = None
            self.observation_time = None
            self.signal_duration = None
            self.max_amplitude = None
            self.max_amplitude_period = None
            self.back_azimuth = None
            self.apparent_velocity = None
            self.signal_to_noise = None
            self.azimuth_residual = None
            self.travel_time_residual = None
            self.location_weight = None
            self.epicenter_distance = None
            self.epicenter_to_station_azimuth = None
            self.event_id = -1
            self.d_id = -1
        else:
            self.station_code = data[self.STATION_CODE]
            self.sp_instrument_type = data[self.SP_INSTRUMENT_TYPE]
            self.sp_component = data[self.SP_COMPONENT]
            self.quality_indicator = data[self.QUALITY_INDICATOR]
            self.phase_type = data[self.PHASE_TYPE]
            self.weight = data[self.WEIGHT]
            self.first_motion = data[self.FIRST_MOTION]
            self.observation_time = data[self.OBSERVATION_TIME]
            self.signal_duration = data[self.SIGNAL_DURATION]
            self.max_amplitude = data[self.MAX_AMPLITUDE]
            self.max_amplitude_period = data[self.MAX_AMPLITUDE_PERIOD]
            self.back_azimuth = data[self.BACK_AZIMUTH]
            self.apparent_velocity = data[self.APPARENT_VELOCITY]
            self.signal_to_noise = data[self.SIGNAL_TO_NOISE]
            self.azimuth_residual = data[self.AZIMUTH_RESIDUAL]
            self.travel_time_residual = data[self.TRAVEL_TIME_RESIDUAL]
            self.location_weight = data[self.LOCATION_WEIGHT]
            self.epicenter_distance = data[self.EPICENTER_DISTANCE]
            self.epicenter_to_station_azimuth = data[self.EPICENTER_TO_STATION_AZIMUTH]
            self.event_id = data[self.EVENT_ID]
            self.d_id = data[self.D_ID]

    station_code = property(operator.attrgetter('_station_code'), doc="")

    @station_code.setter
    def station_code(self, val):
        val_station_code = validateString(val, "station_code", 0, 4, None, self.header_type)
        self._station_code = val_station_code

    sp_instrument_type = property(operator.attrgetter('_sp_instrument_type'), doc="")

    @sp_instrument_type.setter
    def sp_instrument_type(self, val):
        val_sp_instrument_type = validateString(val, "sp_instrument_type", 0, 1, "LSBHEPD", self.header_type)
        self._sp_instrument_type = val_sp_instrument_type

    sp_component = property(operator.attrgetter('_sp_component'), doc="")

    @sp_component.setter
    def sp_component(self, val):
        val_sp_component = validateString(val, "sp_component", 0, 1, "ZNEH12VRTP", self.header_type)
        self._sp_component = val_sp_component

    quality_indicator = property(operator.attrgetter('_quality_indicator'), doc="")

    @quality_indicator.setter
    def quality_indicator(self, val):
        val_quality_indicator = validateString(val, "quality_indicator", 0, 1, None, self.header_type)
        self._quality_indicator = val_quality_indicator

    phase_type = property(operator.attrgetter('_phase_type'), doc="")

    @phase_type.setter
    def phase_type(self, val):
        val_phase_type = validateString(val, "phase_type", 0, 4, None, self.header_type)
        self._phase_type = val_phase_type

    weight = property(operator.attrgetter('_weight'), doc="")

    @weight.setter
    def weight(self, val):
        val_weight = validateInteger(val, "weight", 0, 9, self.header_type)
        self._weight = val_weight

    first_motion = property(operator.attrgetter('_first_motion'), doc="")

    @first_motion.setter
    def first_motion(self, val):
        val_first_motion = validateString(val, "first_motion", 0, 1, "+-DC", self.header_type)
        self._first_motion = val_first_motion

    observation_time = property(operator.attrgetter('_observation_time'), doc="")

    @observation_time.setter
    def observation_time(self, val):
        val_observation_time = validateDatetime(val, "observation_time", self.header_type)
        self._observation_time = val_observation_time

    signal_duration = property(operator.attrgetter('_signal_duration'), doc="")

    @signal_duration.setter
    def signal_duration(self, val):
        val_signal_duration = validateInteger(val, "signal_duration", 0, 9999, self.header_type)
        self._signal_duration = val_signal_duration

    max_amplitude = property(operator.attrgetter('_max_amplitude'), doc="")

    @max_amplitude.setter
    def max_amplitude(self, val):
        val_max_amplitude = validateFloat(val, "max_amplitude", -1.0, 9999.9, self.header_type)
        self._max_amplitude = val_max_amplitude

    max_amplitude_period = property(operator.attrgetter('_max_amplitude_period'), doc="")

    @max_amplitude_period.setter
    def max_amplitude_period(self, val):
        val_max_amplitude_period = validateFloat(val, "max_amplitude_period", -1.0, 99.9, self.header_type)
        self._max_amplitude_period = val_max_amplitude_period

    back_azimuth = property(operator.attrgetter('_back_azimuth'), doc="")

    @back_azimuth.setter
    def back_azimuth(self, val):
        val_back_azimuth = validateFloat(val, "back_azimuth", 0.0, 359.9, self.header_type)
        self._back_azimuth = val_back_azimuth

    apparent_velocity = property(operator.attrgetter('_apparent_velocity'), doc="")

    @apparent_velocity.setter
    def apparent_velocity(self, val):
        val_apparent_velocity = validateFloat(val, "apparent_velocity", 0.0, 99.9, self.header_type)
        self._apparent_velocity = val_apparent_velocity

    signal_to_noise = property(operator.attrgetter('_signal_to_noise'), doc="")

    @signal_to_noise.setter
    def signal_to_noise(self, val):
        val_signal_to_noise = validateFloat(val, "signal_to_noise", 0.0, 99.9, self.header_type)
        self._signal_to_noise = val_signal_to_noise

    azimuth_residual = property(operator.attrgetter('_azimuth_residual'), doc="")

    @azimuth_residual.setter
    def azimuth_residual(self, val):
        val_azimuth_residual = validateInteger(val, "azimuth_residual", -99, 999, self.header_type)
        self._azimuth_residual = val_azimuth_residual

    travel_time_residual = property(operator.attrgetter('_travel_time_residual'), doc="")

    @travel_time_residual.setter
    def travel_time_residual(self, val):
        val_travel_time_residual = validateFloat(val, "travel_time_residual", -999.9, 9999.9, self.header_type)
        self._travel_time_residual = val_travel_time_residual

    location_weight = property(operator.attrgetter('_location_weight'), doc="")

    @location_weight.setter
    def location_weight(self, val):
        val_location_weight = validateInteger(val, "location_weight", 0, 10, self.header_type)
        self._location_weight = val_location_weight

    epicenter_distance = property(operator.attrgetter('_epicenter_distance'), doc="")

    @epicenter_distance.setter
    def epicenter_distance(self, val):
        val_epicenter_distance = validateInteger(val, "epicenter_distance", 0, 99999, self.header_type)
        self._epicenter_distance = val_epicenter_distance

    epicenter_to_station_azimuth = property(operator.attrgetter('_epicenter_to_station_azimuth'), doc="")

    @epicenter_to_station_azimuth.setter
    def epicenter_to_station_azimuth(self, val):
        val_epicenter_to_station_azimuth = validateInteger(val, "epicenter_to_station_azimuth", 0, 359, self.header_type)
        self._epicenter_to_station_azimuth = val_epicenter_to_station_azimuth

    def __str__(self):
        phase_string = " "
        phase_string += addString2String(self.station_code, 4, '<')
        phase_string += " "
        phase_string += addString2String(self.sp_instrument_type, 1, '<')
        phase_string += addString2String(self.sp_component, 1, '<')
        phase_string += " "
        phase_string += addString2String(self.quality_indicator, 1, '<')
        phase_string += addString2String(self.phase_type, 4, '<')
        phase_string += addInteger2String(self.weight, 1, '<')
        phase_string += " "
        phase_string += addString2String(self.first_motion, 1, '<')
        phase_string += " "
        phase_string += addInteger2String(self.observation_time.hour, 2, '0')
        phase_string += addInteger2String(self.observation_time.minute, 2, '0')
        phase_string += " "
        second = float(self.observation_time.second) + float(self.observation_time.microsecond)/1000000
        phase_string += addFloat2String(second, 5, 2, '0')
        phase_string += " "
        phase_string += addInteger2String(self.signal_duration, 4, '>')
        phase_string += " "
        phase_string += addFloat2String(self.max_amplitude, 6, 1, '>')
        phase_string += " "
        phase_string += addFloat2String(self.max_amplitude_period, 4, 2, '<')
        phase_string += " "
        phase_string += addFloat2String(self.back_azimuth, 5, 1, '>')
        phase_string += " "
        phase_string += addFloat2String(self.apparent_velocity, 4, 1, '>')
        phase_string += addFloat2String(self.signal_to_noise, 4, 1, '>')
        phase_string += addInteger2String(self.azimuth_residual, 3, '>')
        phase_string += addFloat2String(self.travel_time_residual, 5, 1, '>')
        phase_string += addInteger2String(self.location_weight, 2, '>')
        phase_string += addInteger2String(self.epicenter_distance, 5, '>')
        phase_string += " "
        phase_string += addInteger2String(self.epicenter_to_station_azimuth, 3, '>')
        phase_string += " "

        return phase_string

    def getAsList(self):
        data_list = []
        data_list.append(self.station_code)
        data_list.append(self.sp_instrument_type)
        data_list.append(self.sp_component)
        data_list.append(self.quality_indicator)
        data_list.append(self.phase_type)
        data_list.append(self.weight)
        data_list.append(self.first_motion)
        data_list.append(self.observation_time)
        data_list.append(self.signal_duration)
        data_list.append(self.max_amplitude)
        data_list.append(self.max_amplitude_period)
        data_list.append(self.back_azimuth)
        data_list.append(self.apparent_velocity)
        data_list.append(self.signal_to_noise)
        data_list.append(self.azimuth_residual)
        data_list.append(self.travel_time_residual)
        data_list.append(self.location_weight)
        data_list.append(self.epicenter_distance)
        data_list.append(self.epicenter_to_station_azimuth)
        data_list.append(self.event_id)

        return data_list

