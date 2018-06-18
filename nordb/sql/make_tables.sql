/*
MAKE TABLES
-----------
Main sql command for creating all tables for nordb. The commands executed 
later will create all tables and policies required for the database to work
and will also grant access to the required user groups: admins, users and 
guests. The given sql command files first always generate the tables in them,
then they generate all tables required for their creation policies.

Generated tables in their recursive form
----------------------------------------
1. nordb_user
2. creation_info
3. nordic_event_root
    a. nordic_file
    b. solution_type
    c. nordic_event
        A. nordic_header_main
           -nordic_header_error
        B. nordic_header_macroseismic
        C. nordic_header_comment
        D. nordic_header_waveform
        E. nordic_phase_data
4. network
    a. station
        A. sitechan
            1. instrument
                a. sensor
                b. response
                    A. fap_response
                    B. paz_response
*/

--1. Run create_roles.sql       -- Creates roles required for the database unless they already exist
\i create_roles.sql

--2. Run nordb_user.sql         -- Create user related tables
\i nordb_user.sql

--3. Run creation_info.sql      -- Create creation metainformation tables
\i creation_info.sql

--4. Run nordic_event_root.sql  -- Create nordic_event related tables
\i nordic_event_root.sql
    \i nordic_file.sql
    \i solution_type.sql
    \i nordic_event.sql
        \i nordic_header_main.sql
            \i nordic_header_error.sql
        \i nordic_header_macroseismic.sql
        \i nordic_header_comment.sql
        \i nordic_header_waveform.sql
        \i nordic_phase_data.sql

--5. Run network.sql            -- Create station related tables
\i network.sql
    \i station.sql
        \i sitechan.sql
            \i response.sql
                \i fap_response.sql 
                \i paz_response.sql
                \i instrument.sql
                    \i sensor.sql

--6. Run all policy files
\i creation_info_policies.sql
\i fap_response_policies.sql
\i instrument_policies.sql
\i network_policies.sql
\i nordb_user_policies.sql
\i nordic_event_policies.sql
\i nordic_event_root_policies.sql
\i nordic_file_policies.sql
\i nordic_header_comment_policies.sql
\i nordic_header_error_policies.sql
\i nordic_header_macroseismic_policies.sql
\i nordic_header_main_policies.sql
\i nordic_header_waveform_policies.sql
\i nordic_phase_data_policies.sql
\i paz_response_policies.sql
\i response_policies.sql
\i sensor_policies.sql
\i sitechan_policies.sql
\i solution_type_policies.sql
\i station_policies.sql

--7. Run grant_access.sql        -- Grant all roles their required access in the database
\i grant_access.sql

