# 🌍 Terre, Vent, Feu, Eau, Data

## ✨ Présentation du projet

Ce projet a pour objectif d’analyser plus de 50 ans d’incendies de forêts en France grâce à la base nationale **BDIFF**.  
Il permet de :
- Suivre l’évolution des feux dans le temps et selon les territoires  
- Identifier les zones et périodes les plus à risque  
- Visualiser les données sur une carte interactive  
- Mettre en place des outils d’aide à la décision pour la prévention et la gestion des incendies  

L’application fournit à la fois des analyses statistiques, des visualisations intuitives et un outil interactif accessible via **Streamlit**.

---

## 🚀 Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/<ton_compte>/<ton_repo>.git
cd terre-vent-feu-eau-data
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate   # Windows : venv\Scripts\activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

---

## 📂 Organisation

- `data/raw/` : fichiers bruts (CSV BDIFF + communes)  
- `data/processed/` : fichiers enrichis générés par les scripts  
- `src/` : scripts Python  
  - `etl_bdiff.py` → pipeline de traitement (nettoyage + enrichissement)  
  - `eda.py` → analyses exploratoires simples  
  - `map_folium.py` → génération d’une heatmap interactive  
- `app/streamlit_app.py` : application Streamlit  
- `notebooks/` : notebooks exploratoires (Jupyter)  

---

## 🛠️ Utilisation

- Lancer le pipeline de traitement :
```bash
python -m src.etl_bdiff
```

- Explorer les données (graphiques simples) :
```bash
python -m src.eda
```

- Générer une carte interactive :
```bash
python -m src.map_folium
```

- Lancer l’application Streamlit :
```bash
streamlit run app/streamlit_app.py
```

---

## 📊 Exemple de résultats

- Nombre de feux par département  
- Répartition par type de végétation  
- Carte interactive (heatmap)  
- Analyse circulaire de la saisonnalité des incendies  

---

## ⚠️ Note

Les données brutes **BDIFF** ne sont pas incluses dans le dépôt.  
👉 Placez-les dans `data/raw/` avant de lancer le pipeline.
