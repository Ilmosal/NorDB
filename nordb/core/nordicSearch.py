from datetime import date
import logging
import psycopg2

from nordb.core import usernameUtilities
from nordb.database import getNordic
from nordb.database import sql2nordic

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

    Args:
        command_tpe (int): Type of command
    
    Attributes:
        command_tpe (int): Type of command
    """
    def __init__(self, command_tpe):
        self.command_tpe = command_tpe

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command. Override this for all classes.

        Args:
            value: value that will be compared to the original value

        Returns:
            Boolean value tha will be always false for Command class.
        """
        return False

class ExactlyValue(Command):
    """
    Command for determining if the value is exactly the given value.

    Args:
        value: value that all other values will be compared to. Can be of any type

    Attributes:
        command_tpe (int): Type of command. In this case 1.
        value: Value that all other values will be compared to. Can be of any type
        
    """
    def __init__(self, value):
        Command.__init__(self, 1)
        self.value = value

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command.

        Args:
            value: value that will be compared to the original for if they are exactly the same

        Returns:
            Boolean value that tells if the values are exactly the same
        """

        if type(value) is not type(self.value):
            return False

        if value == self.value:
            return True
        else:
            return False

class BetweenValues(Command):
    """
    Command for determining if the value is exactly the given value.

    Args:
        valueLower: value of the lower limit of the comparison
        valueUpper: value for the upper limit of the comparison

    Attributes:
        command_tpe (int): Type of command. In this case 2.
        valueLower: value of the lower limit of the comparison
        valueUpper: value for the upper limit of the comparison
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

        Args:
            value: value that will be compared to valueUpper and valueLower

        Returns:
            Boolean value that tells if the value falls between valueUpper and valueLower
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

    Args:
        value: value that all other values will be compared to. Can be of any type.

    Attributes:
        command_tpe (int): Type of command. In this case 3.
        value: Value that all other values will be compared to. Can be of any type.
        
    """
    def __init__(self, value):
        Command.__init__(self, 3)
        self.value = value

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command.

        Args:
            value: value that will be compared to the original for if it is over or equal tothe orginal

        Returns:
            Boolean value that tells if the value is over or equal to the orginal
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

    Args:
        value: value that all other values will be compared to. Can be of any type.

    Attributes:
        command_tpe (int): Type of command. In this case 4.
        value: Value that all other values will be compared to. Can be of any type.
        
    """
    def __init__(self, value):
        Command.__init__(self, 4)
        self.value = value

    def isValueValid(self, value):
        """
        Method for checking whether a value is valid by the command.

        Args:
            value: value that will be compared to the original for if it is lower or equal tothe orginal

        Returns:
            Boolean value that tells if the value is lower or equal to the orginal
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

    Args:
        value (str): string value that will be transformed into correct format
    
    Returns:
        The value in it's correct type. Priority order is Date -> Float -> Integer
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
    
    Args:
        sCommand (str): Command given by user.

    Returns:
        Command that can be used for comparisons.
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
    
    Args:
        command(Command): The command that needs to be validated
        searchID(int): search id of the command

    Returns:
        True or False
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

    Args:
        eveb: Bottom limit of event types
        evet: Top limit of event types

    Returns:
        String of all event types
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

    Args:
        commands: Dictionary of all search criteria

    Returns:
        An tuple where the first value is the query in string format and second value is a tuple of the values inserted into the command
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
    Method that returns all nordic events that fulfil the given crieria.

    Args:
        criteria: All criteria for search

    Returns:
        Array of event_ids that fulfil the criteria
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
        return -1

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
                nordic = sql2nordic.nordicEventToNordic(nordicHandler.readNordicEvent(cur, event[0]))
                print("Event ID: {0}".format(a[0]))
                for line in nordic:
                    print(line, end='')
                print(80*"-")
            else:
                print(("{0:< " + str(largest+1) +"}    {1} {2}").format(event[0], event[1], sql2nordic.nordicEventToNordic(nordicHandler.readNordicEvent(cur, event[0]))[0][:-2]))

    conn.close()

    return 

def searchWithEventId(event_id):
    """
    Method for searching if a event_id exists on the database


    Returns:
        Relevant information from the event: (event_id, event_type, distance_indicator, event_desc_id)
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
    Method for printing out a list of event_ids.

    Args:
        event_ids (int[]): list of event_ids that need to be printed
        verbose (bool): flag if all info from events need to be printed or just the main headers
    """
    if len(events) == 0:
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

    Args:
        criteria({}): dictionary of the criteria
        verbose (bool): flag if all info from events need to be printed or just the main headers

    Returns:
        list of events found with criteria
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
        criterion="Value" -> Checks if the event's value is exactly of value
        criterion="Value1-Value2" -> Checks if the event's value is higher or equal to Value1 and lower or equal to Value2
        criterion="Value+" -> Checks if the event's value is higher or equal to value
        criterion="Value-" -> Checks if the event's value is lower or equal to value
    
    Args:
        criteria ({}): All the criteria for search given by user.
        verbose (bool): flag if all info from events need to be printed or just the main headers
    
    Returns:
        list of event ids or none
    """
    username = usernameUtilities.readUsername()

    event_ids = ()

    if event_root:
        events = searchEventRoot(criteria, verbose)
        return
    elif "event_id" in criteria.keys():
        events = searchWithEventId(criteria["event_id"])
    else:
        events = searchWithCriteria(criteria)

    if not no_outprint:
        printNordic(events, criteria, verbose)

    if output is not None:
        for event in events:
            if output_format == "n":
                sql2nordic.writeNordicEvent(event[0], user_path, output)
            elif output_format == "q":
                sql2quakeml.writeQuakeML(event[0], user_path, output)
            elif output_format == "sc3":
                sql2sc3.writeSC3(event[0], user_path, output)
