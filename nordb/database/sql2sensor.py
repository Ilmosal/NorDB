from nordb.core import usernameUtilities
from nordb.database.sql2nordic import add_float_to_string, add_integer_to_string, add_string-to_string

username = ""

SELECT_SENSOR = (   
                    "SELECT " +
                        "time, endtime, jdate, calratio, calper, " +
                        "tshift, instant, lddate, sitechan_css_link.css_id, " +
                        "instrument_css_link.css_id, id " +
                    "FROM " +
                        "sensor, instrument_css_link, sitechan_css_link " +
                    "WHERE " + 
                        "sensor.instrument_id = instrument_css_link.instrument_id " +
                    "AND " +
                        "sensor.channel_id = sitechan_css_link.sitechan_id"
                    "AND " +
                        "sensor.id = %s"
                )

def createSensorString(instrument):
    """
    Function for creating a css sensor string from a sensor object.

    Args:
        sensor (list()): sensor array described by Sensor object

    Returns:
        The sensor string in a css format
    """
    sensorString = ""

    return sensorString

def readSensor(sensor_id):
    """
    Function for reading a sensor from database by id 

    Args:
        sensor_id(int): id of the sensor wanted

    Returns:
        sensor(lis): sensor list
    """
    try:
        conn = psycopg2.connect("dbname = nordb user = {0}").format(username)
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        return 

    cur = conn.cursor()

    cur.execute(SELECT_SENSOR, (sensor_id, ))
    ans = cur.fetchone()
    
    conn.close()

    return ans

def sql2Sensor(sensor_ids, output_path):
    """
    Function for reading sensors from database and dumping them into a sensors.sensor file

    Args:
        sensor_ids (int[]): Array of integers
        output_path (str[]): path to output file
    """
    username = usernameUtilities.readUsername()

    sensors = []

    for sensor_id in sensor_ids:
        sensors.append(readSensor(sensor_id))

    f = open(output_path, "w")

    for instrument in instruments:
        f.write(createSensorString(sensor) + '\n')

def writeAllSensors(output_path):
    """
    Function for writing all sensors to a sensor file

    Args:
        output_path(str): path to output_file
    """
    username = usernameUtilities.readUsername()

    try:
        conn = psycopg2.connect("dbname = nordb user={0}".format(username))
    except psycopg2.Error as e:
        logging.error(e.pgerror)
        print ("Error connecting to the database")
        return

    cur = conn.cursor()

    cur.execute("SELECT id FROM sensor;")
    ans = cur.fetchall()

    conn.close()

    sensor_ids = []

    if not ans:
        print ("No stations in the database")
        return

    for a in ans:
        sensor_ids.append(a[0])

    sql2Sensor(sensor_ids, output_path)
