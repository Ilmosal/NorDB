/*
+---------------------------+
|FAP RESPONSE TABLE CREATION|
+---------------------------+

This sql file has all the commands for creating a fap_response table.
*/

--Create table command for fap_response
CREATE TABLE fap_response(
    id SERIAL PRIMARY KEY,
    response_id INTEGER REFERENCES response (id) ON DELETE CASCADE
);

--Create table for poles
CREATE TABLE fap(
    fap_id INTEGER REFERENCES fap_response(id) ON DELETE CASCADE,
    frequency FLOAT NOT NULL,
    amplitude FLOAT NOT NULL,
    phase FLOAT,
    amplitude_error FLOAT NOT NULL,
    phase_error FLOAT NOT NULL
);

--Enable row level security
ALTER TABLE fap_response ENABLE ROW LEVEL SECURITY;
ALTER TABLE fap ENABLE ROW LEVEL SECURITY;
