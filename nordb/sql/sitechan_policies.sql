/*
+-----------------+
|SITECHAN POLICIES|
+-----------------+

This file contains the sql commands for creating the correct policies for sitechan.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access sitechan freely 
CREATE POLICY admin_all_policy ON sitechan TO admins
    USING (true) WITH CHECK (true);

/*
STATION MANAGER POLICIES
------------------------
*/

--Station Manager view policy. Allows station_managers to see all sitechan rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON sitechan FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) OR 
            'private' != (SELECT privacy_setting FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
            );

--Station Manager insert policy. Allows station_managers to insert sitechan rows into public and secure stations freely
CREATE POLICY station_manager_insert_policy ON sitechan FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) OR
                'private' != (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
                );

--Station Manager delete policy. Allows station_managers to delete sitechan rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON sitechan FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) AND
            'private' = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
            );

--Station Manager update policy. Allows station_managers to close sitechans
CREATE POLICY station_manager_update_policy ON sitechan FOR UPDATE TO station_managers
    WITH CHECK  (
                current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) OR
                'private' != (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
                );

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all sitechan rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON sitechan FOR SELECT TO default_users
    USING   (
            current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) OR 
            'private' != (SELECT privacy_setting FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
            );

--User insert policy. Allows user to insert private sitechan rows
CREATE POLICY user_insert_policy ON sitechan FOR INSERT TO default_users
    WITH CHECK  (
                current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) AND
                'private' = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
                );


--User delete policy. Allows user to delete sitechan rows if they belong to their own private network
CREATE POLICY user_delete_policy ON sitechan FOR DELETE TO default_users
    USING   (
            current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) AND
            'private' = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
            );

--User update policy. Allows user to close their own private sitechans
CREATE POLICY user_update_policy ON sitechan FOR UPDATE TO default_users
    WITH CHECK  (
                current_user = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id) AND
                'private' = (SELECT owner FROM creation_info, network, station WHERE creation_info.id = network.creation_id AND network.id = station.network_id AND station.id = sitechan.station_id)
                );

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow guest to see all public sitechan rows
CREATE POLICY guest_view_policy ON sitechan FOR SELECT TO guests
    USING   (
            'public' = (SELECT privacy_setting FROM creation_info, network, station WHERE network.creation_id = creation_info.id AND network.id = station.network_id AND station.id = sitechan.station_id)
            );

