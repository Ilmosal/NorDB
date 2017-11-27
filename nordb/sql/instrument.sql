CREATE TABLE instrument(
    id SERIAL PRIMARY KEY,
    instrument_name VARCHAR(50),
    instrument_type Varchar(6),
    band VARCHAR(1),
    digital VARCHAR(1),
    samprate FLOAT,
    ncalib FLOAT,
    ncalper FLOAT,
    dir VARCHAR(64),
    dfile VARCHAR(32),
    rsptype VARCHAR(6),
    lddate DATE
);

CREATE TABLE instrument_css_link(
    instrument_id INTEGER REFERENCES instrument(id),
    css_id INTEGER
);
