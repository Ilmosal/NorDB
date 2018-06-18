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
                "   fap, fap_response, response "
                "WHERE "
                "   response.id = %s AND "
                "   fap_response.response_id = response_id AND "
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
                "   real"
                )

SELECT_RESPONSE =   (
                    "SELECT "
                    "   response.id "
                    "FROM "
                    "   response, instrument, sitechan, station, sensor "
                    "WHERE "
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

def getResponseFromDB(response_id):
    """
    Function for reading a response from database by id

    :param int response_id: id of the Response wanted
    :returns: :class:`PazResponse` or :class:`FapResponse` object
    """
    conn = usernameUtilities.log2nordb()
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

    conn.close()
    return response

def getResponse(station, channel, date=datetime.datetime.now()):
    """
    Function for getting response information from the database.

    :param string station: Station code of the station
    :param string channel: Channel code of the channel
    :param datetime date: date for which you want the response
    :returns: Response object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    timestamp = time.mktime(date.timetuple())

    cur.execute(SELECT_RESPONSE, (station, channel, timestamp, timestamp,
                                  timestamp))
    resp_id = cur.fetchone()

    conn.close()

    if resp_id is None:
        return None

    return getResponseFromDB(resp_id[0])
