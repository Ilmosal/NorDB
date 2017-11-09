CREATE TABLE sitechan(
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES station(id),
    on_date DATE,
    off_date DATE,
    channel_type VARCHAR(4),
    emplacement_depth FLOAT,
    horizontal_angle FLOAT,
    vertical_angle FLOAT,
    description VARCHAR(50),
    load_date DATE

);
