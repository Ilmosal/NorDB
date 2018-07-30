/*
+-------------------+
|NORDN USER POLICIES|
+-------------------+

This file contains the sql commands for creating the correct policies for NorDB users.

*/

/*
ADMIN POLICIES
--------------
*/

--Admin policy. Allow admins to access all users except the owner of the database freely
CREATE POLICY admin_all ON nordb_user FOR ALL TO admins
    USING (role != 'owner') WITH CHECK (role != 'owner');

/*
DEFAULT USER POLICIES
---------------------
*/

--User view policy. Allows user to see their own account
CREATE POLICY user_view ON nordb_user FOR SELECT TO default_users
    USING (username = current_user);

/*
GUEST POLICIES
--------------
*/

--Guest view policy. Allow Guests to see all root ids with public events
CREATE POLICY guest_view ON nordb_user FOR SELECT TO guests
    USING (username = current_user);


