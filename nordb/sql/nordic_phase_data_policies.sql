/*
+--------------------------+
|NORDIC PHASE DATA POLICIES|
+--------------------------+

This file contains the sql commands for creating the correct policies for nordic_phase_data table.
*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access all operations freely.
CREATE POLICY admin_all_policy ON nordic_phase_data TO admins USING (true) WITH CHECK (true);

/*
DEFAULT USER POLICIES
---------------------
*/

--Default user view policy. Allow users to select all nordic_phase_data rows which belong to secure or public events
CREATE POLICY user_view_policy ON nordic_phase_data FOR SELECT TO default_users 
    USING   (
            'private' != (SELECT privacy_setting FROM creation_info, nordic_event WHERE nordic_event.creation_id = creation_info.id AND nordic_event.id = nordic_phase_data.event_id)
            );

--Default user insert policy. Allow users to insert phase data if the event in question belongs to them
CREATE POLICY user_insert_policy ON nordic_phase_data FOR INSERT TO default_users 
    WITH CHECK  (
                current_user = (SELECT owner FROM creation_info, nordic_event WHERE creation_info.id = nordic_event.creation_id AND nordic_event.id = nordic_phase_data.event_id)
                AND
                (SELECT urn FROM nordic_event WHERE nordic_phase_data.event_id = nordic_event.id) IS null
                );

--Default user delete policy. Allow users to delete their own private nordic_phase_data rows freely.
CREATE POLICY user_delete_policy ON nordic_phase_data FOR DELETE TO default_users 
    USING   (
            current_user = (SELECT owner FROM creation_info, nordic_event WHERE creation_info.id = nordic_event.creation_id AND nordic_event.id = nordic_phase_data.event_id) AND
            'private' = (SELECT privacy_setting FROM creation_info, nordic_event WHERE creation_info.id = nordic_event.creation_id AND nordic_event.id = nordic_phase_data.event_id)
            );

/*
GUEST POLICIES
--------------
*/

--Guest select policy. Allow Guests to see all nordic_phase_data rows that belong to public events 
CREATE POLICY guest_select_policy ON nordic_phase_data FOR SELECT TO guests
    USING   (
            'public' = (SELECT privacy_setting FROM creation_info, nordic_event WHERE creation_info.id = nordic_event.creation_id AND nordic_event.id = nordic_phase_data.event_id)
            );
