/*
+-------------------------+
|NORDB USER TABLE CREATION|
+-------------------------+

This file contains the sql commands for creating the nordb_user table. 
*/

--create db_role enum for easy searching of the role of an user
CREATE TYPE db_role as ENUM ('guests', 'default_users', 'station_managers', 'admins', 'owner');

--Create the table for NorDB users
CREATE TABLE nordb_user(
    username VARCHAR(32) PRIMARY KEY,
    role DB_ROLE
);

--Insert the person who runs this command into the values of the table as an owner
INSERT INTO nordb_user (username, role) VALUES (CURRENT_USER, 'owner');

--Enable row level security
ALTER TABLE nordb_user ENABLE ROW LEVEL SECURITY;
