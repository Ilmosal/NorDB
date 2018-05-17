/*
+------------------------------------+
|NORDIC HEADER COMMENT TABLE CREATION|
+------------------------------------+

This sql file has all the commands for creating a nordic_header_comment table.
*/

--Create the nordic_header_comment table
CREATE TABLE nordic_header_comment(
	id SERIAL PRIMARY KEY,
	event_id INTEGER REFERENCES nordic_event(id) ON DELETE CASCADE,
	h_comment VARCHAR(78)
);

--Enable row level security
ALTER TABLE nordic_header_comment ENABLE ROW LEVEL SECURITY;
