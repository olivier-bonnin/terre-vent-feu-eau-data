import os
import pandas as pd
import numpy as np
from .config import BDIFF_FILES, COMMUNES, PROCESSED
from .utils_time import enrich_time
from .utils_geo import join_communes

def load_csv(path):
    return pd.read_csv(path, sep=";", encoding="utf-8", low_memory=False)

def clean_drop_empty_cols(df):
    return df.dropna(axis=1, how="all")

def process_one(path, communes_df):
    df = load_csv(path)
    df = clean_drop_empty_cols(df)
    df = enrich_time(df, "Date de première alerte")
    df = join_communes(df, communes_df, "Code INSEE")
    df["periode"] = os.path.basename(path).replace("Incendies_","").replace(".csv","")
    return df

def main():
    os.makedirs(PROCESSED, exist_ok=True)
    communes_df = load_csv(COMMUNES)
    parts = [process_one(p, communes_df) for p in BDIFF_FILES]
    full = pd.concat(parts, ignore_index=True)
    # types numériques sûrs
    for col in ["Surface parcourue (m2)","Surface forêt (m2)","Surface maquis garrigues (m2)"]:
        if col in full.columns:
            full[col] = pd.to_numeric(full[col], errors="coerce")
    out_parquet = os.path.join(PROCESSED, "bdiff_1973_2024.parquet")
    out_csv = os.path.join(PROCESSED, "bdiff_1973_2024.csv")
    full.to_parquet(out_parquet, index=False)
    full.to_csv(out_csv, index=False)
    print(f"OK -> {out_csv}\nOK -> {out_parquet}")

if __name__ == "__main__":
    main()