-- Топ пилотов по сходам DNF — пилот / число DNF

SELECT 
	d.name,
	r.status,
	COUNT (r.status) AS num
FROM f1.fact_race_results AS r
JOIN f1.dim_drivers AS d USING (driver_id)
WHERE r.status = 'Retired'
GROUP BY r.status, d.name
ORDER BY num DESC