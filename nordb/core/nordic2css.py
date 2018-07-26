from datetime import date
from datetime import datetime
from dateutil import tz
import time

def nordic2Arrival(data, arrival_id):
    """
    Function for converting a nordic file into a Arrival string

    :param NordicData data: NordicData object to be converted
    :param int arrival_id: arrival id of the assoc
    :param int origin_id: origin id of the origin
    :returns: arrival_string
    """
    arrival_string = ""

    station_code = data.station_code
    ar_time = data.observation_time.replace(tzinfo=tz.tzutc()).timestamp()
    jdate = data.observation_time.date()
    station_assoc_id = -1
    channel_id = -1
    if data.sp_component is not None:
        channel = data.sp_component.lower()
    else:
        channel = '-'
    if channel == 'h':
        channel = 'z'

    if data.phase_type is not None:
        iphase = data.phase_type
    else:
        iphase = '-'
    stype = "-"
    deltime = -1.0
    azimuth = -1.0
    delaz = -1.0
    if data.apparent_velocity is not None:
        slow = 110.7 / data.apparent_velocity
    else:
        slow = -1.0
    delslo = -1.0
    ema = -1.0
    rect = -1.0

    if data.max_amplitude is not None:
        amp = data.max_amplitude
    else:
        amp = -1.0
    if data.max_amplitude_period is not None:
        per = data.max_amplitude_period
    else:
        amp = -1.0

    per = -1.0

    logat = -1.0
    clip = '-'
    fm = '-'
    snr = -1.0
    if data.quality_indicator is not None:
        qual = data.quality_indicator.lower()
    else:
        qual = '-'
    auth = '-'
    commid = 1
    lddate = '-'

    a_format =  (
                "{sta:6s} {ar_time:17.5f} {arid:8d} {jdate:8d} {stassid:8d} "
                "{chanid:8d} {chan:8s} {iphase:8s} {stype:1s} {deltim:6.3f} "
                "{azimuth:7.2f} {delaz:7.2f} {slow:7.2f} {delslo:7.2f} "
                "{ema:7.2f} {rect:7.3f} {amp:10.1f} {per:7.2f} {logat:7.2f} "
                "{clip:1s} {fm:2s} {snr:10.2f} {qual:1s} {auth:15s} {commid:8d} "
                "{lddate:17s}"
                )

    arrival_string = a_format.format(
                                    sta = station_code,
                                    ar_time = ar_time,
                                    arid = arrival_id,
                                    jdate = int(jdate.strftime("%Y%j")),
                                    stassid = station_assoc_id,
                                    chanid = channel_id,
                                    chan = channel,
                                    iphase = iphase,
                                    stype = stype,
                                    deltim = deltime,
                                    azimuth = -1.0,
                                    delaz = delaz,
                                    slow = slow,
                                    delslo = delslo,
                                    ema = ema,
                                    rect = rect,
                                    amp = amp,
                                    per = per,
                                    logat = logat,
                                    clip = clip,
                                    fm = fm,
                                    snr = snr,
                                    qual = qual,
                                    auth = auth,
                                    commid = commid,
                                    lddate = lddate
                                    )

    return arrival_string

def nordic2Assoc(data, arrival_id, origin_id):
    """
    Function for converting a nordic file into a Assoc string

    :param NordicData data: NordicData object to be converted
    :param int arrival_id: arrival id of the assoc
    :param int origin_id: origin id of the origin
    :returns: assoc string
    """
    assoc_string = ""

    station_code = data.station_code
    phase = "-"
    belief = -1.0
    if data.epicenter_distance is not None:
        delta = data.epicenter_distance
    else:
        delta = -1.0
    station_to_event_azimuth = -1.0
    if data.epicenter_to_station_azimuth is not None:
        event_to_station_azimuth = data.epicenter_to_station_azimuth
    else:
        event_to_station_azimuth = -1.0
    if data.travel_time_residual is not None:
        time_residual = data.travel_time_residual
    else:
        time_residual = -1.0

    time_def = '-'

    if data.location_weight is not None:
        weight = data.location_weight
    else:
        weight = -1.0

    azimuth_residual = -1.0
    azimuth_def = '-'
    slowness_residual = -1.0
    slowness_def = '-'
    ema_residual = -999.0
    vmodel = '-'
    commid = -1
    lddate = '-'

    a_format =  (
                "{arid:8d} {orid:8d} {sta:6s} {phase:8s} {belief:4.2f} "
                "{delta:8.3f} {seaz:7.2f} {esaz:7.2f} {time_residual:8.3f} "
                "{time_def:1s} {azres:7.1f} {azimuth_def:1s} "
                "{slowness_residual:7.2f} {slowness_def:1s} {ema_residual:7.1f} "
                "{weight:6.3f} {vmodel:15s} {commid:8d} {lddate:17s}\n"
                )

    assoc_string += a_format.format (
                                    arid = arrival_id,
                                    orid = origin_id,
                                    sta = station_code,
                                    phase = phase,
                                    belief = belief,
                                    delta = delta,
                                    seaz = station_to_event_azimuth,
                                    esaz = event_to_station_azimuth,
                                    time_residual = time_residual,
                                    time_def = time_def,
                                    azres = azimuth_residual,
                                    azimuth_def = azimuth_def,
                                    slowness_residual = slowness_residual,
                                    slowness_def = slowness_def,
                                    ema_residual = ema_residual,
                                    weight = weight,
                                    vmodel = vmodel,
                                    commid = commid,
                                    lddate = lddate
                                    )

    return assoc_string

def nordic2Origin(main_h, origin_id):
    """
    Function for converting a nordic file into a Origin string

    :param NordicMain main_h: NordicMain object to be converted
    """
    origin_string = ""

    latitude = main_h.epicenter_latitude
    longitude = main_h.epicenter_longitude
    depth = main_h.depth
    ar_time = datetime.combine(main_h.origin_date, main_h.origin_time).replace(tzinfo=tz.tzutc()).timestamp()
    jdate = main_h.origin_date
    nass =  -1
    ndef = main_h.stations_used
    npd = -1
    grn = -1
    srn = -1
    etype = "-"
    depdp = -999.0
    if main_h.depth_control == 'F':
        dtype = 'g'
    elif main_h.depth_control == ' ':
        dtype = "f"
    else:
        dtype = '-'

    mb = -1.0
    mbid = -1
    ms = -1.0
    msid = -1
    ml = -1.0
    mlid = -1

    if main_h.type_of_magnitude_1 == 'L':
        ml = main_h.magnitude_1
    elif main_h.type_of_magnitude_1 == 'B':
        mb = main_h.magnitude_1
    elif main_h.type_of_magnitude_1 == 'S':
        ms = main_h.magnitude_1

    if main_h.type_of_magnitude_2 == 'L':
        ml = main_h.magnitude_2
    elif main_h.type_of_magnitude_2 == 'B':
        mb = main_h.magnitude_2
    elif main_h.type_of_magnitude_2 == 'S':
        ms = main_h.magnitude_2

    if main_h.type_of_magnitude_3 == 'L':
        ml = main_h.magnitude_3
    elif main_h.type_of_magnitude_3 == 'B':
        mb = main_h.magnitude_3
    elif main_h.type_of_magnitude_3 == 'S':
        ms = main_h.magnitude_3

    algorithm = "-"
    auth = "-"
    commid = -1
    lddate = "-"

    o_format = ("{latitude:9.4f} {longitude:9.4f} {depth:9.4f} {ar_time:17.5f} "
                "{orid:8d} {evid:8d} {jdate:8d} {nass:4d} {ndef:4d} {npd:4d} "
                "{grn:8d} {srn:8d} {etype:7s} {depdp:9.4f} {dtype:1s} {mb:7.2f} "
                "{mbid:8d} {ms:7.2f} {msid:8d} {ml:7.2f} {mlid:8d} "
                "{algorithm:15s} {auth:15s} {commid:8d} {lddate:17s}\n")

    origin_string = o_format.format(latitude = latitude,
                                    longitude = longitude,
                                    depth = depth,
                                    ar_time = ar_time,
                                    orid = origin_id,
                                    evid = -1,
                                    jdate = int(jdate.strftime("%Y%j")),
                                    nass = nass,
                                    ndef = ndef,
                                    npd = npd,
                                    grn = grn,
                                    srn = srn,
                                    etype = etype,
                                    depdp = depdp,
                                    dtype = dtype,
                                    mb = mb,
                                    mbid = mbid,
                                    ms = ms,
                                    msid = msid,
                                    ml = ml,
                                    mlid = mlid,
                                    algorithm = algorithm,
                                    auth = auth,
                                    commid = commid,
                                    lddate = lddate)

    return origin_string

def nordic2Wfdisc(nordic_event):
    """
    Function for converting a nordic file into a Wfdisc file and writing it into a file.

    :param NordicEvent nordic_event: NordicEvent object to be converted
    """
    pass

def nordic2css(nordic_event, css_filename):
    """
    Function for converting a nordic event into css format and writing it into a origin, assoc and arrival files.
    """
    origin_id = 1
    arrival_id = 1

    origin_string = nordic2Origin(nordic_event.main_h[0],
                                  origin_id)
    arrival_string = ""
    assoc_string = ""
    for data in nordic_event.data:
        arrival_string += nordic2Arrival(data, arrival_id) + "\n"
        assoc_string += nordic2Assoc(data, arrival_id, origin_id) + "\n"
        arrival_id += 1

    origin_file = open(css_filename + ".origin", "w")
    origin_file.write(origin_string)
    origin_file.close()
    arrival_file = open(css_filename + ".arrival", "w")
    arrival_file.write(arrival_string)
    arrival_file.close()
    assoc_file = open(css_filename + ".assoc", "w")
    assoc_file.write(assoc_string)
    assoc_file.close()
