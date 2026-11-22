-- Лучшие прорывы: отыгранные места (grid − position).
-- Опционально сузить гонку: AND r.race_id = N
-- Без фильтра — рейтинг прорывов по всем загруженным гонкам.

SELECT
    r.race_id,
    d.name,
    r.grid,
    r.position,
    (r.grid - r.position) AS gain
FROM f1.fact_race_results AS r
JOIN f1.dim_drivers AS d USING (driver_id)
WHERE r.position IS NOT NULL
  -- AND r.race_id = 2
ORDER BY gain DESC;
