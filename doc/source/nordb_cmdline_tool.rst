=======================
NorDB Command Line Tool
=======================

NorDB comes with a handy command line tool for managing the database. Most of the basic functions are available through it, without using the API. This tutorial goes through all of the functions in the nordb command line tool. Every single command in nordb has a help page which can be accessed with --h/-h flag alongside your command.

.. figure:: pictures/screenshot_nordb.png
    :scale: 100%
    :alt: Screenshot of the terminal

    **1. Screenshot of the NorDB terminal command**


Backup - Backing up your database
---------------------------------
This command is accessed by::

    nordb backup [OPTIONS]

nordb backup wraps all backup related commands into a single easy command. It has four optional flags to choose from, which are:

    - --list - Default option of the backup. It lists all backups made by user by date and filename.
    - --create / -c - creates a backup from the current database. 
    - --delete / -d - removes a backup file safely
    - --load / -l - creates the database again from a backup file

Each of the options have a simple command line interface as it prompts the required information from the user. Use the key in the list given by the program to choose which backup file you want to choose for your operation

Chgroot - Changing the root id of the event
-------------------------------------------


