import sys
import os 
import logging

os.chdir("..")
sys.path = sys.path + [""]

import nordb.database.initNorDB

if len(sys.argv) > 1:
	if sys.argv[1] == "-clear":
		nordb.database.initNorDB.destroy_database()
	elif sys.argv[1] == "-init":
		nordb.database.initNorDB.init_database()
	elif sys.argv[1] == "-h":
		print "help not yet implemented"
else:
	logging.error("No flags given for nordb. Type -h for help!")
