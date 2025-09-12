import pandas as pd
from .config import PROCESSED
import os

import matplotlib.pyplot as plt

def load():
    p = os.path.join(PROCESSED, "bdiff_1973_2024.parquet")
    return pd.read_parquet(p)

def feux_par_departement(df):
    c = df["Département"].value_counts().sort_values(ascending=False).head(20)
    plt.figure(figsize=(12, 6))
    c.plot(kind="bar")
    plt.title("Top 20 départements - nombre de feux")
    plt.xlabel("Département")
    plt.ylabel("Feux")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    df = load()
    feux_par_departement(df)