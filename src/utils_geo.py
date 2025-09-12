import pandas as pd

def join_communes(df, communes_df, insee_col="Code INSEE"):
    # Renomme pour join
    df = df.rename(columns={insee_col: "code_insee"})
    cols = ["code_insee", "nom_standard", "latitude_centre", "longitude_centre"]
    merged = df.merge(communes_df[cols], on="code_insee", how="left")
    # coalesce nom
    if "Nom de la commune" in merged.columns:
        merged["nom_commune_finale"] = merged["Nom de la commune"].fillna(merged["nom_standard"])
    else:
        merged["nom_commune_finale"] = merged["nom_standard"]
    return merged