.. NorDB documentation master file, created by
   sphinx-quickstart on Mon Dec 11 11:42:17 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NorDB's documentation!
=================================

NorDB is a python program for saving metadata information surrounding seismic events. The database format is based on the nordic format here described by `International Seismic Center`_. The program stores all event and station related metadata into a postgres database described in :ref:`database_structure`. The database can also read meta-information about Stations and their equipment in `css format`_.

.. _International Seismic Center: http://www.isc.ac.uk/standards/nordic/
.. _css format: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf

Contents:
---------

.. toctree::
    :maxdepth: 1

    database_structure.rst
    documentation.rst
    installation.rst
    nordic_desc.rst
    tutorial.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
