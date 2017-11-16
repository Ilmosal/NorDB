import sys
import logging
import psycopg2
from datetime import date
from nordb.core import nordicSearch, usernameUtilities
from nordb.core.nordic import NordicMain
from nordb.database import sql2nordic
from nordb.database import getNordic

username = ""

def checkForSameEvents(nordic_event, cur, ignore_duplicates):
    """
    Method for finding same events compared to validated nordic string object and asking.

    Args:
        nordic_event(): nordic event string class
        cur(psycopg2.connect.cursor): psycopg cursor class
        ignore_duplicates(bool): flag for if duplicate events need to be ignored
    
    Returns:
        The id of the chosen same event
    """

    criteria = {
        "date":nordic_event.headers[1][0].header[NordicMain.DATE],
        "hour":nordic_event.headers[1][0].header[NordicMain.HOUR],
        "minute":nordic_event.headers[1][0].header[NordicMain.MINUTE],
        "second":nordic_event.headers[1][0].header[NordicMain.SECOND],
        "magnitude":nordic_event.headers[1][0].header[NordicMain.MAGNITUDE_1],
        "latitude":nordic_event.headers[1][0].header[NordicMain.EPICENTER_LATITUDE],
        "longitude":nordic_event.headers[1][0].header[NordicMain.EPICENTER_LONGITUDE]
    }

    to_be_removed = ()
    for key in criteria.keys():
        if criteria[key] is None or criteria[key].strip() == "":
            to_be_removed += (key,)

    for key in to_be_removed:
        criteria.pop(key, None)

    e_info = nordicSearch.getAllNordics(criteria)

    if e_info is None or e_info == []:
        return [-1, None]

    if ignore_duplicates:
        return e_info[0]

    print("Nordics with same information found! Does one of following events represent the same event?")
    largest = -1
    for e_i in e_info:
        if len(str(e_i[0])) > largest:
            largest = len(str(e_i[0]))

    print("EID ETPE YEAR D MO H MI SEC  DE LAT     LON     DEP  REP ST RMS MAG REP MAG REP MAG REP")
    for e_i in e_info:
        n_event = getNordic.readNordicEvent(cur, e_i[0])
        print(("{0:< " + str(largest) +"}   {1}  {2}").format(e_i[0], e_i[1], sql2nordic.nordicEventToNordic(n_event)[0][:-2]))
    
    print ("Your event:")
    print (nordic_event.headers[1][0].header[NordicMain.O_STRING])

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

    return [-9, -9]

def checkForSimilarEvents(nordic_event, cur): 
    """
    Method for finding similar events compared to validated nordic string object and asking. The closest event is determined by taking absolute values from the difference of seconds, latitude, longitude and magnitude of the event and summing it all together and ordering the values in ascending order.

    Args:
        nordic_event(): nordic event string class
        cur(psycopg2.connect.cursor): psycopg cursor class
    
    Returns:
        The id of the chosen same event
    """

    username = usernameUtilities.readUsername()

    weight_string = "("
    values = ()

    ev_seconds = ""
    val_seconds = ""
    if nordic_event.headers[1][0].header[NordicMain.HOUR] is not None and nordic_event.headers[1][0].header[NordicMain.HOUR].strip() != "":
        ev_seconds += "%s*3600.0"
        val_seconds += "hour*3600.0"
        values += (nordic_event.headers[1][0].header[NordicMain.HOUR],)
    if nordic_event.headers[1][0].header[NordicMain.MINUTE] is not None and nordic_event.headers[1][0].header[NordicMain.MINUTE].strip() != "":
        if ev_seconds != "":
            ev_seconds += "+"
            val_seconds += "+"
        ev_seconds += "%s*60.0"
        val_seconds += "minute*60.0"
        values += (nordic_event.headers[1][0].header[NordicMain.MINUTE],)
    if nordic_event.headers[1][0].header[NordicMain.SECOND] is not None and nordic_event.headers[1][0].header[NordicMain.SECOND].strip() != "":
        if ev_seconds != "":
            ev_seconds += "+"
            val_seconds += "+"
        ev_seconds += "%s"
        val_seconds += "second"
        values += (nordic_event.headers[1][0].header[NordicMain.SECOND],)
    
    if ev_seconds != "":
        weight_string += "ABS(("+ev_seconds + ") - (" + val_seconds +"))/60.0"

    if weight_string != "(":
        weight_string += " + " 

    if nordic_event.headers[1][0].header[NordicMain.EPICENTER_LATITUDE] is not None and nordic_event.headers[1][0].header[NordicMain.EPICENTER_LATITUDE].strip() != "":
        weight_string += "ABS(%s - epicenter_latitude)*100"
        values += (nordic_event.headers[1][0].header[NordicMain.EPICENTER_LATITUDE], )

    if weight_string != "(":
        weight_string += " + " 

    if nordic_event.headers[1][0].header[NordicMain.EPICENTER_LONGITUDE] is not None and nordic_event.headers[1][0].header[NordicMain.EPICENTER_LONGITUDE].strip() != "":
        weight_string += "ABS(%s - epicenter_longitude)*100"
        values += (nordic_event.headers[1][0].header[NordicMain.EPICENTER_LONGITUDE], )

    if weight_string != "(":
        weight_string += " + " 

    if nordic_event.headers[1][0].header[NordicMain.MAGNITUDE_1] is not None and nordic_event.headers[1][0].header[NordicMain.MAGNITUDE_1].strip() != "":
        weight_string += "ABS(%s - magnitude_1)*10"
        values += (nordic_event.headers[1][0].header[NordicMain.MAGNITUDE_1], )
    
    if weight_string == "(":
        return [-1, None]

    if weight_string[-2] == "+":
        weight_string = weight_string[:-2]

    weight_string += ")"
    values += values
    values += (nordic_event.headers[1][0].header[NordicMain.DATE],)

    try:
        cur.execute("SELECT event_id, event_type FROM nordic_event, (SELECT event_id, " + weight_string + " as search_weight FROM nordic_header_main) AS header WHERE (event_id, search_weight) IN (SELECT event_id, MIN("+ weight_string +") AS search_weight FROM nordic_event, nordic_header_main WHERE (root_id, event_type) IN (SELECT root_id, MAX(event_type) as event_type FROM nordic_event GROUP BY root_id) AND date=%s AND nordic_header_main.event_id = nordic_event.id GROUP BY event_id) AND event_id = nordic_event.id ORDER BY search_weight", values)
    except:
        print(weight_string)
        print(values)
        raise ValueError
    
    e_info = cur.fetchall()
   
    if e_info == []:
        return [-1, None]

    print("Nordics with similiar information found! Does one of following events represent the same event?")
    largest = -1
    for e_i in e_info:
        if len(str(e_i[0])) > largest:
            largest = len(str(e_i[0]))

    print("EID ETPE YEAR D MO H MI SEC  DE LAT     LON     DEP  REP ST RMS MAG REP MAG REP MAG REP")
    for e_i in e_info:
        n_event = getNordic.readNordicEvent(cur, e_i[0])
        print(("{0:< " + str(largest) +"}   {1}  {2}").format(e_i[0], e_i[1], sql2nordic.nordicEventToNordic(n_event)[0][:-2]))
    
    print ("Your event:")
    print ("        " + nordic_event.headers[1][0].header[NordicMain.O_STRING])
    while True:
        ans = input("Event_id(-1 if none are, -9 if you want to skip event, enter to choose the first event): ")

        if ans == "":
            return [e_info[0][0], e_info[0][1]]

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

    return [-9, -9]
