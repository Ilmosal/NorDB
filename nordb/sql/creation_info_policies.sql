/*
+----------------------+
|CREATION INFO POLICIES|
+----------------------+

This file contains the sql commands for creating the correct policies for creation info table.

*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access creation info freely
CREATE POLICY admin_all_policy ON creation_info TO admins
    USING (true) WITH CHECK (true);

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see all creation info objects that are not private
CREATE POLICY user_view_policy ON creation_info FOR SELECT TO default_users
    USING   (
            owner = current_user OR 
            privacy_setting != 'private'
            );

--User insert policy. Allows user to insert creation_info rows freely 
CREATE POLICY user_insert_policy ON creation_info FOR INSERT TO default_users
    WITH CHECK  (
                owner = current_user
                );

--User delete policy. Allows user to delete creation_info rows if they are private and their own
CREATE POLICY user_delete_policy ON creation_info FOR DELETE TO default_users
    USING   (
            owner = current_user AND
            privacy_setting = 'private'
            );

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow Guests to see only public creation info objects
CREATE POLICY guest_view_policy ON creation_info FOR SELECT TO guests
    USING   (
                privacy_setting = 'public'
            );


