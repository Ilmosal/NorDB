/*
+---------------------+
|PAZ RESPONSE POLICIES|
+---------------------+

This file contains the sql commands for creating the correct policies for paz_response, pole and zero table.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access paz_response freely 
CREATE POLICY admin_all_policy ON paz_response FOR ALL TO admins
    USING (true) WITH CHECK (true);

CREATE POLICY admin_all_policy ON pole FOR ALL TO admins
    USING (true) WITH CHECK (true);

CREATE POLICY admin_all_policy ON zero FOR ALL TO admins
    USING (true) WITH CHECK (true);

/*
STATION MANAGER POLICIES
------------------------
*/

--Station Manager view policy. Allows station_managers to see all paz_response rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON paz_response FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id)
            );

--Station Manager view policy. Allows station_managers to see all pole rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON pole FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = pole.paz_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = pole.paz_id)
            );

--Station Manager view policy. Allows station_managers to see all zero rows except for private ones that do not belong to the user
CREATE POLICY station_manager_view_policy ON zero FOR SELECT TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = zero.paz_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = zero.paz_id)
            );

--Station Manager insert policy. Allows station_managers to insert paz_response rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON paz_response FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        response.id = paz_response.response_id)
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id)
                );

--Station Manager insert policy. Allows station_managers to insert pole rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON pole FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response, paz_response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        response.id = paz_response.response_id AND
                                        paz_response.id = pole.paz_id)
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = pole.paz_id)
                );

--Station Manager insert policy. Allows station_managers to insert zero rows into public and secure network freely and to their own private networks.
CREATE POLICY station_manager_insert_policy ON zero FOR INSERT TO station_managers
    WITH CHECK  (
                current_user = (SELECT 
                                        owner 
                                    FROM 
                                        creation_info, response, paz_response
                                    WHERE 
                                        creation_info.id = response.creation_id AND 
                                        response.id = paz_response.response_id AND
                                        paz_response.id = zero.paz_id)
                OR 
                'private' != (  SELECT 
                                    privacy_setting 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = zero.paz_id)
                );

--Station Manager delete policy. Allows station_managers to delete paz_response rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON paz_response FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id)
            );

--Station Manager delete policy. Allows station_managers to delete pole rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON pole FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = pole.paz_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = pole.paz_id)
            );

--Station Manager delete policy. Allows station_managers to delete zero rows if they are private and their own
CREATE POLICY station_manager_delete_policy ON zero FOR DELETE TO station_managers
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = zero.paz_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = zero.paz_id)
            );

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all paz_response rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON paz_response FOR SELECT TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id)
            );

--User view policy. Allows user to see all pole rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON pole FOR SELECT TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = pole.paz_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = pole.paz_id)
            );

--User view policy. Allows user to see all zero rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON zero FOR SELECT TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = zero.paz_id) 
            OR 
            'private' != (  SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = zero.paz_id)
            );

--User insert policy. Allows user to insert private paz_response rows
CREATE POLICY user_insert_policy ON paz_response FOR INSERT TO default_users
    WITH CHECK  (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id)
            );

--User insert policy. Allows user to insert private pole rows
CREATE POLICY user_insert_policy ON pole FOR INSERT TO default_users
    WITH CHECK  (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = pole.paz_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = pole.paz_id)
            );

--User insert policy. Allows user to insert private pole rows
CREATE POLICY user_insert_policy ON zero FOR INSERT TO default_users
    WITH CHECK  (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = zero.paz_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = zero.paz_id)
            );

--User delete policy. Allows user to delete paz_response rows if they belong to their own private network
CREATE POLICY user_delete_policy ON paz_response FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id)
            );

--User delete policy. Allows user to delete pole rows if they belong to their own private network
CREATE POLICY user_delete_policy ON pole FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = pole.paz_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = pole.paz_id)
            ); 

--User delete policy. Allows user to delete zero rows if they belong to their own private network
CREATE POLICY user_delete_policy ON zero FOR DELETE TO default_users
    USING   (
            current_user = (SELECT 
                                    owner 
                                FROM 
                                    creation_info, response, paz_response
                                WHERE 
                                    creation_info.id = response.creation_id AND 
                                    response.id = paz_response.response_id AND
                                    paz_response.id = zero.paz_id) 
            AND 
            'private' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = zero.paz_id)
            ); 

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow guest to see all public paz_response rows
CREATE POLICY guest_view_policy ON paz_response FOR SELECT TO guests
    USING   (
            'public' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id)
            );

--Guest view policy. Allow guest to see all public pole rows
CREATE POLICY guest_view_policy ON pole FOR SELECT TO guests
    USING   (
            'public' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = pole.paz_id)
            );

--Guest view policy. Allow guest to see all public zero rows
CREATE POLICY guest_view_policy ON zero FOR SELECT TO guests
    USING   (
            'public' = (   SELECT 
                                privacy_setting 
                            FROM 
                                creation_info, response, paz_response
                            WHERE 
                                creation_info.id = response.creation_id AND 
                                response.id = paz_response.response_id AND
                                paz_response.id = zero.paz_id)
            );
