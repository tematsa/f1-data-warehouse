import sys
from pathlib import Path

import pandas as pd
import psycopg2


ROOT = Path(__file__).parent.parent
ENV_PATH = ROOT / ".env"
RAW_DIR = ROOT / "data" / "raw"

def load_env() -> dict[str, str]:
    cfg = {}
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=",1)
        cfg[key.strip()] = value.strip()
    return cfg

def null_if_na(value):
    if pd.isna(value):
        return None
    if isinstance(value, str) and value.strip().lower() in ("", "nan"):
        return None
    return value

def get_connection():
    cfg = load_env()
    return psycopg2.connect(
        host=cfg["PGHOST"],
        port=cfg["PGPORT"],
        user=cfg["PGUSER"],
        password=cfg["PGPASSWORD"],
        database=cfg["PGDATABASE"]
    )

def load_constructors(conn) -> None:
    df = pd.read_csv(RAW_DIR / "constructors_2026.csv")
    sql = """ 
    INSERT INTO f1.dim_constructors (constructor_id, name, nationality, url)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (constructor_id) DO NOTHING
    """
    with conn.cursor() as cursor:
        for _,row in df.iterrows():
            cursor.execute(
                sql,
                (
                    row["constructor_id"],
                    row["constructor_name"],
                    row["constructor_nationality"],
                    row["constructor_url"]
                )
            )
    conn.commit()
    print(f"Loaded {len(df)} constructors")

def load_drivers(conn) -> None:
    df = pd.read_csv(RAW_DIR / "drivers_2026.csv")
    sql = """
    INSERT INTO f1.dim_drivers (driver_id, code, number, name, nationality, date_of_birth, url)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (driver_id) DO NOTHING
    """
    with conn.cursor() as cursor:
        for _,row in df.iterrows():

            num = null_if_na(row["driver_number"])
            num = int(num) if num is not None else None
            
            cursor.execute(
                sql,
                (
                    row["driver_id"],
                    row["driver_code"],
                    null_if_na(row["driver_number"]),
                    row["driver_name"],
                    row["driver_nationality"],
                    null_if_na(row["driver_date_of_birth"]),
                    row["driver_url"]
                )
            ) 
    conn.commit()
    print(f"Loaded {len(df)} drivers")

def load_circuits(conn) -> None:
    df = pd.read_csv(RAW_DIR / "races_2026.csv")
    sql = """
    INSERT INTO f1.dim_circuits (circuit_id, name, location, country)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (circuit_id) DO NOTHING
    """
    with conn.cursor() as cursor:
        for _,row in df.iterrows():
            cursor.execute(
                sql,
                (
                    row["circuit_id"],
                    row["circuit_name"],
                    row["locality"],
                    row["country"]
                )
            )
    conn.commit()
    print(f"Loaded {len(df)} circuits")

def load_races(conn) -> None:
    df = pd.read_csv(RAW_DIR / "races_2026.csv")
    sql = """
    INSERT INTO f1.dim_races (season, round, circuit_id, name, url)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (season, round) DO NOTHING
    """
    with conn.cursor() as cursor:
        for _,row in df.iterrows():
            cursor.execute(
                sql,
                (
                    row["season"],
                    row["round"],
                    row["circuit_id"],
                    row["race_name"],
                    row["url"],
                )
            )
    conn.commit()
    print(f"Loaded {len(df)} races")

if __name__ == "__main__":
    with get_connection() as conn:
        load_constructors(conn)
        load_drivers(conn)
        load_circuits(conn)
        load_races(conn)