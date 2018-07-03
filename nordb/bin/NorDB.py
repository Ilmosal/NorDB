#!/usr/bin/env python3

"""
This is the command line tool of the whole program. The command line tool is created with python library Click and that's why it's functions are not usable in same way compared to the others. If you have installed the Library correctly, you can use the command line tool by typing ``nordb`` into your terminal.
"""

import os
import fnmatch
from subprocess import call
from datetime import datetime

import click
from lxml import etree

MODULE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + os.sep

from nordb.core import usernameUtilities
from nordb.core.nordbConf import confUser, confExists

if not confExists():
    confUser()

from nordb.database import instrument2sql
from nordb.database import nordic2sql
from nordb.database import sensor2sql
from nordb.database import sitechan2sql
from nordb.database import station2sql
from nordb.database import response2sql

from nordb.database import nordicSearch
from nordb.database import norDBManagement
from nordb.database import resetDB
from nordb.database import nordicModify
from nordb.database import solutionTypeHandler
from nordb.database import creationInfo

from nordb.database import sql2instrument
from nordb.database import sql2nordic
from nordb.database import sql2sensor
from nordb.database import sql2station
from nordb.database import sql2sitechan
from nordb.database import sql2response

from nordb.core import nordic
from nordb.core import nordic2quakeml
from nordb.core import nordic2sc3
from nordb.core import nordicRead
from nordb.core import station2stationxml

from nordb.nordic import instrument
from nordb.nordic import sensor
from nordb.nordic import sitechan
from nordb.nordic import station
from nordb.nordic import response

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

class Repo(object):
    def __init__(self):
        pass

@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    """
    This is the command line tool for NorDB database. If this is your first time running the program remember to first configure your .nordb.config file with conf and then create the database using create. You also have to initialize your postgresql user before working with the database

    You can request help for all the commands with -h or --help flags.
    """
    ctx.obj = Repo()

@cli.command('conf', short_help='configure username')
@click.pass_obj
def conf(repo):
    """Configures the config file for the nordb. Give the username option your postgres username so the program can use your postgres-databased."""
    usernameUtilities.confUser()

@cli.command('createuser', short_help = "add users to db")
@click.argument('role', type=click.Choice(['default_users','admins', 'guests',
                                           'station_managers']))
@click.argument('username')
@click.pass_obj
def createuser(repo, role, username):
    """
    Create user to the database.
    """
    norDBManagement.createUser( username,
                                role,
                                click.prompt(   'Please enter password: ',
                                                hide_input=True))

@cli.command('removeuser', short_help = "remove user from db")
@click.argument('username')
@click.pass_obj
def removeuser(repo, username):
    """
    Remove user from the database.
    """
    click.confirm('Do you want to remove user {0}?'.format(username), abort=True)
    norDBManagement.removeUser(username)

@cli.command('search', short_help='search for events')
@click.option('--verbose', '-v', is_flag=True, help="Print the whole nordic file instead of the main header.")
@click.option('--output', '-o', type=click.Path(writable=True), help="file to which all events found are appended")
@click.option('--output-format', '-f', default="n", type = click.Choice(["n", "q", "sc3"]))
@click.option('--event-root', '-r', is_flag=True)
@click.argument("criteria", nargs=-1, type=click.STRING)
@click.pass_obj
def search(repo, output_format, verbose, output, event_root, criteria):
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
                        "mag":"magnitude_1",
                        "ma":"magnitude_1",
                        "m":"magnitude_1",
                        "solution_type":"solution_type",
                        "st":"solution_type",
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
                    real_vals.append(datetime.strptime(val, "%Y%jT%H:%M:%S"))
                except:
                    try:
                        real_vals.append(datetime.strptime(val, "%d.%m.%YT%H:%M:%S"))
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
        click.echo("No events found with criteria: \n{0}".format(search.getCriteriaString()[:-1]))
        return

    type_len = 4
    id_len = 3

    for e in events:
        if len(str(e.solution_type)) > type_len:
            type_len = len(str(e.solution_type))
        if len(str(e.event_id)) > id_len:
            id_len = len(str(e.event_id))

    if criteria:
        click.echo("Event Search \nCriteria: \n{0}".format(search.getCriteriaString()[:-1]))
    else:
        click.echo("All events")
    help_string = " YEAR MODA HRMN SEC  DT LAT     LON    DEP   REP ST RMS MAG REP MAG REP MAG REP"
    click.echo(" id" + (id_len-3)*" " + " | type"+(type_len-3)*" " + "|" + help_string)
    click.echo((type_len+id_len+len(help_string)+5)*"-")
    root_id = -1
    for e in events:
        if root_id != e.root_id:
            root_id = e.root_id
            click.echo("Root id: {0}".format(root_id))
        if not verbose:
            click.echo((" {0:<" + str(id_len) + "}| {1:<" + str(type_len) + "} |{2}").format(e.event_id, e.solution_type, str(e.main_h[0])[:-1]))
        else:
            click.echo(str(e))

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

@cli.command('insertresp', short_help = "insert response files")
@click.argument('response_file',
                nargs=-1,
                type=click.Path(exists=True, readable=True))
@click.pass_obj
def insertresp(repo, response_file):
    """
    This command adds a response file to the database.
    """
    for resp in response_file:
        resp_file = open(resp, 'r').read().split('\n')
        response2sql.insertResponse2Database(response.readResponseArrayToResponse(resp_file,
                                                                                 resp))

@cli.command('getresp', short_help = "get response files")
@click.argument('filename', type = click.Path(exists=False))
@click.argument('response_id', type = click.INT)
@click.pass_obj
def getresp(repo, filename, response_id):
    """
    Get response file from the database by id and write it to a file.
    """
    open(filename, 'w').write(str(sql2response.getResponse(response_id)))

@cli.command('insertsta', short_help='insert station related files')
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen in addition to error log")
@click.option('--all_files', '-a', is_flag=True, help="add all four station files: .site, .sitechan, .instrument, .sensor to db")
@click.argument('station-file', required=True, type=click.Path(exists=True, readable=True))
@click.argument('network', default="HEL")
@click.pass_obj
def insertsta(repo, station_file, network, verbose, all_files):
    """
    This command adds a site file to the database
    """
    if fnmatch.fnmatch(station_file, "*.site"):
        f_stations = open(station_file, 'r')
        stations = []

        for line in f_stations:
            if len(line.strip()) == 0 or line[0] == '#':
                continue

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
            if len(line.strip()) == 0 or line[0] == '#':
                continue

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
            if len(line.strip()) == 0 or line[0] == '#':
                continue

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
            if len(line.strip()) == 0 or line[0] == '#':
                continue

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
@click.argument('stat_ids', nargs=-1, type=click.INT)
@click.argument('output_name', required=True, type=click.Path(exists=False, readable=True))
@click.pass_obj
def getsta(repo, o_format, output_name, stat_ids):
    """
    This command fetches station related information from the database.
    """
    if o_format == "stationxml":
        stations = []
        if not stat_ids:
            stations = sql2station.getAllStations()

        for s_id in stat_ids:
            try:
                stations.append(sql2station.getStation(s_id))
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
            stations = sql2station.getAllStations()

        for s_id in stat_ids:
            try:
                stations.append(sql2station.getStation(s_id))
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
            sitechans = sql2sitechan.getAllSitechans()

        for s_id in stat_ids:
            try:
                sitechans.append(sql2sitechan.getSitechan(s_id))
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
            sensors = sql2sensor.getAllSensors()

        for s_id in stat_ids:
            try:
                sensors.append(sql2sensor.getSensor(s_id))
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
            instruments = sql2instrument.getAllInstruments()

        for i_id in stat_ids:
            try:
                instruments.append(sql2instrument.getInstrument(i_id))
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
@click.argument('event-id', type=click.INT)
@click.argument('root-id', type=click.INT)
@click.pass_obj
def chgroot(repo, root_id, event_id):
    """
    This command changes the root id of a event to root id given by user or creates a new root for the event. If root id is -9, it will attach the event to a new root.

    A root is an id to which different analyses of a same event will refer to. This groups the events together and makes it very simple to follow how the analysis of the single event has evolved. If the insert program fails to find proper root or the user accidentally attaches a event to a wrong root. This command can be used to change the root id to a new one.
    """
    nordicModify.changeEventRoot(event_id, root_id)

@cli.command('chgtype', short_help='change event type')
@click.argument('event-id', type=click.INT)
@click.argument('solution-type', type=click.STRING)
@click.pass_obj
def chgtype(repo, solution_type, event_id):
    """
    This command changes the solution type of a event with id of event-id to solution-type given by user or creates a new root for the event. Solution type refers to how final the analysis of the event is.
    """
    if solution_type not in solutionTypeHandler.getSolutionTypes():
        click.echo("Solution type given is not a valid solution type! ({0})".format(solution_type))
        click.echo("Solution types in database:")
        click.echo("Type Id | Type Description                 | Allow Multiple")
        click.echo("--------+----------------------------------+---------------")
        for s_type in solutionTypeHandler.getSolutionTypes():
            click.echo(" {0:<6} | {1:<32} | {2}".format(s_type[0], s_type[1], s_type[2]))
        return
    nordicModify.changeEventType(event_id, solution_type)

@cli.command("stype", short_help="add, remove and look solution types")
@click.option('--list', '-l', 'stype_option', flag_value='list', default=True, help="List all the solution types in the database")
@click.option('--add', '-a', 'stype_option', flag_value='add', help="add a new solution type to the database")
@click.option('--remove', '-r','stype_option', flag_value='remove', help="remove an old solution type from the database")
@click.pass_obj
def stype(repo, stype_option):
    """
    This command is for adding, removing and looking the solution types in the database. They will prompt the necessary values from the user.
    """
    try:
        if stype_option == "list":
            types = solutionTypeHandler.getSolutionTypes()
            click.echo("Type Id | Type Description                 | Allow Multiple")
            click.echo("--------+----------------------------------+---------------")
            for s_type in types:
                click.echo(" {0:<6} | {1:<32} | {2}".format(s_type[0], s_type[1], s_type[2]))
        elif stype_option == "add":
            click
            type_id = click.prompt("Enter the solution type id(Press CTR-C to escape)")
            if len(type_id) > 6:
                click.echo("{0} is too long! Maximum length of 6 characters".format(type_id))
                return
            if len(type_id) == 0:
                click.echo("No solution type given to the program!")
                return

            type_desc = click.prompt("Enter a short description for the solution type id(CTR-C to escape)")
            if len(type_desc) > 32:
                click.echo("{0} is too long. Maximum length of 32 characters".format(type_desc))
                return

            type_allow = click.prompt("Allow multiple events of same type in same event root? ", type=bool)

            try:
                solutionTypeHandler.addSolutionType(type_id, type_desc, type_allow)
            except:
                click.echo("Solution Type {0} already exists in the database!".format(type_id))
        elif stype_option == "remove":

            type_id = click.prompt("Enter the solution type id(Press CTR-C to escape)")
            if len(type_id) > 6:
                click.echo("{0} is too long! Maximum length of 6 characters".format(type_id))
                return
            if len(type_id) == 0:
                click.echo("No solution type given to the program!")
                return
            if type_id in ["O", "A", "F"]:
                click.echo("Cannot remove the default solution types from the program as that would break the program")
                return

            existing = solutionTypeHandler.getSolutionTypes()
            if type_id not in [existing[i][:1][0] for i in range(0, len(existing))]:
                click.echo("Given solution type does not exist in the database!")
                return

            search = nordicSearch.NordicSearch()
            search.addSearchExactly("solution_type", type_id)
            new_type_id = "O"

            if len(search.searchEventIds()) > 0:
                if not click.prompt("Events found with id {0}. Do you want to move them to another id?".format(type_id), type=bool):
                    return

                new_type_id = click.prompt("Enter the solution type id of the replacing solution type(Press CTR-C to escape)")
                if len(type_id) > 6:
                    click.echo("{0} is too long! Maximum length of 6 characters".format(new_type_id))
                    return
                if len(type_id) == 0:
                    click.echo("No solution type given to the program!")
                    return
                if new_type_id not in [existing[i][:1][0] for i in range(0, len(existing))]:
                    click.echo("Solution type {0} does not exist!".format(new_type_id))
                    return

            solutionTypeHandler.removeSolutionType(type_id, new_type_id)
    except KeyboardInterrupt:
        pass

@cli.command('insert', short_help="insert events")
@click.option('--nofix', '-nf', is_flag=True, help="Do not use the fixing tool to add nordics with broken syntax the database")
@click.option('--ignore-duplicates', '-ig', is_flag=True, help="In case of a duplicate event, ignore the new event")
@click.option('--no-duplicates', '-n', is_flag=True, help="Inform the program that there are no duplicate events, add all as new events with new root ids")
@click.option('--add-automatic', '-a', is_flag=True, help="In case of duplicate events, the event will be added automatically to the first event found. All similar events will be ignored")
@click.option('--verbose', '-v', is_flag=True, help="print all errors to screen instead of errorlog")
@click.argument('privacy-level', required=True, type=click.Choice(['private', 'public', 'secure']))
@click.argument('solution-type', required=True)
@click.argument('filenames', required=True, nargs=-1, type=click.Path(exists=True, readable=True))
@click.pass_obj
def insert(repo, solution_type, nofix, ignore_duplicates, no_duplicates, add_automatic, filenames, verbose, privacy_level):
    """This command adds an nordic file to the Database. The SOLUTION-TYPE tells the database what's the  solution type of the event. The suffix of the filename must be .n, .nordic or .nordicp)."""
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
                    nordic_events.append(nordic.readNordic(n_string, not nofix, -1, -1, solution_type))
                except Exception as e:
                    click.echo("Error reading nordic: {0}".format(e))
                    click.echo(n_string[0])
                    nordic_failed.append("Errors:\n{0}\n------------------------------\n".format(e))
                    nordic_failed.append(n_string)

            creation_id = creationInfo.createCreationInfo(privacy_level)
            for nord in nordic_events:

                event_id = -1
                if not no_duplicates:
                    same_events = nordicSearch.searchSameEvents(nord)
                    if add_automatic and same_events:
                        event_id = same_events[0].event_id
                    elif same_events:
                        if ignore_duplicates:
                            click.echo("Duplicate found! Ignoring event:\n{0}".format(nord.main_h[0]))
                            continue

                        click.echo("Identical events to current found! Is any of these a duplicate of yours?")
                        click.echo("{0} - (Yours)".format(nord.main_h[0]))
                        click.echo("-----------------------------------------------------------------------------------------")
                        root_id = -1
                        for e in same_events:
                            if root_id != e.root_id:
                                root_id = e.root_id
                                click.echo("Root id: {0}".format(root_id))
                            click.echo(" id: {0} - {1}".format(e.event_id, e.main_h[0]))
                        while True:
                            try:
                                event_id = int(input("Event id of the same event: "))
                                break
                            except:
                                click.echo("Not a valid id!")
                                creationInfo.deleteCreationInfoIfUnnecessary(creation_id)
                                return

                    if event_id == -1 and not add_automatic:
                        similar_events = nordicSearch.searchSimilarEvents(nord)

                        if similar_events:
                            if ignore_duplicates:
                                click.echo("Duplicate found! Ignoring event:\n{0}".format(nord.main_h[0]))
                                continue

                            click.echo("Similar events to current found! Is any of these a duplicate of yours?")
                            click.echo("{0} (Yours)".format(nord.main_h[0]))
                            click.echo("-----------------------------------------------------------------------------------------")
                            root_id = -1
                            for e in same_events:
                                if root_id != e.root_id:
                                    root_id = e.root_id
                                    click.echo("Root id: {0}".format(root_id))
                                click.echo(" id: {0} - {1}".format(e.event_id, e.main_h[0]))
                            while True:
                                try:
                                    event_id = int(input("Event id of the same event: "))
                                    break
                                except:
                                    click.echo("Not a valid id!")

                try:
                    nordic2sql.event2Database(nord, solution_type, f_nordic.name, creation_id, event_id)
                except Exception as e:
                    click.echo("Error pushing nordic to database: {0}".format(e))
                    click.echo(nord.main_h[0])
                    nordic_failed.append("Errors:\n{0}\n------------------------------\n".format(e))
                    nordic_failed.append(str(nord))

            creationInfo.deleteCreationInfoIfUnnecessary(creation_id)

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
@click.option('--event-root', is_flag=True, help="search as event_root_ids instead")
@click.option('--output-format', '-f', default="n", type = click.Choice(["n", "q", "sc3"]), help="What format you want to use. Default 'n'")
@click.pass_obj
def get(repo, output_format, event_ids, output_name, event_root):
    """
    Command for getting files out from the database. ID tells which event you want, FORMAT tells the program that in what format you want the file(n - nordic, q - quakeml, sc3 - seiscomp3) and output-name tells the output file's name if you want to specify it.

    You can create an output file by searching events with search command using --output or -o flag or simply writing event_ids on a blank file with every id being on a new line.
    """
    n_events = []
    if event_root:
        for e_id in event_ids:
            n_events.extend(sql2nordic.getNordicsRoot(e_id))
    else:
        n_events = sql2nordic.getNordics(event_ids)

    n_events = [nordic_event for nordic_event in n_events if nordic_event is not None]

    if not n_events:
        if event_root:
            click.echo("No event roots with id {0}".format(event_ids))
        else:
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

@cli.command('backup', short_help='manage backups')
@click.option('--list', 'backup_option', flag_value='list', default=True, help="list all backups, default option")
@click.option('--create', '-c', 'backup_option', flag_value='create', help="create backup from the database")
@click.option('--delete', '-d', 'backup_option', flag_value='delete', help="remove a backup from the list")
@click.option('--load', '-l','backup_option', flag_value='load', help="load backup to the database")
@click.pass_obj
def backup(repo, backup_option):
    """
    Create backups and load them.
    """
    if backup_option == "create":
        norDBManagement.createBackup()
        click.echo("Backup created!")
        return

    files = os.listdir(MODULE_PATH + "/../backups")
    backup_files = {}

    for f in files:
        try:
            time_stamp = datetime.strptime(f.split("_")[-1], "%Y%jT%H%M%S")
            backup_files[time_stamp] = f
        except:
            pass

    if not backup_files.keys():
        click.echo("No backup files found!")
        return

    key_bkup = {}

    click.echo(" backup date         | filename              | key ")
    click.echo(" --------------------+-----------------------+-----")
    i = 1

    for key in sorted(backup_files.keys()):
        click.echo(" {0} | {1} | {2}".format(key.strftime("%Y-%m-%d %H:%M:%S"), backup_files[key], i))
        key_bkup[i] = backup_files[key]
        i+=1

    if backup_option == "list":
        return

    try:
        msg = ""
        if backup_option == "load":
            msg = "To which backup you want to revert to (give key)"
        elif backup_option == "delete":
            msg = "Which backup you want to delete"

        key = int(click.prompt(msg))
    except:
        click.echo("Not a valid key! Aborting...")
        return

    if key not in key_bkup.keys():
        click.echo("Key not in list!")
        return

    if backup_option == "load":
        norDBManagement.loadBackup(key_bkup[key])

    if backup_option == "delete":
        call(["rm", os.path.dirname(MODULE_PATH) + os.sep + ".." + os.sep + "backups" + os.sep + key_bkup[key]])

if __name__ == "__main__":
    cli()
