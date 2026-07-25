## F1 Data Warehouse
ETL-пайплайн для данных о гоночных соревнованиях Formula 1 (сезон **2026**):
публичный API -> pandas -> PostgreSQL.

## Цель
Структурировать хранилище (звездная схема) для аналитики:
- чемпионаты
- квалификация
- гонка
- пит-стоп

## Источник данных 
- API: [Jolpi Ergast](https://api.jolpi.ca/ergast/f1) (без ключа)
- Формат: JSON (совместим с Ergast)

## Статус 
- [X] Репозиторий
- [] Extract: сезон / drivers / constructors -> CSV
- [] Load в PostgreSQL
- [] Docker Compose
- [] SQL-витрины + README с примерами

## Стек
Python, pandas, requests, PostgreSQL, Docker (позже)

## Структура (план)




