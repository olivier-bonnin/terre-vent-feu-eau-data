# terre-vent-feu-eau-data

## Introduction  

## Veille Technologique  

**<u>1. Comprendre la structure de la BDIFF et ses évolutions depuis 2006</u>**  

<u>_Qu’est-ce que la BDIFF ?_</u>

La BDIFF (Base de Données sur les Incendies de Forêts en France) est une base nationale créée en 2006, gérée par le Ministère de l’Agriculture et hébergée par l’IGN.
Elle centralise chaque année plus de 9 000 feux recensés par les services départementaux d’incendie et de secours (SDIS).
La période couverte va de 1973 à 2024 (les données 2025 sont en cours d’intégration).  

<u>_Structure typique d'un fichier_</u>  

<b>Chaque ligne correspond à un incendie.  </b>

Les colonnes disponibles varient selon les millésimes, mais on retrouve généralement :  

**Identifiants et localisation:**  
- Année  
- Numéro  
- Département  
- Code INSEE  
- Nom de la commune  

**Chronologie:**  
- Date de première alerte  

**Surfaces brûlées (en m²):**  
- Surface parcourue  
- Surface forêt  
- Surface maquis garrigues  
- Autres surfaces naturelles hors forêt  
- Surfaces agricoles  
- Autres surfaces  
- Surface autres terres boisées  
- Surfaces non boisées naturelles  
- Surfaces non boisées artificialisées  
- Surfaces non boisées  
- Précision des surfaces (niveau de fiabilité de l'estimation)  

**Caractéristiques:**  
- Type de peuplement (type de végétation majoritaire)  
- Nature (origine présumée)  

**Impacts:**  
- Décès ou bâtiments touchés  
- Nombre de décès  
- Nombre de bâtiments totalment détruits  
- Nombre de bâtiments partiellement détruits  

**Métadonnées:**  
- Précision de la donnée (niveau de qualité/fiabilité de l’enregistrement)  

