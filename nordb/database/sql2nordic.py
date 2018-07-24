"""
This module contains all functions for getting the nordic out from the database and creating NordicEvent object out of them.

Functions and Classes
---------------------
"""

import psycopg2
from nordb.core import usernameUtilities
from nordb.nordic.nordicEvent import NordicEvent
from nordb.nordic.nordicMain import NordicMain
from nordb.nordic.nordicMacroseismic import NordicMacroseismic
from nordb.nordic.nordicComment import NordicComment
from nordb.nordic.nordicError import NordicError
from nordb.nordic.nordicWaveform import NordicWaveform
from nordb.nordic.nordicData import NordicData

SELECT_QUERY =   {
                  0:(
                    "SELECT "
                    "   id, root_id, creation_id, nordic_file_id, solution_type, author_id "
                    "FROM "
                    "   nordic_event "
                    "WHERE id = %s"
                    ),
                  1:(
                    "SELECT "
                    "   origin_time, origin_date, location_model, distance_indicator, "
                    "   event_desc_id, epicenter_latitude, epicenter_longitude, depth, "
                    "   depth_control, locating_indicator, epicenter_reporting_agency, "
                    "   stations_used, rms_time_residuals, "
                    "   magnitude_1, type_of_magnitude_1, magnitude_reporting_agency_1, "
                    "   magnitude_2, type_of_magnitude_2, magnitude_reporting_agency_2, "
                    "   magnitude_3, type_of_magnitude_3, magnitude_reporting_agency_3, "
                    "   event_id, id "
                    "FROM "
                    "   nordic_header_main "
                    "WHERE "
                    "   event_id = %s"
                    ),
                  2:(
                    "SELECT "
                    "   description, diastrophism_code, tsunami_code, seiche_code, "
                    "   cultural_effects, unusual_effects, maximum_observed_intensity, "
                    "   maximum_intensity_qualifier, intensity_scale, macroseismic_latitude, "
                    "   macroseismic_longitude, macroseismic_magnitude, type_of_magnitude, "
                    "   logarithm_of_radius, logarithm_of_area_1, bordering_intensity_1, "
                    "   logarithm_of_area_2, bordering_intensity_2, quality_rank,  "
                    "   reporting_agency, event_id, id "
                    "FROM "
                    "   nordic_header_macroseismic "
                    "WHERE "
                    "   event_id = %s"
                    ),
                  3:(
                    "SELECT "
                    "   h_comment, event_id, id "
                    "FROM "
                    "   nordic_header_comment "
                    "WHERE "
                    "   event_id = %s"
                    ),
                  5:(
                    "SELECT "
                    "   gap, second_error, epicenter_latitude_error, epicenter_longitude_error, "
                    "   depth_error, magnitude_error, header_id, id "
                    "FROM "
                    "   nordic_header_error "
                    "WHERE "
                    "   header_id = %s"
                    ),
                  6:(
                    "SELECT "
                    "   waveform_info, event_id, id "
                    "FROM "
                    "   nordic_header_waveform "
                    "WHERE "
                    "   event_id = %s"
                    ),
                  8:(
                    "SELECT "
                    "   station_code, sp_instrument_type, sp_component, quality_indicator,  "
                    "   phase_type, weight, first_motion, observation_time, "
                    "   signal_duration, max_amplitude, max_amplitude_period, back_azimuth, "
                    "   apparent_velocity, signal_to_noise, azimuth_residual, "
                    "   travel_time_residual, location_weight, epicenter_distance, "
                    "   epicenter_to_station_azimuth, event_id, id "
                    "FROM "
                    "   nordic_phase_data "
                    "WHERE "
                    "   event_id = %s"
                    )
                }

SELECT_ROOT_ID =    (
                    "SELECT "
                    "   nordic_event.id "
                    "FROM "
                    "   nordic_event "
                    "WHERE "
                    "   nordic_event.root_id = %s"
                    )

SELECT_EVENT_ROOT_ID =  (
                        "SELECT "
                        "   nordic_event.root_id "
                        "FROM "
                        "   nordic_event "
                        "WHERE "
                        "   nordic_event.id = %s "
                        )

def getEventRootId(event_id, db_conn = None):
    """
    Function for getting nordic event root id from nordic event.

    :param int event_id: event_id of the event
    :returns: event root id as integer or None if event with event_id does not exist
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    cur.execute(SELECT_EVENT_ROOT_ID, (event_id,))
    ans = cur.fetchone()

    root_id = -1

    if ans is not None:
        root_id = ans[0]

    if db_conn is None:
        conn.close()

    return root_id

def getNordicsRoot(root_id, db_conn = None):
    """
    Method for getting all events attached to a root id from the database and returning them in a array.

    :param int root_id: root id of the event root you want to fetch
    :returns: Array of NordicEvent objects
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()
    cur.execute(SELECT_ROOT_ID, (root_id,))
    e_ids = cur.fetchall()
    conn.close()
    nordic_root = []

    e_ids = [e_id[0] for e_id in e_ids]

    nordics = getNordics(e_ids, db_conn = conn)

    if db_conn is None:
        conn.close()

    return nordics

def getNordics(event_ids, db_conn = None):
    """
    Method for getting multiple nordics from the database with a event_id array.

    :param Array event_ids: Array of event id integers you want as events
    :returns: Array of NordicEvent objects
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    events = []

    for e_id in event_ids:
        event = getNordic(e_id, db_conn = conn)
        if event is not None:
            events.append(event)

    if db_conn is None:
        conn.close()

    return events

def getNordic(event_id, db_conn = None):
    """
    Method that reads a nordic event with id event_id from the database and creates NordicEvent object from the query

    :param int event_id: Event id of the event
    :returns: NordicEvent object or None if no event is found
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    cur.execute(SELECT_QUERY[0], (event_id,))
    n_events = cur.fetchone()

    if not n_events:
        if db_conn is None:
            conn.close()
        return None

    event = NordicEvent(event_id, n_events[1], n_events[2], n_events[4])

    cur.execute(SELECT_QUERY[NordicMain.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        event.main_h.append(NordicMain(a))

    cur.execute(SELECT_QUERY[NordicMacroseismic.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        event.macro_h.append(NordicMacroseismic(a))

    cur.execute(SELECT_QUERY[NordicComment.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        event.comment_h.append(NordicComment(a))

    for main_h in event.main_h:
        cur.execute(SELECT_QUERY[5], (main_h.h_id,))
        ans = cur.fetchone()

        if ans is not None:
            main_h.error_h = NordicError(ans)

    cur.execute(SELECT_QUERY[NordicWaveform.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        event.waveform_h.append(NordicWaveform(a))

    cur.execute(SELECT_QUERY[NordicData.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        event.data.append(NordicData(a))

    if db_conn is None:
        conn.close()

    return event

