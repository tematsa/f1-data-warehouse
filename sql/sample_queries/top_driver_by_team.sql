-- Лучший пилот команды по очкам + отрыв от напарника (ожидаем 2 пилота в команде).
-- Срез по раундам: поменяй условие w.round <= N (или убери для всего сезона).

SELECT
    team,
    driver,
    points,
    gap
FROM (
    SELECT
        c.name AS team,
        d.name AS driver,
        couple.points,
        MAX(couple.points) OVER (PARTITION BY couple.constructor_id) AS max_in_team,
        -- при 2 пилотах в команде: очки лидера − очки напарника
        MAX(couple.points) OVER (PARTITION BY couple.constructor_id)
            - MIN(couple.points) OVER (PARTITION BY couple.constructor_id) AS gap
    FROM (
        SELECT
            r.driver_id,
            r.constructor_id,
            SUM(r.points) AS points
        FROM f1.fact_race_results AS r
        JOIN f1.dim_races AS w USING (race_id)
        WHERE w.season = 2026
          AND w.round <= 8
        GROUP BY r.driver_id, r.constructor_id
    ) AS couple
    JOIN f1.dim_drivers AS d USING (driver_id)
    JOIN f1.dim_constructors AS c USING (constructor_id)
) AS ranked
WHERE points = max_in_team
ORDER BY team;
