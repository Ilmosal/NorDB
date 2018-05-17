/*
+----------------+
|NETWORK POLICIES|
+----------------+

This file contains the sql commands for creating the correct policies for network table.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access network freely 
CREATE POLICY admin_all_policy ON network TO admins
    USING (true) WITH CHECK (true);

/*
STATION MANAGER POLICIES
------------------------
*/

--Station Manager view policy. Allows station_managers to see all network rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON network FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT owner FROM creation_info WHERE creation_info.id = network.creation_id) OR 
            'private' != (SELECT privacy_setting FROM creation_info WHERE creation_info.id = network.creation_id)
            );

--Station Manager insert policy. Allows station_managers to insert network rows freely
CREATE POLICY station_manager_insert_policy ON network FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT owner FROM creation_info WHERE creation_info.id = network.creation_id)
                );

--Station Manager delete policy. Allows station_managers to delete network rows if there are no stations that refer to the network
CREATE POLICY station_manager_delete_policy ON network FOR DELETE TO station_managers
    USING   (
            0 = (SELECT COUNT(*) FROM station WHERE station.network_id = network.id)
            );

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all network rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON network FOR SELECT TO default_users
    USING   (
            current_user = (SELECT owner FROM creation_info WHERE creation_info.id = network.creation_id) OR 
            'private' != (SELECT privacy_setting FROM creation_info WHERE creation_info.id = network.creation_id)
            );

--User insert policy. Allows user to insert private network rows
CREATE POLICY user_insert_policy ON network FOR INSERT TO default_users
    WITH CHECK  (
                'private' = (SELECT privacy_setting FROM creation_info WHERE creation_info.id = network.creation_id) AND
                current_user = (SELECT owner FROM creation_info WHERE creation_info.id = network.creation_id)
                );

--User delete policy. Allows user to delete their own empty private networks
CREATE POLICY user_delete_policy ON network FOR DELETE TO default_users
    USING   (
            0 = (SELECT COUNT(*) FROM station WHERE station.network_id = network.id) AND
            current_user = (SELECT owner FROM creation_info WHERE creation_info.id = network.creation_id) AND
            'private' = (SELECT privacy_setting FROM creation_info WHERE creation_info.id = network.creation_id)
            );

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow guest to see all public network rows
CREATE POLICY guest_view_policy ON network FOR SELECT TO guests
    USING   (
            'public' = (SELECT privacy_setting FROM creation_info WHERE network.creation_id = creation_info.id)
            );

