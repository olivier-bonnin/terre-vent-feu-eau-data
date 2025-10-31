# BDIFF Wildfire — PostGIS + Streamlit

![Python](https://img.shields.io/badge/Python-3.13-informational)
![Streamlit](https://img.shields.io/badge/Streamlit-app-success)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![PostGIS](https://img.shields.io/badge/PostGIS-geospatial-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)

Analyse spatio-temporelle des **incendies de forêt** (BDIFF) en région PACA, enrichie par des **features météo/NDVI** et servie via une **app Streamlit**.  
Objectif : fournir une **lecture opérationnelle** des risques (zones, saisons, tendances), et ouvrir la voie à une **v1.5 prédictive** exploitant des modèles ML adaptés au géospatial.

> Projet vitrine “Data & IA appliquée à l’environnement” — stack propre, CI légère, doc claire, roadmap ambitieuse.

---

## 1) 🎯 Objectifs

- Centraliser et normaliser les **données incendies (BDIFF)** + **exogènes** (météo, végétation NDVI).
- Modéliser une **base PostGIS** prête pour la carto et l’analytique.
- Construire un **pipeline ETL** reproductible (scripts `src/`).
- Proposer une **app Streamlit** de visualisation (cartes, filtres, stats).
- Roadmap **v1.5/v2** : features spatio-temporelles avancées et **modèles prédictifs** (classification / ranking de risque).

---

## 2) 🌐 Sources de données

- **BDIFF** (évènements feu) : géométrie, date, surface, type de végétation…
- **Météo** (ouvertes) : températures, vent, humidité, sécheresse… (agrégations spatio-temporelles)
- **Images satellites** (NDVI, Copernicus/Sentinel) : proxy végétation/fuel

> Les scripts prévoient des *connecteurs modulaires* (CSV/GeoJSON/API). Les clés privées ne sont pas versionnées.

---

## 3) 🧱 Architecture technique (Vue d’ensemble)

```mermaid
flowchart LR
    A[BDIFF (raw)] --> B[ETL Python]
    A2[Météo (raw)] --> B
    A3[NDVI (raw)] --> B
    B --> C[(PostgreSQL + PostGIS)]
    C --> D[Features / Views]
    D --> E[App Streamlit]
    E --> U[Utilisateur (cartes/graphes/exports)]
