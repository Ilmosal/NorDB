"""
This module contains all information for getting the response information out of the database. 

Functions and Classes
---------------------
"""


from nordb.database import sql2instrument
from nordb.core import usernameUtilities
from nordb.nordic.response import FapResponse, PazResponse

SELECT_RESPONSE =   (   
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
                "   frequency, amplitude, phase, frequency_error, amplitude_error "
                "FROM "
                "   fap, fap_response, response "
                "WHERE "
                "   response.id = %s AND "
                "   fap_response.response_id = response_id AND "
                "   fap.fap_id = fap_response.id "
                )

SELECT_PAZ =    (
                "SELECT "
                "   scale_factor "
                "FROM "
                "   paz_response, response "
                "WHERE "
                "   paz_response.response_id = response.id"
                )

SELECT_POLES =  (
                "SELECT "
                "   real, imag, real_error, imag_error "
                "FROM "
                "   pole, paz_response, response "
                "WHERE "
                "   response.id = %s AND "
                "   pole.paz_id = paz_response.id AND "
                "   paz_response.response_id = response.id"
                )

SELECT_ZEROS =  (
                "SELECT "
                "   real, imag, real_error, imag_error "
                "FROM "
                "   zero, paz_response, response "
                "WHERE "
                "   response.id = %s AND "
                "   zero.paz_id = paz_response.id AND "
                "   paz_response.response_id = response.id"
                )

def getResponse(response_id):
    """
    Function for reading a response from database by id 

    :param int response_id: id of the Response wanted
    :returns: :class:`PazResponse` or :class:`FapResponse` object
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    response = None

    cur.execute(SELECT_RESPONSE, (response_id, ))
    response_data = cur.fetchone()

    if response_data[FapResponse.RESPONSE_FORMAT] == 'fap':
        cur.execute(SELECT_FAP, (response_id,))
        fap = cur.fetchall()

        response = FapResponse(response_data, fap)
    elif response_data[FapResponse.RESPONSE_FORMAT] == 'paz':
        cur.execute(SELECT_PAZ, (response_id,))
        scale_factor = cur.fetchone()[0]

        cur.execute(SELECT_POLES, (response_id,))
        poles = cur.fetchall()

        cur.execute(SELECT_POLES, (response_id,))
        zeros = cur.fetchall()

        response = PazResponse(response_data, scale_factor, poles, zeros)

    conn.close()
    return response
