"""
This module contains all functions for modifying meta-information of events that are in the database.

Functions and Classes
---------------------
"""

import psycopg2
from nordb.core import usernameUtilities

def changeSolutionType(event_id, solution_type):
    """
    Method that changes the solution_type of the event and modifies all event types accordingly.

    :param int event_id: id of the event
    :param str solution_type: new solution type
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("SELECT allow_multiple FROM solution_type WHERE type_id = %s", (solution_type,))
    ans = cur.fetchone()
    
    if ans is None:
        raise Exception("{0} is not a valid solution_type! Either add the solution type to the database or use another solution_type".format(solution_type))

    allow_multiple = ans[0]

    cur.execute("SELECT id, solution_type, root_id FROM nordic_event WHERE id = %s;", (event_id,))
    event = cur.fetchone()

    if event is None:
        raise Exception("Event with id: {0} does not exist!".format(event_id))

    if event[1] == solution_type:
        raise Exception("Event already has type {0}!".format(solution_type))

    if not allow_multiple:
        cur.execute("UPDATE nordic_event SET solution_type = %s WHERE root_id = %s AND solution_type = %s", ("O", event[2], solution_type))
    
    cur.execute("UPDATE nordic_event SET solution_type = %s WHERE id = %s", (solution_type, event_id))

    conn.commit()
    conn.close()

def changeEventRoot(event_id, root_id):
    """
    Method that changes the root_id of the event and checks if there are any events with same solution_type. If there is and the solution_type is not A or O, it will change the event type of the old event to O. if root_id of -9 is given to the method, it will generate a new root_id for the event.

    :param int event_id: id of the event that needs to be moved
    :param int root_id: new existiting root id for the event
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, solution_type, root_id, urn from nordic_event WHERE id = %s;", (event_id,))
        event = cur.fetchone()

        if event is None:
            raise Exception("Event with id: {0} does not exist!".format(event_id))

        if event[3] is not None:
            raise Exception("Event has a urn so it cannot be modified!")

        old_root_id = event[2]

        if root_id != -9:
            cur.execute("SELECT id from nordic_event_root WHERE id = %s;", (root_id,))
            if cur.fetchone() is None:
                raise Exception("Event with root_id: {0} does not exist!".format(root_id))
        else:
            cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES RETURNING id;")
            root_id = cur.fetchone()[0]

        cur.execute("UPDATE nordic_event SET root_id = %s WHERE id = %s RETURNING root_id", (root_id, event_id))

        cur.execute("SELECT id, solution_type FROM nordic_event WHERE root_id = %s;", (root_id,))
        ans = cur.fetchall()

        for a in ans:
            if a[1] == event[1] and event[1] not in "OAR ":
               cur.execute("UPDATE nordic_event SET solution_type = %s WHERE id = %s AND NOT id = %s;", ("O", a[0], event_id)) 
       
        cur.execute("SELECT id FROM nordic_event WHERE root_id = %s", (old_root_id,))
        if cur.fetchone() is None:
            cur.execute("DELETE FROM nordic_event_root WHERE id = %s", (old_root_id,))
    except Exception as e:
        conn.close()
        raise e
    
    conn.commit() 
    conn.close()
