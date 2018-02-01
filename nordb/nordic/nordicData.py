"""
Contains information relevant to NordicData header
"""

import operator

from nordb.core.validationTools import validateFloat
from nordb.core.validationTools import validateInteger
from nordb.core.validationTools import validateString
from nordb.core.validationTools import validateDate
from nordb.core.utils import addString2String
from nordb.core.utils import addInteger2String
from nordb.core.utils import addFloat2String

class NordicData:
    """
    A class that functions as a collection of enums. Contains the information of the phase data line of a nordic file. 
    :ivar list data: The data of a nordic phase in a list where each index of a value corresponds to NordicData's pseudo-enum. The data easily accessed with the enums provided by the class
    :ivar int header_type: This value tells that this is a NordicData object Value of 7
    :ivar int STATION_CODE: The location of the station id. Value of 0
    :ivar int SP_INSTRUMENT_TYPE: The location of the type of the instrument that observed the event. Value of 1
    :ivar int SP_COMPONENT: The location of the component of the observation. Value of 2
    :ivar int QUALITY_INDICATOR: The location of the quality of the observation. Value of 3 
    :ivar int PHASE_TYPE: The location of the type of the phase observed. Value of 4
    :ivar int WEIGHT: The location of the weight value. Value of 5
    :ivar int FIRST_MOTION: The location of the direction of the first motion. Value of 6
    :ivar int TIME_INFO: The location of the information on which day the event was observed relative the the day it actually happened. Value of 7
    :ivar int HOUR: The location of the hour time of the observation. Value of 8
    :ivar int MINUTE: The location of the minute time of the observation.  Value of 9 
    :ivar int SECOND: The location of the second time of the observation.Value of 10
    :ivar int SIGNAL_DURATION: The location of the signal duration of the observation. Value of 11
    :ivar int MAX_AMPLITUDE: The location of the maximum amplitude of the observation. Value of 12 
    :ivar int MAX_AMPLITUDE_PERIOD: The location of the maximum amplitude period of the observation. Value of 13
    :ivar int BACK_AZIMUTH: The location of the back azimuth of the observation. Value of 14
    :ivar int APPARENT_VELOCITY: The location of the apparent velocity of the observation. Value of 15
    :ivar int SIGNAL_TO_NOISE: The location of the signal to noise ratio of the observation. Value of 16
    :ivar int AZIMUTH_RESIDUAL: The location of the azimuth residual of the observation. Value of 17
    :ivar int TRAVEL_TIME_RESIDUAL: The location of the travel time residual of the observation. Value of 18
    :ivar int LOCATION_WEIGHT: The location of the actual weight of the observation. Value of 19
    :ivar int EPICENTER_DISTANCE: The location of the epicenter distance of the observation. Value of 20
    :ivar int EPICENTER_TO_STATION_AZIMUTH: The location of the epicenter to station azimuth of the observation. Value of 21
    :ivar int EVENT_ID: The location of the event id of the observation. Value of 22
    :ivar int D_ID: The location of the id of the observation. Value of 23
    """
    header_type = 8
    STATION_CODE = 0
    SP_INSTRUMENT_TYPE = 1
    SP_COMPONENT = 2
    QUALITY_INDICATOR = 3 
    PHASE_TYPE = 4
    WEIGHT = 5
    FIRST_MOTION = 6
    TIME_INFO = 7
    HOUR = 8
    MINUTE = 9 
    SECOND = 10
    SIGNAL_DURATION = 11
    MAX_AMPLITUDE = 12 
    MAX_AMPLITUDE_PERIOD = 13
    BACK_AZIMUTH = 14
    APPARENT_VELOCITY = 15
    SIGNAL_TO_NOISE = 16
    AZIMUTH_RESIDUAL = 17
    TRAVEL_TIME_RESIDUAL = 18
    LOCATION_WEIGHT = 19
    EPICENTER_DISTANCE = 20
    EPICENTER_TO_STATION_AZIMUTH = 21
    EVENT_ID = 22
    D_ID = 23

    def __init__(self, data):
        self.station_code = data[self.STATION_CODE]
        self.sp_instrument_type = data[self.SP_INSTRUMENT_TYPE]
        self.sp_component = data[self.SP_COMPONENT]
        self.quality_indicator = data[self.QUALITY_INDICATOR]
        self.phase_type = data[self.PHASE_TYPE]
        self.weight = data[self.WEIGHT]
        self.first_motion = data[self.FIRST_MOTION]
        self.time_info = data[self.TIME_INFO]
        self.hour = data[self.HOUR]
        self.minute = data[self.MINUTE]
        self.second = data[self.SECOND]
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

    station_code = property(operator.attrgetter('_station_code'))

    @station_code.setter
    def station_code(self, val):
        val_station_code = validateString(val, "station_code", 0, 4, "", False, self.header_type)
        self._station_code = val_station_code

    sp_instrument_type = property(operator.attrgetter('_sp_instrument_type'))
    
    @sp_instrument_type.setter
    def sp_instrument_type(self, val):
        val_sp_instrument_type = validateString(val, "sp_instrument_type", 0, 1, "LSBHE", True, self.header_type)
        self._sp_instrument_type = val_sp_instrument_type

    sp_component = property(operator.attrgetter('_sp_component'))
    
    @sp_component.setter
    def sp_component(self, val):
        val_sp_component = validateString(val, "sp_component", 0, 1, "ZNEH12VRT", True, self.header_type)
        self._sp_component = val_sp_component

    quality_indicator = property(operator.attrgetter('_quality_indicator'))
    
    @quality_indicator.setter
    def quality_indicator(self, val):
        val_quality_indicator = validateString(val, "quality_indicator", 0, 1, "", False, self.header_type)
        self._quality_indicator = val_quality_indicator

    phase_type = property(operator.attrgetter('_phase_type'))
    
    @phase_type.setter
    def phase_type(self, val):
        val_phase_type = validateString(val, "phase_type", 0, 4, "", False, self.header_type)
        self._phase_type = val_phase_type

    weight = property(operator.attrgetter('_weight'))
    
    @weight.setter
    def weight(self, val):
        val_weight = validateInteger(val, "weight", 0, 9, True, self.header_type)
        self._weight = val_weight

    first_motion = property(operator.attrgetter('_first_motion'))
    
    @first_motion.setter
    def first_motion(self, val):
        val_first_motion = validateString(val, "first_motion", 0, 1, "CD+- ", True, self.header_type)
        self._first_motion = val_first_motion

    time_info = property(operator.attrgetter('_time_info'))
    
    @time_info.setter
    def time_info(self, val):
        val_time_info = validateString(val, "time_info", 0, 1, "-+ ", True, self.header_type)
        self._time_info = val_time_info

    hour = property(operator.attrgetter('_hour'))
    
    @hour.setter
    def hour(self, val):
        val_hour = validateInteger(val, "hour", 0, 23, True, self.header_type)
        self._hour = val_hour

    minute = property(operator.attrgetter('_minute'))
    
    @minute.setter
    def minute(self, val):
        val_minute = validateInteger(val, "minute", 0, 59, True, self.header_type)
        self._minute = val_minute

    second = property(operator.attrgetter('_second'))
    
    @second.setter
    def second(self, val):
        val_second = validateFloat(val, "second", 0.0, 59.99, True, self.header_type)
        self._second = val_second

    signal_duration = property(operator.attrgetter('_signal_duration'))
    
    @signal_duration.setter
    def signal_duration(self, val):
        val_signal_duration = validateInteger(val, "signal_duration", 0, 9999, True, self.header_type)
        self._signal_duration = val_signal_duration

    max_amplitude = property(operator.attrgetter('_max_amplitude'))
    
    @max_amplitude.setter
    def max_amplitude(self, val):
        val_max_amplitude = validateFloat(val, "max_amplitude", -1.0, 9999.9, True, self.header_type)
        self._max_amplitude = val_max_amplitude

    max_amplitude_period = property(operator.attrgetter('_max_amplitude_period'))
    
    @max_amplitude_period.setter
    def max_amplitude_period(self, val):
        val_max_amplitude_period = validateFloat(val, "max_amplitude_period", -1.0, 99.9, True, self.header_type)
        self._max_amplitude_period = val_max_amplitude_period

    back_azimuth = property(operator.attrgetter('_back_azimuth'))
    
    @back_azimuth.setter
    def back_azimuth(self, val):
        val_back_azimuth = validateFloat(val, "back_azimuth", 0.0, 359.9, True, self.header_type)
        self._back_azimuth = val_back_azimuth

    apparent_velocity = property(operator.attrgetter('_apparent_velocity'))
    
    @apparent_velocity.setter
    def apparent_velocity(self, val):
        val_apparent_velocity = validateFloat(val, "apparent_velocity", 0.0, 99.9, True, self.header_type)
        self._apparent_velocity = val_apparent_velocity

    signal_to_noise = property(operator.attrgetter('_signal_to_noise'))
    
    @signal_to_noise.setter
    def signal_to_noise(self, val):
        val_signal_to_noise = validateFloat(val, "signal_to_noise", 0.0, 99.9, True, self.header_type)
        self._signal_to_noise = val_signal_to_noise

    azimuth_residual = property(operator.attrgetter('_azimuth_residual'))
    
    @azimuth_residual.setter
    def azimuth_residual(self, val):
        val_azimuth_residual = validateInteger(val, "azimuth_residual", -99, 999, True, self.header_type)
        self._azimuth_residual = val_azimuth_residual

    travel_time_residual = property(operator.attrgetter('_travel_time_residual'))
    
    @travel_time_residual.setter
    def travel_time_residual(self, val):
        val_travel_time_residual = validateFloat(val, "travel_time_residual", -999.9, 9999.9, True, self.header_type)
        self._travel_time_residual = val_travel_time_residual

    location_weight = property(operator.attrgetter('_location_weight'))
    
    @location_weight.setter
    def location_weight(self, val):
        val_location_weight = validateInteger(val, "location_weight", 0, 10, True, self.header_type)
        self._location_weight = val_location_weight

    epicenter_distance = property(operator.attrgetter('_epicenter_distance'))
    
    @epicenter_distance.setter
    def epicenter_distance(self, val):
        val_epicenter_distance = validateInteger(val, "epicenter_distance", 0, 99999, True, self.header_type)
        self._epicenter_distance = val_epicenter_distance

    epicenter_to_station_azimuth = property(operator.attrgetter('_epicenter_to_station_azimuth'))
    
    @epicenter_to_station_azimuth.setter
    def epicenter_to_station_azimuth(self, val):
        val_epicenter_to_station_azimuth = validateInteger(val, "epicenter_to_station_azimuth", 0, 359, True, self.header_type)
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
        phase_string += addString2String(self.time_info, 1, '<')
        phase_string += addInteger2String(self.hour, 2, '0')
        phase_string += addInteger2String(self.minute, 2, '0')
        phase_string += " "
        phase_string += addFloat2String(self.second, 5, 2, '0')
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
        data_list.append(self.time_info)
        data_list.append(self.hour)
        data_list.append(self.minute)
        data_list.append(self.second)
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

