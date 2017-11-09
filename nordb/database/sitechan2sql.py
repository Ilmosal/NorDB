from datetime import date, timedelta
import string
import logging

import psycopg2

from nordb.core import usernameUtilities

username = ""

SITECHAN_INSERT = ""

class Sitechan:

