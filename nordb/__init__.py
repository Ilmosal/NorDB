"""
Documentation of the project is on this page. The program has four modules which contain submodules that contain all the functions in the program.
"""

try:
    from nordb.core import usernameUtilities
except:
    print("NorDB has not been initialized! Please run the initNorDB.sh "
          "command in the root folder of the program")
    exit()
from nordb.nordic.station import Station
from nordb.nordic.nordicEvent import NordicEvent
from nordb.database.nordicSearch import NordicSearch, searchEvents
from nordb.database.sql2station import getAllStations, getStation
from nordb.database.sql2nordic import getNordic
from nordb.core.nordic import readNordic, createNordicEvents
from nordb.database.sql2response import getResponse

__all__ = ["Station", "NordicEvent", "NordicSearch", "getAllStations",
           "getStation", "getNordic", "readNordic", "getResponse",
           "createNordicEvents", "searchEvents"]
