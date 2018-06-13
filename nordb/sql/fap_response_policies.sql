/*
+---------------------+
|FAP RESPONSE POLICIES|
+---------------------+

This file contains the sql commands for creating the correct policies for fap_response and fap table.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access fap_response freely 
CREATE POLICY admin_all_policy ON fap_response TO admins
    USING (true) WITH CHECK (true);

/*
STATION MANAGER POLICIES
------------------------
*/

--Station Manager view policy. Allows station_managers to see all fap_response rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON fap_response FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id)
            );

--Station Manager view policy. Allows station_managers to see all fap rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON fap FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, fap_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id AND
                                    fap_response.id = fap.fap_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, fap_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id AND
                                fap_response.id = fap.fap_id)
            );


--Station Manager insert policy. Allows station_managers to insert fap_response rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON fap_response FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        response.id = fap_response.response_id)
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id)
                );

--Station Manager insert policy. Allows station_managers to insert fap rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON fap FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response, fap_response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        response.id = fap_response.response_id AND
                                        fap_response.id = fap.fap_id)
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response, fap_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id AND
                                    fap_response.id = fap.fap_id)
                );



--Station Manager delete policy. Allows station_managers to delete fap_response rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON fap_response FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id)
            );

--Station Manager delete policy. Allows station_managers to delete fap rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON fap FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, fap_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id AND
                                    fap_response.id = fap.fap_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, fap_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id AND
                                fap_response.id = fap.fap_id)
            );

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all fap_response rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON fap_response FOR SELECT TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id)
            );

--User view policy. Allows user to see all fap rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON fap FOR SELECT TO default_users
    USING   (
            current_user = (    SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, fap_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id AND
                                    fap_response.id = fap.fap_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, fap_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id AND
                                fap_response.id = fap.fap_id)
            );


--User insert policy. Allows user to insert private fap_response rows
CREATE POLICY user_insert_policy ON fap_response FOR INSERT TO default_users
    WITH CHECK  (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, instrument, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id)
            );

--User insert policy. Allows user to insert private fap rows
CREATE POLICY user_insert_policy ON fap FOR INSERT TO default_users
    WITH CHECK  (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, fap_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id AND
                                    fap_response.id = fap.fap_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, fap_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id AND
                                fap_response.id = fap.fap_id)
            );


--User delete policy. Allows user to delete fap_response rows if they belong to their own private network
CREATE POLICY user_delete_policy ON fap_response FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id)
            );

--User delete policy. Allows user to delete fap rows if they belong to their own private network
CREATE POLICY user_delete_policy ON fap FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, fap_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = fap_response.response_id AND
                                    fap_response.id = fap.fap_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, fap_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id AND
                                fap_response.id = fap.fap_id)
            ); 


/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow guest to see all public fap_response rows
CREATE POLICY guest_view_policy ON fap_response FOR SELECT TO guests
    USING   (
            'public' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id)
            );

--Guest view policy. Allow guest to see all public fap rows
CREATE POLICY guest_view_policy ON fap FOR SELECT TO guests
    USING   (
            'public' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, fap_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = fap_response.response_id AND
                                fap_response.id = fap.fap_id)
            );
