Get - Get nordics out from the database
---------------------------------------
This command fetches Nordic Events from the database and recreates them in the format of users choice. Basic usage is::
    
    nordb get [OPTIONS] [EVENT_IDS]... OUTPUT_NAME

EVENT_IDS here is a list of integers which tell the program which events to get from the database. OUTPUT_NAME is the name of the file or path to file to be written. For example command::

    nordb get 1 5 19 6 output

would fetch nordic events with event_ids 1, 5, 19, 6 and write a nordic file called output.n from them in the given order.

Get also has options which are:
    
    - --event-root
    - -f/--output-format
 
Event root flag tells the program to search the events by root id instead of event id. If for example three events with ids 182, 981 and 1023 would refer to same event root id of 107, command::
    
    nordb get --event-root 107 output

would fetch all events referring to the nordic root id and write a nordic file out of thmm.

Format option changes the file format of the written event. Currently the nordb program can translate the nordic files into quakeML files and seiscomp3 SC3 files. default value for the option is nordic. You have to specify to the option which format do you want by writing

    - n - nordic format
    - q - quakeml
    - sc3 - SC3 seiscomp format

after your option flag::

    nordb get -f q 1 output

Nordb get will append the correct filename extension to your output-name, which are .n for nordic files and .xml for quakeml and sc3 files.

Getsta - Get station files out from the database
------------------------------------------------
Getsta fetches station information out from the database with the id of the station. The basic usage of the command is::

    nordb getsta [OPTIONS] [STAT_IDS]... OUTPUT_NAME

Getsta STAT_IDS refer to the integer ids of the station files in the database and OUTPUT_NAME ferers to the name of the file outputted by the command.

Getsta has one relevant option: -f/--format. Which tells the program which format you want to get out from the database. As in css format, the station files are usually saved to different flat files, specifying "site", "sitechan", "sensor" or "instrument" to the command will only fetch the one corresponding file. If "all" is given, the program will output all four relevant files. If "stationxml" is given to the option, the program will transform the station information into stationXML format.

Insert - Insert Nordic Files to the database
--------------------------------------------
This command is the main way of adding nordic files to the nordb database. It only works for files in the nordic format. The basic format for the command is::

    nordb insert [OPTIONS] SOLUTION_TYPE FILENAMES...

SOLUTION_TYPE tells the command the type of the solution of the nordic files to be pushed into the database. Filenames refer to all files that will be read and pushed to the database.

The options for nordb insert are

    - -nf/--nofix
    - -ig/--ignore-duplicates
    - -n/--no-duplicates
    - -a/--add-automatic

--nofix tells the program to not use automatic fixing tool to fix some common mistakes in nordic files. Be warned that the files probably wont be pushed to the database if this option is put on.--ignore-duplicates tells the program to ignore all identical Nordic Events that already exist in the dabase. --no-duplicates tells the database to ignore all same or similar events found on the database and just assume that the events pushed do not exist on the database. --add-automatic tells the program to automatically add the event to the first found event root without prompts from the user. All similar events will be ignored.


Insersta - Insert station files to the database
-----------------------------------------------

Reset - Reset database 
----------------------

Search - Search for events in the database
------------------------------------------

Stype - Manage database solution types
--------------------------------------

Undo - Undo commands
--------------------
