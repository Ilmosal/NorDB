#!/usr/bin/env python
import sys
import os 
import logging
import inspect
import fnmatch

#FILE PATHS
MODULE_PATH = os.path.realpath(__file__)[:-6] + "/.."
USER_PATH = os.getcwd()

os.chdir(MODULE_PATH)
sys.path = sys.path + [""]

from nordb.database import initNorDB
from nordb.io import nordic2sql

#TODO
def print_help():
	pass

if len(sys.argv) > 1:
	if sys.argv[1] == "-clear":
		initNorDB.destroy_database()
	elif sys.argv[1] == "-init":
		initNorDB.init_database()
	elif sys.argv[1] == "-h":
		print_help()
	elif sys.argv[1] == "-conf":
		username = input("Give name for the postgres user: ")
		f = open(MODULE_PATH + "user.config", "w")
		f.write(username)
		f.close()
	elif sys.argv[1] == "-a":
		if len(sys.argv) > 3:
			if not sys.argv[2] in "OPRFS":
				print(sys.argv[2] + " is not a valid flag! Only O, P, R, F or S are allowed")
				sys.exit()
			else:
				event_id = sys.argv
			if (fnmatch.fnmatch(sys.argv[3], "*.nordic") 
			or fnmatch.fnmatch(sys.argv[3], "*.nordicp") 
			or fnmatch.fnmatch(sys.argv[3], "*.n")):
				try:
					print(USER_PATH + sys.argv[3])
					f_nordic = open(USER_PATH  + "/" + sys.argv[3], 'r')
				except:
					print("No such file in current folder")
					sys.exit()
	
				nordic2sql.read_nordicp(f_nordic, event_id, True)

				f_nordic.close()
		else:
			print("No nordic file given to the program! Is your file extension .nordic .nordicp or .n?");
else:
	print("No flags given for nordb. Type -h for help!")
