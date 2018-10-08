# NorDB
[![Build Status](https://travis-ci.org/MrCubanfrog/NorDB.svg?branch=master)](https://travis-ci.org/MrCubanfrog/NorDB)[![Code Health](https://landscape.io/github/MrCubanfrog/NorDB/master/landscape.svg?style=flat)](https://landscape.io/github/MrCubanfrog/NorDB/master)[![codecov](https://codecov.io/gh/MrCubanfrog/NorDB/branch/master/graph/badge.svg)](https://codecov.io/gh/MrCubanfrog/NorDB)[![Documentation Status](https://readthedocs.org/projects/nordb/badge/?version=latest)](https://nordb.readthedocs.io/en/latest/?badge=latest)

Database project for reading seismic data from .nordic files into a postgres database.

## Installation

NorDB works with only with python 3.2=> so remember to install your most recent python version. Clone the module to somewhere, go into its root folder and run

> pip install --user .

This should install the module correctly. If you want to build the documentation just run the build\_docs.sh script to build the documentation page for this project. The documentation will be located in the docs folder. To open the index page for the project just open the file /docs/build/index.html with your preferred browser. 

> ./build_docs.sh
> firefox docs/build/index.html


## Database

To use the database capabilities of NorDB you need to have a PostgreSQL database of version 10-> running on your computer. If you want to use the more advanced user features your should modify your postgresql configuration files so that your postgresql server requires a password to enter. Otherwise you can just use the program without any passwords.

To create the database you have to first configure your PostgreSQL user to the database. This is done by using the "nordb conf add" command on your terminal, or modifying your .nordb.config file with your text editor.
