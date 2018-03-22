"""
This module contains all functions for modifying meta-information of events that are in the database.

Functions and Classes
---------------------
"""

import psycopg2
from nordb.core import usernameUtilities

def changeEventType(event_id, event_type):
    """
    Method that changes the type of the event and modifies all event types accordingly.

    :param int event_id: id of the event
    :param str event_type: new event type
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT allow_multiple FROM event_type WHERE e_type_id = %s", (event_type,))
    ans = cur.fetchone()
    
    if ans is None:
        raise Exception("{0} is not a valid event_type! Either add the event type to the database or use another event_type".format(event_type))

    allow_multiple = ans[0]

    cur.execute("SELECT id, event_type, root_id from nordic_event WHERE id = %s;", (event_id,))
    event = cur.fetchone()

    if event is None:
        raise Exception("Event with id: {0} does not exist!".format(event_id))

    if event[1] == event_type:
        raise Exception("Event already has type {0}!".format(event_type))

    if not allow_multiple:
        cur.execute("UPDATE nordic_event SET event_type = %s WHERE root_id = %s AND event_type = %s", ("O", event[2], event_type))
    
    cur.execute("UPDATE nordic_event SET event_type = %s WHERE id = %s", (event_type, event_id))

    conn.commit()
    conn.close()

def changeEventRoot(event_id, root_id):
    """
    Method that changes the root_id of the event and checks if there are any events with same event_type. If there is and the event_type is not A or O, it will change the event type of the old event to O. if root_id of -999 is given to the method, it will generate a new root_id for the event.

    :param int event_id: id of the event that needs to be moved
    :param int root_id: new existiting root id for the event
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT id, event_type, root_id from nordic_event WHERE id = %s;", (event_id,))
    event = cur.fetchone()
    if event is None:
        raise Exception("Event with id: {0} does not exist!".format(event_id))

    old_root_id = event[2]

    if root_id != -999:
        cur.execute("SELECT id from nordic_event_root WHERE id = %s;", (root_id,))
        if cur.fetchone() is None:
            raise Exception("Event with root_id: {0} does not exist!".format(root_id))
    else:
        cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES RETURNING id;")
        root_id = cur.fetchone()[0]

    cur.execute("UPDATE nordic_event SET root_id = %s WHERE id = %s RETURNING root_id", (root_id, event_id))

    cur.execute("SELECT id, event_type FROM nordic_event WHERE root_id = %s;", (root_id,))
    ans = cur.fetchall()

    for a in ans:
        if a[1] == event[1] and event[1] not in "OAR ":
           cur.execute("UPDATE nordic_event SET event_type = %s WHERE id = %s AND NOT id = %s;", ("O", a[0], event_id)) 
   
    cur.execute("SELECT id FROM nordic_event WHERE root_id = %s", (old_root_id,))
    if cur.fetchone() is None:
        cur.execute("DELETE FROM nordic_event_root WHERE id = %s", (old_root_id,))

    conn.commit() 
    conn.close()
