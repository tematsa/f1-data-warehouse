CREATE TABLE IF NOT EXISTS f1.fact_race_results (
    result_id SERIAL PRIMARY KEY,
    race_id INT NOT NULL REFERENCES f1.dim_races(race_id),
    driver_id VARCHAR(255) NOT NULL REFERENCES f1.dim_drivers(driver_id),
    constructor_id VARCHAR(255) NOT NULL REFERENCES f1.dim_constructors(constructor_id),
    grid INT,
    position INT,
    position_text VARCHAR(8),
    points NUMERIC(5, 1),
    laps INT,
    status TEXT,
    UNIQUE (race_id, driver_id)
);