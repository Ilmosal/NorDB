/*
+---------------------------+
|PAZ RESPONSE TABLE CREATION|
+---------------------------+

This sql file has all the commands for creating a paz_response table.
*/

--Create table command for paz_response
CREATE TABLE paz_response(
    id SERIAL PRIMARY KEY,
    response_id INTEGER REFERENCES response (id) ON DELETE CASCADE,
    scale_factor FLOAT
);

--Create table for poles
CREATE TABLE pole(
    paz_id INTEGER REFERENCES paz_response(id) ON DELETE CASCADE,
    real FLOAT NOT NULL,
    imag FLOAT NOT NULL,
    real_error FLOAT NOT NULL,
    imag_error FLOAT NOT NULL
);

--Create table for zeroes
CREATE TABLE zero(
    paz_id INTEGER REFERENCES paz_response(id) ON DELETE CASCADE,
    real FLOAT NOT NULL,
    imag FLOAT NOT NULL,
    real_error FLOAT NOT NULL,
    imag_error FLOAT NOT NULL
);

--Enable row level security
ALTER TABLE paz_response ENABLE ROW LEVEL SECURITY;
ALTER TABLE pole ENABLE ROW LEVEL SECURITY;
ALTER TABLE zero ENABLE ROW LEVEL SECURITY;
