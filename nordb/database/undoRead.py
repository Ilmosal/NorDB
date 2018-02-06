"""
This module contains the undo functions for the database.

Functions and Classes
---------------------
"""
import psycopg2
import logging
import os

from nordb.core import usernameUtilities

def removeEvent(event_id, cur):
    """
    Method for removing a event from the database.

    :param int event_id: the id of the event that needs to be removed
    :param psycopg2.cursor cur: cursor object that executes the operations
    """
    cur.execute("SELECT id FROM nordic_event WHERE id = %s", (event_id,))
    if cur.fetchone() is None:
        raise Exception("No such event in the database")

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
    """
    Method that removes all the events that correspond to a creation id. Operation also destroys the creation info of the creation_id.

    :param int creation_id: creation id that needs to be cleared
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM nordic_event WHERE creation_id = %s", (creation_id,))

    ids = cur.fetchall()

    for event_id in ids:
        removeEvent(event_id[0], cur)

    cur.execute("DELETE FROM creation_id WHERE id = %s", (creation_id,))

    conn.commit()
    conn.close()

def undoMostRecent():
    """
    Method that removes the most recent additions to the database based on creation_info table
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    
    cur.execute("SELECT id FROM creation_info ORDER BY creation_date DESC ")
    creation_id = cur.fetchone()

    if creation_id is None:
        raise Exception("No creation ids")

    cur.execute("SELECT id FROM nordic_event WHERE creation_id = %s", (creation_id,))

    ids = cur.fetchall()

    for event_id in ids:
        removeEvent(event_id[0], cur)

    cur.execute("DELETE FROM creation_info WHERE id = %s", (creation_id,))

    conn.commit()
    conn.close()


