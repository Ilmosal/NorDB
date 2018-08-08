"""
This module contains all information for getting the response information out
of the database.

Functions and Classes
---------------------
"""

import datetime
import time

from nordb.core import usernameUtilities
from nordb.nordic.response import FapResponse, PazResponse

SELECT_RESPONSE_ID =    (
                        "SELECT "
                        "   file_name, source, stage, description, "
                        "   format, author, id "
                        "FROM "
                        "   response "
                        "WHERE "
                        "   id = %s"
                        )

SELECT_FAP =    (
                "SELECT "
                "   frequency, amplitude, phase, amplitude_error, phase_error "
                "FROM "
                "   fap, fap_response "
                "WHERE "
                "   response_id = %s AND "
                "   fap.fap_id = fap_response.id "
                "ORDER BY "
                "   frequency "
                )

SELECT_PAZ =    (
                "SELECT "
                "   scale_factor "
                "FROM "
                "   paz_response, response "
                "WHERE "
                "   paz_response.response_id = response.id "
                "AND "
                "   response.id = %s"
                )

SELECT_POLES =  (
                "SELECT "
                "   real, imag, real_error, imag_error "
                "FROM "
                "   pole, paz_response, response "
                "WHERE "
                "   response.id = %s AND "
                "   pole.paz_id = paz_response.id AND "
                "   paz_response.response_id = response.id "
                "ORDER BY "
                "   real "
                )

SELECT_ZEROS =  (
                "SELECT "
                "   real, imag, real_error, imag_error "
                "FROM "
                "   zero, paz_response, response "
                "WHERE "
                "   response.id = %s AND "
                "   zero.paz_id = paz_response.id AND "
                "   paz_response.response_id = response.id "
                "ORDER BY "
                "   ABS(real) DESC"
                )

SELECT_RESPONSE =   (
                    "SELECT "
                    "   response.id "
                    "FROM "
                    "   response, instrument, sitechan, station, sensor "
                    "WHERE496, "
                    "   response.id = instrument.response_id AND "
                    "   instrument.id = sensor.instrument_id AND "
                    "   sensor.sitechan_id = sitechan.id AND "
                    "   sitechan.station_id = station.id AND "
                    "   station_code = %s AND "
                    "   sitechan.channel_code = %s AND "
                    "   ("
                    "       (sensor.time <= %s AND sensor.endtime >= %s) "
                    "   OR "
                    "       (sensor.time <= %s AND sensor.endtime IS NULL) "
                    "   )"
                    )

SELECT_RESPONSES =  (
                    "SELECT "
                    "   response.file_name, response.source, "
                    "   response.stage, response.description, "
                    "   response.format, response.author, response.id, "
                    "   sitechan.station_id, sitechan.id, sensor.id "
                    "FROM "
                    "   response, instrument, sitechan, sensor "
                    "WHERE "
                    "   (sitechan.station_id, instrument.id) IN %(instrument_ids)s AND "
                    "   response.id = instrument.response_id AND "
                    "   instrument.id = sensor.instrument_id AND "
                    "   sensor.sitechan_id = sitechan.id"
                    )

SELECT_FAPS =   (
                "SELECT "
                "   frequency, amplitude, phase, amplitude_error, phase_error, "
                "   response_id "
                "FROM "
                "   fap, fap_response "
                "WHERE "
                "   response_id IN %(response_ids)s AND "
                "   fap.fap_id = fap_response.id "
                "ORDER BY "
                "   frequency "
                )

SELECT_PAZS =   (
                "SELECT "
                "   scale_factor, response_id "
                "FROM "
                "   paz_response, response "
                "WHERE "
                "   paz_response.response_id = response.id "
                "AND "
                "   response.id IN %(response_ids)s"
                )

SELECT_ALL_POLES =  (
                    "SELECT "
                    "   real, imag, real_error, imag_error, response_id "
                    "FROM "
                    "   pole, paz_response, response "
                    "WHERE "
                    "   response.id IN %(response_ids)s AND "
                    "   pole.paz_id = paz_response.id AND "
                    "   paz_response.response_id = response.id "
                    "ORDER BY "
                    "   real "
                    )

SELECT_ALL_ZEROS =  (
                    "SELECT "
                    "   real, imag, real_error, imag_error, response_id "
                    "FROM "
                    "   zero, paz_response, response "
                    "WHERE "
                    "   response.id IN %(response_ids)s AND "
                    "   zero.paz_id = paz_response.id AND "
                    "   paz_response.response_id = response.id "
                    "ORDER BY "
                    "   real"
                    )


def responses2stations(stations, db_conn = None):
    """
    Function for attaching responses to station information

    :param Dict stations: Dictionary of stations with station id as first parameter
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    try:
        instrument_ids = []

        for stat in stations.values():
            for sitechan in stat.sitechans:
                for sensor in sitechan.sensors:
                    instrument_ids.append((stat.s_id, sensor.instrument_id))

        instrument_ids = tuple(instrument_ids)

        if len(instrument_ids) == 0:
            if db_conn is None:
                conn.close()
            return

        cur = conn.cursor()

        cur.execute(SELECT_RESPONSES, {'instrument_ids':instrument_ids})

        ans = cur.fetchall()
        responses = []
        response_ids = []

        for a in ans:
            responses.append([a[-3], a[-2], a[-1], a[:-3]])
            response_ids.append(a[-4])

        response_ids = tuple(response_ids)

        cur.execute(SELECT_FAPS, {'response_ids':response_ids})
        fap_resp = cur.fetchall()
        cur.execute(SELECT_PAZS, {'response_ids':response_ids})
        paz_resp = cur.fetchall()
        cur.execute(SELECT_ALL_POLES, {'response_ids':response_ids})
        poles_resp = cur.fetchall()
        cur.execute(SELECT_ALL_ZEROS, {'response_ids':response_ids})
        zeros_resp = cur.fetchall()

        for resp in responses:
            for sitechan in stations[resp[0]].sitechans:
                for sen in sitechan.sensors:
                    for instrument in sen.instruments:
                        if instrument.response_id == resp[-1][-1]:
                            if resp[-1][4] == 'fap':
                                faps = []
                                for f in fap_resp:
                                    if f[-1] == resp[-1][-1]:
                                        faps.append(f[:-1])
                                instrument.response = FapResponse(resp[-1], faps)

                            elif resp[-1][4] == 'paz':
                                poles = []
                                zeros = []
                                for pole in poles_resp:
                                    if pole[-1] == resp[-1][-1]:
                                        poles.append(pole[:-1])
                                for zero in zeros_resp:
                                    if zero[-1] == resp[-1][-1]:
                                        zeros.append(zero[:-1])
                                for paz in paz_resp:
                                    if paz[-1] == resp[-1][-1]:
                                        instrument.response = PazResponse(resp[-1],
                                                                        paz[0],
                                                                        poles,
                                                                        zeros)
                                        break

    except Exception as e:
        conn.close()
        raise e

    if db_conn is None:
        conn.close()

def getResponseFromDB(response_id, db_conn = None):
    """
    Function for reading a response from database by id

    :param int response_id: id of the Response wanted
    :returns: :class:`PazResponse` or :class:`FapResponse` object
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    response = None

    cur.execute(SELECT_RESPONSE_ID, (response_id, ))
    response_data = cur.fetchone()

    if response_data is None:
        return None

    if response_data[FapResponse.RESPONSE_FORMAT] == 'fap':
        cur.execute(SELECT_FAP, (response_id,))
        fap = cur.fetchall()
        response = FapResponse(response_data, fap)

    elif response_data[FapResponse.RESPONSE_FORMAT] == 'paz':
        cur.execute(SELECT_PAZ, (response_id,))
        scale_factor = cur.fetchone()[0]

        cur.execute(SELECT_POLES, (response_id,))
        poles = cur.fetchall()

        cur.execute(SELECT_ZEROS, (response_id,))
        zeros = cur.fetchall()

        response = PazResponse(response_data, scale_factor, poles, zeros)


    if db_conn is None:
        conn.close()
    return response

def getResponse(station, channel, date=datetime.datetime.now(), db_conn = None):
    """
    Function for getting response information from the database.

    :param string station: Station code of the station
    :param string channel: Channel code of the channel
    :param datetime date: date for which you want the response
    :returns: Response object
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    timestamp = time.mktime(date.timetuple())

    cur.execute(SELECT_RESPONSE, (station, channel, timestamp, timestamp,
                                  timestamp))
    resp_id = cur.fetchone()

    if resp_id is None:
        return None

    response = getResponseFromDB(resp_id[0], conn)

    if db_conn is None:
        conn.close()

    return response
