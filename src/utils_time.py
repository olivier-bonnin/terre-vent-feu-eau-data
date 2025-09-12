import numpy as np
import pandas as pd
from .config import PUBLIC_HOLIDAYS, SUMMER_MONTHS

def enrich_time(df, date_col="Date de première alerte"):
    d = pd.to_datetime(df[date_col], format="%d/%m/%Y %H:%M", errors="coerce")
    df[date_col] = d
    df["timestamp"] = d.view("int64") // 10**9
    df["heure"] = d.dt.hour
    df["minute"] = d.dt.minute
    df["mois"] = d.dt.month
    df["jour"] = d.dt.day
    df["jour_semaine"] = d.dt.dayofweek  # 0=lundi
    df["mois_jour_code"] = d.dt.strftime("%m%d")
    df["jour_de_l_annee"] = d.dt.dayofyear

    angle = 2 * np.pi * df["jour_de_l_annee"] / 365.25
    df["cos_jour"], df["sin_jour"] = np.cos(angle), np.sin(angle)

    df["is_weekend"] = df["jour_semaine"].isin([5, 6]).astype(int)
    df["is_public_holiday"] = df["mois_jour_code"].isin(PUBLIC_HOLIDAYS).astype(int)
    df["is_school_vacation"] = df["mois"].isin(SUMMER_MONTHS).astype(int)
    df["est_jour_ouvre"] = (~((df["is_weekend"] == 1) | (df["is_public_holiday"] == 1) | (df["is_school_vacation"] == 1))).astype(int)
    return df