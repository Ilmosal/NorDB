/*
+---------------------+
|NORDIC EVENT POLICIES|
+---------------------+

This file contains the sql commands for creating the correct policies for nordic events.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access all operations freely.
CREATE POLICY admin_all_policy ON nordic_event FOR ALL TO admins USING (true) WITH CHECK (true);

/*
DEFAULT USER POLICIES
---------------------
*/

--Default user view policy. Allow users to select all event roots which have secure or public events in them
CREATE POLICY user_view_policy ON nordic_event FOR SELECT TO default_users 
    USING   (
            'private' != (SELECT privacy_setting FROM creation_info WHERE nordic_event.creation_id = creation_info.id) OR
            current_user = (SELECT owner FROM creation_info WHERE nordic_event.creation_id = creation_info.id)
            );

--view for evading possible infinite policy recursion for inserting nordic_events
CREATE VIEW user_thing AS 
	(
	SELECT nordic_event.root_id as root_id, owner, privacy_setting FROM nordic_event, creation_info WHERE nordic_event.creation_id = creation_info.id
	);

GRANT SELECT ON user_thing TO default_users;

--Default user insert policy. Allow users to insert events if the solution type belongs to them or is public/secure and the root_id does not have only private solutions that don't belong to the current user.
CREATE POLICY user_insert_policy ON nordic_event FOR INSERT TO default_users 
    WITH CHECK  (
                ('private' != (SELECT privacy_setting FROM creation_info, solution_type WHERE solution_type.type_id = nordic_event.solution_type AND solution_type.creation_id = creation_info.id) OR
                current_user = (SELECT owner FROM creation_info, solution_type WHERE solution_type.type_id = nordic_event.solution_type AND solution_type.creation_id = creation_info.id)) 
                OR
                ('public' = (SELECT privacy_setting FROM user_thing WHERE user_thing.root_id = nordic_event.root_id) OR
                'secure' = (SELECT privacy_setting FROM user_thing WHERE user_thing.root_id = nordic_event.root_id) OR
                current_user in (SELECT owner FROM user_thing WHERE nordic_event.root_id = user_thing.root_id) 
                ));

--Default user delete policy. Allow users to delete their own private nordic_events freely.
CREATE POLICY user_delete_policy ON nordic_event FOR DELETE TO default_users 
    USING   (
            'private' = (SELECT privacy_setting FROM creation_info WHERE creation_info.id = nordic_event.creation_id AND creation_info.owner = current_user)
            );

/*
GUEST POLICIES
--------------
*/

--Guest select policy. Allow Guests to see all public events
CREATE POLICY guest_select_policy ON nordic_event FOR SELECT TO guests
    USING   (
            'public' = (SELECT privacy_setting from creation_info WHERE nordic_event.creation_id = creation_info.id)
            );
