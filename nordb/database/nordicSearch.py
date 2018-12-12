"""
This module contains all commands for searching the database for events with given criteria. The most important function here is searchNordic and most other functions and classes are here just to support it.

Functions and Classes
---------------------
"""
import numpy as np
from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import time
from nordb.core import usernameUtilities
from nordb.database import sql2nordic

SEARCH_TYPES = {
                    "origin_date":[date],
                    "origin_time":[time],
                    "epicenter_latitude":[float],
                    "epicenter_longitude":[float],
                    "magnitude_1":[float],
                    "solution_type":[str],
                    "distance_indicator":[str],
                    "event_desc_id":[str],
                    "event_id":[int],
                    "depth":[float]
               }

SEARCH_TYPE_HEADERS =   {
                            "origin_time":"nordic_header_main",
                            "origin_date":"nordic_header_main",
                            "epicenter_latitude":"nordic_header_main",
                            "epicenter_longitude":"nordic_header_main",
                            "magnitude_1":"nordic_header_main",
                            "solution_type":"nordic_event",
                            "distance_indicator":"nordic_header_main",
                            "event_desc_id":"nordic_header_main",
                            "event_id":"nordic_header_main",
                            "depth":"nordic_header_main"
                        }

class NordicSearch:
    """
    Class for searching events from database with multiple criteria.
    """
    def __init__(self):
        self.criteria = []

    def getCriteriaString(self):
        """
        Get all criteria in a formatted string for printing purposes.
        """
        criteria_string = ""
        for crit in self.criteria:
            if crit.command_type == 1:
               criteria_string += " {0}: {1}\n".format(crit.search_type, crit.getValue()[0])
            elif crit.command_type == 2:
               criteria_string += " {0}: {1}-{2}\n".format(crit.search_type, crit.getValue()[0], crit.getValue()[1])
            elif crit.command_type == 3:
               criteria_string += " {0}: {1}-> \n".format(crit.search_type, crit.getValue()[0])
            else:
               criteria_string += " {0}: <-{1} \n".format(crit.search_type, crit.getValue()[0])

        return criteria_string

    def getCriteriaAmount(self):
        """
        Return the amount of criteria in the NordicSearch
        """
        return len(self.criteria)

    def clear(self):
        """
        Clear all criteria from NordicSearch object
        """
        self.criteria = []

    def addSearchExactly(self, search_type, search_val):
        """
        Add SearchExactly criteria to the NordicSearch object.

        :param str search_type:
        :param int,float,datetime,str search_val: Value to which the search type will be compared to
        """
        self.criteria.append(ExactlyValue(search_type, search_val))

    def addSearchBetween(self, search_type, search_val_low, search_val_upp):
        """
        Add SearchBetween criteria to the NordicSearch object.

        :param str search_type:
        :param int,float,datetime,str search_val_low: Lower value to which the search type will be compared to
        :param int,float,datetime,str search_val_upp: Upper value to which the search type will be compared to
        """
        self.criteria.append(BetweenValues(search_type, search_val_low, search_val_upp))

    def addSearchOver(self, search_type, search_val):
        """
        Add SearchOver criteria to the NordicSearch object.

        :param str search_type:
        :param int,float,datetime,str search_val: Value to which the search type will be compared to
        """
        self.criteria.append(OverValue(search_type, search_val))

    def addSearchUnder(self, search_type, search_val):
        """
        Add SearchUnder criteria to the NordicSearch object.

        :param str search_type:
        :param int,float,datetime,str search_val: Value to which the search type will be compared to
        """
        self.criteria.append(UnderValue(search_type, search_val))

    def getSearchQueryAndValues(self):
        query_str = ""
        query_vals = []
        for query in self.criteria:
            query_str += "AND " + query.getQuery()
            query_vals.extend(query.getValue())

        return query_str, query_vals

    def searchEventIdAndDate(self, db_conn = None):
        """
        Search for all event ids and their dates that fit to the criteria given to the NordicSearch and return them

        :returns: a list of event_ids and dates
        """
        if db_conn is None:
            conn = usernameUtilities.log2nordb()
        else:
            conn = db_conn
        events = []
        query = (   "SELECT "
                    "   id, origin_date, origin_time "
                    "FROM "
                    "   (SELECT "
                    "       DISTINCT ON (nordic_event.id) nordic_event.id AS id, "
                    "       nordic_header_main.origin_time AS origin_time, "
                    "       nordic_header_main.origin_date AS origin_date, "
                    "       nordic_event.root_id AS root_id "
                    "   FROM "
                    "       nordic_event, nordic_header_main "
                    "   WHERE "
                    "       nordic_event.id = nordic_header_main.event_id "
                )
        query_str, query_vals = self.getSearchQueryAndValues()
        query += query_str

        query += ") AS subq ORDER BY root_id"

        cur = conn.cursor()

        cur.execute(query, query_vals)
        ans = cur.fetchall()

        if db_conn is None:
            conn.close()

        if len(ans) == 0:
            return []

        return ans

    def searchEvents(self, db_conn = None):
        """
        Search for all the events that fit to the criteria given to the NordicSearch and return them.

        :returns: array of NordicEvent objects
        """
        if db_conn is None:
            conn = usernameUtilities.log2nordb()
        else:
            conn = db_conn
        event_ids = self.searchEventIds(db_conn = conn)
        events = sql2nordic.getNordic(event_ids, db_conn = conn)

        if db_conn is None:
            conn.close()

        return events

    def searchEventIds(self, db_conn = None):
        """
        Search for all event ids that fit to the criteria given to the NordicSearch and return them.

        :returns: a list of event ids
        """
        event_ids = []
        temp = self.searchEventIdAndDate(db_conn=db_conn)
        return [temp[i][0] for i in range(len(temp))]

    def searchEventRoots(self, db_conn = None):
        """
        Search for event root ids that have events that fit to the criteria given to the NordicSearch and return them.
        :returns: a list of event root ids
        """
        if db_conn is None:
            conn = usernameUtilities.log2nordb()
        else:
            conn = db_conn

        root_ids = []

        query = (
                "SELECT "
                "   DISTINCT nordic_event.root_id "
                "FROM "
                "   nordic_event, nordic_header_main "
                "WHERE "
                "   nordic_event.id = nordic_header_main.event_id "
                )

        query_str, query_vals = self.getSearchQueryAndValues()
        query += query_str

        ans = None
        conn = usernameUtilities.log2nordb()
        cur = conn.cursor()

        cur.execute(query, query_vals)
        ans = cur.fetchall()

        if db_conn is None:
            conn.close()

        return ans

class Command:
    """
    Class for command that is returned by string2Command.

    :ivar int command_type: Type of command.
    """
    def __init__(self, command_type, search_type):
        if search_type not in SEARCH_TYPES.keys():
            raise Exception("Not a valid search type! ({0})".format(search_type))

        if command_type != 1:
            if search_type in ["solution_type", "distance_indicator", "event_desc_id"]:
                raise Exception("Cannot search between string values! ({0})".format(search_type))

        self.command_type = command_type
        self.search_type = search_type

    def getQuery(self):
        """
        Functiong for creating the query for the command
        """
        return None

    def getValue(self):
        return None

    def createQuery(self, value):
        search_criteria = "{0}.{1}".format(SEARCH_TYPE_HEADERS[self.search_type], self.search_type)

        if self.command_type == 1:
            return "    {0} = %s ".format(search_criteria)
        elif self.command_type == 2:
            return "    {0} >= %s AND {0} <= %s ".format(search_criteria)
        elif self.command_type == 3:
            return "    {0} >= %s ".format(search_criteria)
        elif self.command_type == 4:
            return "    {0} <= %s ".format(search_criteria)

class ExactlyValue(Command):
    """
    Command for determining if the value is exactly the given value.

    :ivar int command_tpe: Type of command. Initial value: 1
    :ivar int,float,datetime value: Value that all other values will be compared to. Can be of any type. Initial value: value
    """
    def __init__(self, search_type, value):
        Command.__init__(self, 1, search_type)
        if type(value) not in SEARCH_TYPES[search_type]:
            raise Exception("Given search value is not a correct type! (Given: {0}, Required: {1})".format(type(value), SEARCH_TYPES[search_type]))
        self.value = value

    def getQuery(self):
        return self.createQuery(self.value)

    def getValue(self):
        return (self.value,)

class BetweenValues(Command):
    """
    Command for determining if a value falls exactly between the given values.

    :ivar int command_tpe: Type of command. In this case 2.
    :ivar int,float,datetime valueLower: value of the lower limit of the comparison
    :ivar int,float,datetime valueUpper: value for the upper limit of the comparison
    """
    def __init__(self, search_type, value_lower, value_upper):
        Command.__init__(self, 2, search_type)
        if type(value_lower) not in SEARCH_TYPES[search_type]:
            raise Exception("Given lower search value is not a correct type! (Given: {0}, Required: {1})".format(type(value_lower), SEARCH_TYPES[search_type]))

        if type(value_upper) not in SEARCH_TYPES[search_type]:
            raise Exception("Given upper search value is not a correct type! (Given: {0}, Required: {1})".format(type(value_upper), SEARCH_TYPES[search_type]))

        self.value_lower = value_lower
        self.value_upper = value_upper

    def getQuery(self):
        return self.createQuery(self.value_lower)

    def getValue(self):
        return self.value_lower, self.value_upper

class OverValue(Command):
    """
    Command for determining if the value is over or equal to the Commands value

    :ivar int,float,datetime command_tpe (int): Type of command. In this case 3.
    :ivar int value: Value that all other values will be compared to. Can be of any type.

    """
    def __init__(self, search_type, value):
        Command.__init__(self, 3, search_type)
        if type(value) not in SEARCH_TYPES[search_type]:
            raise Exception("Given search value is not a correct type! (Given: {0}, Required: {1})".format(type(value), SEARCH_TYPES[search_type]))

        self.value = value

    def getQuery(self):
        return self.createQuery(self.value)

    def getValue(self):
        return (self.value,)

class UnderValue(Command):
    """
    Command for determining if the value is lower or equal to the Commands value

    :ivar int command_tpe: Type of command. In this case 4.
    :ivar int,float,datetime value: Value that all other values will be compared to. Can be of any type.

    """
    def __init__(self, search_type, value):
        Command.__init__(self, 4, search_type)
        if type(value) not in SEARCH_TYPES[search_type]:
            raise Exception("Given search value is not a correct type! (Given: {0}, Required: {1})".format(type(value), SEARCH_TYPES[search_type]))

        self.value = value

    def getQuery(self):
        return self.createQuery(self.value)

    def getValue(self):
        return (self.value,)

def searchSameEvents(nordic_event):
    """
    Function for searching and returning all events that are the same compared to the event given by the user.

    :param NordicEvent nordic_event: Event for which the search is done for
    :returns: List of :class:`NordicEvent` that are indentical to the event
    """
    m_header = nordic_event.main_h[0]
    search = NordicSearch()

    if m_header.origin_date is not None:
        search.addSearchExactly("origin_date", m_header.origin_date)
    if m_header.origin_time is not None:
        search.addSearchExactly("origin_time", m_header.origin_time)
    if m_header.epicenter_latitude is not None:
        search.addSearchExactly("epicenter_latitude", m_header.epicenter_latitude)
    if m_header.epicenter_longitude is not None:
        search.addSearchExactly("epicenter_longitude", m_header.epicenter_longitude)
    if m_header.magnitude_1 is not None:
        search.addSearchExactly("magnitude_1", m_header.magnitude_1)

    return search.searchEvents()

def searchSimilarEvents(nordic_event, time_diff = 20.0, latitude_diff = 0.2, longitude_diff = 0.2, magnitude_diff = 0.5):
    """
    Function for searching and returning all events that are considered similar to the event given by user.

    Default conditions for similarity: \b

        -Events must occur 20 seconds maximum apart from each other
        -Events must be 0.2 deg maximum apart from each other in latitude and longitude
        -Events must have magnitude difference of 0.5 maximum

    :param NordicEvent nordic_event: Event for which the search is done for
    :param float time_diff: maximum time difference in seconds
    :param float latitude_diff: maximum latitude difference in degrees
    :param float longitude_diff: maximum longitude difference in degrees
    :param float magnitude_diff: maximum magnitude difference
    :returns: Array of :class:`NordicEvent` that fit to the search criteria
    """
    m_header = nordic_event.main_h[0]
    search = NordicSearch()

    if (m_header.origin_date is None or m_header.origin_time is None):
        return []

    origin_datetime = datetime.combine(m_header.origin_date, m_header.origin_time)

    search.addSearchBetween("origin_date",
                            (origin_datetime - timedelta(seconds = time_diff)).date(),
                            (origin_datetime + timedelta(seconds = time_diff)).date())
    search.addSearchBetween("origin_time",
                            (origin_datetime - timedelta(seconds = time_diff)).time(),
                            (origin_datetime + timedelta(seconds = time_diff)).time())
    if m_header.epicenter_latitude is not None:
        search.addSearchBetween("epicenter_latitude", m_header.epicenter_latitude - latitude_diff, m_header.epicenter_latitude + latitude_diff)
    if m_header.epicenter_longitude is not None:
        search.addSearchBetween("epicenter_longitude", m_header.epicenter_longitude - longitude_diff, m_header.epicenter_longitude + longitude_diff)
    if m_header.magnitude_1 is not None:
        search.addSearchBetween("magnitude_1", m_header.magnitude_1 - magnitude_diff, m_header.magnitude_1 + magnitude_diff)

    return search.searchEvents()

def searchEvents(latitude, longitude, distance = 100.0,
                 magnitude = -9.0, magnitude_diff = 2.0,
                 date=None, date_diff=-9.0):
    """
    Search all events close to a location close to a point.

    :param float latitude: latitude coordinate of the point
    :param float longitude: longitude coordinate of the point
    :param float distance: distance from the point in kilometers
    :param float magnitude: magnitude of the event
    :param float magnitude_diff: maximum allowed magnitude difference of the event. Set negative value for searching exactly for a magnitude
    :param date date: date of the event
    :paran float date_diff: maximum allowed date difference from date in days. Set negative value for searching exactly at the date
    """
    search = NordicSearch()
    lat_diff = (0.5*distance) / 110.574
    lon_diff = (0.5*distance) / (float(np.cos(np.deg2rad(latitude))) * 111.32)

    search.addSearchBetween("epicenter_latitude", latitude-lat_diff, latitude+lat_diff)
    search.addSearchBetween("epicenter_longitude", longitude-lon_diff, longitude+lon_diff)

    if magnitude > 0.0:
        if magnitude_diff < 0:
            search.addSearchExactly("magnitude_1", magnitude)
        else:
            search.addSearchBetween("magnitude_1",
                                    magnitude-magnitude_diff,
                                    magnitude+magnitude_diff)

    if date is not None:
        if date_diff < 0:
            search.addSearchBetween("origin_date", date, date)
        else:
            search.addSearchBetween("origin_date",
                                    date-timedelta(days=date_diff),
                                    date+timedelta(days=date_diff))

    return search.searchEvents()
