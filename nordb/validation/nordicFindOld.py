import logging
import psycopg2
from datetime import date
from nordb.core import nordicSearch, nordicHandler
from nordb.database import sql2nordic

def checkForSameEvents(nordic_event, cur):
    """
    Method for finding same events compared to validated nordic string object and asking.

    Args:
        nordic_event(): nordic event string class
        cur(psycopg2.connect.cursor): psycopg cursor class
    
    Returns:
        The id of the chosen same event
    """

    criteria = {
        "date":nordic_event.headers[0].date,
        "hour":nordic_event.headers[0].hour,
        "minute":nordic_event.headers[0].minute,
        "second":nordic_event.headers[0].second,
        "magnitude":nordic_event.headers[0].magnitude_1,
        "latitude":nordic_event.headers[0].epicenter_latitude,
        "longitude":nordic_event.headers[0].epicenter_longitude
    }

    for key in criteria.keys():
        if criteria[key] is None:
            criteria.pop(key, None)

    e_info = nordicSearch.getAllNordics(criteria)

    if e_info is None or e_info == []:
        return [-1, None]

    if len(e_info) == 1:
        return [e_info[0][0], e_info[0][1]]

    print("Nordics with same information found! Does one of following events represent the same event?")
    largest = -1
    for e_i in e_info:
        if len(str(e_i[0])) > largest:
            largest = len(str(e_i[0]))

    print("EID ETPE YEAR D MO H MI SEC  DE LAT     LON     DEP  REP ST RMS MAG REP MAG REP MAG REP")
    for e_i in e_info:
        n_event = nordicHandler.readNordicEvent(cur, e_i[0])
        print(("{0:< " + str(largest) +"}   {1}  {2}").format(e_i[0], e_i[1], sql2nordic.nordicEventToNordic(n_event)[0][:-2]))
    
    print ("Your event:")
    print (nordic_event.headers[0].o_string[:-2])

    while True:
        ans = input("Event_id(-1 if none are, -9 if is but you want to skip event): ")
        try:
            if int(ans) > -2 or int(ans) == -9:
                print("")
                if int(ans) < 0:
                    return [int(ans), None]
                cur.execute("SELECT event_type FROM nordic_event where id = %s", (int(ans),))
                e_type = cur.fetchone()
                if e_type is None:
                    return [int(ans), None]
                else:
                    return [int(ans), e_type[0]]
        except ValueError:
            pass

    return -9

    return int(ans)

def checkForSimilarEvents(nordic_event, cur): 
    """
    Method for finding similar events compared to validated nordic string object and asking.

    Args:
        nordic_event(): nordic event string class
        cur(psycopg2.connect.cursor): psycopg cursor class
    
    Returns:
        The id of the chosen same event
    """

    hour_error = 1
    magnitude_error = 1.0
    latitude_error = 0.5
    longitude_error = 0.5

    criteria = {
        "date":nordic_event.headers[0].date,
        "hour":str(int(nordic_event.headers[0].hour)-hour_error) + "-" + str(int(nordic_event.headers[0].hour)+hour_error),
        "magnitude":str(float(nordic_event.headers[0].magnitude_1)-magnitude_error) + "-" + str(float(nordic_event.headers[0].magnitude_1)+magnitude_error),
        "latitude":str(float(nordic_event.headers[0].epicenter_latitude)-latitude_error) + "-" + str(float(nordic_event.headers[0].epicenter_latitude)+latitude_error),
        "longitude":str(float(nordic_event.headers[0].epicenter_longitude)-longitude_error) + "-" + str(float(nordic_event.headers[0].epicenter_longitude)+longitude_error)
    }

    if int(nordic_event.headers[0].hour) == 0:
        criteria["hour"] = "00-01"
    elif int(nordic_event.headers[0].hour) == 23:
        criteria["hour"] = "22-23"

    e_info = nordicSearch.getAllNordics(criteria)

    if e_info is None or e_info == []:
        return [-1, None]

    print("Nordics with similiar information found! Does one of following events represent the same event?")
    largest = -1
    for e_i in e_info:
        if len(str(e_i[0])) > largest:
            largest = len(str(e_i[0]))

    print("EID ETPE YEAR D MO H MI SEC  DE LAT     LON     DEP  REP ST RMS MAG REP MAG REP MAG REP")
    for e_i in e_info:
        n_event = nordicHandler.readNordicEvent(cur, e_i[0])
        print(("{0:< " + str(largest) +"}   {1}  {2}").format(e_i[0], e_i[1], sql2nordic.nordicEventToNordic(n_event)[0][:-2]))
    
    print ("Your event:")
    print (nordic_event.headers[0].o_string[:-2])
    while True:
        ans = input("Event_id(-1 if none are, -9 if is but you want to skip event): ")
        try:
            if int(ans) > -2 or int(ans) == -9:
                if int(ans) < 0:
                    return [int(ans), None]
                cur.execute("SELECT event_type FROM nordic_event where id = %s", (int(ans),))
                e_type = cur.fetchone()

                if e_type is None:
                    return [int(ans), None]
                else:
                    return [int(ans), e_type[0]]
        except ValueError:
            pass

    return -9
