"""
This module contains all commands for searching the database for events with given criteria. The most important function here is searchNordic and most other functions and classes are here just to support it.

Functions and Classes
---------------------
"""

from datetime import date
import logging
import psycopg2

from nordb.core import usernameUtilities
from nordb.database import getNordic
from nordb.database import sql2nordic
from nordb.database import sql2quakeml
from nordb.database import sql2sc3

username = ""

COMMAND_TPES = {1:"exactly", 2:"between", 3:"over", 4:"under"}

SEARCH_IDS = {"date":1, 
                "hour":2,
                "minute":3,
                "second":4,
                "latitude":5, 
                "longitude":6, 
                "magnitude":7,
                "event_type":8,
                "distance_indicator":9,
                "event_desc_id":10,
                "event_id":11,
                "depth":12}

SEARCH_IDS_REV = {1:"date", 
                2:"hour",
                3:"minute",
                4:"second",
                5:"latitude", 
                6:"longitude", 
                7:"magnitude",
                8:"event_type",
                9:"distance_indicator",
                10:"event_desc_id",
                11:"event_id",
                12:"depth"}

SEARCH_TYPES = { 1:date, 
                2:int,
                3:int,
                4:float,
                5:float, 
                6:float, 
                7:float,
                8:str,
                9:str,
                10:str,
                12:float}

EVENT_TYPE_VALS = {'O':1,
                    'A':2,
                    'R':3,
                    'P':4,
                    'F':5,
                    'S':6}

class Command:
    """
    Class for command that is returned by string2Command. 

    :ivar int command_tpe: Type of command. Initial value: command_tpe
    """
    def __init__(self, command_tpe):
        self.command_tpe = command_tpe

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command. Override this for all classes.
        
        :param value: value that will be compared to the original value
        :type value: int or float or datetime
        :return: Boolean value that will be always false for Command class.
        """
        return False

class ExactlyValue(Command):
    """
    Command for determining if the value is exactly the given value.

    :ivar int command_tpe: Type of command. Initial value: 1
    :ivar int,float,datetime value: Value that all other values will be compared to. Can be of any type. Initial value: value
    """
    def __init__(self, value):
        Command.__init__(self, 1)
        self.value = value

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command.
        
        :param value: value that will be compared to the original for if they are exactly the same
        :type value: int, float or datetime
        :return: Boolean value that tells if the values are exactly the same
        """

        if type(value) is not type(self.value):
            return False

        if value == self.value:
            return True
        else:
            return False

class BetweenValues(Command):
    """
    Command for determining if a value falls exactly between the given values.
    
    :ivar int command_tpe: Type of command. In this case 2.
    :ivar int,float,datetime valueLower: value of the lower limit of the comparison
    :ivar int,float,datetime valueUpper: value for the upper limit of the comparison
    :raises: **TypeError** -- TypeError given to user if valueLower and valueUpper are of different type
    """
    def __init__(self, valueLower, valueUpper):
        Command.__init__(self, 2)
        if type(valueLower) is not type(valueUpper):
            raise TypeError

        self.valueLower = valueLower
        self.valueUpper = valueUpper

    def isValueValid(self, value):
        """
        Method for checking whether a value is smaller or as equal to valueUpper but higher than valueLower.

        :param value: value that will be compared to valueUpper and valueLower
        :type value: int, float, datetime
        :return: Boolean value that tells if the value falls between valueUpper and valueLower
        """

        if type(value) is not type(self.valueLower):
            return False

        if value <= self.valueUpper and value >= self.valueLower:
            return True
        else:
            return False


class OverValue(Command):
    """
    Command for determining if the value is over or equal to the Commands value

    :ivar int,float,datetime command_tpe (int): Type of command. In this case 3.
    :ivar int value: Value that all other values will be compared to. Can be of any type.
        
    """
    def __init__(self, value):
        Command.__init__(self, 3)
        self.value = value

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command.

        :param value: value that will be compared to the original for if it is over or equal tothe orginal
        :type value: int, float, datetime
        :return: Boolean value that tells if the value is over or equal to the orginal
        """

        if type(value) is not type(self.value):
            return False

        if value >= self.value:
            return True
        else:
            return False

class UnderValue(Command):
    """
    Command for determining if the value is lower or equal to the Commands value


    :ivar int command_tpe: Type of command. In this case 4.
    :ivar int,float,datetime value: Value that all other values will be compared to. Can be of any type.
        
    """
    def __init__(self, value):
        Command.__init__(self, 4)
        self.value = value

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command.
        
        :param int,float,datetime value: value that will be compared to the original for if it is lower or equal to the orginal
        :return: Boolean value that tells if the value is lower or equal to the orginal
        """

        if type(value) is not type(self.value):
            return False

        if value <= self.value:
            return True
        else:
            return False

def returnValueFromString(value):
    """
    Function for returning a valid date, float or integer value from a string

    :param str value: string value that will be transformed into correct format
    :return: The value in it's correct type. Priority order is Date -> Float -> Integer
    :raise: **ValueError** -- Value error if the string vannot be parsed into any value supported by  the program
    """
    try:
        if len(value) != 10:
            raise ValueError
        return date(day=int(value[:2]), month=int(value[3:5]), year=int(value[6:]))
    except ValueError:
        pass

    try:
        return date(day=int(value[8:]), month=int(value[5:7]), year=int(value[:4]))
    except ValueError:
        pass

    try:
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
  
    if len(value) == 1:
        return value
 
    return False

def string2Command(sCommand, cmd_type):
    """
    Generate a command from a string.
    
    :param str sCommand: Command given by user.
    :return: Command that can be used for comparisons.
    :raises: **ValueError** -- Program raises value error if the sCommand is in a incorrect format
    """
    parts = sCommand.split('-')

    if cmd_type == "distance_indicator" or cmd_type == "event_desc_id":
        if len(sCommand) != 1:
            raise ValueError

    if len(parts) == 2 and parts[1] != "" and sCommand[0] != "-": 
        val1 = returnValueFromString(parts[0])
        val2 = returnValueFromString(parts[1])
        if val1 is False or val2 is False:
            raise ValueError
        command = BetweenValues(val1, val2)
    elif sCommand.endswith('-'):
        val = returnValueFromString(sCommand[:-1])
        if val is False:
            raise ValueError
        command = UnderValue(val)
    elif sCommand.endswith('+'):
        val = returnValueFromString(sCommand[:-1])
        if val is False:
            raise ValueError
        command = OverValue(val)
    else:
        if (cmd_type == "distance_indicator" or cmd_type == "event_desc_id") and sCommand == " ":
            val = None
        else:
            val = returnValueFromString(sCommand)

        if val is False:
            raise ValueError
        command = ExactlyValue(val)

    return command

def validateCommand(command, searchId):
    """
    Validate command checks if the type of the value in command matches it's search_id's expected type.
    
    :param Command command: The command that needs to be validated
    :param int searchID: search id of the command
    :return: True or False depending on if the command goes through validation
    """


    if (searchId == 9 or searchId == 10) and command.value == None:
        return True

    if command.command_tpe == 2:
        if isinstance(command.valueLower, SEARCH_TYPES[searchId]) and isinstance(command.valueUpper, SEARCH_TYPES[searchId]):
            return True
    else:
        if isinstance(command.value, SEARCH_TYPES[searchId]):
            return True

    return False

def rangeOfEventType(eveb, evet):
    """
    Method for getting all event types in range as a string.

    :param str eveb: Bottom limit of event types
    :param str evet: Top limit of event types
    :return: String of all event types
    """
    bot = EVENT_TYPE_VALS[eveb]
    top = EVENT_TYPE_VALS[evet]

    events = ""

    for key in EVENT_TYPE_VALS.keys():
        if EVENT_TYPE_VALS[key] >= bot and EVENT_TYPE_VALS[key] <= top:
            events += key     

    return events

def createSearchQuery(commands):
    """
    Method for creating the search query.

    :param commands: Dictionary of all search criteria
    :return: An tuple where the first value is the query in string format and second value is a tuple of the values inserted into the command
    """

    query = "SELECT DISTINCT ON (event_id) event_id, event_type, distance_indicator, event_desc_id FROM nordic_event, nordic_header_main WHERE nordic_event.id = nordic_header_main.event_id"

    vals = ()

    for c in commands.keys():
        value = SEARCH_IDS_REV[c]
        if value == "magnitude":
            value += "_1"
        
        if value == "event_type":
            if commands[c].command_tpe == 1:
                query += " AND nordic_event." + value + " = %s"
                vals += (commands[c].value,)

            elif commands[c].command_tpe == 2:
                query += " AND nordic_event." + value + " = %s"
                vals += (rangeOfEventType(commands[c].valueLower, commands[c].valueUpper),)
            elif commands[c].command_tpe == 3:
                query += " AND nordic_event." + value + " = %s"
                vals += (rangeOfEventType(commands[c].value), 'S')
            elif commands[c].command_tpe == 4:
                query += " AND nordic_event." + value + " = %s"
                vals += ('O',rangeOfEventType(commands[c].value))
        else:     
            if commands[c].command_tpe == 1:
                if value == "latitude" or value == "longitude":
                    value = "epicenter_" + value

                if commands[c].value == None:
                    query += " AND nordic_header_main." + value + " is %s"
                else:
                    query += " AND nordic_header_main." + value + " = %s"
                vals += (commands[c].value,)
            elif commands[c].command_tpe == 2:
                if value == "latitude" or value == "longitude":
                    value = "epicenter_" + value

                query += " AND nordic_header_main." + value + " >= %s"
                query += " AND nordic_header_main." + value + " <= %s"
                vals += (commands[c].valueLower,)
                vals += (commands[c].valueUpper,)
            elif commands[c].command_tpe == 3:
                if value == "latitude" or value == "longitude":
                    value = "epicenter_" + value

                query += " AND nordic_header_main." + value + " >= %s"
                vals += (commands[c].value,)
            elif commands[c].command_tpe == 4:
                if value == "latitude" or value == "longitude":
                    value = "epicenter_" + value

                query += " AND nordic_header_main." + value + " <= %s"
                vals += (commands[c].value,)

    query += " ORDER BY event_id"

    search = [query, vals]

    return search

def getAllNordics(criteria):
    """
    Method that returns all nordic events that fulfil the given criteria.

    :param dict criteria: All criteria for search
    :return: Array of event_ids that fulfil the criteria
    """
    if not criteria:
        return None

    username = usernameUtilities.readUsername()

    commands = {}

    for arg in criteria.keys():
        commands[SEARCH_IDS[arg]] = string2Command(criteria[arg], arg)

    for c in commands.keys():
        if not validateCommand(commands[c], c):
            return -2

    search = createSearchQuery(commands)

    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to database!!")
        return -1
 
    cur = conn.cursor()

    cur.execute(search[0], search[1])
    ans = cur.fetchall()

    return ans

def searchEventRoot(criteria, verbose):
    """
    Function for searching all events with certain criteria given by user. Criteria needs to be a dict where the key and the values are strings from which the criteria for the search is generated from.

    :param dict criteria: Criteria given by user. This function is used mainly by the NorDB.py module which is the command line tool that controls the program
    :param bool verbose: flag if all info from events need to be printed or just the main headers
    :return: True or False depending on if the search was operated succesfully or not
    """
    if "event_id" in criteria.keys():
        events = searchWithEventId(criteria["event_id"])
    else:
        events = searchWithCriteria(criteria)
    e_ids = ()
    for e in events:
        e_ids += (e[0],)

    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to database!!")
        return False

    cur = conn.cursor()

    e_roots_tmp = ()

    for eid in e_ids:
        cur.execute("SELECT root_id FROM nordic_event WHERE id = %s", (eid,)) 
        e_roots_tmp += tuple(cur.fetchall())

    e_tmp = ()

    for e in e_roots_tmp:
        e_tmp  += (e[0],)

    e_set = set(e_tmp)
    e_all_roots = ()

    for e in e_set:

        cur.execute("SELECT DISTINCT ON (nordic_event.id) nordic_event.id, event_type, nordic_header_main.distance_indicator, nordic_header_main.event_desc_id, root_id FROM nordic_event, nordic_header_main WHERE nordic_event.root_id = %s AND nordic_header_main.event_id = nordic_event.id ORDER BY event_type;", (e,))
        e_all_roots += (tuple(cur.fetchall()),)
    
    largest = -1
    for e_roots_list in e_all_roots:
        for e in e_roots_list:
            if len(str(e[0])) > largest:
                largest = len(str(e[0]))

    for e_roots_list in e_all_roots:
        print ("Event root: {0}".format(e_roots_list[0][4]))
        print("EID" +" "*(largest+1) + "ETP YEAR M DA H MI SEC  DE LAT     LON     DEP  REP ST RMS MAG REP MAG REP MAG REP")

        for event in e_roots_list:
            if verbose:
                nordic = sql2nordic.nordicEventToNordic(getNordic.readNordicEvent(cur, event[0]))
                print("Event ID: {0}".format(a[0]))
                for line in nordic:
                    print(line, end='')
                print(80*"-")
            else:
                print(("{0:< " + str(largest+1) +"}    {1} {2}").format(event[0], event[1], sql2nordic.nordicEventToNordic(getNordic.readNordicEvent(cur, event[0]))[0][:-2]))

    conn.close()

    return True

def searchWithEventId(event_id):
    """
    Method for searching if a event_id exists on the database

    :param int event_id: id of the event that is being searched
    :return: Relevant information from the event: (event_id, event_type, distance_indicator, event_desc_id)
    """
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to database!!")
        return -1

    cur = conn.cursor()
 
    cur.execute("SELECT nordic_event.id, event_type, nordic_header_main.distance_indicator, nordic_header_main.event_desc_id FROM nordic_event, nordic_header_main WHERE (root_id, event_type) IN (SELECT root_id, MIN(event_type) from nordic_event GROUP BY root_id) AND nordic_event.id = %s AND nordic_header_main.event_id = nordic_event.id LIMIT 1;", (event_id,)) 
    event = cur.fetchall()

    conn.close()
  
    return event

def printNordic(events, criteria, verbose):
    """
    Method for printing out a list of events.

    :param array event_ids: list of event_ids that need to be printed
    :param dict criteria: Criteria given by user. This function is used mainly by the NorDB.py module which is the command line tool that controls the program
    :param bool verbose: flag if all info from events need to be printed or just the main headers
    :return: None if the operations were succesful
    """
    if events is None or len(events) == 0:
        print("No events found with criteria!")
    else:
        if len(criteria.keys()) == 0:
            print("Events in database:")
            print("---------------------------")
        else:
            print("Events found with criteria:")
            for key in criteria.keys():
                print(key + ": " + criteria[key] + " ", end='')
            print("\n---------------------------")

        try:
            conn = psycopg2.connect("dbname=nordb user={0}".format(username))
        except:
            logging.error("Couldn't connect to database!!")
            return None
 
        cur = conn.cursor()

        if verbose:
            for event in events:
                nordic = sql2nordic.nordicEventToNordic(getNordic.readNordicEvent(cur, event[0]))
                print("Event ID: {0}".format(event[0]))
                for line in nordic:
                    print(line, end='')
                print(80*"-")

        else:
            largest = -1
            for event in events:
                if len(str(event[0])) > largest:
                    largest = len(str(event[0]))

            print("EID" +" "*(largest+1) + "ETP YEAR M DA H MI SEC  DE LAT     LON     DEP  REP ST RMS MAG REP MAG REP MAG REP")
            for event in events:
                print(("{0:< " + str(largest+1) +"}    {1} {2}").format(event[0], event[1], sql2nordic.nordicEventToNordic(getNordic.readNordicEvent(cur, event[0]))[0][:-2]))

        conn.close()

def searchWithCriteria(criteria):
    """
    Method for searching events with given criteria. Description for the criteria is given in the documentation of searchNordic.

    :param dict criteria: Criteria given by user. This function is used mainly by the NorDB.py module which is the command line tool that controls the program
    :param bool verbose: flag if all info from events need to be printed or just the main headers
    :return: list of events found with criteria or None if the search was not succesful
    """
    commands = {}

    for arg in criteria.keys():
        commands[SEARCH_IDS[arg]] = string2Command(criteria[arg], arg)

    for c in commands.keys():
        if not validateCommand(commands[c], c):
            return None

    search = createSearchQuery(commands)

    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to database!!")
        return None
 
    cur = conn.cursor()

    cur.execute(search[0], search[1])
    ans = cur.fetchall()

    conn.close()

    largest = -1
    event_ids = ()
    for a in ans:
        event_ids += (a[0],)
    
    return ans

def searchNordic(criteria, verbose, output, event_root, user_path, output_format, no_outprint):
    """
    Method for searching for events. Allows searching for events with following criteria: date, hour, minute, second, latitude, longitude, event_desc_id and magnitude. The function shows the user all the events that fit the criteria.

    Arguments must be given in following format:

        * criterion="Value" -- Checks if the event's value is exactly of value
        * criterion="Value1-Value2" -- Checks if the event's value is higher or equal to Value1 and lower or equal to Value2
        * criterion="Value+" -- Checks if the event's value is higher or equal to value
        * criterion="Value-" -- Checks if the event's value is lower or equal to value
    
    :param dict criteria: Criteria given by user. This function is used mainly by the NorDB.py module which is the command line tool that controls the program
    :param bool verbose: flag if all info from events need to be printed or just the main headers
    :return: list of event ids or none
    """
    username = usernameUtilities.readUsername()

    if event_root:
        events = searchEventRoot(criteria, verbose)
        return
    elif "event_id" in criteria.keys():
        events = searchWithEventId(criteria["event_id"])
    else:
        events = searchWithCriteria(criteria)

    if not no_outprint:
        printNordic(events, criteria, verbose)

    event_ids = []

    for e in events:
        event_ids.append(e[0])

    if output is not None:
        if output_format == "n":
            for e_id in event_ids:
                sql2nordic.writeNordicEvent(e_id, user_path, output)
        elif output_format == "q":
            sql2quakeml.writeQuakeML(event_ids, user_path, output)
        elif output_format == "sc3":
            sql2sc3.writeSC3(event_ids, user_path, output)
