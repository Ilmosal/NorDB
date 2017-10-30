import logging
import psycopg2

from nordb.core import usernameUtilities

username = ""

def changeEventType(event_id, event_type):
    """
    Method that changes the type of the event and modifies all event types accordingly.

    Args:
        event_id(int): id of the event
        event_type(str): new event type
    """
    username = usernameUtilities.readUsername()

    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to database!!")
        return -1

    cur = conn.cursor()

    cur.execute("SELECT id, event_type, root_id from nordic_event WHERE id = %s;", (event_id,))
    event = cur.fetchone()
    if event is None:
        logging.error("Event with id: {0} does not exist!".format(event_id))
        return

    if event[1] == event_type:
        logging.error("Event already has type {0}!".format(event_type))
        return

    if event_type not in "AO":
        cur.execute("UPDATE nordic_event SET event_type = %s WHERE root_id = %s AND event_type = %s", ("O", event[2], event_type))
    
    cur.execute("UPDATE nordic_event SET event_type = %s WHERE id = %s", (event_type, event_id))

    conn.commit()
    conn.close()

    print("Event type of event {0} is now {1}!".format(event_id, event_type))


def changeEventRoot(event_id, root_id):
    """
    Method that changes the root_id of the event and checks if there are any events with same event_type. If there is and the event_type is not A or O, it will change the event type of the old event to O. if roo_id of -999 is given to the method, it will generate a new root_id for the event.

    Args:
        event_id(int): id of the event that needs to be moved
        root_id(int): new existiting root id for the event
    """
    username = usernameUtilities.readUsername()

    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to database!!")
        return -1

    cur = conn.cursor()

    cur.execute("SELECT id, event_type from nordic_event WHERE id = %s;", (event_id,))
    event = cur.fetchone()
    if event is None:
        logging.error("Event with id: {0} does not exist!".format(event_id))
        return

    if root_id != -999:
        cur.execute("SELECT id from nordic_event_root WHERE id = %s;", (root_id,))
        if cur.fetchone() is None:
            logging.error("Event root with id: {0} does not exist!".format(root_id))
            return
    else:
        cur.execute("INSERT INTO nordic_event_root DEFAULT VALUES RETURNING id;")
        root_id = cur.fetchone()[0]

    cur.execute("UPDATE nordic_event SET root_id = %s WHERE id = %s RETURNING root_id", (root_id, event_id))

    cur.execute("SELECT id, event_type FROM nordic_event WHERE root_id = %s;", (root_id,))
    ans = cur.fetchall()

    for a in ans:
        if a[1] == event[1] and event[1] not in "OAR ":
           cur.execute("UPDATE nordic_event SET event_type = %s WHERE id = %s AND NOT id = %s;", ("O", a[0], event_id)) 
   
    cur.execute("SELECT id FROM nordic_event WHERE root_id = %s", (root_id,))
    if cur.fetchone() is None:
        cur.execute("DELETE nordic_event_root WHERE id = %s", (root_id,))

    conn.commit() 
    conn.close()

    print("Event {0} root is now {1}". format(event_id, root_id))
