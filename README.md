# F1 Data Warehouse

ETL-пайплайн для данных Formula 1 (сезон **2026**):
публичный API → pandas → PostgreSQL.

## Цель

Структурированное хранилище (звездная схема) для аналитики сезона 2026.

**Сейчас в данных:** справочники (drivers, constructors, circuits, races) + результаты гонок (`fact_race_results`).

**Дальше (next steps):** квалификация, пит-стопы, SQL-витрины.

## Источник данных

- API: [Jolpi Ergast](https://api.jolpi.ca/ergast/f1) (без ключа)
- Формат: JSON (совместим с Ergast)

## Статус

- [x] Репозиторий
- [x] Extract: races / drivers / constructors / results → CSV
- [x] Load в PostgreSQL
- [x] Docker Compose (`postgres` + `etl`)
- [x] Примеры SQL в README (№1–6) + файлы в `sql/sample_queries/`
- [ ] SQL-витрины (marts) / дашборд BI

## Стек

Python, pandas, requests, PostgreSQL, Docker Compose

## Архитектура

```mermaid
flowchart LR
  API[Jolpi Ergast API] --> ETL[Python ETL]
  ETL --> PG[(PostgreSQL)]
```

## Запуск

1. Скопируй env и задай пароль:

```bash
cp .env.example .env
```

В `.env` укажи `POSTGRES_USER`, `POSTGRES_PASSWORD` (и при необходимости `PG*`).

2. Подними Postgres:

```bash
docker compose up -d postgres
```

3. Накатай схему:

```bash
docker compose exec -T postgres psql -U postgres -d f1_data_warehouse < sql/01_schema_dims.sql
docker compose exec -T postgres psql -U postgres -d f1_data_warehouse < sql/02_schema_facts.sql
```

4. Собери и запусти ETL (load CSV → PostgreSQL):

```bash
docker compose up --build etl
```

Порт Postgres на хосте: **5433** (внутри Docker-сети для `etl` — `5432`, хост `postgres`).

## Примеры запросов

Запросы ниже — к схеме `f1` после load. Таблица фактов: `f1.fact_race_results`.  
Полные файлы: [`sql/sample_queries/`](sql/sample_queries/).

### 1. Лучший пилот команды + отрыв от напарника

Срез: `round <= N` (сейчас 8) или убери фильтр для всего сезона.  
`gap` = max − min очков в команде (для стандартных **2** пилотов = отрыв от напарника).

```sql
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
```

### 2. Топ пилотов по сходам (DNF)

В наших данных сход = `status = 'Retired'`.

```sql
SELECT
    d.name,
    r.status,
    COUNT(r.status) AS num
FROM f1.fact_race_results AS r
JOIN f1.dim_drivers AS d USING (driver_id)
WHERE r.status = 'Retired'
GROUP BY r.status, d.name
ORDER BY num DESC;
```

### 3. Чемпионат пилотов

```sql
SELECT
    d.name AS driver,
    SUM(f.points) AS points
FROM f1.fact_race_results AS f
JOIN f1.dim_drivers AS d USING (driver_id)
GROUP BY d.name
ORDER BY points DESC;
```

### 4. Кубок конструкторов

```sql
SELECT
    c.name AS constructor,
    SUM(f.points) AS points
FROM f1.fact_race_results AS f
JOIN f1.dim_constructors AS c USING (constructor_id)
GROUP BY c.name
ORDER BY points DESC;
```

### 5. Лучшие прорывы (`grid - position`)

Без фильтра — по всем гонкам; при желании добавь `AND r.race_id = N`.

```sql
SELECT
    r.race_id,
    d.name,
    r.grid,
    r.position,
    (r.grid - r.position) AS gain
FROM f1.fact_race_results AS r
JOIN f1.dim_drivers AS d USING (driver_id)
WHERE r.position IS NOT NULL
ORDER BY gain DESC;
```

### 6. Динамика по раундам (накопительные очки и место после этапа)

Длинная таблица на всех пилотов — под линии набора очков / мест в BI.  
Файл: [`sql/sample_queries/rank_by_rounds_2026.sql`](sql/sample_queries/rank_by_rounds_2026.sql)

```sql
WITH step1 AS (
    SELECT
        d.name,
        r.round,
        frr.points AS points_race,
        SUM(frr.points) OVER (
            PARTITION BY d.name
            ORDER BY r.round
        ) AS points_cum
    FROM f1.fact_race_results AS frr
    JOIN f1.dim_drivers AS d USING (driver_id)
    JOIN f1.dim_races AS r USING (race_id)
    WHERE r.season = 2026
)
SELECT
    name,
    round,
    points_race,
    points_cum,
    RANK() OVER (
        PARTITION BY round
        ORDER BY points_cum DESC
    ) AS rank_after_round
FROM step1
ORDER BY round, rank_after_round;
```
