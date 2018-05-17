/*
+---------------+
|SENSOR POLICIES|
+---------------+

This file contains the sql commands for creating the correct policies for sensor.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access sensor freely 
CREATE POLICY admin_all_policy ON sensor TO admins
    USING (true) WITH CHECK (true);

/*
STATION MANAGER POLICIES
------------------------
*/

--Station Manager view policy. Allows station_managers to see all sensor rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON sensor FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id)
            );

--Station Manager insert policy. Allows station_managers to insert sensor rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON sensor FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, network, station, sitechan
                                    WHERE 
                                        creation_info.id = network.creation_id AND 
                                        network.id = station.network_id AND 
                                        station.id = sitechan.station_id AND
                                        sitechan.id = sensor.sitechan_id) 
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id)
                );


--Station Manager delete policy. Allows station_managers to delete sensor rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON sensor FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id) 
            AND
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id)
            );

--Station Manager update policy. Allows station_managers to close sensors
CREATE POLICY station_manager_update_policy ON sensor FOR UPDATE TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, network, station, sitechan
                                    WHERE 
                                        creation_info.id = network.creation_id AND 
                                        network.id = station.network_id AND 
                                        station.id = sitechan.station_id AND
                                        sitechan.id = sensor.sitechan_id) 
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id)
                );


/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all sensor rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON sensor FOR SELECT TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id)
            );

--User insert policy. Allows user to insert private sensor rows
CREATE POLICY user_insert_policy ON sensor FOR INSERT TO default_users
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, network, station, sitechan
                                    WHERE 
                                        creation_info.id = network.creation_id AND 
                                        network.id = station.network_id AND 
                                        station.id = sitechan.station_id AND
                                        sitechan.id = sensor.sitechan_id) 
                AND
                'private' = (   SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id)
                );


--User delete policy. Allows user to delete sensor rows if they belong to their own private network
CREATE POLICY user_delete_policy ON sensor FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, network, station, sitechan
                            WHERE 
                                creation_info.id = network.creation_id AND 
                                network.id = station.network_id AND 
                                station.id = sitechan.station_id AND
                                sitechan.id = sensor.sitechan_id)
            );

--User update policy. Allows user to close their own private sensors
CREATE POLICY user_update_policy ON sensor FOR UPDATE TO default_users
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, network, station, sitechan
                                    WHERE 
                                        creation_info.id = network.creation_id AND 
                                        network.id = station.network_id AND 
                                        station.id = sitechan.station_id AND
                                        sitechan.id = sensor.sitechan_id) 
                AND 
                'private' = (   SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id)
                );

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow guest to see all public sensors rows
CREATE POLICY guest_view_policy ON sensor FOR SELECT TO guests
    USING   (
            'public' = (   SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, network, station, sitechan
                                WHERE 
                                    creation_info.id = network.creation_id AND 
                                    network.id = station.network_id AND 
                                    station.id = sitechan.station_id AND
                                    sitechan.id = sensor.sitechan_id)
            );
