-- Лучшие прорывы в гонке — пилот / отыгранные места (grid − position)
SELECT  
	r.race_id,
	d.name,
	r.grid,
	r.position,
	(r.grid - r.position) AS gain
FROM f1.fact_race_results as r
JOIN f1.dim_drivers AS d USING(driver_id)
WHERE r.race_id = 2
ORDER BY gain DESC



