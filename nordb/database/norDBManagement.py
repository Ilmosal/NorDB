import sys
import os
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

MODULE_PATH = os.path.realpath(__file__)[:-len("norDBManagement.py")]

username = ""

from nordb.core import usernameUtilities

def create_database():
    username = usernameUtilities.readUsername()
    try:
        conn = psycopg2.connect("dbname=postgres user={0}".format(username))
    except:
        logging.error("Username is not correct! Reconfigure your username with -conf flag!")
        sys.exit()

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname='nordb'")
    if cur.fetchall():
        logging.error("Database already exists. Destroy the database with destroy and try again!")
        conn.close()
        sys.exit()

    cur.execute(open("nordb/sql/init_nordb.sql", "r").read())

    conn.commit()
    conn.close()

    conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    cur = conn.cursor()
    
    cur.execute(open("nordb/sql/nordic_event_root.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_file.sql", "r").read())
    cur.execute(open("nordb/sql/creation_info.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_event.sql", "r").read())
    cur.execute(open("nordb/sql/scandia_header.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_modified.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_header_main.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_header_comment.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_header_error.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_header_macroseismic.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_header_waveform.sql", "r").read())
    cur.execute(open("nordb/sql/nordic_phase_data.sql", "r").read())

    conn.commit()
    conn.close()

def destroy_database():
    username = usernameUtilities.readUsername()

    conn = psycopg2.connect("dbname=postgres user={0}".format(username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname='nordb'")
    if not cur.fetchall():
        logging.error("Database doesn't exists. Exiting program.")
        conn.close()
        sys.exit()

    conn.close()

    conn = psycopg2.connect("dbname=nordb user={0}".format(username))
    cur = conn.cursor()

    cur.execute("DROP SCHEMA public CASCADE")

    conn.commit()
    conn.close()


    conn = psycopg2.connect("dbname=postgres user={0}".format(username))
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("DROP DATABASE nordb")

    conn.commit()
    conn.close()

    pass
