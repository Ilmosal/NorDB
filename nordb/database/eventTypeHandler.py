"""
This module contains all functions for adding, modifying and removing event_type ids in the database.

Functions and Classes
---------------------
"""
from nordb.core import usernameUtilities
from nordb.database import nordicModify
from nordb.database import nordicSearch

def addEventType(e_type_id, e_type_desc, allow_multiple):
    """
    This function adds a new event type to the database with id of e_type_id.
    
    :param str e_type_id: The id of the event_type. Maximum of 6 characters
    :param str e_type_desc: The description of the event type id. Maximum of 32 characters
    :param boolean allow_multiple: flag for allowing multiple events with same event_type into the event_root
    """
    if len(e_type_id) > 6:
        raise Exception("Event type {0} is too long! Maximum of 6 characters!".format(e_type_id))

    if len(e_type_desc) > 32:
        raise Exception("Event type description ({0}) is too long! Maximum on 32 characters")

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT allow_multiple FROM event_type WHERE e_type_id = %s", (e_type_id,))
    ans = cur.fetchone()
    
    if ans is not None:
        raise Exception("{0} is already in the database! Either remove the old event type from the database or consider a new id for the new one".format(e_type_id))

    cur.execute("INSERT INTO event_type (e_type_id, e_type_desc, allow_multiple) VALUES (%s, %s, %s)", (e_type_id, e_type_desc, allow_multiple))

    conn.commit()
    conn.close() 

def getEventTypes():
    """
    Function for getting all event types from the database as an array.
    :returns: Event type id, description and allow_multiple values in a array
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT e_type_id, e_type_desc, allow_multiple FROM event_type")
    ans = cur.fetchall()

    conn.close()
    return ans

def removeEventType(event_type, new_event_type = None):
    """
    This function changes all old events with event type id event_type to new_event_type and removes the event_type from the database.

    :param str event_type: event_type to be removed
    :param str new_event_type: new event_type
    """
    search = nordicSearch.NordicSearch()
    search.addSearchExactly("event_type", event_type)
    e_ids = search.searchEventIds()

    for e_id in e_ids:
        nordicModify.changeEventType(e_id, new_event_type)

    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("DELETE FROM event_type WHERE e_type_id = %s", (event_type,))

    conn.commit()
    conn.close()
