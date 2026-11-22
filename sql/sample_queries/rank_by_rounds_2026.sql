/* Срез по росту очков по этапам чемпионата 2026*/

WITH step1 AS (
	SELECT 
		d.name, 	
		r.round, 	
		frr.points AS points_race,	
		SUM(frr.points) OVER (
			PARTITION BY d.name 
			ORDER BY r.round
		) AS points_cum
	FROM f1.fact_race_results as frr
	JOIN f1.dim_drivers AS d USING (driver_id)
	JOIN f1.dim_races AS r USING (race_id)
	WHERE r.season = 2026
)
SELECT 
	name, 	
	round, 	
	points_race,	
	points_cum,
	RANK () OVER (
		PARTITION BY round 	
		ORDER BY points_cum DESC
	) AS rank_after_round
FROM step1
ORDER BY round, rank_after_round ASC
