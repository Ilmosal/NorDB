"""
Python module for logging into quake server with paramiko and establishing a sftp connection with it. This module is only useful in it's current state for the computers in our own network and it requires RSA-key to work.

Functions and Classes
---------------------
"""

import datetime
import base64
from binascii import hexlify
import getpass
import os
import sys
import socket
import traceback
import paramiko
import psycopg2 

from nordb.core import nordicRead
from nordb.core import usernameUtilities
from nordb.core.nordic import NordicData
from nordb.core.nordic import NordicMain
from nordb.core import nordic
from nordb.database import nordic2sql
from nordb.database import getNordic

arcdata_cfg_path = "/b/fdc/config/arcdata_id.cfg"

username = ""

stat_locations =    {
                        "peak":"/net/peak/home/sysop/seiscomp3/acquisition/archive",
                        "fenno":"/net/obelix/space/sysop/seiscomp3/acquisition/archive",
                        "tarvas":"/net/tarvas/rack/disk2/archive",
                        "oulu":"/net/tarvas/rack/disk3/archive"
                    }

channel_folders =   {
                        "BHE.D",
                        "HHE.D",
                        "BHN.D",
                        "HHN.D",
                        "BHZ.D",
                        "HHZ.D"
                    }

def agentAuth(t, username):
    """
    Attempt to authenticate to the given transport using any of the private keys available from a SSH agent
    
    :param paramiko.Transport transport: Paramiko transport object
    :param str username: name of the connecting user
    """
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()

    if len(agent_keys) == 0:
        return

    for key in agent_keys:
        print("Trying ssh-agent key {0}".format(hexlify(key.get_fingerprint())))
        try:
            t.auth_publickey(username, key)
            print('... success!')
            return
        except paramiko.SSHException:
            print('... nope.')

def manualAuth(username, hostname, t):
    """
    Function for manual authentication of the Transport.

    :param str username: name of the connecting user
    :param str hostname: name of the host 
    :param paramiko.Transport t: Paramiko transport object
    """
    path = os.path.join(os.environ('HOME', '.ssh', 'id_rsa'))
    try:
        key = paramiko.RSAKey.from_private_key_file(path)
    except Exception as e:
        print("Error with trying to get the key file")
        raise e
    t.auth_publickey()
    
def getSeed(station, year, day, silent=True):
    """
    Function for connecting into quake and finding the seed data from the server.

    :param str station: station name
    :param int year: year of the event
    :param int jday: julian day of the event
    :return: The names of the files written
    :raises: IOExceptions or Paramiko exceptions in case something goes wrong.
    """
    #logging
    paramiko.util.log_to_file("quake_conn.log")

    # get host name
    hostname = 'quake'
    username = getpass.getuser()
    port = 22

    path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')

    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception as e:
        if not silent:
            print('*** Connect failed: ' + str(e))
            traceback.print_exc()
        raise e

    try:
        t = paramiko.Transport(sock)

        try:
            t.start_client()
        except paramiko.SSHException as e:
            if not silent:
                print('*** SSH negotiation failed')
            raise e
        
        #get host key
        hostkeytype = None
        hostkey = None

        try:
            host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                host_keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                if not silent:
                    print("*** Unable to open host keys file")
                host_keys = {}
                raise IOError

        key = t.get_remote_server_key()

        if hostname not in host_keys:
            if not silent:
                print("*** WARNING: Unknown host key!")
        elif key.get_name() not in host_keys[hostname]:
            if not silent:
                print("*** WARNING: Unknown host key!")
        elif keys[hostname][key.get_name()] != host_key:
            if not silent:
                print("*** WARNING: Host key has changed!")
            raise Exception
        else:
            if not silent:
                print("*** Host key OK.")

        agentAuth(t, username)
        
        if not t.is_authenticated():
            manualAuth(username, hostname, t)
        if not t.is_authenticated():
            if not silent:
                print("*** Authentication failed.")
            t.close()
            raise Exception

        sftp = paramiko.SFTPClient.from_transport(t)

        try:
            arcdata_cfg = sftp.file(arcdata_cfg_path)
        except IOError:
            if not silent:
                print("*** Warning arcdata_id.cfg not found in path: {0}".format(arcdata_cfg_path))
            t.close()
            raise IOError

        ans = None

        for line in arcdata_cfg:
            vals = [val for val in line[:-1].split(" ") if val.strip() != ""]
            if vals[1] == station:
                ans = vals
                break

        arcdata_cfg.close()

        try:
            path = stat_locations[ans[4]]
        except Exception as e:
            if not silent:
                print("Such station does not exist in arcdata!")
            raise e
        path += "/{0}/{1}/{2}/".format(year, ans[0], ans[1])

        file_name = "{0}.{1}..{2}.{3}.{4:03d}".format(ans[0], ans[1], "{0}", year, day)
   
        file_names = []
         
        for cha in channel_folders:
            s_path = "{0}{1}/{2}".format(path, cha, file_name.format(cha)) 
            try:
                sftp.get(s_path, file_name.format(cha))
            except Exception as e:
                if not silent:
                    print("*** Something went wrong while getting the file {0} from quake!\nError:{1}".format(file_name.format(cha), e))
            if os.stat(file_name.format(cha)).st_size == 0:
                os.remove(file_name.format(cha))
                continue
            file_names.append(file_name.format(cha))
        
        t.close()
        return file_names

    except Exception as e:
        try:
            t.close()
        except:
            pass
        
        raise e

def getSeedFromNordicId(nordic_id):
    """
    Function for getting a miniseed files from quake from a nordic event id.

    :param int nordic_id: id of the nordic event for which the miniseeds are fetched for
    :return: list of all filenames that was created with the operation
    """
    username = usernameUtilities.readUsername()

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except:
        logging.error("Couldn't connect to the database. Either you haven't initialized the database or your username is not valid")
        return

    cur = conn.cursor()

    nordic = getNordic.readNordicEvent(cur, nordic_id)

    date = nordic.headers[1][0].header[NordicMain.DATE]

    stations = []

    for phase_data in nordic.data:
        days = date.timetuple().tm_yday
        if phase_data.data[NordicData.TIME_INFO] == "+":
            days += 1
        year = date.timetuple().tm_year
        station = phase_data.data[NordicData.STATION_CODE]

        if station not in stations:
            stations.append(station)
    
    filenames = []

    for station in stations:
        filenames.extend(getSeed(station, year, days))

    return filenames 

def getSeedFromNordicFile(nordic_file, fix_nordic):
    """
    Function for getting a miniseed file from quake from a nordic file

    :param file nordic_file: File for which the miniseeds are fetched for
    :param bool fix_nordic: Flag for fixing some common problem with the nordic files. See nordicFix module
    :return: list of all filenames created by the operation
    """
    nordics = nordic.readNordic(nordic_file, fix_nordic)[0]
    filenames = [] 
    for n in nordics:
        date = n.headers[1][0].header[NordicMain.DATE]

        stations = []

        for phase_data in n.data:
            days = date.timetuple().tm_yday
            if phase_data.data[NordicData.TIME_INFO] == "+":
                days += 1
            year = date.timetuple().tm_year
            station = phase_data.data[NordicData.STATION_CODE]

            if station not in stations:
                stations.append(station)
        
        for station in stations:
            filenames.extend(getSeed(station, year, days))

    return filenames 
