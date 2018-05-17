/*
+----------------------+
|NETWORK TABLE CREATION|
+----------------------+

This sql file has all the commands for creating a network table.

*/

--Create table command for network
CREATE TABLE network(
    id SERIAL PRIMARY KEY,
    creation_id INTEGER REFERENCES creation_info(id),
    network VARCHAR(6)
);

--Enable row level security
ALTER TABLE network ENABLE ROW LEVEL SECURITY;
