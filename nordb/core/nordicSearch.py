from datetime import date
import logging
import psycopg2

from nordb.core import nordicHandler, usernameUtilities
from nordb.io import sql2nordic

username = ""

COMMAND_TPES = {1:"exactly", 2:"between", 3:"over", 4:"under"}

SEARCH_IDS = {"date":1, 
                "hour":2,
                "minute":3,
                "second":4,
                "latitude":5, 
                "longitude":6, 
                "magnitude":7}

SEARCH_IDS_REV = {1:"date", 
                2:"hour",
                3:"minute",
                4:"second",
                5:"latitude", 
                6:"longitude", 
                7:"magnitude"}

SEARCH_TYPES = { 1:date, 
                2:int,
                3:int,
                4:float,
                5:float, 
                6:float, 
                7:float}

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
        return int(value)
    except ValueError:
        pass
    
    try:
        return float(value)
    except ValueError:
        pass
   
    return False

def string2Command(sCommand):
    """
    Generate a command from a string.
    
    Args:
        sCommand (str): Command given by user.

    Returns:
        Command that can be used for comparisons.
    """
    parts = sCommand.split('-')
    if len(parts) == 2 and parts[1] != "": 
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
            print("asdasd")
            raise ValueError
        command = OverValue(val)
    else:
        val = returnValueFromString(sCommand)
        if val is False:
            raise ValueError
        command = ExactlyValue(sCommand)

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

    if command.command_tpe == 2:
        if isinstance(command.valueLower, SEARCH_TYPES[searchId]) and isinstance(command.valueUpper, SEARCH_TYPES[searchId]):
            return True
    else:
        if isinstance(command.value, SEARCH_TYPES[searchId]):
            return True

    return False

def createSearchQuery(commands):
    """
    Method for creating the search query.

    Args:
        commands: Dictionary of all search criteria

    Returns:
        An tuple where the first value is the query in string format and second value is a tuple of the values inserted into the command
    """
    query = "SELECT DISTINCT event_id FROM nordic_event, nordic_header_main WHERE nordic_event.id = nordic_header_main.event_id"

    vals = ()

    for c in commands.keys():
        value = SEARCH_IDS_REV[c]
        if value == "magnitude":
            value += "_1"

        if commands[c].command_tpe == 1:
            query += " AND nordic_header_main." + value + " = %s"
            vals += (commands[c].value,)
        if commands[c].command_tpe == 2:
            query += " AND nordic_header_main." + value + " >= %s"
            query += " AND nordic_header_main." + value + " <= %s"
            vals += (commands[c].valueLower,)
            vals += (commands[c].valueUpper,)
        if commands[c].command_tpe == 3:
            query += " AND nordic_header_main." + value + " >= %s"
            vals += (commands[c].value,)
        if commands[c].command_tpe == 4:
            query += " AND nordic_header_main." + value + " <= %s"
            vals += (commands[c].value,)

    search = [query, vals]

    return search

def searchNordic(criteria):
    """
    Function for searching for events. Allows searching for events with following criteria: date, hour, minute, second, latitude, longitude, event_desc_id and magnitude. The function shows the user all the events that fit the criteria.

    |b
    Arguments must be given in following format:
        criterion="Value" -> Checks if the event's value is exactly of value
        criterion="Value1-Value2" -> Checks if the event's value is higher or equal to Value1 and lower or equal to Value2
        criterion="Value+" -> Checks if the event's value is higher or equal to value
        criterion="Value-" -> Checks if the event's value is lower or equal to value
    
    Args:
        criteria: All the criteria for search given by user.
    
    Returns:
        Function returns the id for the event that was wanted.
    """

    if not criteria:
        return -1

    username = usernameUtilities.readUsername()
    commands = {}

    for arg in criteria.keys():
        commands[SEARCH_IDS[arg]] = string2Command(criteria[arg])

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

    print("Events found with criteria:")
    print("---------------------------")
    largest = -1
    for a in ans:
        if len(str(a[0])) > largest:
            largest = len(str(a[0]))

    for a in ans:
        print(("event id: {0:<" + str(largest) +"} - {1}").format(a[0], sql2nordic.nordicEventToNordic(nordicHandler.readNordicEvent(cur, a))[0][:-1]))

