import psycopg2
import logging

from nordb.core import nordic
from nordb.core.nordic import NordicWaveform

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
                  7:"SELECT " +
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

def readNordicEvent(cur, event_id):
    """
    Method that reads a nordic event with id event_id from the database and creates NordicEvent object from the query

    Args:
        cur (Cursor): psycopg2 cursor object
        event_id (int): event_id of the event that needs to be read

    Returns:
        NordicEvent object
    """
    headers = {1:[], 2:[], 3:[], 5:[], 6:[]}
    data = []
    main_ids = []

    cur.execute("SELECT id from nordic_event WHERE id = %s", (event_id,))
    ans = cur.fetchone()

    if not ans:
        logging.error("Event with id {0} does not exists!".format(event_id))

    cur.execute(SELECT_QUERY[nordic.NordicMain.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        main_ids.append(a[-1])
        headers[nordic.NordicMain.header_type].append(nordic.NordicMain(a))

    cur.execute(SELECT_QUERY[nordic.NordicMacroseismic.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        headers[nordic.NordicMacroseismic.header_type].append(nordic.NordicMacroseismic(a))

    cur.execute(SELECT_QUERY[nordic.NordicComment.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        headers[nordic.NordicComment.header_type].append(nordic.NordicComment(a))

    for m_id in main_ids:
        cur.execute(SELECT_QUERY[nordic.NordicError.header_type], (m_id,))
        ans = cur.fetchall()

        for a in ans:
            headers[nordic.NordicError.header_type].append(nordic.NordicError(a, m_id))

    cur.execute(SELECT_QUERY[nordic.NordicWaveform.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        headers[nordic.NordicWaveform.header_type].append(NordicWaveform(a))

    cur.execute(SELECT_QUERY[nordic.NordicData.header_type], (event_id,))
    ans = cur.fetchall()

    for a in ans:
        data.append(nordic.NordicData(a))

    return nordic.NordicEvent(headers, data, event_id)

