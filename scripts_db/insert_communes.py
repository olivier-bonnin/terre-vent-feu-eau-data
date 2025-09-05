import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "communes-france-2025.csv"

def main():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL manquant dans .env")
        sys.exit(1)

    engine = create_engine(db_url)

    try:
        df = pd.read_csv(
            CSV_PATH,
            encoding="utf-8",
            low_memory=False,
            dtype={
                "code_insee": "string",
                "dep_code": "string",
                "reg_code": "string",
            },
        )
    except Exception as e:
        print(f"Erreur de lecture {CSV_PATH} : {e}")
        sys.exit(1)

    expected = [
        "code_insee","nom_standard","dep_code","reg_code",
        "population","superficie_km2","densite","altitude_moyenne",
        "latitude_centre","longitude_centre"
    ]
    missing = [c for c in expected if c not in df.columns]
    if missing:
        print(f"Colonnes manquantes dans {CSV_PATH.name} : {missing}")
        sys.exit(1)

    df = df[expected].copy()

    for c in ["population","altitude_moyenne"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    for c in ["superficie_km2","densite","latitude_centre","longitude_centre"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE communes CASCADE;"))
        df.to_sql("communes", conn, if_exists="append", index=False, chunksize=5000, method="multi")

    print(f"Communes chargées : {len(df):,} lignes depuis {CSV_PATH.name}")

if __name__ == "__main__":
    main()
