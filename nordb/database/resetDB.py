"""
This module contains all functions for reseting the database. Use the following commands with care as these operations are not reversible!
"""

import logging
import time
import os
import sys

import psycopg2

from nordb.core import usernameUtilities

def resetDatabase():
    """
    Function for clearing the database from all of its data

    :returns: bool -- the return code, which tells if the operation was succesful or not
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    start =  time.time()
    print("Resetting database: ")
    print("-------------------")
    print("Clearing sensor...")
    cur.execute("DELETE FROM sensor")
    print("Clearing instrument_css_link...")
    cur.execute("DELETE FROM instrument_css_link")
    print("Clearing instrument...")
    cur.execute("DELETE FROM instrument")
    print("Clearing sitechan_css_link...")
    cur.execute("DELETE FROM sitechan_css_link")
    print("Clearing sitechan...")
    cur.execute("DELETE FROM sitechan")
    print("Clearing station...")
    cur.execute("DELETE FROM station")
    print("Clearing network...")
    cur.execute("DELETE FROM network")
    print("Clearing nordic_phase_data...")
    cur.execute("DELETE FROM nordic_phase_data")
    print("Clearing nordic_header_comment...")
    cur.execute("DELETE FROM nordic_header_comment")    
    print("Clearing nordic_header_error...")
    cur.execute("DELETE FROM nordic_header_error")
    print("Clearing nordic_header_macroseismic...")
    cur.execute("DELETE FROM nordic_header_macroseismic")   
    print("Clearing nordic_header_waveform...")
    cur.execute("DELETE FROM nordic_header_waveform")
    print("Clearing nordic_header_main...")
    cur.execute("DELETE FROM nordic_header_main")   
    print("Clearing nordic_modified...")
    cur.execute("DELETE FROM nordic_modified")  
    print("Clearing scandia_header")
    cur.execute("DELETE FROM scandia_header")
    print("Clearing nordic_event")
    cur.execute("DELETE FROM nordic_event")
    print("Clearing nordic_file")
    cur.execute("DELETE FROM nordic_file")
    print("Clearing creation_info")
    cur.execute("DELETE FROM creation_info")
    print("Clearing nordic_event_root")
    cur.execute("DELETE FROM nordic_event_root")

    print ("Altering sequence ids")
    cur.execute("ALTER SEQUENCE nordic_event_root_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE creation_info_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_file_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_event_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_modified_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE scandia_header_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_phase_data_id_seq RESTART WITH 1")   
    cur.execute("ALTER SEQUENCE instrument_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE sensor_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE sitechan_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE station_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE network_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_header_main_id_seq RESTART WITH 1")  
    cur.execute("ALTER SEQUENCE nordic_header_comment_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_header_error_id_seq RESTART WITH 1") 
    cur.execute("ALTER SEQUENCE nordic_header_macroseismic_id_seq RESTART WITH 1")  
    cur.execute("ALTER SEQUENCE nordic_header_waveform_id_seq RESTART WITH 1")  
    
    end = time.time() - start

    print("All done! Time taken: {0} seconds!".format(end))

    conn.commit()
    conn.close()

    return True

def resetEvents():
    """
    Function for clearing the database from all event data

    :returns: bool -- the return code, which tells if the operation was successful or not
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    start =  time.time()
    print("Resetting database: ")
    print("-------------------")
    print("Clearing nordic_phase_data...")
    cur.execute("DELETE FROM nordic_phase_data")
    print("Clearing nordic_header_comment...")
    cur.execute("DELETE FROM nordic_header_comment")    
    print("Clearing nordic_header_error...")
    cur.execute("DELETE FROM nordic_header_error")
    print("Clearing nordic_header_macroseismic...")
    cur.execute("DELETE FROM nordic_header_macroseismic")   
    print("Clearing nordic_header_waveform...")
    cur.execute("DELETE FROM nordic_header_waveform")
    print("Clearing nordic_header_main...")
    cur.execute("DELETE FROM nordic_header_main")   
    print("Clearing nordic_modified...")
    cur.execute("DELETE FROM nordic_modified")  
    print("Clearing scandia_header")
    cur.execute("DELETE FROM scandia_header")
    print("Clearing nordic_event")
    cur.execute("DELETE FROM nordic_event")
    print("Clearing nordic_file")
    cur.execute("DELETE FROM nordic_file")
    print("Clearing creation_info")
    cur.execute("DELETE FROM creation_info")
    print("Clearing nordic_event_root")
    cur.execute("DELETE FROM nordic_event_root")

    print ("Altering sequence ids")
    cur.execute("ALTER SEQUENCE nordic_event_root_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE creation_info_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_file_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_event_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_modified_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE scandia_header_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_phase_data_id_seq RESTART WITH 1")   
    cur.execute("ALTER SEQUENCE nordic_header_main_id_seq RESTART WITH 1")  
    cur.execute("ALTER SEQUENCE nordic_header_comment_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE nordic_header_error_id_seq RESTART WITH 1") 
    cur.execute("ALTER SEQUENCE nordic_header_macroseismic_id_seq RESTART WITH 1")  
    cur.execute("ALTER SEQUENCE nordic_header_waveform_id_seq RESTART WITH 1")  
    
    end = time.time() - start

    print("All done! Time taken: {0} seconds!".format(end))

    conn.commit()
    conn.close()

    return True

def resetStations():
    """
    Function for clearing the database from all station and networ kdata

    :returns: bool -- the return code which tells the user if the operation was successful or not
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    start =  time.time()

    print("Resetting database: ")
    print("-------------------")
    print("Clearing station...")
    cur.execute("DELETE FROM sensor")
    print("Clearing instrument_css_link...")
    cur.execute("DELETE FROM instrument_css_link")    
    print("Clearing instrument...")
    cur.execute("DELETE FROM instrument")
    print("Clearing sitechan_css_link...")
    cur.execute("DELETE FROM sitechan_css_link")
    print("Clearing sitechan...")
    cur.execute("DELETE FROM sitechan")
    print("Clearing station...")
    cur.execute("DELETE FROM station")
    print("Clearing network...")
    cur.execute("DELETE FROM network")
   
    print("Altering Sequence ids")
    cur.execute("ALTER SEQUENCE instrument_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE sensor_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE sitechan_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE station_id_seq RESTART WITH 1")
    cur.execute("ALTER SEQUENCE network_id_seq RESTART WITH 1")

    end = time.time() - start

    print("All done! Time taken: {0} seconds!".format(end))

    conn.commit()
    conn.close()

    return True

