-- Чемпионат Пилотов

SELECT
    d.name AS driver,
    SUM(f.points) AS points
FROM f1.fact_race_results AS f
JOIN f1.dim_drivers AS d USING (driver_id)
GROUP BY d.name
ORDER BY points DESC;