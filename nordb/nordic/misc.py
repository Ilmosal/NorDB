"""
This module contains all miscellaneous classes that are too small to have their own modules

Functions and Classes
---------------------
"""
from datetime import datetime

class CreationInfo(object):
    """
    Class for containing basic creation info for a nordb entry.

    :ivar int c_id: database id of the CreationInfo entry
    :ivar datetime creation_date: datetime of the time of creation
    :ivar str owner: owner of the creationInfo entry
    :ivar str privacy: privacy level of the creationInfo object
    """
    def __init__(self, owner, c_id = -1, creation_date = datetime.now(), privacy = 'public', creation_comment = None):
        self.owner = owner
        self.c_id = c_id
        self.creation_date = creation_date
        self.privacy = privacy
        self.creation_comment = creation_comment

class Magnitude(object):
    """
    A magnitude wrapper class for the NordicEvent. Does not modify the actual value inside the NordicEvent. Can be cast into float with float()

    :ivar float val: the magnitude as a float
    :ivar str magnitude_type: type of the magnitude as described in the NordicMain class
    :ivar str reporting_agency: reporting agency of the event
    :ivar float error: Error in the magnitude va Error in the magnitude value
    """
    def __init__(self, val, mtype, reporting_agency, error = 0.0):
        self.val = val
        self.magnitude_type = mtype
        self.reporting_agency = reporting_agency
        self.error = error

    def __float__(self):
        return self.val

class Coordinate(object):
    """
    A wrapper class for coordinates fro the NordicEvent. Does not modify the actual value inside the NordicEvent. Can be cast into float with float()

    :ivar float val: latitude or longitude of the event in degrees
    :ivar float error: latitude or longitude error of the value 
    """
    def __init__(self, val, error = 0.0):
        self.val = val
        self.error = error

    def __float__(self):
        return self.val

class Depth(object):
    """
    A wrapper class for depth for the NordicEvent. Does not modify the actual value inside the NordicEvent. Can be cast into float with float()

    :ivar float val: depth of the event in kilometers
    :ivar float error: depth error of the value
    """
    def __init__(self, val, depth_control, error = 0.0):
        self.val = val
        self.depth_control = depth_control
        self.error = error

    def __float__(self):
        return self.val

class OriginTime(object):
    """
    A wrapper class for origin_time for the NordicEvent. Does not modify the actual value inside the NordicEvent. Can be cast into datetime with datetime()

    :ivar datetime val: origin time as a datetime
    :ivar float error: error value of origin time in seconds
    """
    def __init__(self, val, error = 0.0):
        self.val = val
        self.error = error

    def __datetime__(self):
        return self.val

    def __str__(self):
        return str(self.val)
