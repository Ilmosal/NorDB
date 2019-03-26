"""
This module handles all operations done to creation info table

Functions and Classes
---------------------
"""
from nordb.core import usernameUtilities
from nordb.nordic.misc import CreationInfo

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

SELECT_CREATION_INFO =  (
                        "SELECT "
                        "   id, creation_date, owner, privacy_setting, creation_comment "
                        "FROM "
                        "   creation_info "
                        "WHERE "
                        "   id IN %s "
                        )

def getCreationInfo(creation_ids, db_conn = None):
    """
    Function for fetching CreationInfo entries from the database and returning them as a dict

    :params list creation_ids: list of ids to be fetched from the database
    :returns: dict of CreationInfo objects with the creation_id being the key
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()

    creation_ids = tuple(set(creation_ids))

    cur.execute(SELECT_CREATION_INFO, (creation_ids,))
    ans = cur.fetchall()

    creation_info = {}

    for a in ans:
        creation_info[a[0]] = CreationInfo(a[2], a[0], a[1], a[3], a[4])

    if db_conn is None:
        conn.close()

    return creation_info

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
        conn = db_conn
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

