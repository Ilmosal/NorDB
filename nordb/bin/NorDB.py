#!/usr/bin/env python3

import os
import sys
import logging
import inspect
import fnmatch
import click

MODULE_PATH = os.path.realpath(__file__)[:-len("bin/NorDB.py")]
USER_PATH = os.getcwd()

os.chdir(MODULE_PATH)
sys.path = sys.path + [""]

from nordb.io import nordic2sql, scandia2sql, sql2nordic, sql2quakeml, sql2sc3, station2sql
from nordb.database import resetDB, undoRead, norDBManagement
from nordb.core import usernameUtilities, nordicSearch

os.chdir(USER_PATH)

class Repo(object):
    def __init__(self):
        pass

@click.group()
@click.pass_context
def cli(ctx):
    """This is a command line tool for NorDB database. If this is your first time running the program remember to first configure your .user.config file with conf and then create the database using create."""
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
@click.option('--event-type', default="-999", help="Search with event-type. Example:\n--event-type=F")
@click.option('--distance-indicator', default="-999", help="Search with distance-indicator. Example:\n--distance-indicator=R")
@click.option('--event-desc-id', default="-999", help="Search with event-desc-id. Example:\nevent-desc-id=Q")
@click.option('--event-id', default="-999", help="\b Search with event-id. Example:\n--event-id=123")
@click.option('--verbose', is_flag=True, help="Print the whole nordic file instead of the main header.")
@click.pass_obj
def search(repo, date, hour, minute, second, latitude, longitude, event_id,
            magnitude, event_type, distance_indicator, event_desc_id, verbose):
    """
This command searches for events by given criteria and prints them to the screen. Output works in a following way:

\b
    --parameter=A   -> Parameter has to be exactly A
    --parameter=A+  -> Parameter has to be over or equal to A
    --parameter=A-  -> Parameter has to be under or equal to A
    --parameter=A-B -> Parameter has to be equal to or in between of A and B

WARNING: Do not use --verbose flag when there are serveral search results. The output will clog your terminal. You can pipeline them into a file with > in following way:

\b    
    NorDB search --verbose -date=01.01.2009+ > outputfile

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
    if event_type != "-999":
        criteria["event_type"] = event_type
    if event_desc_id != "-999":
        criteria["event_desc_id"] = event_desc_id
    if distance_indicator != "-999":
        criteria["distance_indicator"] = distance_indicator
    if event_id != "-999":
        criteria["event_id"] = event_id

    ans = nordicSearch.searchNordic(criteria, verbose)

    if ans == -1:
        click.echo("No criteria given to program!!")

@cli.command()
@click.argument('station-file', required=True, type=click.Path(exists=True, readable=True))
@click.pass_obj
def insertStation(repo, station_file):
    """
    This command adds a site table to the database
    """
    if fnmatch.fnmatch(station_file, "*.site"):
        station2sql.readStations(open(station_file, 'rb'))
    else:
        click.echo("Filename must be in format *.sites")

@cli.command()
@click.argument('event-type', type=click.Choice(["A", "R", "P", "F", "S", "O"]))
@click.option('--fix', is_flag=True, help="Use the fixing tool to add nordics with broken syntax t the database")
@click.option('--ignore-duplicates', is_flag=True, help="In case of a duplicate event, ignore the new event")
@click.option('--no-duplicates', is_flag=True, help="Inform the program that there are no duplicate events, add all the new events")
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
@click.pass_obj
def reset(repo):
    """Resets the database to it's orginal form but keeps the tables intact. WARNING: this command will delete all information in the database"""
    resetDB.reset_database()

@cli.command()
@click.argument('event_id', click.INT)
@click.argument('output-format', type = click.Choice(["n", "q", "sc3"]))
@click.argument("output-name", required=False)
@click.pass_obj
def get(repo, event_id, output_format, output_name):
    """Command for getting files out from the database. ID tells which event you want, FORMAT tells the program that in what format you want the file(n - nordic, q - quakeml, sc3 - seiscomp3) and output-name tells the output file's name if you want to specify it."""
    if output_format == "n":
        sql2nordic.writeNordicEvent(event_id, USER_PATH)
    elif output_format == "q":
        sql2quakeml.writeQuakeML(event_id, USER_PATH)
    elif output_format == "sc3":
        sql2sc3.writeSC3(event_id, USER_PATH)

@cli.command()
@click.pass_obj
def undo(repo):
    """Undo the last file insert made into the database"""
    undoRead.undoMostRecent()

if __name__ == "__main__":
    cli()
