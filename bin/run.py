#!/usr/bin/env python3
import sys
import os 
import logging
import inspect
import fnmatch
import pkg_resources

version = "0.1.0"

#FILE PATHS
MODULE_PATH = os.path.realpath(__file__)[:-10]
USER_PATH = os.getcwd()

os.chdir(MODULE_PATH)
sys.path = sys.path + [""]

if len(sys.argv) > 1:
	if (sys.argv[1] == "-conf"):
		username = str(input("Give name for the postgres user: "))
		f = open(MODULE_PATH + "nordb/.user.config", "w")
		f.write(username)
		f.close()
		sys.exit()
else: 
	print("No flags given for nordb. Type -h for help!")
	sys.exit()

from nordb.database import initNorDB
from nordb.io import nordic2sql

#TODO
def print_help():
	print("")
	print("NORDB - Version: {0}".format(version))
	print("COMMANDS:")
	print("----------------------------------------------------------")
	print("filename | Add given file to the database. File must be in")
	print("         | nordic format described in the doc folder. File")
	print("         | extension must be .n, .[01-12]n, .nordic or    ")
	print("         | .nordicp. After filename you have to give the  ")
	print("         | file a tag(AOPRFS) which tells what is the     ")
	print("         | importance of the file                         ")
	print("----------------------------------------------------------")
	print("-init    | Initialize the database from scratch           ")
	print("----------------------------------------------------------")
	print("-destroy | Destroy the database                           ")
	print("----------------------------------------------------------")
	print("-conf    | Configure the user.config file. You must do    ")
	print("         | before doing anything. You must also configure ")
	print("         | your postgres to accept the username beforehand") 
	print("----------------------------------------------------------")
	print("-reset   | Reset database from all entries                ")
	print("----------------------------------------------------------")
	print("-h       | Print help")
	print("")


if sys.argv[1] == "-reset":
	nordic2sql.reset_database()
elif sys.argv[1] == "-destroy":
	initNorDB.destroy_database()
elif sys.argv[1] == "-init":
	initNorDB.init_database()
elif sys.argv[1] == "-h":
	print_help()
elif len(sys.argv) > 2:
	if not sys.argv[2] in "AOPRFS":
		print(sys.argv[2] + " is not a valid flag! Only A, O, P, R, F or S are allowed")
		sys.exit()
	else:
		event_id = sys.argv[2]
	print 
	if (fnmatch.fnmatch(sys.argv[1], "*.nordic") 
	or fnmatch.fnmatch(sys.argv[1], "*.nordicp") 
	or fnmatch.fnmatch(sys.argv[1], "*n")):
		try:
			f_nordic = open(USER_PATH  + "/" + sys.argv[1], 'r')
		except:
			print("No such file in current folder")
			sys.exit()
		
		nordic2sql.read_nordicp(f_nordic, event_id, True)
		f_nordic.close()
else:
	print("Not a valid command! Type -h for help.")
