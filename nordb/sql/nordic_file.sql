/*
+--------------------------+
|NORDIC FILE TABLE CREATION|
+--------------------------+

This sql file has all the commands for creating a nordic_file table.
*/

--Create table command for nordic_file
CREATE TABLE nordic_file(
	id SERIAL PRIMARY KEY,
	file_location TEXT
);
