"""
NorDB is a python program for saving metadata information surrounding seismic events. The database format is based on the nordic format here described by `International Seismic Center`_. The program saves all it's data in a postgres database described in :ref:`database_structure`. The database can also read meta-information about Stations and their equipment in css format  described `here`_.

.. _International Seismic Center: http://www.isc.ac.uk/standards/nordic/
.. _here: ftp://ftp.pmel.noaa.gov/newport/lau/tphase/data/css_wfdisc.pdf
"""

import nordb.core
import nordb.database
import nordb.bin
import nordb.validation
