import psycopg2
import logging
import os

MODULE_PATH = os.path.realpath(__file__)[:-len("undoRead.py")]

try:
    f_user = open(MODULE_PATH[:-len("database/")] + ".user.config")
    username = f_user.readline().strip()
    f_user.close()
except:
    logging.error("No .user.config file!! Run the program with -conf flag to initialize the user.conif")
    sys.exit(-1)

def removeEvent(event_id, cur):
    cur.execute("SELECT id FROM nordic_header_main WHERE event_id = %s", (event_id,))
    mheader_ids = cur.fetchall()

    for mheader_id in mheader_ids:
        cur.execute("DELETE FROM nordic_header_error WHERE header_id = %s", (mheader_id,))

    cur.execute("DELETE FROM nordic_header_main WHERE event_id = %s", (event_id,))
    cur.execute("DELETE FROM nordic_header_comment WHERE event_id = %s", (event_id,))
    cur.execute("DELETE FROM nordic_header_waveform WHERE event_id = %s", (event_id,))
    cur.execute("DELETE FROM nordic_header_macroseismic WHERE event_id = %s", (event_id,))
    cur.execute("DELETE FROM nordic_phase_data WHERE event_id = %s", (event_id,))

    cur.execute("DELETE FROM nordic_modified WHERE replacement_event_id = %s RETURNING old_event_type, event_id", (event_id,))
    ans = cur.fetchone()

    if ans != None:
        cur.execute("UPDATE nordic_event SET event_type = %s WHERE id = %s", (ans[0], ans[1]))

    cur.execute("DELETE FROM nordic_event WHERE id = %s RETURNING nordic_file_id, root_id", (event_id,))
    ans = cur.fetchone()
    
    cur.execute("SELECT COUNT(*) FROM nordic_event WHERE nordic_file_id = %s", (ans[0],))
    if cur.fetchone()[0] == 0:
        cur.execute("DELETE FROM nordic_file WHERE id = %s", (ans[0],))

    cur.execute("SELECT COUNT(*) FROM nordic_event WHERE root_id = %s", (ans[1],))
    if cur.fetchone()[0] == 0:
        cur.execute("DELETE FROM nordic_event_root WHERE id = %s", (ans[1],))


def removeEventsWithCreationId(creation_id):
    print("Removing events with creation_id {0}".format(creation_id))
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return False

    cur = conn.cursor()
    
    cur.execute("SELECT id FROM nordic_event WHERE creation_id = %s", (creation_id,))

    ids = cur.fetchall()

    for event_id in ids:
        removeEvent(event_id[0], cur)

    cur.execute("DELETE FROM creation_id WHERE id = %s", (creation_id,))

    conn.commit()
    conn.close()

    return True

def undoMostRecent():
    try:
        conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
        return False

    cur = conn.cursor()
    
    cur.execute("SELECT id FROM creation_info ORDER BY creation_date DESC ")
    creation_id = cur.fetchone()

    if creation_id is None:
        logging.error("Database is empty!!")
        return

    cur.execute("SELECT id FROM nordic_event WHERE creation_id = %s", (creation_id,))

    ids = cur.fetchall()

    for event_id in ids:
        removeEvent(event_id[0], cur)

    cur.execute("DELETE FROM creation_info WHERE id = %s", (creation_id,))

    conn.commit()
    conn.close()

    return True


