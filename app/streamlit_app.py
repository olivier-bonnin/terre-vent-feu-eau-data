import os, streamlit as st, pandas as pd
from pathlib import Path

DATA = Path("./data/processed/bdiff_1973_2024.parquet")

@st.cache_data
def load_data():
    return pd.read_parquet(DATA)

st.title("BDIFF – Incendies (1973–2024)")
df = load_data()

with st.sidebar:
    annee = st.slider("Année", int(df["Année"].min()), int(df["Année"].max()), (2000, 2024))
    mois = st.multiselect("Mois", list(range(1,13)), default=[6,7,8,9])
    dept = st.multiselect("Département", sorted(df["Département"].dropna().unique().tolist()))

filtre = (df["Année"].between(*annee)) & (df["mois"].isin(mois))
if dept: filtre &= df["Département"].isin(dept)
dfs = df[filtre]

st.metric("Nombre de feux", len(dfs))
st.metric("Surface totale (ha)", round(dfs["Surface parcourue (m2)"].sum()/10_000, 1))

st.bar_chart(dfs["mois"].value_counts().sort_index())
st.line_chart(dfs.groupby("Année")["Surface parcourue (m2)"].sum())
st.dataframe(dfs.head(100))
