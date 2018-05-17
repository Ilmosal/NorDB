/*
+-----------------+
|RESPONSE POLICIES|
+-----------------+

This file contains the sql commands for creating the correct policies for response table.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access response freely 
CREATE POLICY admin_all_policy ON response TO admins
    USING (true) WITH CHECK (true);

/*
STATION MANAGER POLICIES
------------------------
*/

--Station Manager view policy. Allows station_managers to see all response rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON response FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan, sensor, instrument
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id AND
                                    instrument.id = sensor.instrument_id AND
                                    instrument.id = response.instrument_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan, sensor, instrument
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id AND 
                                instrument.id = sensor.instrument_id AND
                                instrument.id = response.instrument_id)
            );

--Station Manager insert policy. Allows station_managers to insert response rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON response FOR INSERT TO station_managers
    WITH CHECK  (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan, sensor, instrument
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id AND
                                    instrument.id = sensor.instrument_id AND
                                    instrument.id = response.instrument_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan, sensor, instrument
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id AND 
                                instrument.id = sensor.instrument_id AND
                                instrument.id = response.instrument_id)
            );


--Station Manager delete policy. Allows station_managers to delete response rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON response FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan, sensor, instrument
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id AND
                                    instrument.id = sensor.instrument_id AND
                                    instrument.id = response.instrument_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan, sensor, instrument
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id AND 
                                instrument.id = sensor.instrument_id AND
                                instrument.id = response.instrument_id)
            );

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all response rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON response FOR SELECT TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan, sensor, instrument
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id AND
                                    instrument.id = sensor.instrument_id AND
                                    instrument.id = response.instrument_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan, sensor, instrument
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id AND 
                                instrument.id = sensor.instrument_id AND
                                instrument.id = response.instrument_id)
            );

--User insert policy. Allows user to insert private response rows
CREATE POLICY user_insert_policy ON response FOR INSERT TO default_users
    WITH CHECK  (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan, sensor, instrument
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id AND
                                    instrument.id = sensor.instrument_id AND
                                    instrument.id = response.instrument_id) 
            AND 
            'private' = (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan, sensor, instrument
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id AND 
                                instrument.id = sensor.instrument_id AND
                                instrument.id = response.instrument_id)
            );


--User delete policy. Allows user to delete response rows if they belong to their own private network
CREATE POLICY user_delete_policy ON response FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan, sensor, instrument
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id AND
                                    instrument.id = sensor.instrument_id AND
                                    instrument.id = response.instrument_id) 
            AND 
            'private' = (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan, sensor, instrument
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id AND 
                                instrument.id = sensor.instrument_id AND
                                instrument.id = response.instrument_id)
            );

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow guest to see all public response rows
CREATE POLICY guest_view_policy ON response FOR SELECT TO guests
    USING   (
            'public' = (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan, sensor, instrument
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id AND 
                                instrument.id = sensor.instrument_id AND
                                instrument.id = response.instrument_id)
            );
