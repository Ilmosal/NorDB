#!/usr/bin/env python3

import os
import sys
import datetime
import logging
import functools
import fnmatch

import click

MODULE_PATH = os.path.realpath(__file__)[:-len("bin/NorDB.py")]
USER_PATH = os.getcwd()
ERROR_PATH = MODULE_PATH +"../errorlogs/{0}_error_"+ str(datetime.datetime.now().strftime("%Y%j%H%M%S_%f")) +".log"

os.chdir(MODULE_PATH)
sys.path = sys.path + [""]
os.chdir(USER_PATH)

from nordb.database import nordic2sql, scandia2sql, sql2nordic, sql2quakeml, sql2sc3, station2sql, resetDB, undoRead, norDBManagement, sql2station, sql2stationxml, sql2sitechan, sql2instrument
from nordb.core import usernameUtilities, nordicSearch, nordicModify

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

def configError(filename):
    logging.basicConfig(filename=ERROR_PATH.format(filename), level=logging.ERROR)

class Repo(object):
    def __init__(self):
        pass

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """This is the command line tool for NorDB database. If this is your first time running the program remember to first configure your .user.config file with conf and then create the database using create. You also have to initialize your postgresql user before working with the database"""
    ctx.obj = Repo()

@cli.command('conf', short_help='configure username')
@click.option('--username', '-u', prompt=True, help="your postgres username")
@click.pass_obj
def conf(repo, username):
    """Configures the userfile for the database. Give the username option your postgres username so the program can use your postgres-databased."""
    usernameUtilities.confUser(username) 

@cli.command('search', short_help='search for events')
@click.option('--date', '-d', default="-999", help="Search with date. Example:\n--date=12.01.2010")
@click.option('--hour', '-h',default="-999", help="Search with hour. Example:\n--hour=14")
@click.option('--minute', '-m', default="-999", help="Search with minute. Example:\n--minute=14")
@click.option('--second', '-s', default="-999",  help="Search with second. Example:\n--second=59.02")
@click.option('--latitude', '-la', default="-999", help="Search with latitude. Example:\n--latitude=69.09")
@click.option('--longitude', '-lo', default="-999", help="Search with longitude. Example:\n--longitude=69.09")
@click.option('--magnitude', '-ma', default="-999", help="Search with magnitude. Example:\n--magnitude=69.09")
@click.option('--depth', '-de', default="-999", help="Search with depth. Example:\n--depth=9.9")
@click.option('--event-type', '-e', default="-999", help="Search with event-type. Example:\n--event-type=F")
@click.option('--distance-indicator', '-di', default="-999", help="Search with distance-indicator. Example:\n--distance-indicator=R")
@click.option('--event-desc-id', '-eid', default="-999", help="Search with event-desc-id. Example:\nevent-desc-id=Q")
@click.option('--event-id', '-id', default="-999", help="\b Search with event-id. Example:\n--event-id=123")
@click.option('--verbose', '-v', is_flag=True, help="Print the whole nordic file instead of the main header.")
@click.option('--output', '-o', type=click.Path(readable=True), help="file to which all events found are appended")
@click.option('--output-format', '-f', default="n", type = click.Choice(["n", "q", "sc3"]))
@click.option('--event-root', '-r', is_flag=True)
@click.option('--silent', '-s', is_flag=True)
@click.pass_obj
def search(repo, date, hour, minute, second, latitude, longitude, depth, event_id, output_format,
            magnitude, event_type, distance_indicator, event_desc_id, verbose, output, event_root,
            silent):
    """
This command searches for events by given criteria and prints them to the screen. Output works in a following way:

\
    --parameter=A   -> Parameter has to be exactly A
    --parameter=A+  -> Parameter has to be over or equal to A
    --parameter=A-  -> Parameter has to be under or equal to A
    --parameter=A-B -> Parameter has to be equal to or in between of A and B

WARNING: Do not use --verbose flag when there are serveral search results. The output will clog your terminal. You can pipeline them into a file with > in following way:

\b    
    NorDB search --verbose -date=01.01.2009+

This will print all nordic events from date 01.01.2009 onwards into the outputfile. Better way of getting files from the database is get command.
    """
    criteria = {}
    if date != "-999":
        criteria["date"] = date
    if hour != "-999":
        criteria["hour"] = hour
    if minute != "-999":
        criteria["minute"] = minute
    if second != "-999":
        criteria["second"] = second
    if latitude != "-999":
        criteria["latitude"] = latitude
    if longitude != "-999":
        criteria["longitude"] = longitude
    if magnitude != "-999":
        criteria["magnitude"] = magnitude
    if depth != "-999":
        criteria["depth"] = depth
    if event_type != "-999":
        criteria["event_type"] = event_type
    if event_desc_id != "-999":
        criteria["event_desc_id"] = event_desc_id
    if distance_indicator != "-999":
        criteria["distance_indicator"] = distance_indicator
    if event_id != "-999":
        criteria["event_id"] = event_id

    if len(criteria) == 0:
        click.echo("No criteria given to search. NorDB will print all events. This might take a while. Ctrl-C will abort the search")

    nordicSearch.searchNordic(  criteria, verbose, 
                                output, event_root, 
                                USER_PATH, output_format, 
                                silent
                                )

@cli.command('insertins', short_help='insert instrument file')
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen")
@click.argument('instrument-file', required=True, type=click.Path(exists=True, readable=True))
@click.pass_obj
def insertins(repo, instrument_file, verbose):
    """
    This command adds a instrument css file to the database.
    """
    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        logging.root.addHandler(ch)

    if fnmatch.fnmatch(instrument_file, "*.instrument"):
        station2sql.readInstruments(open(instrument_file, 'r'), ERROR_PATH.split("/")[-1])
    else:
        click.echo("Filename must be in format *.instrument")

@cli.command('insertsen', short_help='insert sensor file')
@click.option('verbose', '-v', is_flag=True, help="print all errors to screen")
@click.argument('sensor-file', required=True, type=click.Path(exists=True, readable=True))
@click.pass_obj
def insertsen(repo, sensor_file, verbose):
    """
    This command adds a sensor css file to the database. Insert the related instrument and sitechan files before inserting the sensor file.
    """
    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        logging.root.addHandler(ch)

    if fnmatch.fnmatch(sensor_file, "*.sensor"):
        station2sql.readSensors(open(sensor_file, 'r'), ERROR_PATH.split("/")[-1])
    else:
        click.echo("Filename must be in format *.sensor")



@cli.command('insertcha', short_help='insert sitechan file')
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen")
@click.argument("channel-file", required=True, type=click.Path(exists=True, readable=True))
@click.pass_obj
def insertcha(repo, channel_file, verbose):
    """
    This command adds a sitechan css file to the database. Insert the related site files before inserting any sitechan files.
    """

    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        logging.root.addHandler(ch)

    if fnmatch.fnmatch(channel_file, "*.sitechan"):
        station2sql.readChannels(open(channel_file, 'r'), ERROR_PATH.split("/")[-1])
    else:
        click.echo("Filename must be in format *.sitechan")

@cli.command('insertsta', short_help='insert site file')
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen in addition to error log")
@click.argument('station-file', required=True, type=click.Path(exists=True, readable=True))
@click.argument('network', default="HEL")
@click.pass_obj
def insertsta(repo, station_file, network, verbose):
    """
    This command adds a site table to the database
    """
    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        logging.root.addHandler(ch)

    if fnmatch.fnmatch(station_file, "*.site"):
        station2sql.readStations(open(station_file, 'r'), network, ERROR_PATH.split("/")[-1])
    else:
        click.echo("Filename must be in format *.site")

@cli.command('getsta', short_help='get stations from network')
@click.argument('output', default="stations" ,type=click.Path(exists=False))
@click.option('--o_format', '-f', default="site", type=click.Choice(["site", "stationxml"]), help="format of the stations. Default site")
@click.option('--network', '-n', default="HEL", help="network from where you want to get your stations. Default HEL")
@click.pass_obj
def getsta(repo, output, o_format, network):
    """
    This command fetches the stations that match the criteria given by user and parses them to output. Network default val is HEL
    """
    if o_format == "site":
        sql2station.writeAllStations(output + ".site")
    elif o_format == "stationxml":
        sql2stationxml.writeNetworkToStationXML(network, output + ".xml")

@cli.command('getins', short_help="get instrument")
@click.argument('output', default='instruments', type=click.Path(exists=False))
@click.pass_obj
def getins(repo, output):
    """
    This command fetches the instruments that match the criteria given by user
    """
    sql2instrument.writeAllInstruments(output + ".instrument")

@cli.command('getcha', short_help="get sitechans")
@click.argument('output', default="sitechans" ,type=click.Path(exists=False))
@click.pass_obj
def getcha(repo, output):
    """
    This command fetches the sitechans that match the criteria given by user.
    """
    sql2sitechan.writeAllSitechans(output + ".sitechan")


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


@cli.command('insert', short_help="insert events")
@click.argument('event-type', type=click.Choice(["A", "R", "P", "F", "S", "O"]))
@click.option('--fix', '-f', is_flag=True, help="Use the fixing tool to add nordics with broken syntax t the database")
@click.option('--ignore-duplicates', '-iq', is_flag=True, help="In case of a duplicate event, ignore the new event")
@click.option('--no-duplicates', '-n', is_flag=True, help="Inform the program that there are no duplicate events, add all as new events with new root ids")
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen instead of errorlog")
@click.argument('filenames', required=True, nargs=-1,type=click.Path(exists=True, readable=True))
@click.pass_obj
def insert(repo, event_type, fix, ignore_duplicates, no_duplicates, filenames, verbose):
    """This command adds an nordic file to the Database. The EVENT-TYPE tells the database what's the type of the event((A)utomatic, (R)evieved, (P)reliminary, (F)inal, (S)candic, (O)ther). The suffix of the filename must be .n, .nordic or .nordicp)."""

    if verbose:
        ch = logging.StreamHandler(sys.stderr)
        ch.setLevel(logging.ERROR)
        logging.root.addHandler(ch)

    for filename in filenames:
        click.echo("reading {0}".format(filename.split("/")[len(filename.split("/")) - 1]))
        if (fnmatch.fnmatch(filename, "*.*n") or fnmatch.fnmatch(filename, "*.nordic") or fnmatch.fnmatch(filename, "*.nordicp")):
            f_nordic = open(filename, 'r')
            nordic2sql.read_nordicp(f_nordic, event_type, fix, ignore_duplicates, no_duplicates, ERROR_PATH)
            f_nordic.close()
        elif (fnmatch.fnmatch(filename, "*.catalog")):
            f_scandia = open(filename, 'r')
            scandia2sql.read_scandia_file(f_scandia)
            f_scandia.close()
        else:
            click.echo("File not in a valid format! See insert --help for information about valid formats")

@cli.command('create', short_help='create database')
@click.pass_obj
def create(repo):
    """This command creates the nordb dabase and inserts the required tables to the database. If you want to destroy the database beforehand remember to destroy the database with destroy command beforehand"""
    norDBManagement.create_database()
    click.echo("Database created!")

@cli.command('destroy', short_help='destroy database')
@click.confirmation_option()
@click.pass_obj
def destroy(repo):
    """Destroys the database. WARNING: this command will delete all information in the database"""
    norDBManagement.destroy_database()
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
@click.option('--output-format', '-f', default="n", type = click.Choice(["n", "q", "sc3"]), help="What format you want to use. Default 'n'")
@click.option('--event-id', '-id', type=click.INT, help = "id of the event you want to get")
@click.option('--event-id-file', '-idf', type=click.Path(exists=True, readable=True), help="link to a id file which you have created with search commands --output flag")
@click.option('--output', '-o', type=click.Path(exists=False), help='output filename')
@click.pass_obj
def get(repo, event_id, event_id_file, output_format, output):
    """
    Command for getting files out from the database. ID tells which event you want, FORMAT tells the program that in what format you want the file(n - nordic, q - quakeml, sc3 - seiscomp3) and output-name tells the output file's name if you want to specify it.

    You can create an output file by searching events with search command using --output or -o flag or simply writing event_ids on a blank file with every id being on a new line.
    """

    if event_id is None and event_id_file is None:
        click.echo("event-id and event-id-file cannot both be None")
        return

    if output is not None:
        click.echo(output + "has been created!")

    if isinstance(event_id, int):
        e_id = int(event_id) 
        if output_format == "n":
            sql2nordic.writeNordicEvent(event_id, USER_PATH, output)
        elif output_format == "q":
            sql2quakeml.writeQuakeML(event_id, USER_PATH, output)
        elif output_format == "sc3":
            sql2sc3.writeSC3(event_id, USER_PATH, output)
        return

    f = open(event_id_file, 'r')

    for line in f:
        try:
            e_id = int(line.strip())
        except:
            click.echo("Error parsing event-id-file. Problem with line: " + line)
            return

        if output_format == "n":
            sql2nordic.writeNordicEvent(e_id, USER_PATH, output)
        elif output_format == "q":
            sql2quakeml.writeQuakeML(e_id, USER_PATH, output)
        elif output_format == "sc3":
            sql2sc3.writeSC3(e_id, USER_PATH, output)

@cli.command('undo', short_help='undo last insert')
@click.pass_obj
def undo(repo):
    """
    Undo the last file insert made into the database. This will delete all events added to the db with a single insert command and modify the database to the way it was before the insert.
    """
    undoRead.undoMostRecent()

if __name__ == "__main__":
    cli()
