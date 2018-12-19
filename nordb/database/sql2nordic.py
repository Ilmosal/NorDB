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
                    "WHERE id in %s"
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
                    "   event_id in %s"
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
                    "   event_id in %s"
                    ),
                  3:(
                    "SELECT "
                    "   h_comment, event_id, id "
                    "FROM "
                    "   nordic_header_comment "
                    "WHERE "
                    "   event_id in %s"
                    ),
                  5:(
                    "SELECT "
                    "   gap, second_error, epicenter_latitude_error, epicenter_longitude_error, "
                    "   depth_error, magnitude_error, nordic_header_error.header_id, "
                    "   nordic_header_error.id, event_id "
                    "FROM "
                    "   nordic_header_error, nordic_header_main "
                    "WHERE "
                    "   header_id in %s "
                    "AND "
                    "   header_id = nordic_header_main.id "
                    ),
                  6:(
                    "SELECT "
                    "   waveform_info, event_id, id "
                    "FROM "
                    "   nordic_header_waveform "
                    "WHERE "
                    "   event_id in %s"
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
                    "   event_id in %s"
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

    nordics = getNordic(e_ids, db_conn = conn)

    if db_conn is None:
        conn.close()

    return nordics

def getNordic(event_id, db_conn = None):
    """
    Method that reads a nordic event with id event_id from the database and creates NordicEvent object from the query

    :param list int event_id: Event id of the event or list of event_ids
    :returns: List of NordicEvent objects or an empty list if none are found
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    if isinstance(event_id, int):
        event_ids = tuple([event_id])
    elif isinstance(event_id, list):
        event_ids = tuple(event_id)
    elif isinstance(event_id, tuple):
        event_ids = event_id
    else:
        conn.close()
        raise Exception('event_id is not in a integer or list!')

    if len(event_ids) == 0:
        if db_conn is None:
            conn.close()
        return []

    cur.execute(SELECT_QUERY[0], (event_ids,))
    n_events = cur.fetchall()

    if not n_events:
        if db_conn is None:
            conn.close()
        return []

    nordic_events = {}

    for n_event in n_events:
        nordic_events[n_event[0]] = NordicEvent(n_event[0], n_event[1], n_event[2], n_event[4])

    cur.execute(SELECT_QUERY[NordicMain.header_type], (event_ids,))
    ans = cur.fetchall()

    main_ids = []

    for a in ans:
       nordic_events[a[-2]].main_h.append(NordicMain(a))
       main_ids.append(a[-1])

    main_ids = tuple(main_ids)

    cur.execute(SELECT_QUERY[NordicMacroseismic.header_type], (event_ids,))
    ans = cur.fetchall()

    for a in ans:
        nordic_events[a[-2]].macro_h.append(NordicMacroseismic(a))

    cur.execute(SELECT_QUERY[NordicComment.header_type], (event_ids,))
    ans = cur.fetchall()

    for a in ans:
        nordic_events[a[-2]].comment_h.append(NordicComment(a))

    cur.execute(SELECT_QUERY[NordicError.header_type], (main_ids, ))
    ans = cur.fetchall()

    for a in ans:
        for main_h in nordic_events[a[-1]].main_h:
            if main_h.h_id == a[-2]:
                main_h.error_h = NordicError(a[:-1])
                break

    cur.execute(SELECT_QUERY[NordicWaveform.header_type], (event_ids,))
    ans = cur.fetchall()

    for a in ans:
        nordic_events[a[-2]].waveform_h.append(NordicWaveform(a))

    cur.execute(SELECT_QUERY[NordicData.header_type], (event_ids,))
    ans = cur.fetchall()

    for a in ans:
        nordic_events[a[-2]].data.append(NordicData(a))

    if db_conn is None:
        conn.close()

    return list(nordic_events.values())
