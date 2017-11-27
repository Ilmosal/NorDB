CREATE TABLE sitechan(
    id SERIAL PRIMARY KEY,
    station_id INTEGER REFERENCES station(id),
    channel_code VARCHAR(8),
    on_date DATE,
    off_date DATE,
    channel_type VARCHAR(4),
    emplacement_depth FLOAT,
    horizontal_angle FLOAT,
    vertical_angle FLOAT,
    description VARCHAR(50),
    load_date DATE
);

CREATE TABLE sitechan_css_link(
    css_id INTEGER NOT NULL,
    sitechan_id INTEGER NOT NULL REFERENCES sitechan(id),
    PRIMARY KEY (css_id, sitechan_id)
);
