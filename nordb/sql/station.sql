CREATE TABLE station(
    id SERIAL PRIMARY KEY,
    network_id INTEGER REFERENCES network(id), 
    station_code VARCHAR(6),
    on_date DATE,
    off_date DATE,
    latitude FLOAT,
    longitude FLOAT,
    elevation FLOAT,
    station_name VARCHAR(50),
    station_type VARCHAR(2),
    reference_station VARCHAR(6),
    north_offset FLOAT,
    east_offset FLOAT,
    load_date DATE
)
