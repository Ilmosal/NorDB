import sys
import logger
import logger

#TODO: init_db
def init_database():
	pass

#TODO: destroy db
def destroy_database():
	pass

#TODO: help function
def print_help():
	pass

if __name__="__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] == "-d":
			logger.info("Destroying the database")
			destroy_database()
			logger.info("Database has been destroyed")
		elif sys.argv[1] == "-i"
			logger.info("Initializing the database")
			init_database()
			logger.info("Database has been Initialized")
		else:
			logger.error("No such flag. Type -h for help.")
			sys.exit()
	else:
		logger.error("No flag given for the program. Type -h for help")	
