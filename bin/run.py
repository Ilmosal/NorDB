#!/usr/bin/env python
import sys
import os 
import logging
import inspect

#FILE PATHS
MODULE_PATH = os.path.realpath(__file__)[:-6] + "/.."
USER_PATH = os.getcwd()

os.chdir(MODULE_PATH)
sys.path = sys.path + [""]

import nordb.database.initNorDB

#TODO
def print_help():
	pass

if len(sys.argv) > 1:
	if sys.argv[1] == "-clear":
		nordb.database.initNorDB.destroy_database()
	elif sys.argv[1] == "-init":
		nordb.database.initNorDB.init_database()
	elif sys.argv[1] == "-h":
		print_help()
	elif sys.argv[1] == "-conf":
		username = input("Give name for the postgres user: ")
		f = open(MODULE_PATH + "user.config", "w")
		f.write(username)
		f.close()
else:
	print("No flags given for nordb. Type -h for help!")
