========================
Nordic to CSS conversion
========================
Nordic files do not convert one to one into the css format as it lacks station information, but this document contains the extensive conversion from nordic into the css format.

Nordic Main Header
------------------
All time related information (Year, day, hour) etc -> origin.time, origin.jdate
quality indicator -> origin.qual
distance indicator -> origaux.epfixf
event id -> origin.etype
epicenter latitude -> origin.latitude
epicenter longitude -> origin.longitude
depth -> origin.depth
depth control -> origin.dtype
locating indicator -> origin.algorithm
epicenter reporting agency -> origin.auth
number of stations used -> netmag.nstat
rms of time residuals -> origerr.sdobs
magnitude 1 -> netmag.magnitude, (origin.ml, origin.ms or origin.mb)
type of magnitude 1 -> netmag.magtype
magnitude reporting agency 1 -> netmag.net
magnitude 2 -> origin.ml, origin.ms or origin.mb
type of magnitude 2 -> netmag.magtype
magnitude reporting agency 2 -> netmag.net
magnitude 3 -> origin.ml, origin.ms or origin.mb
type of magnitude 3 -> netmag.magtype
magnitude reporting agency 3 -> netmag.net

Comment Header
--------------
text -> remark.text

Error Header
------------
gap -> origaux.gap
second error -> origerr.stt^0.5, origerr.stime
epicenter latitude error -> origerr.sxx^0.5
epicenter longitude error -> origerr.syy^0.5
depth error -> origerr.sdepth, origerr.szz^0.5
magnitude error -> netmag.uncertainty

Waveform Header
---------------
waveform info -> Wfdisk file will be enough

Phase Arrival
-------------
station code -> assoc.station_code, arrival.station_code
instrument type -> #this is the job of the instrument table in css
component -> arrival.channel
quality indicator -> arrival.qual
phase type -> arrival.iphase
weighting indicator -> 
first motion -> arrival.fm
time related information (time info, hour, minute..) -> arrival.time, arrival.jdate
signal duration -> arrival.deltim
maximum amplitude -> arrival.amp
maximum amplitude period -> arrival.per
back azimuth -> arrival.azimuth
apparent velocity -> 110.7 / arrival.slow
signal to noise ratio -> arrival.snr
azimuth residual -> assoc.azres
travel time residual -> assoc.timeres
actual locating weight -> assoc.locating_weight
epicenter distance -> assoc.delta
epicenter to station azimuth -> assoc.esaz

