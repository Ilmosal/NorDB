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
                  1:"SELECT " +
                       "date, hour, minute, second, location_model, distance_indicator, " +
                       "event_desc_id, epicenter_latitude, epicenter_longitude, depth, " +
                       "depth_control, locating_indicator, epicenter_reporting_agency, " +
                       "stations_used, rms_time_residuals, " +
                       "magnitude_1, type_of_magnitude_1, magnitude_reporting_agency_1, " +
                       "magnitude_2, type_of_magnitude_2, magnitude_reporting_agency_2, " +
                       "magnitude_3, type_of_magnitude_3, magnitude_reporting_agency_3, " +
                       "event_id, id " +
                    "FROM " +
                       "nordic_header_main " +
                    "WHERE " +
                       "event_id = %s",
                  2:"SELECT " +
                       "description, diastrophism_code, tsunami_code, seiche_code, " +
                       "cultural_effects, unusual_effects, maximum_observed_intensity, " +
                       "maximum_intensity_qualifier, intensity_scale, macroseismic_latitude, " +
                       "macroseismic_longitude, macroseismic_magnitude, type_of_magnitude, " +
                       "logarithm_of_radius, logarithm_of_area_1, bordering_intensity_1, " +
                       "logarithm_of_area_2, bordering_intensity_2, quality_rank,  " +
                       "reporting_agency, event_id, id " +
                   "FROM " +
                       "nordic_header_macroseismic " +
                   "WHERE " +
                       "event_id = %s",
                  3:"SELECT " +
                       "h_comment, event_id, id " +
                    "FROM " +
                       "nordic_header_comment " +
                    "WHERE " +
                       "event_id = %s",
                  5:"SELECT " +
                       "gap, second_error, epicenter_latitude_error, epicenter_longitude_error, " +
                       "depth_error, magnitude_error, header_id, id " +
                    "FROM " +
                       "nordic_header_error " +
                    "WHERE " +
                       "header_id = %s",
                  6:"SELECT " +
                       "waveform_info, event_id, id " +
                    "FROM " +
                       "nordic_header_waveform " +
                    "WHERE " +
                       "event_id = %s",
                  8:"SELECT " +
                        "station_code, sp_instrument_type, sp_component, quality_indicator,  " +
                        "phase_type, weight, first_motion, time_info, hour, minute, second, " +
                        "signal_duration, max_amplitude, max_amplitude_period, back_azimuth, " +
                        "apparent_velocity, signal_to_noise, azimuth_residual, " +
                        "travel_time_residual, location_weight, epicenter_distance, " + 
                        "epicenter_to_station_azimuth, event_id, id " +
                     "FROM " +
                        "nordic_phase_data " +
                     "WHERE " +
                        "event_id = %s"
                }

def getNordicFromDB(event_id):
    """
    Method that reads a nordic event with id event_id from the database and creates NordicEvent object from the query

    :param int event_id: Event id of the event
    :returns: NordicEvent object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    headers = {1:[], 2:[], 3:[], 5:[], 6:[]}
    data = []
    main_ids = []

    cur.execute("SELECT id from nordic_event WHERE id = %s", (event_id,))
    ans = cur.fetchone()

    if not ans:
        return None

    cur.execute(SELECT_QUERY[NordicMain.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        main_ids.append(a[-1])
        headers[NordicMain.header_type].append(NordicMain(a))

    cur.execute(SELECT_QUERY[NordicMacroseismic.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        headers[NordicMacroseismic.header_type].append(NordicMacroseismic(a))

    cur.execute(SELECT_QUERY[NordicComment.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        headers[NordicComment.header_type].append(NordicComment(a))

    for m_id in main_ids:
        cur.execute(SELECT_QUERY[NordicError.header_type], (m_id,))
        ans = cur.fetchall()

        for a in ans:
            headers[NordicError.header_type].append(NordicError(a, -1))

    cur.execute(SELECT_QUERY[NordicWaveform.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        headers[NordicWaveform.header_type].append(NordicWaveform(a))
    
    cur.execute(SELECT_QUERY[NordicData.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        data.append(NordicData(a))

    return NordicEvent(headers, data, event_id)

