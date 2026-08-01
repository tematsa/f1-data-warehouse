
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

def extract_drivers() -> list[dict]:
    data = get_json(f"{SEASON}/drivers.json")
    drivers = data["MRData"]["DriverTable"]["Drivers"]
    rows = []
    for driver in drivers:
        number = driver.get("permanentNumber")
        code = driver.get("code")
        url = driver.get("url")
        date_of_birth = driver.get("dateOfBirth")
        nationality = driver.get("nationality")
        rows.append(
            {
                "season": int(data["MRData"]["DriverTable"]["season"]),
                "driver_id": driver["driverId"],
                "driver_number": int(number) if number is not None else None,
                "driver_code": driver["code"] if code is not None else None,
                "driver_url": driver["url"] if url is not None else None,
                "driver_name": driver["givenName"] + " " + driver["familyName"],
                "driver_date_of_birth": driver["dateOfBirth"] if date_of_birth is not None else None,
                "driver_nationality": driver["nationality"] if nationality is not None else None,                
            }
        )
    return rows

def extract_constructors() -> list[dict]:
    data = get_json(f"{SEASON}/constructors.json")
    constructors = data["MRData"]["ConstructorTable"]["Constructors"]
    rows = []
    for constructor in constructors:
        rows.append(
            {
                "season": int(data["MRData"]["ConstructorTable"]["season"]),
                "constructor_id": constructor["constructorId"],
                "constructor_name": constructor["name"],
                "constructor_nationality": constructor["nationality"],
                "constructor_url": constructor["url"],
            }
        )
    return rows


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True,exist_ok=True)
     
    rows = extract_constructors()
    df = pd.DataFrame(rows)
    out = RAW_DIR / f"constructors_{SEASON}.csv"
    df.to_csv(out, index=False)
    print(f"Saved {len(df)} constructors -> {out}")



    """ # drivers
    rows = extract_drivers()
    df = pd.DataFrame(rows)

    out = RAW_DIR / f"drivers_{SEASON}.csv"
    df.to_csv(out, index=False)

    print(f"Saved {len(df)} drivers -> {out}")
    """
    


    """ # races
    rows = extract_races()
    df = pd.DataFrame(rows)

    out = RAW_DIR / f"races_{SEASON}.csv"
    df.to_csv(out, index=False)

    print(f"Saved {len(df)} races -> {out}")
    """
    
    """ #check connection
    rows = extract_races()
    print(len(rows))
    print(rows[0])    
    """

    """ # racess
    data = get_json(f"{SEASON}/races.json")
    print(data["MRData"]["RaceTable"]["season"])
    print(len (data["MRData"]["RaceTable"]["Races"]))
    """