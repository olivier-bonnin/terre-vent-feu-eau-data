# 🌲🔥 BDIFF – Incendies de forêts en France (1973–2024)

## 🎯 Objectif du projet
Ce projet a pour but d’analyser et de visualiser les incendies de forêts en France à partir de la **BDIFF** (Base de Données sur les Incendies de Forêts en France).  
La base couvre la période **1973–2024** (avec homogénéisation et standardisation nationale depuis **2006**).  
Les données sont croisées avec les référentiels INSEE et IGN pour permettre une analyse statistique et cartographique fiable.

---

## 📂 Structure des données

Chaque ligne du fichier BDIFF correspond à **un incendie**.  
Les colonnes varient selon les millésimes mais on retrouve généralement :

- **Identifiants et localisation**
  - Année, Numéro, Département, Code INSEE, Nom de la commune
- **Chronologie**
  - Date de première alerte
- **Surfaces brûlées (en m²)**
  - Surface parcourue totale
  - Détail par type : forêts, maquis/garrigues, surfaces agricoles, autres surfaces naturelles, surfaces artificialisées
- **Caractéristiques**
  - Type de peuplement (taillis, futaies feuillues, résineux, etc.)
  - Nature/origine (naturelle, accidentelle, malveillance, etc.)
- **Impacts**
  - Décès
  - Bâtiments détruits ou endommagés
- **Métadonnées**
  - Niveau de précision des surfaces (estimée / mesurée)
  - Fiabilité de l’enregistrement

---

## ⏳ Évolutions dans le temps

- **Avant 2006**
  - Données reconstituées, formats variables selon départements
  - Valeurs manquantes fréquentes (type de végétation, causes…)
  - Moins homogènes
- **Depuis 2006**
  - Centralisation nationale et standardisation
  - Colonnes enrichies (surfaces par type, causes précises)
  - Fiabilité accrue
- **Changements 2023**
  - Évolution de la définition des surfaces (ex. maquis/garrigues intégrés à la catégorie « forêt » en aire méditerranéenne)

---

## 📊 Points clés pour l’analyse

- Les données **pré-2006** sont intéressantes pour l’historique, mais nécessitent un gros nettoyage.
- Les données **2006–2024** sont fiables et adaptées à la modélisation prédictive.
- Attention aux **changements de codes INSEE** (fusions de communes, notamment après 2015).
- Toujours **convertir les surfaces en hectares (ha)** pour lisibilité.
- Penser à **pondérer ou filtrer selon la précision** (estimée vs mesurée).

---

## 🗂️ Schéma SQL proposé

### Table `communes`
- `code_insee` (clé unique)
- `nom_commune`, `dep_code`, `reg_code`
- `population`, `superficie_km2`, `altitude_moyenne`
- `latitude_centre`, `longitude_centre`

### Table `incendies`
- `id_incendie`, `annee`, `code_insee`
- `date_premiere_alerte`, `nature`, `type_de_peuplement`
- `surface_parcourue_m2` + surfaces détaillées
- `nb_deces`, `nb_batiments_totalement_detruits`, `nb_batiments_partiellement_detruits`
- `src_file_name`, `batch_id`, `loaded_at` (traçabilité)

---

## 🔗 Sources officielles
- **BDIFF (Ministère de l’Agriculture / IGN)** : [Portail officiel](https://www.data.gouv.fr/fr/datasets/base-de-donnees-sur-les-incendies-de-forets-bdiff/)  
- **INSEE – Code Officiel Géographique (COG)** : [INSEE COG](https://www.insee.fr/fr/information/2666684)  
- **IGN – Admin Express** : [Admin Express](https://geoservices.ign.fr/adminexpress)  

---

## 🚀 Utilisation du repo

- `data/raw/` : fichiers CSV téléchargés depuis la BDIFF  
- `data/interim/` : fichiers nettoyés ou préparés  
- `data/processed/` : données finales prêtes pour analyse  
- `notebooks/` : notebooks Jupyter (EDA, analyses, visualisations)  
- `scripts/` : scripts Python d’ingestion/traitement des données  

---

## ✅ A retenir

- **Création officielle de la BDIFF : 2006**  
- **Couverture temporelle des données : 1973–2024**  
- **2006 = rupture méthodologique** → données fiables et standardisées  
- Bien gérer : surfaces (m² → ha), codes INSEE, évolution des définitions (notamment 2023)

---
![Python](https://img.shields.io/badge/Python-3.13-informational) ![Streamlit](https://img.shields.io/badge/Streamlit-app-success) ![PostGIS](https://img.shields.io/badge/PostGIS-geospatial-blue)
> Refresh: 2025-10-30 13:27
