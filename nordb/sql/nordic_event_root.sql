/*
+--------------------------------+
|NORDIC EVENT ROOT TABLE CREATION|
+--------------------------------+

This file contains the sql commands for creating the nordic event root table. 
Currently event root only has the id of the event root, but this might change 
in the future.
*/

--Create the nordic_event_root table
CREATE TABLE nordic_event_root(
	id SERIAL PRIMARY KEY
);

--Enable row level security
ALTER TABLE nordic_event_root ENABLE ROW LEVEL SECURITY;
