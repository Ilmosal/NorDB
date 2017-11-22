CREATE TABLE sensor(
    id SERIAL PRIMARY KEY,
    instrument_id INTEGER REFERENCES instrument(id),
    channel_id INTEGER REFERENCES sitechan(id),
    time FLOAT,
    endtime FLOAT,
    jdate DATE,
    calratio FLOAT,
    calper FLOAT,
    tshift FLOAT,
    instant VARCHAR(1),
    lddate DATE
)
