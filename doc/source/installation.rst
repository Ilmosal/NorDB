============
Installation
============
First download or clone the program from the `Github page`_. After fetching, it to a location of your choosing run::
    
    pip install --editable .

on the main folder which contains the setup.py file. This should also install all relevant python libraries for the program. You might need sudo rights for the installation. You can also use the programs commandline tool by executing the NorDB/nordb/bin/NorDB.py file. 

After installing run the command::
    
    nordb

To see if the installation was succesful or not. You should be greeted by the help screen of the program.

Getting Postgres to work
------------------------
Before you can do anything with the NorDB program you have to initialise postgres. `Here`_ is a handy guide for doing that.

Initialising NorDB 
------------------
Before doing anything you have to initialise the database. This can be done in following way. First you have to initialise the username file to tell your username for the program::

    nordb conf --username <your postgres username>

This creates a username file in the program so you don't have to give the program your username all the time. Then you have to create the database::

    nordb create

At this point you should be ready to use the Program.

.. _Github page: https://github.com/MrCubanfrog/NorDB
.. _Here: https://wiki.postgresql.org/wiki/Detailed_installation_guides
