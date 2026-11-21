-- Пилот/Команда/ОЧКИ

SELECT 
	r.driver_id, 
	r.constructor_id, 
	SUM(r.points) AS points
FROM f1.fact_race_results AS r
JOIN f1.dim_races AS w USING(race_id)
WHERE w.season = 2026 AND w.round <= 8
GROUP BY r.driver_id, r.constructor_id
ORDER BY points DESC

