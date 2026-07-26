#!/usr/bin/env python3
"""
predict.py — Script de prédiction de segmentation
Segmentation des ménages haïtiens exclus du crédit formel
Groupe 5 — FRST-FDS / CTPEA 2025-2026

Usage
-----
from predict import predire_segments
import pandas as pd

# Charger vos nouvelles données
df_nouvelles = pd.read_excel("nouvelles_donnees.xlsx",
                              sheet_name="Donnees")

# Filtrer les individus sans crédit formel
df_cible = df_nouvelles[
    df_nouvelles["Jamais_Eu_Credit_Formel"] == "Oui"
].copy()

# Prédire les segments
df_resultat, X_pca = predire_segments(df_cible)

# Afficher les résultats
print(df_resultat[["ID_Individu","Cluster","Profil"]].head(20))
print(df_resultat["Profil"].value_counts())
"""

import joblib
import pandas as pd
import numpy as np

PIPELINE_DIR = "pipeline_segmentation"

def predire_segments(df_nouvelles, pipeline_dir=PIPELINE_DIR):
    scaler_p = joblib.load(f"{pipeline_dir}/scaler.pkl")
    pca_p    = joblib.load(f"{pipeline_dir}/pca_afdm.pkl")
    kmeans_p = joblib.load(f"{pipeline_dir}/kmeans_final.pkl")
    enc      = joblib.load(f"{pipeline_dir}/encodeurs.pkl")

    ordre_ed   = enc["ordre_education"]
    ordre_pl   = enc["ordre_planification"]
    ordre_in   = enc["ordre_inclusion"]
    vars_bin   = enc["VARS_BIN"]
    cols_model = enc["COLS_MODEL"]
    noms_cl    = enc["noms_clusters"]

    df_out = df_nouvelles.copy()
    for var in vars_bin:
        if var in df_out.columns:
            df_out[var] = (df_out[var] == "Oui").astype(int)
    if "Niveau_Education" in df_out.columns:
        df_out["Niveau_Education"] = df_out["Niveau_Education"]                                           .map(ordre_ed)
    if "Planification_Financiere" in df_out.columns:
        df_out["Planification_Financiere"] =             df_out["Planification_Financiere"].map(ordre_pl)
    if "Niveau_Inclusion_Financiere" in df_out.columns:
        df_out["Niveau_Inclusion_Financiere"] =             df_out["Niveau_Inclusion_Financiere"].map(ordre_in)
    if "Revenu_Mensuel_HTG" in df_out.columns:
        df_out["Revenu_log"] = np.log1p(df_out["Revenu_Mensuel_HTG"])
    if "Secteur_Activite" in df_out.columns:
        df_out = pd.get_dummies(df_out,
                                columns=["Secteur_Activite"],
                                prefix="Sec", drop_first=False)
    for col in cols_model:
        if col not in df_out.columns:
            df_out[col] = 0
    X_new        = df_out[cols_model].copy()
    X_new_scaled = scaler_p.transform(X_new)
    X_new_pca    = pca_p.transform(X_new_scaled)
    labels_new   = kmeans_p.predict(X_new_pca)

    df_nouvelles         = df_nouvelles.copy()
    df_nouvelles["Cluster"] = labels_new
    df_nouvelles["Profil"]  = [noms_cl[c] for c in labels_new]
    return df_nouvelles, X_new_pca


if __name__ == "__main__":
    print("Pipeline de segmentation chargé.")
    print("Importez predire_segments() dans votre script.")
    print("Voir la docstring pour les instructions d'usage.")
