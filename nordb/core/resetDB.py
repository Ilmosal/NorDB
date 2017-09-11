import logging
import time
import os
import sys

import psycopg2

MODULE_PATH = os.path.realpath(__file__)[:-len("resetDB.py")]

try:
	f_user = open(MODULE_PATH[:-len("core/")] + ".user.config")
	username = f_user.readline().strip()
	f_user.close()
except:
	logging.error("No .user.config file!! Run the program with -conf flag to initialize the user.conf")
	sys.exit(-1)


#Clearing the database
def reset_database():
	try:
		conn = psycopg2.connect("dbname = nordb user={0}".format(username))
	except:
		logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid!")
		return 

	cur = conn.cursor()

	start =  time.time()
	print("Resetting database: ")
	print("-------------------")
	print("Clearing nordic_phase_data...")
	cur.execute("DELETE FROM nordic_phase_data")
	print("Clearing nordic_header_comment...")
	cur.execute("DELETE FROM nordic_header_comment")	
	print("Clearing nordic_header_error...")
	cur.execute("DELETE FROM nordic_header_error")
	print("Clearing nordic_header_macroseismic...")
	cur.execute("DELETE FROM nordic_header_macroseismic")	
	print("Clearing nordic_header_waveform...")
	cur.execute("DELETE FROM nordic_header_waveform")
	print("Clearing nordic_header_main...")
	cur.execute("DELETE FROM nordic_header_main")	
	print("Clearing nordic_modified...")
	cur.execute("DELETE FROM nordic_modified")	
	print("Clearing scandia_header")
	cur.execute("DELETE FROM scandia_header")
	print("Clearing nordic_event")
	cur.execute("DELETE FROM nordic_event")
	print("Clearing nordic_file")
	cur.execute("DELETE FROM nordic_file")
	print("Clearing nordic_event_root")
	cur.execute("DELETE FROM nordic_event_root")

	print ("Altering sequence ids")
	cur.execute("ALTER SEQUENCE nordic_event_root_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_file_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_event_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_modified_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE scandia_header_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_phase_data_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_main_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_comment_id_seq RESTART WITH 1")
	cur.execute("ALTER SEQUENCE nordic_header_error_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_macroseismic_id_seq RESTART WITH 1")	
	cur.execute("ALTER SEQUENCE nordic_header_waveform_id_seq RESTART WITH 1")	
	
	end = time.time() - start

	print("All done! Time taken: {0} seconds!".format(end))

	conn.commit()
	conn.close()


