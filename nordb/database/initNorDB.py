import sys
import os
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

MODULE_PATH = os.path.realpath(__file__)[:-len("initnordb.py")]

try:
	f_user = open(MODULE_PATH[:-len("database/")] + "user.config")
	username = f_user.readline()[:-1]
	f_user.close()
except:
	logging.error("No user.config file!! Run the program with -conf flag to initialize the user.conif")
	sys.exit(-1)

def init_database():
	conn = psycopg2.connect("dbname=postgres user={0}".format(username))
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()

	cur.execute("SELECT 1 FROM pg_database WHERE datname='nordb'")
	if cur.fetchall():
		logging.error("Database already exists. Destroy the database with -clear and try again!")
		conn.close()
		sys.exit()

	cur.execute(open("nordb/nordsql/init_nordb.sql", "r").read())

	conn.commit()
	conn.close()

	conn = psycopg2.connect("dbname=nordb user={0}".format(username))
	cur = conn.cursor()
	
	cur.execute(open("nordb/nordsql/nordic_event_root.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_file.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_event.sql", "r").read())
	cur.execute(open("nordb/nordsql/scandia_header.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_modified.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_header_main.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_header_error.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_header_macroseismic.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_header_waveform.sql", "r").read())
	cur.execute(open("nordb/nordsql/nordic_phase_data.sql", "r").read())

	conn.commit()
	conn.close()

def destroy_database():
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

if __name__ == "__main__":
	#go to main dir
	os.chdir("../..")

	if len(sys.argv) > 1:
		if sys.argv[1] == "-d":
			logging.info("Destroying the database")
			destroy_database()
			logging.info("Database has been destroyed")
		elif sys.argv[1] == "-i":
			logging.info("Initializing the database")
			init_database()
			logging.info("Database has been Initialized")
	else:
		logging.error("No flag given for the program. Type -h for help")	
