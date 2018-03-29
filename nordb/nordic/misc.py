"""
This module contains all miscellaneous classes that are too small to have their own modules

Functions and Classes
---------------------
"""

class Magnitude(object):
    """
    A magnitude wrapper class for the NordicEvent. Does not modify the actual value inside the NordicEvent
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
    A wrapper class for coordinates fro the NordicEvent. Does not modify the actual value inside the NordicEvent
    """
    def __init__(self, val, error = 0.0):
        self.val = val
        self.error = error

    def __float__(self):
        return self.val

class Depth(object):
    """
    A wrapper class for depth for the NordicEvent. Does not modify the actual value inside the NordicEvent
    """
    def __init__(self, val, depth_control, error = 0.0):
        self.val = val
        self.depth_control = depth_control
        self.error = error

    def __float__(self):
        return self.val

class OriginTime(object):
    """
    A wrapper class for origin_time for the NordicEvent. Does not modify the actual value inside the NordicEvent
    """
    def __init__(self, val, error = 0.0):
        self.val = val
        self.error = error

    def __float__(self):
        return self.val

