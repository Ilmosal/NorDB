import logging
import psycopg2

from nordb.core import usernameUtilities

username = ""

def changeEventRoot(event_id, root_id):
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

    cur.execute("SELECT id from nordic_event_root WHERE id = %s;", (root_id,))
    if cur.fetchone() is None:
        logging.error("Event root with id: {0} does not exist!".format(root_id))
        return

    cur.execute("UPDATE nordic_event SET root_id = %s WHERE id = %s RETURNING root_id", (root_id, event_id))

    cur.execute("SELECT id, event_type FROM nordic_event WHERE root_id = %s;", (root_id,))
    ans = cur.fetchall()

    for a in ans:
        if a[1] == event[1] and event[1] not in "OAR ":
           cur.execute("UPDATE nordic_event SET event_type = %s WHERE id = %s AND NOT id = %s;", ("0", a[0], event_id)) 
   
    cur.execute("SELECT id FROM nordic_event WHERE root_id = %s", (root_id,))
    if cur.fetchone() is None:
        cur.execute("DELETE nordic_event_root WHERE id = %s", (root_id,))

    conn.commit() 
    conn.close()

    print("Event {0} root is now {1}". format(event_id, root_id))
