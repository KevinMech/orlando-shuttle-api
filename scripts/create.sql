CREATE TABLE buses(
    id      SERIAL PRIMARY KEY,
    name    VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE stops(
    id          INTEGER REFERENCES buses(id),
    longitude   DECIMAL NOT NULL,
    latitude    DECIMAL NOT NULL
);

CREATE TABLE routes(
    id          INTEGER REFERENCES buses(id),
    longitude   DECIMAL NOT NULL,
    latitude    DECIMAL NOT NULL
);
