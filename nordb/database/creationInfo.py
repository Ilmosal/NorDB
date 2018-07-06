"""
This module handles all operations done to creation info table

Functions and Classes
---------------------
"""
import psycopg2
from nordb.core import usernameUtilities

CREATE_CREATION_INFO =  (
                        "INSERT INTO  " 
                        "   creation_info  " 
                        "   (privacy_setting)  "
                        "VALUES " 
                        "   (%s) "
                        "RETURNING id"
                        )

DELETE_UNNECESSARY_CREATION_INFO =  (
                                    "SELECT "
                                    "   COUNT(*) "
                                    "FROM " 
                                    "   creation_info "
                                    "LEFT JOIN nordic_event ON"
                                    "       nordic_event.creation_id = creation_info.id "
                                    "LEFT JOIN solution_type ON"
                                    "       solution_type.creation_id = creation_info.id "
                                    "LEFT JOIN network ON"
                                    "       network.creation_id = creation_info.id "
                                    "WHERE "
                                    "   creation_info.id = %s"
                                    "AND "
                                    "   ("
                                    "   nordic_event.id IS NOT NULL OR "
                                    "   solution_type IS NOT NULL OR"
                                    "   network.id IS NOT NULL "
                                    "   )"
                                    )

def createCreationInfo(privacy_level, db_conn = None):
    """
    Function for creating the creation_info entry to the database.

    :params privacy_level str: privacy level of the creation info object. Possible values are: private, public, secure
    :returns: The creation id of the creation_info entry created
    """
    creation_id = -1
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn()
    cur = conn.cursor()

    if privacy_level not in ["public", "secure", "private"]:
        raise Exception("Privacy level not a valid privacy level! ({0})".format(privacy_level))

    cur.execute(CREATE_CREATION_INFO, (privacy_level,))
    creation_id = cur.fetchone()[0]

    conn.commit()

    if db_conn is None:
        conn.close()

    return creation_id

def deleteCreationInfoIfUnnecessary(creation_id, db_conn = None):
    """
    Function for deleting an unnecessary creation info object

    :param int creation_id: id of the creation_info that needs to be deleted
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    cur.execute(DELETE_UNNECESSARY_CREATION_INFO, (creation_id,))

    if cur.fetchone()[0] != 0:
        if db_conn is None:
            conn.close()
        return

    cur.execute("DELETE FROM creation_info WHERE id = %s", (creation_id,))


    conn.commit()

    if db_conn is None:
        conn.close()

