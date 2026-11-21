-- Нетто за сезон по соотношению отыграных и потеряных позиций

SELECT  
	d.name,
	SUM(r.grid - r.position ) AS gain
FROM f1.fact_race_results as r
JOIN f1.dim_drivers AS d USING(driver_id)
GROUP BY d.name
ORDER BY gain DESC
