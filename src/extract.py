
import time
from pathlib import Path

import pandas as pd

import requests

BASE_URL = "https://api.jolpi.ca/ergast/f1" 
SEASON = 2026 
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" 

def get_json(path: str) -> dict: 
    url = f"{BASE_URL}/{path}"
    print(f"GET {url}")
    response = requests.get(url,timeout=30)
    response.raise_for_status()
    time.sleep(0.4)
    return response.json() 

def extract_races() -> list[dict]:
    data = get_json(f"{SEASON}/races.json")
    races = data["MRData"]["RaceTable"]["Races"]
    rows = []
    for race in races:
        circuit = race["Circuit"]
        location = circuit["Location"]
        rows.append(
            {
               "season": int(race["season"]),
               "round": int(race["round"]),
               "url":race ["url"],
               "race_name": race["raceName"],
               "circuit_id": circuit["circuitId"],
               "curcuit_name": circuit["circuitName"],
               "country": location["country"],
               "locality": location["locality"], 
            }
        )
    return rows



if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True,exist_ok=True)

    rows = extract_races()
    df = pd.DataFrame(rows)

    out = RAW_DIR / f"races_{SEASON}.csv"
    df.to_csv(out, index=False)

    print(f"Saved {len(df)} races -> {out}")

    
    """
    rows = extract_races()
    print(len(rows))
    print(rows[0])    
    """

    """
    data = get_json(f"{SEASON}/races.json")
    print(data["MRData"]["RaceTable"]["season"])
    print(len (data["MRData"]["RaceTable"]["Races"]))
    """