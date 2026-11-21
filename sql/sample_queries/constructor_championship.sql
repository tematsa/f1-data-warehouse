-- Чемпионат Конструкторов

SELECT
    c.name AS constructor,
    SUM(f.points) AS points
FROM f1.fact_race_results AS f
JOIN f1.dim_constructors AS c USING (constructor_id)
GROUP BY c.name
ORDER BY points DESC;