============
Installation
============
First download or clone the program from the `Github page`_. Remember that NorDB requires Python3. After fetching it to a location of your choosing run the next command in the projects root folder::
    
    pip install --user .

or just::

    pip install .

if your are using pyenv or some other virtual python environment

This also installs all relevant python libraries for the program. 

After installation run the command::
    
    nordb

To see if the installation was succesful or not. You should be greeted by the help screen of the program.

Getting Postgres to work
------------------------
Before you can do anything with the NorDB program you have to initialise postgres. `Here`_ is a handy guide for doing that.

Initialising NorDB 
------------------
Before doing anything you have to initialise the database. First you have to configure your database for the program::

    nordb conf add

If your want to use a local database, the configuration should be the following::

    Configuration name: my_db_config_name (This can be anything, but you should avoid spaces)
    Database name: nordb (The database can have an other name, but this is not supported yet)
    Username: my_postgresql_username (your postgresql username that is allowed to create)
    Password: my_postgresql_password (This password is not safe, so you should avoid using any real passwords until a safe method for password safekeeping is found)
    Location: local

Then change your current config into your newly created one::

    nordb conf change my_db_config_name


Then you need to create the database::

    nordb create

If your organization has already a nordb database running on a computer, you can just configure your connection to that::

    Configuration name: my_db_config_name (This can be anything, but you should avoid spaces)
    Database name: organization_db_name (Usually just nordb)
    Username: my_postgresql_username (Your database username. Ask your nordb admin to create one for you)
    Password: my_postgresql_password (Remainder: This password is not safe yet)
    Location: remote
    Host Ip: ip_of_hosting_computer
    Host port: host port (Usually 5432)

At this point you should be ready to use the database.

.. _Github page: https://github.com/MrCubanfrog/NorDB
.. _Here: https://wiki.postgresql.org/wiki/Detailed_installation_guides
