#!/usr/bin/env python3

"""
This is the command line tool of the whole program. The command line tool is created with python library Click and that's why it's functions are not usable in same way compared to the others. If you have installed the Library correctly, you can use the command line tool by typing ``nordb`` into your terminal.
"""

import os
import sys
from datetime import datetime
import logging
import fnmatch

import click
from lxml import etree

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep
ERROR_PATH = MODULE_PATH +"../errorlogs/error_"+ str(datetime.now().strftime("%Y%j%H%M%S_%f")) +".log"

from nordb.database import instrument2sql
from nordb.database import nordic2sql
from nordb.database import sensor2sql
from nordb.database import sitechan2sql
from nordb.database import station2sql

from nordb.database import nordicSearch
from nordb.database import norDBManagement
from nordb.database import resetDB
from nordb.database import undoRead
from nordb.database import nordicModify
from nordb.database import eventTypeHandler

from nordb.database import sql2instrument
from nordb.database import sql2nordic
from nordb.database import sql2sensor
from nordb.database import sql2station
from nordb.database import sql2sitechan

from nordb.core import nordic
from nordb.core import nordic2quakeml
from nordb.core import nordic2sc3
from nordb.core import nordicRead
from nordb.core import station2stationxml
from nordb.core import usernameUtilities

from nordb.nordic import instrument
from nordb.nordic import sensor
from nordb.nordic import sitechan
from nordb.nordic import station

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logging.basicConfig(filename=ERROR_PATH, level=logging.ERROR)

class Repo(object):
    def __init__(self):
        pass

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    This is the command line tool for NorDB database. If this is your first time running the program remember to first configure your .user.config file with conf and then create the database using create. You also have to initialize your postgresql user before working with the database
    
    You can request help for all the commands with -h or --help flags.
    """
    ctx.obj = Repo()

@cli.command('conf', short_help='configure username')
@click.option('--username', '-u', prompt=True, help="your postgres username")
@click.pass_obj
def conf(repo, username):
    """Configures the userfile for the database. Give the username option your postgres username so the program can use your postgres-databased."""
    usernameUtilities.confUser(username) 

@cli.command('search', short_help='search for events')
@click.option('--verbose', '-v', is_flag=True, help="Print the whole nordic file instead of the main header.")
@click.option('--output', '-o', type=click.Path(writable=True), help="file to which all events found are appended")
@click.option('--output-format', '-f', default="n", type = click.Choice(["n", "q", "sc3"]))
@click.option('--event-root', '-r', is_flag=True)
@click.option('--silent', '-s', is_flag=True)
@click.argument("criteria", nargs=-1, type=click.STRING)
@click.pass_obj
def search(repo, output_format, verbose, output, event_root, silent, criteria):
    """
    This command searches for events by given criteria and prints them to the screen. Output works in a following way:

    \b
        --parameter=A   -> Parameter has to be exactly A
        --parameter=A+  -> Parameter has to be over or equal to A
        --parameter=A-  -> Parameter has to be under or equal to A
        --parameter=A-B -> Parameter has to be equal to or in between of A and B

    WARNING: Do not use --verbose flag when there are serveral search results. The output will clog your terminal. You can pipeline them into a file with > in following way:

    \b    
        NorDB search --verbose -date=01.01.2009+

    This will print all nordic events from date 01.01.2009 onwards into the outputfile. Better way of getting files from the database is get command.
    """
    search = nordicSearch.NordicSearch()
  
    search_types =  {
                        "date":"origin_time",
                        "d":"origin_time",
                        "origin_time":"origin_time",
                        "latitude":"epicenter_latitude",
                        "la":"epicenter_latitude",
                        "epicenter_latitude":"epicenter_latitude",
                        "longitude":"epicenter_longitude",
                        "lo":"epicenter_longitude",
                        "epicenter_longitude":"epicenter_longitude",
                        "magnitude":"magnitude_1",
                        "magnitude_1":"magnitude_1",
                        "ma":"magnitude_1",
                        "m":"magnitude_1",
                        "event_type":"event_type",
                        "et":"event_type",
                        "distance_indicator":"distance_indicator",
                        "di":"distance_indicator",
                        "event_desc_id":"event_desc_id",
                        "ed":"event_desc_id",
                        "eid":"event_desc_id",
                        "event_id":"event_id",
                        "id":"event_id",
                        "depth":"depth",
                        "de":"depth",
                    }
 
    for crit in criteria:
        try:
            tpe, values = crit.split('=')
        except:
            click.echo("Criteria not in valid format! Use --help/-h for support. ({0})".format(crit))
            return
        if tpe not in search_types.keys():
            click.echo("Criteria type not a valid type! ({0})".format(tpe))
            return

        strvalues = []

        if '-' in values and values[-1] != '-':
            strvalues = values.split('-')
        else:
            if values[-1] in "-+":
                strvalues = [values[:-1]]
            else:
                strvalues = [values]
       
 
        real_vals = []        

        for val in strvalues:
            if search_types[tpe] == "origin_time":
                try:
                    real_vals.append(datetime.strptime(val, "%Y%j_%H:%M:%S"))
                except:
                    try:
                        real_vals.append(datetime.strptime(val, "%d.%m.%Y_%H:%M:%S"))
                    except:
                        try:
                            real_vals.append(datetime.strptime(val, "%Y%j").date())
                        except:
                            try:
                                real_vals.append(datetime.strptime(val, "%d.%m.%Y").date())
                            except:
                                click.echo("origin_time not in a correct format! ({0})".format(val))
                                return
            elif search_types[tpe] in ["epicenter_latitude", "epicenter_longitude", "magnitude_1", "depth"]:
                try:
                    real_vals.append(float(val))
                except:
                    click.echo("{0} not in a float! ({1})".format(tpe, val))
                    return
            elif search_types[tpe] in ["event_id"]:
                try:
                   real_vals.append(int(val)) 
                except:
                    click.echo("{0} not in a int! ({1})".format(tpe, val))
                    return
            else:
                real_vals.append(val)

        if len(real_vals) == 2:
            search.addSearchBetween(search_types[tpe], real_vals[0], real_vals[1])
        elif values[-1] == "-":
            search.addSearchUnder(search_types[tpe], real_vals[0])
        elif values[-1] == "+":
            search.addSearchOver(search_types[tpe], real_vals[0])
        else:
            search.addSearchExactly(search_types[tpe], real_vals[0])

    if search.getCriteriaAmount() == 0:
        click.echo("No criteria given to search. NorDB will print all events. This might take a while. Ctrl-C will abort the search")

    events = search.searchEvents()
    
    if not events:
        click.echo("No events found with criteria: \n{0}".format(criteria))
        return

    if criteria:
        click.echo("Event Search \nCriteria: \n{0}".format(search.getCriteriaString()[:-1]))
    else:
        click.echo("All events")
    click.echo("-------------------------------------------------------------")
    for e in events:
        if not verbose:
            print("id: {0} type: {1} - {2}".format(e.event_id, e.event_type, str(e.headers[1][0])[:-1]))
        else:
            print(str(e) + "\n-------------------------------------------------------------")

    if output is not None:
        f_output = open(output, 'w')

        if output_format == "n":
            for event in events:
                f_output.write(str(event))         
                f_output.write("\n")

        elif output_format == "q":
            qml = nordic2quakeml.nordicEvents2QuakeML(events, True)
            f_output.write(etree.tostring(qml, pretty_print=True).decode('utf8'))

        elif output_format == "sc3":
            sc3 = nordic2sc3.nordicEvents2SC3(events)
            f_output.write(etree.tostring(sc3, pretty_print=True).decode('utf8'))

        f_output.close()

@cli.command('insertsta', short_help='insert station related files')
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen in addition to error log")
@click.option('--all_files', '-a', is_flag=True, help="add all four station files: .site, .sitechan, .instrument, .sensor to db")
@click.argument('station-file', required=True, type=click.Path(exists=True, readable=True))
@click.argument('network', default="HEL")
@click.pass_obj
def insertsta(repo, station_file, network, verbose, all_files):
    """
    This command adds a site table to the database
    """
    if fnmatch.fnmatch(station_file, "*.site"):
        f_stations = open(station_file, 'r')
        stations = []

        for line in f_stations:
            try:
                stations.append(station.readStationStringToStation(line, network))
            except Exception as e:
                click.echo("Error reading line: {0}".format(e))
                click.echo("Line: {0}".format(line))

        for sen in stations:
            try:
                station2sql.insertStation2Database(sen, network)
            except Exception as e:
                click.echo("Error pushing station to the database: {0}".format(e))
                click.echo("Line: {0}".format(sen))
        
        if all_files:
            station_file = station_file.split(".")[0] + ".sitechan"
    if fnmatch.fnmatch(station_file, "*.sitechan"):
        f_sitechans = open(station_file, 'r')
        sitechans = []

        for line in f_sitechans:
            try:
                sitechans.append(sitechan.readSiteChanStringToSiteChan(line))
            except Exception as e:
                click.echo("Error reading line: {0}".format(e))
                click.echo("Line: {0}".format(line))

        for chan in sitechans:
            try:
                sitechan2sql.insertSiteChan2Database(chan)
            except Exception as e:
                click.echo("Error pushing sitechan to the database: {0}".format(e))
                click.echo("Line: {0}".format(chan))

        if all_files:
            station_file = station_file.split(".")[0] + ".instrument"

    if fnmatch.fnmatch(station_file, "*.instrument"):
        f_instruments = open(station_file, 'r')
        instruments = []

        for line in f_instruments:
            try:
                instruments.append(instrument.readInstrumentStringToInstrument(line))
            except Exception as e:
                click.echo("Error reading line: {0}".format(e))
                click.echo("Line: {0}".format(line))

        for ins in instruments:
            try:
                instrument2sql.insertInstrument2Database(ins)
            except Exception as e:
                click.echo("Error pushing instrument to the database: {0}".format(e))
                click.echo("Line: {0}".format(ins))

        if all_files:
            station_file = station_file.split(".")[0] + ".sensor"

    if fnmatch.fnmatch(station_file, "*.sensor"):
        f_sensors = open(station_file, 'r')
        sensors = []

        for line in f_sensors:
            try:
                sensors.append(sensor.readSensorStringToSensor(line))
            except Exception as e:
                click.echo("Error reading line: {0}".format(e))
                click.echo("Line: {0}".format(line))

        for sen in sensors:
            try:
                sensor2sql.insertSensor2Database(sen)
            except Exception as e:
                click.echo("Error pushing sensor to the database: {0}".format(e))
                click.echo("Line: {0}".format(sen))

@cli.command('getsta', short_help='get station related info')
@click.option('--o_format', '-f', default="stationxml", type=click.Choice(["site", "sitechan", "sensor", "instrument", "all", "stationxml"]), help="File that you want to get from the database")
@click.argument('output_name', required=True, type=click.Path(exists=False, readable=True))
@click.argument('stat_ids', nargs=-1, type=click.INT)
@click.pass_obj
def getsta(repo, o_format, output_name, stat_ids):
    """
    This command fetches station related information from the database.
    """
    if o_format == "stationxml":
        stations = []
        if not stat_ids:
            stations = sql2station.readAllStations()

        for s_id in stat_ids:
            try:
                stations.append(sql2station.readStation(s_id))
            except:
                click.echo("No station with id {0} in the database!".format(s_id)) 

        if not stations:
            return

        statxml = station2stationxml.stationsToStationXML(stations)
        f_write = open(output_name+".xml", "w")
        f_write.write(etree.tostring(statxml, pretty_print=True).decode("utf8"))

        f_write.close()
    if o_format == "site" or o_format == "all":
        stations = []
        if not stat_ids:
            stations = sql2station.readAllStations()

        for s_id in stat_ids:
            try:
                stations.append(sql2station.readStation(s_id))
            except:
                click.echo("No station with id {0} in the database!".format(s_id))

        if not stations:
            return

        f_write = open(output_name+".site", "w")
        for stat in stations:
            f_write.write(str(stat) + "\n")

        f_write.close()
    if o_format == "sitechan" or o_format == "all":
        sitechans = []
        if not stat_ids:
            sitechans = sql2sitechan.readAllSitechans()
        
        for s_id in stat_ids:
            try:
                sitechans.append(sql2sitechan.readSitechan(s_id))
            except:
                click.echo("No sitechan with id {0} in the database!".format(s_id))

        if not sitechans:
            return

        f_write = open(output_name+".sitechan", "w")
        for chan in sitechans:
            f_write.write(str(chan) + "\n")

        f_write.close()
    if o_format == "sensor" or o_format == "all":
        sensors = []
        if not stat_ids:
            sensors = sql2sensor.readAllSensors()

        for s_id in stat_ids:
            try:
                sensors.append(sql2sensor.readSensor(s_id))    
            except:
                click.echo("No sensor with id {0} in the database!".format(s_id))        
       
        if not sensors:
            return
 
        f_write = open(output_name+".sensor", "w")
        for sen in sensors:
            f_write.write(str(sen) + "\n")

        f_write.close()
    if o_format == "instrument" or o_format == "all":
        instruments = []
        if not stat_ids:
            instruments = sql2instrument.readAllInstruments()

        for i_id in stat_ids:
            try:
                instruments.append(sql2instrument.readInstrument(i_id))
            except:
                click.echo("No instrument with id {0} in the database!".format(i_id))

        if not instruments:
            return

        f_write = open(output_name+".instrument", "w")
        for ins in instruments:
            f_write.write(str(ins) + "\n")

        f_write.close()

    if o_format == "all":
        click.echo("{0}.site, {0}.sitechan, {0}.instrument, {0}.sensor written!".format(output_name))
    elif o_format == "stationxml":
        click.echo("{0}.xml written!".format(output_name))
    else:
        click.echo("{0}.{1} written!".format(output_name, o_format))

@cli.command('chgroot', short_help='change root id')
@click.option('--root-id', '-id', default=-999, type=click.INT, help="root to which the event is attached to")
@click.argument('event-id', type=click.INT)
@click.pass_obj
def chgroot(repo, root_id, event_id):
    """
    This command changes the root id of a event to root id given by user or creates a new root for the event. If no root-id is given to the command, it will attach the event to a new root.

    A root is an id to which different analyses of a same event will refer to. This groups the events together and makes it very simple to follow how the analysis of the single event has evolved. If the insert program fails to find proper root or the user accidentally attaches a event to a wrong root. This command can be used to change the root id to a new one.
    """
    nordicModify.changeEventRoot(event_id, root_id)


@cli.command('chgtype', short_help='change event type')
@click.argument('event-type', type=click.Choice(["A", "R", "P", "F", "S", "O"]))
@click.argument('event-id', type=click.INT)
@click.pass_obj
def chgtype(repo, event_type, event_id):
    """
    This command changes the event type of a event with id of event-id to event-type given by user or creates a new root for the event. Event type refers to how final the analysis of the event is.
    
    \b
    Event type
    ----------
    A - Automatic
    R - Reviewed
    P - Preliminary
    F - Final
    (S - Scandia) NOT YET IMPLEMENTED
    O - Other
    """
   
    nordicModify.changeEventType(event_id, event_type)

@cli.command("etype", short_help="add, remove and look event types")
@click.option('--list', '-l', 'etype_option', flag_value='list', default=True, help="List all the event types in the database")
@click.option('--add', '-a', 'etype_option', flag_value='add', help="add a new event type to the database")
@click.option('--remove', '-r','etype_option', flag_value='remove', help="remove an old event type from the database")
@click.pass_obj
def etype(repo, etype_option):
    """
    This command is for adding, removing and looking the event types in the database. They will prompt the necessary values from the user.
    """ 
    try: 
        if etype_option == "list":
            e_types = eventTypeHandler.getEventTypes()
            click.echo("Type Id | Event Type Description           | Allow Multiple")
            click.echo("-----------------------------------------------------------")
            for e_type in e_types:
                click.echo(" {0:<6} | {1:<32} | {2}".format(e_type[0], e_type[1], e_type[2]))
        elif etype_option == "add":
            click
            e_type_id = click.prompt("Enter the event type id(Press CTR-C to escape)")
            if len(e_type_id) > 6:
                click.echo("{0} is too long! Maximum length of 3 characters".format(e_type_id))
                return
            if len(e_type_id) == 0:
                click.echo("No event type given to the program!")
                return

            e_type_desc = click.prompt("Enter a short description for the event type id(CTR-C to escape)")
            if len(e_type_desc) > 32:
                click.echo("{0} is too long. Maximum length of 32 characters".format(e_type_desc))
                return

            e_type_allow = click.prompt("Allow multiple events of same type in same event root? ", type=bool)

            try:
                eventTypeHandler.addEventType(e_type_id, e_type_desc, e_type_allow)
            except:
                click.echo("Event Type {0} already exists in the database!".format(e_type_id))
        elif etype_option == "remove": 
            
            e_type_id = click.prompt("Enter the event type id(Press CTR-C to escape)")
            if len(e_type_id) > 6:
                click.echo("{0} is too long! Maximum length of 6 characters".format(e_type_id))
                return
            if len(e_type_id) == 0:
                click.echo("No event type given to the program!")
                return

            existing = eventTypeHandler.getEventTypes() 
            if e_type_id not in [existing[i][:1][0] for i in range(0, len(existing))]:
                click.echo("Given event type does not exist in the database!")
                return

            search = nordicSearch.NordicSearch()
            search.addSearchExactly("event_type", e_type_id) 
            new_e_type_id = "O"

            if len(search.searchEventIds()) > 0:
                if not click.prompt("Events found with id {0}. Do you want to move them to another id?".format(e_type_id), type=bool):
                    return

                new_e_type_id = click.prompt("Enter the event type id of the replacing event type(Press CTR-C to escape)")
                if len(e_type_id) > 6:
                    click.echo("{0} is too long! Maximum length of 3 characters".format(new_e_type_id))
                    return
                if len(e_type_id) == 0:
                    click.echo("No event type given to the program!")
                    return
                if new_e_type_id not in [existing[i][:1][0] for i in range(0, len(existing))]:
                    click.echo("Event type {0} does not exist!".format(new_e_type_id))
                    return

            eventTypeHandler.removeEventType(e_type_id, new_e_type_id)
    except KeyboardInterrupt:
        pass

@cli.command('insert', short_help="insert events")
@click.option('--nofix', '-nf', is_flag=True, help="Do not use the fixing tool to add nordics with broken syntax the database")
@click.option('--ignore-duplicates', '-iq', is_flag=True, help="In case of a duplicate event, ignore the new event")
@click.option('--no-duplicates', '-n', is_flag=True, help="Inform the program that there are no duplicate events, add all as new events with new root ids")
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen instead of errorlog")
@click.argument('event-type')
@click.argument('filenames', required=True, nargs=-1,type=click.Path(exists=True, readable=True))
@click.pass_obj
def insert(repo, event_type, nofix, ignore_duplicates, no_duplicates, filenames, verbose):
    """This command adds an nordic file to the Database. The EVENT-TYPE tells the database what's the type of the event((A)utomatic, (R)evieved, (P)reliminary, (F)inal, (S)candic, (O)ther). The suffix of the filename must be .n, .nordic or .nordicp)."""

    if verbose:
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.ERROR)
        logging.root.addHandler(ch)

    for filename in filenames:
        click.echo("reading {0}".format(filename.split("/")[len(filename.split("/")) - 1]))
        if (fnmatch.fnmatch(filename, "*.*n") or fnmatch.fnmatch(filename, "*.nordic") or fnmatch.fnmatch(filename, "*.nordicp")):
            f_nordic = open(filename, 'r')
            try:
                nordic_strings = nordicRead.readNordicFile(f_nordic)
            except Exception as e:
                click.echo("Error reading nordic file: {0}".format(e))
                return

            nordic_events = []
            nordic_failed = []

            for n_string in nordic_strings:
                try:
                    nordic_events.append(nordic.createNordicEvent(n_string, not nofix, -1, -1, event_type))
                except Exception as e:
                    click.echo("Error reading nordic: {0}".format(e))
                    click.echo(n_string[0])
                    nordic_failed.append("Errors:\n{0}\n------------------------------\n".format(e))
                    nordic_failed.append(n_string)

            creation_id = nordic2sql.createCreationInfo()
            for nord in nordic_events:
                
                event_id = -1
                if not no_duplicates:
                    same_events = nordicSearch.searchSameEvents(nord)
                    if same_events:
                        if ignore_duplicates:
                            click.echo("Duplicate found! Ignoring event:\n{0}".format(nord.headers[1][0]))
                            continue

                        click.echo("Identical events to current found! Is any of these a duplicate of yours?")
                        click.echo("{0} - (Yours)".format(nord.headers[1][0]))
                        click.echo("-----------------------------------------------------------------------------------------")
                        for e in same_events:
                            click.echo("{0} - ({1})".format(e.headers[1][0], e.event_id))
                        while True:
                            try:
                                event_id = int(input("Event id of the same event: "))
                                break
                            except:
                                click.echo("Not a valid id!")

                    if event_id == -1:
                        similar_events = nordicSearch.searchSimilarEvents(nord)
                       
                        if similar_events:
                            if ignore_duplicates:
                                click.echo("Duplicate found! Ignoring event:\n{0}".format(nord.headers[1][0]))
                                continue

                            click.echo("Similar events to current found! Is any of these a duplicate of yours?")
                            click.echo("{0} (Yours)".format(nord.headers[1][0]))
                            click.echo("-----------------------------------------------------------------------------------------")
                            for e in similar_events:
                                click.echo("{0} - ({1})".format(e.headers[1][0], e.event_id))
                            while True:
                                try:
                                    event_id = int(input("Event id of the same event: "))
                                    break
                                except:
                                    click.echo("Not a valid id!")

                try:
                    nordic2sql.event2Database(nord, event_type, f_nordic.name, creation_id, event_id)
                except Exception as e:
                    click.echo("Error pushing nordic to database: {0}".format(e))
                    click.echo(nord.headers[1][0])
                    nordic_failed.append("Errors:\n{0}\n------------------------------\n".format(e))
                    nordic_failed.append(str(nord))
           
            nordic2sql.deleteCreationInfoIfUnnecessary(creation_id)

            if len(nordic_failed) > 0:
                failed = open("f_" + os.path.basename(f_nordic.name), "w")

                for n in nordic_failed:
                    for line in n:
                        failed.write(line)  
                    failed.write("\n")

            f_nordic.close()
        else:
            click.echo("File not in a valid format! See insert --help for information about valid formats")

@cli.command('create', short_help='create database')
@click.pass_obj
def create(repo):
    """This command creates the nordb dabase and inserts the required tables to the database. If you want to destroy the database beforehand remember to destroy the database with destroy command beforehand"""
    norDBManagement.createDatabase()
    click.echo("Database created!")

@cli.command('destroy', short_help='destroy database')
@click.confirmation_option()
@click.pass_obj
def destroy(repo):
    """Destroys the database. WARNING: this command will delete all information in the database"""
    norDBManagement.destroyDatabase()
    click.echo("Database destroyed!")

@cli.command('reset', short_help='reset database')
@click.confirmation_option()
@click.argument("reset-type", default="all", type=click.Choice(["all", "events", "stations"]))
@click.pass_obj
def reset(repo, reset_type):
    """
    Resets the database to it's orginal form but keeps the tables intact. WARNING: this command will delete all information in the database.
    Possible options: all, events, stations

    all         - resets all information from the database.
    events      - resets all information relevant to events.
    stations    - resets all information relevant to stations.
    """
    if reset_type == "all":
        resetDB.resetDatabase()
    elif reset_type == "events":
        resetDB.resetEvents()
    elif reset_type == "stations":
        resetDB.resetStations()

@cli.command('get', short_help='get event')
@click.argument('event-ids', nargs=-1, type=click.INT)
@click.argument('output-name', type=click.Path(exists=False))
@click.option('--output-format', '-f', default="n", type = click.Choice(["n", "q", "sc3"]), help="What format you want to use. Default 'n'")
@click.pass_obj
def get(repo, output_format, event_ids, output_name):
    """
    Command for getting files out from the database. ID tells which event you want, FORMAT tells the program that in what format you want the file(n - nordic, q - quakeml, sc3 - seiscomp3) and output-name tells the output file's name if you want to specify it.

    You can create an output file by searching events with search command using --output or -o flag or simply writing event_ids on a blank file with every id being on a new line.
    """
    n_events = []
    for e_id in event_ids:
        n_events.append(sql2nordic.getNordicFromDB(e_id))

    n_events = [nordic_event for nordic_event in n_events if nordic_event is not None]

    if not n_events:
        click.echo("No events with ids {0}".format(event_ids))
        return  

    f_output = open(output_name, 'w')
    if output_format == "n":
        for n_event in n_events:
            f_output.write(str(n_event))         
            f_output.write("\n")
    elif output_format == "q":
        qml = nordic2quakeml.nordicEvents2QuakeML(n_events, True)
        f_output.write(etree.tostring(qml, pretty_print=True).decode('utf8'))
    elif output_format == "sc3":
        sc3 = nordic2sc3.nordic2SC3(n_events)
        f_output.write(etree.tostring(sc3, pretty_print=True).decode('utf8'))

    f_output.close()

@cli.command('undo', short_help='undo last insert')
@click.pass_obj
def undo(repo):
    """
    Undo the last file insert made into the database. This will delete all events added to the db with a single insert command and modify the database to the way it was before the insert.
    """
    try:
        undoRead.undoMostRecent()
    except:
        click.echo("No events in database")

if __name__ == "__main__":
    cli()
