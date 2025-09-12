import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv("DATA_DIR", "./data")
RAW = os.path.join(DATA_DIR, "raw")
INTERIM = os.path.join(DATA_DIR, "interim")
PROCESSED = os.path.join(DATA_DIR, "processed")

# Fichiers attendus
COMMUNES = os.path.join(RAW, "communes-france-2025.csv")
BDIFF_FILES = [
    os.path.join(RAW, f) for f in [
        "Incendies_1973_1979.csv",
        "Incendies_1980_1989.csv",
        "Incendies_1990_1999.csv",
        "Incendies_2000_2009.csv",
        "Incendies_2010_2019.csv",
        "Incendies_2020_2024.csv",
    ]
]

# Jours fériés (codes MMJJ) – à affiner
PUBLIC_HOLIDAYS = {'0101', '0501', '0704', '0714', '1111', '1225', '1231'}
SUMMER_MONTHS = {7, 8}