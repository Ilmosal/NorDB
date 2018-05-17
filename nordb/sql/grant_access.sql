/*
+------------+
|GRANT ACCESS|
+------------+

This folder contains all sql commands for giving database roles the proper access rights.
*/

/*
ADMIN RIGHTS
------------
*/

--Grant all privileges for admins
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admins;
--Give admins a right to create new roles
ALTER USER admins WITH CREATEROLE;

/*
STATION MANAGER RIGHTS
----------------------
Not needed as station manager inherits the rights of the default user
*/


/*
DEFAULT USER RIGHTS
-------------------
*/

--Default user rights
GRANT
    SELECT, INSERT, DELETE
ON
    creation_info, fap_response, fap, instrument, network,
    nordb_user, nordic_event, nordic_event_root, nordic_file,
    nordic_header_comment, nordic_header_error, nordic_header_macroseismic,
    nordic_header_main, nordic_header_waveform, nordic_phase_data,
    paz_response, pole, zero, response, sensor, sitechan, solution_type, station
TO
    default_users;

--Give user a right to update off_date value of station
GRANT
    UPDATE(off_date)
ON
    station
TO
    default_users;

GRANT 
    USAGE
ON
    creation_info_id_seq, fap_response_id_seq, instrument_id_seq, network_id_seq,
    nordic_event_id_seq, nordic_event_root_id_seq, nordic_file_id_seq, nordic_header_comment_id_seq,
    nordic_header_error_id_seq, nordic_header_macroseismic_id_seq, nordic_header_main_event_id_seq,
    nordic_header_main_id_seq, nordic_header_waveform_id_seq, nordic_phase_data_id_seq,
    paz_response_id_seq, response_id_seq, sensor_id_seq, station_id_seq
TO
    default_users;
/*
GUEST RIGHTS
------------
*/

--Guest rights
GRANT
    SELECT
ON
    creation_info, fap_response, fap, instrument, network,
    nordb_user, nordic_event, nordic_event_root, nordic_file,
    nordic_header_comment, nordic_header_error, nordic_header_macroseismic,
    nordic_header_main, nordic_header_waveform, nordic_phase_data,
    paz_response, pole, zero, response, sensor, sitechan, solution_type, station
TO
    guests;

