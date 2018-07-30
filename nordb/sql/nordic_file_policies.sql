/*
+-------------------+
|NORDIC FILEPOLICIES|
+-------------------+

This file contains the sql commands for creating the correct policies for nordic file table.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access nordic_file freely 
CREATE POLICY admin_all_policy ON nordic_file FOR ALL TO admins
    USING (true) WITH CHECK (true);

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all nordic_file rows except for private ones that do not belong to the user
CREATE POLICY user_view_policy ON nordic_file FOR SELECT TO default_users
    USING   (
            current_user = (SELECT owner FROM creation_info, nordic_event WHERE creation_info.id = nordic_event.creation_id AND nordic_event.nordic_file_id = nordic_file.id) OR 
            'private' != (SELECT privacy_setting FROM creation_info, nordic_event WHERE creation_info.id = nordic_event.creation_id AND nordic_event.nordic_file_id = nordic_file.id)
            );

--User insert policy. Allows user to insert nordic_file rows freely
CREATE POLICY user_insert_policy ON nordic_file FOR INSERT TO default_users
    WITH CHECK (true);

--User delete policy. Allows user to delete nordic_file rows if they are allowed there are no events that refer to the nordic_file
CREATE POLICY user_delete_policy ON nordic_file FOR DELETE TO default_users
    USING   (
            0 = (SELECT COUNT(*) FROM nordic_event WHERE nordic_event.nordic_file_id = nordic_file.id)
            );

