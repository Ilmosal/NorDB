"""
This module contains all functions for reseting the database. Use the following commands with care as these operations are not reversible!
"""
import psycopg2

from nordb.database import norDBManagement
from nordb.core import usernameUtilities

def resetDatabase():
    """
    Function for clearing the database from all of its data

    """
    resetEvents()
    resetStations()

def resetEvents():
    """
    Function for clearing the database from all event data
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    cur.execute("DELETE FROM nordic_event_root")
    cur.execute("DELETE FROM nordic_file")
    try:
        cur.execute("ALTER SEQUENCE nordic_event_root_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE nordic_file_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE nordic_event_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE nordic_phase_data_id_seq RESTART WITH 1")   
        cur.execute("ALTER SEQUENCE nordic_header_main_id_seq RESTART WITH 1")  
        cur.execute("ALTER SEQUENCE nordic_header_comment_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE nordic_header_error_id_seq RESTART WITH 1") 
        cur.execute("ALTER SEQUENCE nordic_header_macroseismic_id_seq RESTART WITH 1")  
        cur.execute("ALTER SEQUENCE nordic_header_waveform_id_seq RESTART WITH 1")  
    except Exception as e:
        conn.close
        raise e

    conn.commit()
    conn.close()

def resetStations():
    """
    Function for clearing the database from all station and network data
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM response")
        cur.execute("DELETE FROM network")
        cur.execute("ALTER SEQUENCE instrument_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE sensor_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE response_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE fap_response_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE paz_response_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE sitechan_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE station_id_seq RESTART WITH 1")
        cur.execute("ALTER SEQUENCE network_id_seq RESTART WITH 1")
    except Exception as e:
        conn.close
        raise e
    conn.commit()
    conn.close()

