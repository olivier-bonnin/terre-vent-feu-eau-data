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


<u>_Évolutions depuis 2006_</u>  

**Avant 2006 :**  

- Données reconstituées et moins homogènes.  
- Beaucoup de valeurs manquantes (ex. types de végétation, causes détaillées).  
- Formats variables selon les départements.  

**Depuis 2006 :**

- Standardisation nationale de la collecte.  
- Colonnes enrichies (surface par type de végétation, causes précises).  
- Fiabilité accrue grâce à la centralisation.
- Export disponible en CSV (par paquets de 30 000 lignes).
- Alignement facilité avec les référentiels INSEE/IGN (codes INSEE).  

<u>_Points clés pour le projet_</u>  

- Les données pré-2006 : intéressantes pour l’historique, mais nécessitent un fort nettoyage.

- Les données 2006–2024 : plus complètes et adaptées pour la modélisation rapide.

- Attention aux changements de codes INSEE (fusions et créations de communes, surtout après 2015).

- Nécessité de concevoir un schéma SQL flexible intégrant :
- - Les champs anciens (surface brûlée totale, date, commune).
- - Les champs récents (détail des surfaces, causes, horaires).  


**<u>2. Analyser les définitions officielles</u>**  

**Incendie de Forêt**

_Définition officielle :_
Un incendie est considéré comme « de forêt » s’il démarre en forêt, s’il s’y propage ou s’il touche des terres boisées au cours de son évolution. Dans l’aire méditerranéenne, un feu de maquis ou de garrigue est assimilé à un feu de forêt.

_Analyse :_
Cette définition élargie implique que certaines catégories de végétation (maquis, garrigues) doivent être intégrées aux statistiques des feux de forêt.  
Pour l’analyse et la modélisation, il faut donc regrouper ces types de surfaces avec les forêts afin de rester conforme à la nomenclature nationale.  

**Date d’alerte**

_Définition officielle :_
Date et heure où l’information d’un départ de feu parvient au CODIS (Centre Opérationnel Départemental d’Incendie et de Secours).

_Analyse :_
La date d’alerte ne correspond pas toujours à l’heure réelle de départ du feu, mais au moment où il est signalé aux autorités. Pour les analyses temporelles (ex. rapidité de détection, saisonnalité, heures critiques), il faut garder en tête ce décalage potentiel qui peut introduire un biais dans l’interprétation des données.  

**Surface parcourue :**  

_Définition officielle :_  
Surface totale parcourue par le feu au cours de son évolution, quelle que soit la végétation touchée.  

_Analyse :_  
La surface parcourue est l’indicateur central de gravité d’un incendie.  
Elle doit être utilisée en combinaison avec les types de végétation pour distinguer les impacts (forêts, maquis, surfaces agricoles, etc.). Les données sont exprimées en m² → conversion en hectares (ha) recommandée pour une meilleure lisibilité et comparabilité.  

**Précision des surfaces :**  

_Définition officielle :_   
- Estimées : valeurs renseignées dans la BDIFF sans mesure directe.  
- Mesurées : valeurs issues de relevés terrain ou d’un Système d’Information Géographique (SIG).

_Analyse :_  
La précision renseigne sur la fiabilité de l’information. Les surfaces estimées peuvent introduire un biais, notamment sur les petits feux ou dans les zones mal cartographiées.  
Pour les analyses fines ou l’entraînement du modèle, il peut être pertinent de :

- filtrer uniquement les surfaces mesurées,
- ou bien pondérer les données selon leur précision.  

**Surface de forêt :**  

_Définition officielle :_  
Surface touchée par l’incendie située en forêt, c’est-à-dire dans des milieux naturels boisés répondant aux critères suivants :

- Taux de couvert arboré > 10 % (végétaux ligneux pouvant atteindre 5 m de haut à maturité).  
- Surface d’un seul tenant > 0,5 ha.
- Largeur > 20 m.  

Sont incluses les plantations ainsi que les jeunes peuplements issus de régénération naturelle ou artificielle.  

_Analyse :_  
Cette définition normalisée distingue la forêt des autres types de végétation (maquis, garrigues, surfaces agricoles…). 
Cela permet d’éviter d’inclure par erreur de petites zones boisées ou des haies agricoles. Pour les analyses statistiques, il faut donc respecter ces seuils et regrouper uniquement les surfaces répondant aux critères comme « forêt ». Cela garantit la comparabilité des données à l’échelle nationale.  

**Autres surfaces naturelles hors forêt**  

_Définition officielle :_  
Surface parcourue par le feu dans un milieu naturel ne répondant pas à la définition stricte de la forêt. Cela inclut notamment :

- Des zones boisées avec un taux de couvert arboré < 10 %.
- Des zones boisées de superficie < 0,5 ha (ex. bosquets).
- Des zones boisées de largeur < 20 m (ex. cordons boisés, haies).
- Des zones à plus de 10 % occupées par des arbustes/arbrisseaux < 5 m (ex. landes ligneuses).
- Des zones herbacées naturelles (ex. prairies naturelles, pelouses d’altitude, landes herbacées).
- Des zones humides (ex. marécages, roselières).  

_Analyse :_  
Cette catégorie regroupe une grande diversité de milieux naturels, souvent plus fragmentés et hétérogènes que la forêt. Dans les analyses, elle doit être considérée comme un ensemble distinct, car les dynamiques de propagation du feu y diffèrent fortement (ex. haies et cordons boisés jouent un rôle de corridor, alors que prairies ou marécages limitent la propagation). Pour la modélisation, il peut être pertinent de tester séparément l’influence des sous-types plutôt que de les agréger en un bloc unique.  

**Surfaces Agricoles:**  

_Définition officielle :_  
Surface parcourue par le feu dans un milieu agricole. Cela concerne :

- Les cultures pérennes et non pérennes.
- Les prairies temporaires.
- Les vergers et surfaces assimilées (noyeraies, plantations de chênes truffiers, agroforesterie, etc.).  

_Analyse :_  
Les surfaces agricoles représentent des zones fortement anthropisées, où l’impact économique est souvent direct (perte de récoltes, destruction de vergers). 
Dans l’analyse des incendies, il peut être intéressant de distinguer ces feux des feux strictement « naturels » (forêts, maquis, landes), car leur fréquence et leurs causes (accidentelles ou liées aux pratiques agricoles) diffèrent. Pour la prédiction du risque, cette catégorie peut également refléter une interaction forte avec l’activité humaine, qui est à l’origine de 90 % des départs de feu.  

**Autres Surfaces :**  

_Définition officielle :_  
Surface parcourue par le feu dans des milieux ne relevant pas des catégories précédentes. Cela inclut notamment :  
- Les friches.
- Les talus.
- Les zones végétalisées artificielles (jardins, pelouses, parcs urbains).  

_Analyse :_  
Cette catégorie est résiduelle et regroupe des milieux très variés, souvent en lien direct avec les zones urbaines ou périurbaines. 
Leur présence traduit un risque d’interface habitat/forêt : les feux qui touchent jardins, parcs ou talus peuvent menacer rapidement des zones habitées. Dans la modélisation, cette catégorie peut être utilisée comme indicateur de vulnérabilité humaine et matérielle, plus que comme variable écologique.  

**Surfaces de forêt Pour les départements de l’aire méditerranéenne:**  

_Définition officielle :_  
Surface touchée par l’incendie située uniquement en forêt. Est considérée comme « forêt » toute zone répondant avant l’incendie aux critères suivants :
- Taux de couvert arboré > 10 % (végétaux ligneux pouvant atteindre in situ plus de 5 m à maturité).
- Surface d’un seul tenant > 0,5 ha.
- Largeur > 20 m.
Sont incluses : les plantations et les jeunes peuplements issus de régénération (naturelle ou artificielle).  

_Analyse :_  
Cette définition distingue clairement la forêt des autres milieux boisés ou semi-naturels (maquis, garrigue, haies, bosquets). 
Pour l’analyse, cela permet d’éviter d’inclure par erreur de petites zones boisées dans les statistiques forestières. Dans la modélisation, la variable « surfaces de forêt » est un indicateur majeur de risque et de gravité, car ces milieux concentrent les feux les plus étendus et les plus difficiles à maîtriser.  

**Maquis, Garrigues :**  

_Définition officielle :_  
Surface parcourue par le feu dans les zones de maquis ou de garrigue dans l’aire méditerranéenne. Ces milieux sont assimilés à des feux de forêt dans cette zone géographique.  

_Analyse :_  
Dans la BDIFF, les maquis et garrigues sont explicitement rattachés à la catégorie “forêt” lorsqu’ils se situent en aire méditerranéenne. 
Cela implique que pour les analyses nationales, il faut regrouper systématiquement ces surfaces avec les surfaces de forêt afin d’assurer la cohérence statistique. Pour la modélisation prédictive, cette normalisation permet d’éviter une sous-estimation du risque dans les départements méditerranéens, où ces milieux sont parmi les plus inflammables.  

**Type de peuplement :**  

_Définition officielle :_  
Indique le type de formation végétale principalement touchée par le feu. Les valeurs possibles sont :
- Landes, garrigues, maquis
- Taillis
- Futaies feuillues
- Futaies résineuses
- Futaies mélangées
- Régénération et reboisement (d’origine naturelle ou artificielle)  

_Analyse :_  
Cette variable permet de qualifier plus finement la végétation affectée. 
Elle peut être utilisée comme variable explicative dans le modèle prédictif, car le type de peuplement influence fortement la propagation et l’intensité du feu (ex. résineux = hautement inflammables).
Il faudra cependant :
- standardiser les catégories (certaines années ou départements peuvent mal renseigner la donnée),
- regrouper si nécessaire certaines classes rares pour éviter des déséquilibres statistiques.  

**Surfaces de forêt (campagnes antérieures à 2023, hors aire méditerranéenne)**  

_Définition officielle:_  
Surface touchée par l’incendie située uniquement en forêt, définie avant 2023 selon les critères suivants :
- Taux de couvert arboré > 10 % (végétaux ligneux pouvant atteindre in situ plus de 5 m à maturité).
- Surface d’un seul tenant > 0,5 ha.
- Largeur > 20 m.
Sont incluses : les plantations et les jeunes peuplements issus de régénération (naturelle ou artificielle).

Différence avec l’aire méditerranéenne : avant 2023, les maquis et garrigues ne sont pas assimilés aux forêts pour les départements hors zone méditerranéenne.  

_Analyse :_  
Cette définition montre que la catégorisation des surfaces a évolué dans le temps. 
Dans une analyse longue période (avant/après 2023), il faudra :
- bien distinguer les zones hors Méditerranée, où maquis/garrigues étaient exclus de la forêt,
- normaliser les données si l’on veut comparer toutes les régions et toutes les années sur une base homogène.
Sinon, on risque de sous-estimer la part de « forêts » dans les anciens enregistrements par rapport aux récents.  

**Surfaces Autres Terres Boisées (campagnes antérieures à 2023, hors aire méditerranéenne):**  

_Définition officielle :_  
Surface parcourue par le feu dans des zones boisées ne répondant pas à la définition de la forêt. Les
surfaces peuvent être :
- Des zones boisées dont le taux de couvert arboré est inférieur à 10 %
- Des zones boisées dont la superficie totale est inférieure à 0.5 ha telles que les bosquets
- Des zones boisées dont la largeur est généralement inférieure à 20 m telles que les cordons
boisés et les haies
Cette catégorie de surface comprend les landes, maquis et garrigues lorsqu’ils répondent à ces trois
critères.  

_Analyse :_  
Avant 2023, hors aire méditerranéenne, une partie des maquis et garrigues pouvait être classée comme « autres terres boisées » et non comme « forêts ». 
Cela crée un décalage de classification avec la période post-2023 et avec les départements méditerranéens (où maquis/garrigue = forêt).
Pour une analyse diachronique, il faudra donc harmoniser ces catégories afin d’éviter de sous-estimer la part de surfaces forestières dans les données anciennes.  

**Surfaces non boisées naturelles :**  

_Définition officielle :_  
Surface parcourue par le feu dans des zones qui ne répondent ni à la définition de la forêt ni à celle des autres terres boisées, et correspondant à des milieux naturels. Cela inclut :
- Les landes herbacées.
- Les prairies naturelles.
- Les zones humides.  

_Analyse :_  
Cette catégorie permet de distinguer les milieux naturels ouverts (herbacés ou humides) des zones boisées. 
Ces milieux ont en général une inflammabilité plus faible que les forêts ou maquis, mais ils peuvent jouer un rôle important dans la propagation locale (prairies sèches en été, par exemple).
Dans la modélisation, il peut être utile de considérer cette catégorie comme un facteur atténuateur ou de transition dans l’espace (zones tampons entre surfaces boisées et zones agricoles/urbaines).  

**Surfaces non boisées artificielles :**  

_Définition officielle :_  
Surface parcourue par le feu dans des zones ne répondant pas à la définition de la forêt ni à celle des autres terres boisées, et correspondant à des milieux artificiels. Cela inclut notamment :
- Les prairies temporaires.
- Les zones cultivées (terres arables, vergers).
- Les jardins autour des constructions.
- Toute autre surface artificialisée.  

_Analyse :_  
Cette catégorie regroupe des espaces directement liés aux activités humaines. 
Leur présence est importante pour identifier les feux à l’interface habitat/agriculture/forêt, où les enjeux économiques et humains sont plus élevés.
Dans la modélisation prédictive, ces surfaces peuvent servir d’indicateur de risque accru lié à l’activité humaine, sachant que 90 % des départs de feux sont d’origine anthropique.  

**Surfaces de forêt (campagnes antérieures à 2023 – aire méditerranéenne) :**  

_Définition officielle :_  
Surface touchée par l’incendie située uniquement en forêt, définie par les critères suivants :
- Taux de couvert arboré > 10 % (végétaux ligneux pouvant atteindre in situ plus de 5 m à maturité).
- Surface d’un seul tenant > 0,5 ha.
- Largeur > 20 m.
Sont incluses : les plantations et les jeunes peuplements issus de régénération naturelle ou artificielle.  

Spécificité méditerranéenne avant 2023 : dans ces départements, les maquis et garrigues sont exclus de la catégorie « forêt » et comptabilisés séparément.  

_Analyse :_  
Ce point est crucial pour toute analyse diachronique :

- Avant 2023, les maquis/garrigues étaient considérés comme une catégorie distincte dans l’aire méditerranéenne.
- Après 2023, ils sont intégrés à la définition de « forêt ».

Pour comparer les données dans le temps, il faudra donc harmoniser la classification afin d’éviter de surestimer artificiellement la hausse des surfaces forestières brûlées dans les séries post-2023.  

**Maquis, garrigues (campagnes antérieures à 2023 – aire méditerranéenne) :**  

_Définition officielle :_  
Surface parcourue par le feu dans les zones de maquis ou de garrigue situées dans l’aire méditerranéenne.  

_Analyse :_  
Avant 2023, les maquis et garrigues formaient une catégorie distincte des forêts dans les départements méditerranéens. Cela implique que :
- Pour la période pré-2023, ces surfaces doivent être traitées séparément.
- Pour la période post-2023, elles sont intégrées dans la catégorie « forêts ».

Pour les analyses comparatives dans le temps ou entre régions, il faudra normaliser les catégories afin de ne pas introduire de rupture artificielle dans les séries (ex. hausse apparente des feux de forêts après 2023 liée uniquement à un changement de définition).  

**Autres surfaces (campagnes antérieures à 2023 – aire méditerranéenne) :**  

_Définition officielle :_  
Surface parcourue par le feu dans les milieux autres que les catégories ci-dessus. Concerne
notamment les surfaces de friches, les talus et les zones végétalisées artificielles (jardins, pelouses et
parcs urbains).  

_Analyse :_  
Cette catégorie est une classe résiduelle, qui regroupe des milieux variés, souvent proches ou intégrés aux zones urbanisées. 
Leur présence traduit un risque accru en interface habitat/nature (jardins et parcs urbains directement exposés).
Pour l’analyse, ces surfaces doivent être distinguées car elles mettent davantage en évidence les enjeux humains et matériels que les caractéristiques écologiques. Dans le modèle prédictif, elles peuvent servir de variable de vulnérabilité socio-spatiale.  

**Type de peuplement (campagnes antérieures à 2023 – aire méditerranéenne) :**  

_Définition officielle :_  
Indique le type de formation végétale principalement touchée par le feu. Les valeurs possibles sont :
- Landes, garrigues, maquis
- Taillis
- Futaies feuillues
- Futaies résineuses
- Futaies mélangées
- Régénération et reboisement (d’origine naturelle ou artificielle)  

_Analyse :_  
Cette variable précise la structure de la végétation affectée, ce qui est essentiel pour comprendre la dynamique et l’intensité des incendies. 👉 Dans l’aire méditerranéenne, la distinction entre garrigues/maquis et les autres peuplements est particulièrement importante car ce sont des milieux hautement inflammables.
Pour la modélisation prédictive, il faudra :
- utiliser cette variable comme facteur explicatif clé du risque,
- regrouper ou simplifier certaines classes rares pour améliorer la robustesse statistique,
- harmoniser les catégories après 2023 (où maquis/garrigues sont intégrés à la forêt).  

**Nature de l'incendie :**  

_Définition officielle :_  
La variable Nature indique l’origine de l’incendie lorsque l’information est connue. Les valeurs possibles sont :
- Naturelle : incendie non causé par une activité humaine directe ou indirecte (ex. foudre).
- Accidentelle : incendie lié à un événement ou une installation humaine de façon indirecte (ex. rupture de ligne électrique, échappements de véhicules).
- Malveillance : incendie déclenché volontairement.
- Involontaire (travaux) : incendie causé par des activités humaines professionnelles sans intention de déclenchement (ex. travaux forestiers, agricoles, de construction).
- Involontaire (particulier) : incendie causé par des activités humaines dans un cadre privé (ex. travaux domestiques, brûlage, bricolage).  

_Analyse :_  
La variable Nature est essentielle pour distinguer les causes humaines (qui représentent environ 90 % des départs de feu) des causes naturelles. Elle permet :
- une meilleure compréhension des facteurs de risque liés aux activités humaines,
- la mise en évidence de zones sensibles (ex. proximité de lignes électriques, zones agricoles actives),
- un potentiel usage comme variable explicative dans le modèle prédictif.

Limite : cette information est souvent incomplète ou imprécise. Certaines fiches incendies restent marquées comme « inconnues », ce qui nécessite soit de les traiter comme une catégorie à part, soit de les exclure selon les analyses.  

**Nombre de décès :** 

_Définition officielle :_  
Nombre de personnes décédées durant l’incendie ou des suites directes de l’incendie.


_Analyse :_  
Cette variable mesure l’impact humain le plus grave. 
Elle est utile pour identifier les événements majeurs, mais les cas restent heureusement rares. Son faible volume limite son usage statistique, mais elle peut servir comme indicateur de gravité exceptionnelle.  

**Nombre de bâtiments partiellment détruits :**  

_Définition officielle: _  
Nombre de bâtiments en dur endommagés par l’incendie, dont seule une partie a été touchée. La toiture n’est pas détruite et le bâtiment reste en partie utilisable.

_Analyse :_
Cette variable indique un niveau d’impact matériel intermédiaire. 
Elle permet de repérer les incendies en zone d’interface habitat/nature, où les habitations sont vulnérables. En modélisation, elle peut être intégrée comme variable qualitative pour signaler une exposition humaine forte.  

**Nombre de bâtiments totalement détruits :**  

_Définition officielle :_  
Nombre de bâtiments en dur détruits par l’incendie. La toiture est totalement effondrée, le bâtiment est à ciel ouvert et inutilisable sans reconstruction lourde.

_Analyse :_
C’est un indicateur d’impact matériel extrême. 
Comme pour les décès, cette donnée est souvent rare mais essentielle pour qualifier les incendies catastrophiques. Elle met en évidence les zones à très forte vulnérabilité (villages, zones urbanisées exposées).  

**<u>3. Explorer l'API et les formats de téléchargement BDIFF</u>**  

_Vue d’ensemble_

La BDIFF est consultable via l’interface publique Recherche et consultation des incendies. On y filtre les données par dates, heures, surfaces, localisation (région/département/commune) ou période glissante. Les résultats sont affichés dans un tableau et sur une carte.  

<b>Téléchargement</b> : un bouton CSV sous le tableau génère une archive ZIP contenant : (1) un CSV avec toutes les colonnes publiques de la sélection, (2) Mentions légales.pdf, (3) Définitions.pdf. Les fichiers sont en UTF-8.  

<b>Couverture temporelle</b> : données disponibles nationalement depuis 2006, et depuis 1973 pour certains départements de l’aire méditerranéenne. Les années en cours de saisie ne sont pas diffusées.  

_Format des fichiers fournis_  

ZIP → CSV + PDFs (définitions, mentions). Encodage UTF-8 recommandé pour ouvrir le CSV (accents).  

Le tableau de l’interface affiche des surfaces en hectares, mais les définitions officielles (fichier Définitions.pdf inclus) indiquent des surfaces renseignées en m² dans les colonnes détaillées par type — prévoir une conversion m² → ha pour les analyses.  

**<u>4. Étudier les référentiels géographiques INSEE disponibles</u>**  

_Objectif_

Les fichiers BDIFF utilisent le Code INSEE comme identifiant unique des communes. Pour exploiter les données (cartographie, agrégation, voisinage géographique), il est nécessaire de relier ce code à des informations géographiques et administratives issues des référentiels de l’INSEE.  

_Sources principales_

1. Code officiel géographique (COG) – INSEE

- Référentiel annuel des communes françaises.
- Contient : codes INSEE, libellés, rattachements aux départements/régions.
- Historique disponible (permet de gérer les fusions/suppressions de communes au fil du temps).
- Format : CSV et fichiers normalisés.

2. Base Adresse Nationale (BAN) / adresse.data.gouv.fr

- Fichiers téléchargeables par département.
- Contiennent les coordonnées latitude/longitude des communes.
- Colonnes principales : code_insee, nom_commune, lat, lon.
- Source officielle pour le géocodage des communes.

3. IGN – Admin Express
- Base géographique vectorielle des entités administratives (communes, cantons, départements, régions).
- Inclut les polygones (géométries précises des limites communales).
- Format : shapefile / GeoJSON (utile pour cartographie avancée).  

_Problématiques à prendre en compte_  

Evolutions des codes INSEE:  
- Des communes fusionnent (ex. « communes nouvelles » depuis 2015).  
- Certaines sont supprimées ou scindées.  
- Il est indispensable de choisir une version de référence (ex. COG 2024) et d’y rattacher toutes les données historiques.  

Granularité:  
- La BDIFF est au niveau communal → il suffit d’avoir les coordonnées du centroïde (lat/lon) pour une cartographie simple.
- Pour des analyses spatiales fines (voisinage, densité, surfaces boisées), l’Admin Express est préférable.  

Jointures:  
- La clé de jointure principale = code_insee.
- Prévoir une table SQL communes qui centralise :
- - Code INSEE
- - Nom de la commune
- - Département / Région
- - Coordonnées (lat, lon)
- - Géométrie (optionnel pour carto avancée)  

**<u>5. Comprendre les enjeux de consolidation multi-sources</u>**  

_Pourquoi consolider plusieurs sources ?_  

La BDIFF seule ne suffit pas à produire une analyse complète.
Elle fournit des données détaillées sur les incendies (où, quand, combien de surface, quel type de végétation, origine).  
Mais pour une application de prédiction des risques, il faut enrichir ces données avec des référentiels géographiques et contextuels.  

_Sources à consolider_

1. BDIFF
- Base des incendies recensés (1973–2024).
- Niveau communal (code INSEE).

2. Référentiels géographiques INSEE
- Codes INSEE, rattachements administratifs, coordonnées (lat/lon).
- Données nécessaires pour cartographier et agréger les incendies.

3. IGN – Admin Express (optionnel)
- Polygones des communes pour cartographie avancée.
- Permet de calculer des relations de voisinage (communes limitrophes).

4. Données de contexte (futures extensions)
- Météo : température, vent, sécheresse.
- Occupation du sol : surfaces agricoles, forêts, zones urbanisées.
- Topographie : altitude, proximité du littoral méditerranéen.  

_Défis techniques_  

Hétérogénéité des formats :

- CSV (BDIFF, INSEE) vs shapefiles/GeoJSON (IGN).
- Nécessité d’un pipeline ETL capable de lire plusieurs formats.

Évolution temporelle :
- Fusions/suppressions de communes → un même code INSEE peut ne plus exister.
- Solution : choisir un référentiel de référence (COG 2024) et y rattacher toutes les données historiques.

Granularité différente :
- BDIFF = commune.
- Météo = maille départementale ou infra-départementale.
- Occupation du sol = parcelles ou zones CORINE Land Cover.
- Nécessité d’agréger et normaliser les niveaux géographiques.

Qualité des données :
- Valeurs manquantes, surfaces estimées, incohérences géographiques.
- Important de prévoir un module de validation et nettoyage lors de l’ingestion.  

_Bonnes pratiques de consolidation_  

Créer une base SQL centralisée avec des tables normalisées :
- incendies (BDIFF)
- communes (INSEE + coordonnées)
- meteo (extension future)

Mettre en place des pipelines automatisés pour :
- Télécharger et charger les fichiers bruts.
- Normaliser les codes INSEE.
- Ajouter les coordonnées lat/lon.
- Documenter toutes les étapes pour assurer la reproductibilité.