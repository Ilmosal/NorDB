"""
This module contains all necessary functions for handling network related information

Classes and Functions
---------------------
"""

from nordb.core import usernameUtilities
from nordb.database import creationInfo

def addNetwork(network_code, privacy_level, db_conn = None):
    """
    Function that adds a new network with network code network_code to the database.

    :param string network_code: Network code of the new network
    :param string privacy_level: Privacy level of the new network
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    cur.execute("SELECT network FROM network WHERE network=%s", (network_code,))
    ans = cur.fetchone()

    if ans is not None:
        raise Exception("Network with such name already exists")

    creation_id = creationInfo.createCreationInfo(privacy_level, db_conn = conn)

    cur.execute("INSERT INTO network (network, creation_id) VALUES (%s, %s)", (network_code, creation_id))

    conn.commit()

    if db_conn is None:
        conn.close()

def removeNetwork(network_code, db_conn = None):
    """
    Function for removing a network from the database.

    :param string network_code: Network code for the new network
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn
    cur = conn.cursor()
    cur.execute("SELECT network FROM network WHERE network=%s", (network_code,))
    ans = cur.fetchone()

    if len(ans) == 0:
        raise Exception("Network with such name does not exist")

    cur.execute("DELETE FROM network WHERE network = %s", (network_code,))

    conn.commit()

    if db_conn is None:
        conn.close()

def getNetworks(db_conn = None):
    """
    Function for returning all networks in a list to user.

    :returns: list of networks
    """
    if db_conn is None:
        conn = usernameUtilities.log2nordb()
    else:
        conn = db_conn

    cur = conn.cursor()

    cur.execute("SELECT network FROM network")
    ans = cur.fetchall()

    if len(ans) == 0:
        return []

    if db_conn is None:
        conn.close()

    return [network[0] for network in ans]
