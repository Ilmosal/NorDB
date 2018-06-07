"""
This module contains all functions and classes for reading a response file and pushing it into the database

Functions and Classes
---------------------
"""

from nordb.database import sitechan2sql
from nordb.core import usernameUtilities

RESPONSE_INSERT =   (
                    "INSERT INTO response "
                    "   (file_name, source, stage, description, "
                    "   format, author) "
                    "VALUES "
                    "   (%s, %s, %s, %s, %s, %s)"
                    "RETURNING id"
                    )

PAZ_RESPONSE_INSERT =   (
                        "INSERT INTO paz_response "
                        "   (response_id, scale_factor) "
                        "VALUES "
                        "   (%s, %s) "
                        "RETURNING id"
                        )

POLE_INSERT =   (
                "INSERT INTO pole "
                "   (real, imag, real_error, imag_error, paz_id) "
                "VALUES "
                "   (%s, %s, %s, %s, %s) "
                )

ZERO_INSERT =   (
                "INSERT INTO zero "
                "   (real, imag, real_error, imag_error, paz_id) "
                "VALUES "
                "   (%s, %s, %s, %s, %s) "
                )

FAP_RESPONSE_INSERT =   (
                        "INSERT INTO fap_response "
                        "   (response_id) "
                        "VALUES "
                        "   (%s) "
                        "RETURNING id"
                        )

FAP_INSERT =    (
                "INSERT INTO fap "
                "   (frequency, amplitude, phase, "
                "   amplitude_error, phase_error, fap_id) "
                "VALUES "
                "   (%s, %s, %s, %s, %s, %s)"
                )

def insertResponse2Database(response):
    """
    Function for inserting the response object to the database

    :param Response response: response that will be inserted to the database
    """
    conn = usernameUtilities.log2nordb()
    cur = conn.cursor()

    try:
        cur.execute(RESPONSE_INSERT, response.getAsList())
        response.response_id = cur.fetchone()[0]

        if response.response_format == 'fap':
            cur.execute(FAP_RESPONSE_INSERT, (response.response_id,))
            fap_id = cur.fetchone()[0]
            for fap in response.fap:
                cur.execute(FAP_INSERT, fap + [fap_id])

        elif response.response_format == 'paz':
            cur.execute(PAZ_RESPONSE_INSERT, (response.response_id, response.scale_factor))
            paz_id = cur.fetchone()[0]
            for pole in response.poles:
                cur.execute(POLE_INSERT, pole + [paz_id])
            for zero in response.zeros:
                cur.execute(ZERO_INSERT, zero + [paz_id])

        else:
            raise Exception("No such response format! ({0})".format(response.response_format))
    except Exception as e:
        conn.close()
        raise e
    conn.commit()
    conn.close()

