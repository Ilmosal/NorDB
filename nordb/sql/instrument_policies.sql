/*
+-------------------+
|INSTRUMENT POLICIES|
+-------------------+

This file contains the sql commands for creating the correct policies for instrument table.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access instrument freely 
CREATE POLICY admin_all_policy ON instrument FOR ALL TO admins
    USING (true) WITH CHECK (true);

/*
STATION MANAGER POLICIES
------------------------
*/

--Station Manager view policy. Allows station_managers to see all instrument rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON instrument FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.response_id = response.id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = instrument.response_id)
            );

--Station Manager insert policy. Allows station_managers to insert instrument rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON instrument FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        instrument.response_id = response.id) 
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.response_id = response.id)
                );


--Station Manager delete policy. Allows station_managers to delete instrument rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON instrument FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.response_id = response.id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                instrument.response_id = response.id)
            );

--Station Manager update policy. Allows station_managers to close instruments
CREATE POLICY station_manager_update_policy ON instrument FOR UPDATE TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        instrument.response_id = response.id) 
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.response_id = response.id)
                );


/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all instrument rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON instrument FOR SELECT TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.response_id = response.id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                instrument.response_id = response.id)
            );

--User insert policy. Allows user to insert private instrument rows
CREATE POLICY user_insert_policy ON instrument FOR INSERT TO default_users
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        instrument.response_id = response.id) 
                AND 
                'public' != (   SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.id = response.id)
                );


--User delete policy. Allows user to delete instrument rows if they belong to their own private network
CREATE POLICY user_delete_policy ON instrument FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.response_id = response.id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                instrument.response_id = response.id)
            );

--User update policy. Allows user to close their own private instruments
CREATE POLICY user_update_policy ON instrument FOR UPDATE TO default_users
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        instrument.response_id = response.id) 
                AND 
                'private' = (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    instrument.response_id = response.id)
                );

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow guest to see all public instrument rows
CREATE POLICY guest_view_policy ON instrument FOR SELECT TO guests
    USING   (
            'public' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                instrument.response_id = response.id)
            );
