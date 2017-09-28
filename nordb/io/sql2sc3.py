from lxml import etree
import logging
import sys
import os

import psycopg2

MODULE_PATH = os.path.realpath(__file__)[:-len("sql2sc3.py")]

try:
	f_user = open(MODULE_PATH[:-len("io/")] + ".user.config")
	username = f_user.readline().strip()
	f_user.close()
except:
	logging.error("No .user.config file!! Run the program with -conf flag to initialize the .user.conf")


from nordb.core import nordicHandler
from nordb.io import sql2quakeml

def writeSC3(nordicEventId, usr_path):
	try:
		int(nordicEventId)
	except:
		logging.error("Argument {0} is not  a valid event id!".format(nordicEventId))
		return False

	try:
		conn = psycopg2.connect("dbname = nordb user={0}".format(username))
	except:
		logging.error("Couldn't connect to database. Either you haven't initialized the database or your username is not valid")
		return False

	cur = conn.cursor()

	nordic = nordicHandler.getNordicEvent(nordicEventId, cur)

	if nordic == None:
		return False
	
	qml = sql2quakeml.nordicEventToQuakeMl(nordic, True)

	if qml == None:
		return False

	try:
		f = open(MODULE_PATH + "../xml/quakeml_1.2__sc3ml_0.9.xsl")
	except:
		logging.error("quakeml_1.2__sc3ml_0.9.xsl is missing!")
		return False
	qml2scc3 = etree.parse(f)
	f.close()

	qml2sc3_transform = etree.XSLT(qml2scc3)

	sc3doc = qml2sc3_transform(qml)

	filename = "{:d}{:03d}{:02d}{:02d}{:02d}".format(nordic.headers[1][0].date.year, nordic.headers[1][0].date.timetuple().tm_yday, nordic.headers[1][0].hour, nordic.headers[1][0].minute, int(nordic.headers[1][0].second)) + ".xml"



	print(filename + " has been created")

	f = open(usr_path + "/" + filename, "wb")

	f.write(etree.tostring(sc3doc, pretty_print=True))

	f.close()
	conn.close()

	return True
