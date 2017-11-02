#!/usr/bin/env python3

import os
import sys
import logging
import fnmatch
import click

MODULE_PATH = os.path.realpath(__file__)[:-len("bin/NorDB.py")]
USER_PATH = os.getcwd()

os.chdir(MODULE_PATH)
sys.path = sys.path + [""]

from nordb.database import nordic2sql, scandia2sql, sql2nordic, sql2quakeml, sql2sc3, station2sql, resetDB, undoRead, norDBManagement, sql2station, sql2stationxml
from nordb.core import usernameUtilities, nordicSearch, nordicModify

os.chdir(USER_PATH)

class Repo(object):
    def __init__(self):
        pass

@click.group()
@click.pass_context
def cli(ctx):
    """This is a command line tool for NorDB database. If this is your first time running the program remember to first configure your .user.config file with conf and then create the database using create. You also have to initialize your postgresql user before working with the database"""
    ctx.obj = Repo()

@cli.command()
@click.option('--username', prompt=True)
@click.pass_obj
def conf(repo, username):
    """Configures the userfile for the database. Give the username option your postgres username so the program can use your postgres-databased."""
    usernameUtilities.confUser(username) 

@cli.command()
@click.option('--date', default="-999", help="Search with date. Example:\n--date=12.01.2010")
@click.option('--hour', default="-999", help="Search with hour. Example:\n--hour=14")
@click.option('--minute', default="-999", help="Search with minute. Example:\n--minute=14")
@click.option('--second', default="-999",  help="Search with second. Example:\n--second=59.02")
@click.option('--latitude', default="-999", help="Search with latitude. Example:\n--latitude=69.09")
@click.option('--longitude', default="-999", help="Search with longitude. Example:\n--longitude=69.09")
@click.option('--magnitude', default="-999", help="Search with magnitude. Example:\n--magnitude=69.09")
@click.option('--depth', default="-999", help="Search with depth. Example:\n--depth=9.9")
@click.option('--event-type', default="-999", help="Search with event-type. Example:\n--event-type=F")
@click.option('--distance-indicator', default="-999", help="Search with distance-indicator. Example:\n--distance-indicator=R")
@click.option('--event-desc-id', default="-999", help="Search with event-desc-id. Example:\nevent-desc-id=Q")
@click.option('--event-id', default="-999", help="\b Search with event-id. Example:\n--event-id=123")
@click.option('--verbose', is_flag=True, help="Print the whole nordic file instead of the main header.")
@click.option('--output', type=click.Path(readable=True), help="file to which all events found are appended")
@click.option('--output-format', default="n", type = click.Choice(["n", "q", "sc3"]))
@click.option('--event-root', is_flag=True)
@click.option('--silent', is_flag=True)
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

    nordicSearch.searchNordic(  criteria, verbose, 
                                output, event_root, 
                                USER_PATH, output_format, 
                                silent
                                )

@cli.command()
@click.argument('station-file', required=True, type=click.Path(exists=True, readable=True))
@click.argument('network', default="HEL")
@click.pass_obj
def insertsta(repo, station_file, network):
    """
    This command adds a site table to the database
    """
    if fnmatch.fnmatch(station_file, "*.site"):
        station2sql.readStations(open(station_file, 'rb'), network)
    else:
        click.echo("Filename must be in format *.sites")

@cli.command()
@click.argument('output', default="stations" ,type=click.Path(exists=False))
@click.option('--o-format', default="site", type=click.Choice(["site", "stationxml"]))
@click.option('--network', default="HEL")
@click.pass_obj
def getsta(repo, output, o_format, network):
    """
    This command fetches the stations that match the criteria given by user.
    """
    if o_format == "site":
        sql2station.writeAllStations(output + ".site")
    elif o_format == "stationxml":
        sql2stationxml.writeNetworkToStationXML(network, output + ".xml")

@cli.command()
@click.option('--root-id', default=-999, type=click.INT, help="root to which the event is attached to")
@click.argument('event-id', type=click.INT)
@click.pass_obj
def chgroot(repo, root_id, event_id):
    """
    This command changes the root id of a event to root id given by user or creates a new root for the event. If no root-id is given to the command, it will attach the event to a new root.
    """
    nordicModify.changeEventRoot(event_id, root_id)

@cli.command()
@click.argument('event-type', type=click.Choice(["A", "R", "P", "F", "S", "O"]))
@click.argument('event-id', type=click.INT)
@click.pass_obj
def chgtype(repo, event_type, event_id):
    """
    This command changes the event type of a event with id of event-id to event-type given by user or creates a new root for the event. 
    """
    nordicModify.changeEventType(event_id, event_type)


@cli.command()
@click.argument('event-type', type=click.Choice(["A", "R", "P", "F", "S", "O"]))
@click.option('--fix', is_flag=True, help="Use the fixing tool to add nordics with broken syntax t the database")
@click.option('--ignore-duplicates', is_flag=True, help="In case of a duplicate event, ignore the new event")
@click.option('--no-duplicates', is_flag=True, help="Inform the program that there are no duplicate events, add all as new events with new root ids")
@click.argument('filenames', required=True, nargs=-1,type=click.Path(exists=True, readable=True))
@click.pass_obj
def insert(repo, event_type, fix, ignore_duplicates, no_duplicates, filenames):
    """This command adds an nordic file to the Database. The EVENT-TYPE tells the database what's the type of the event((A)utomatic, (R)evieved, (P)reliminary, (F)inal, (S)candic, (O)ther). The suffix of the filename must be .n, .nordic or .nordicp)."""
    if ignore_duplicates and no_duplicates:
        click.echo("--ignore-duplicates and --no-duplicates cannot be on at the same time!")
        return
    for filename in filenames:
        click.echo("reading {0}".format(filename.split("/")[len(filename.split("/")) - 1]))
        if (fnmatch.fnmatch(filename, "*.*n") or fnmatch.fnmatch(filename, "*.nordic") or fnmatch.fnmatch(filename, "*.nordicp")):
            f_nordic = open(filename, 'r')
            nordic2sql.read_nordicp(f_nordic, event_type, fix, ignore_duplicates, no_duplicates)
            f_nordic.close()
        elif (fnmatch.fnmatch(filename, "*.catalog")):
            f_scandia = open(filename, 'r')
            scandia2sql.read_scandia_file(f_scandia)
            f_scandia.close()
        else:
            click.echo("File not in a valid format! See insert --help for information about valid formats")

@cli.command()
@click.pass_obj
def create(repo):
    """This command creates the nordb dabase and inserts the required tables to the database. If you want to destroy the database beforehand remember to destroy the database with destroy command beforehand"""
    norDBManagement.create_database()
    click.echo("Database created!")

@cli.command()
@click.confirmation_option()
@click.pass_obj
def destroy(repo):
    """Destroys the database. WARNING: this command will delete all information in the database"""
    norDBManagement.destroy_database()
    click.echo("Database destroyed!")

@cli.command()
@click.confirmation_option()
@click.option("--reset-type", required=True, type=click.Choice(["all", "events", "stations"]))
@click.pass_obj
def reset(repo, reset_type):
    """Resets the database to it's orginal form but keeps the tables intact. WARNING: this command will delete all information in the database"""
    if reset_type == "all":
        resetDB.resetDatabase()
    elif reset_type == "events":
        resetDB.resetEvents()
    elif reset_type == "stations":
        resetDB.resetStations()

@cli.command()
@click.option('--output-format', default="n", type = click.Choice(["n", "q", "sc3"]))
@click.option('--event-id', type=click.INT)
@click.option('--event-id-file', type=click.Path(exists=True, readable=True))
@click.option('--output', type=click.Path(exists=False))
@click.pass_obj
def get(repo, event_id, event_id_file, output_format, output):
    """Command for getting files out from the database. ID tells which event you want, FORMAT tells the program that in what format you want the file(n - nordic, q - quakeml, sc3 - seiscomp3) and output-name tells the output file's name if you want to specify it."""

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

@cli.command()
@click.pass_obj
def undo(repo):
    """Undo the last file insert made into the database"""
    undoRead.undoMostRecent()

if __name__ == "__main__":
    cli()
