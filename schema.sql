CREATE TABLE station (
    id SERIAL PRIMARY KEY,
    name_fi TEXT,
    address_fi TEXT,
    x_coord NUMERIC,
    y_coord NUMERIC
);

CREATE TABLE journey (
    id SERIAL PRIMARY KEY,
    departure_time TIMESTAMP,
    return_time TIMESTAMP,
    departure_station_id INTEGER REFERENCES stations,
    return_station_id INTEGER REFERENCES stations,
    distance INTEGER,
    duration INTEGER
);
