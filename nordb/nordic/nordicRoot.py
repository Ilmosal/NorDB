"""
This module contains the NordicRoot class and it's methods.

Functions and Classes
---------------------
"""

class NordicRoot:
    """
    NordicRoot class.
    """
    def __init__(self, root_id=-1, events = None):
        self.events = []
        self.root_id = root_id
        if events is not None:
            self.events = events

