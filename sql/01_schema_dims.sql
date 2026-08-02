CREATE SCHEMA IF NOT EXISTS f1;

CREATE TABLE IF NOT EXISTS f1.dim_constructors (
    constructor_id VARCHAR(255) PRIMARY KEY,
    name TEXT,
    nationality TEXT,
    url TEXT
);

CREATE TABLE IF NOT EXISTS f1.dim_drivers (
    driver_id VARCHAR(255) PRIMARY KEY,
    code VARCHAR(255),
    number INT,
    name TEXT,
    nationality TEXT,
    date_of_birth DATE,
    url TEXT
);

CREATE TABLE IF NOT EXISTS f1.dim_circuits (
    circuit_id VARCHAR(255) PRIMARY KEY,
    name TEXT,
    location TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS f1.dim_races (
    race_id SERIAL PRIMARY KEY,
    season INT,
    round INT,
    circuit_id VARCHAR(255) REFERENCES f1.dim_circuits(circuit_id),
    name TEXT,
    url TEXT,
    UNIQUE (season, round)
);