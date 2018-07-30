/*
+----------------------+
|SOLUTION TYPE POLICIES|
+----------------------+

This file contains the sql commands for creating the correct policies for solution type table.

*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access solution type freely except for default solutions A, O, F
CREATE POLICY admin_all_policy ON solution_type FOR ALL TO admins
    USING (true) WITH CHECK (
                            type_id != 'A' OR 
                            type_id != 'O' OR
                            type_id != 'F'
                            );

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all solution_type rows except for private ones which do not belong to the user
CREATE POLICY user_view_policy ON solution_type FOR SELECT TO default_users
    USING   (
            current_user = (SELECT owner FROM creation_info WHERE creation_info.id = solution_type.creation_id) OR 
            'private' != (SELECT privacy_setting FROM creation_info WHERE creation_info.id = solution_type.creation_id)
            );

--User insert policy. Allows user to insert solution_type rows freely if the created solution types are private and their own
CREATE POLICY user_insert_policy ON solution_type FOR INSERT TO default_users
    WITH CHECK  (
                current_user = (SELECT owner FROM creation_info WHERE creation_info.id = solution_type.creation_id) AND
                'private' = (SELECT privacy_setting FROM creation_info WHERE creation_info.id = solution_type.creation_id)
                );

--User delete policy. Allows user to delete solution_type rows if they are private and their own
CREATE POLICY user_delete_policy ON solution_type FOR DELETE TO default_users
    USING   (
            (current_user = (SELECT owner FROM creation_info WHERE creation_info.id = solution_type.creation_id) AND
            'private' = (SELECT privacy_setting FROM creation_info WHERE creation_info.id = solution_type.creation_id)) 
            AND
            (0 = (SELECT COUNT(*) FROM nordic_event WHERE nordic_event.solution_type = solution_type.type_id)) 
            );

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow Guests to see only public solution_type rows
CREATE POLICY guest_view_policy ON solution_type FOR SELECT TO guests
    USING   (
            'public' = (SELECT privacy_setting FROM creation_info WHERE creation_info.id = solution_type.creation_id)
            );

