-- ===================================================================
-- Schéma minimal pour le proto BDIFF (communes + incendies)
-- ===================================================================

-- 1) Table COMMUNES (référentiel INSEE)

DROP TABLE IF EXISTS communes CASCADE;
CREATE TABLE communes (
    code_insee TEXT PRIMARY KEY,
    nom_standard TEXT,
    dep_code TEXT,
    reg_code TEXT,
    population INT,
    superficie_km2 NUMERIC,
    densite NUMERIC,
    altitude_moyenne INT,
    latitude_centre DOUBLE PRECISION,
    longitude_centre DOUBLE PRECISION
);
CREATE INDEX IF NOT EXISTS idx_communes_dep ON communes(dep_code);

-- 2) Table INCENDIES

DROP TABLE IF EXISTS incendies CASCADE;
CREATE TABLE incendies (
    id_incendie BIGSERIAL PRIMARY KEY,
    annee INT,
    numero TEXT,
    code_insee TEXT REFERENCES communes(code_insee),
    nom_commune TEXT,
    departement TEXT,
    date_premiere_alerte TIMESTAMP NULL,

    surface_parcourue_m2 BIGINT,
    surface_foret_m2 BIGINT,
    surface_maquis_garrigues_m2 BIGINT,
    autres_surfaces_naturelles_hors_foret_m2 BIGINT,
    surfaces_agricoles_m2 BIGINT,
    autres_surfaces_m2 BIGINT,
    surface_autres_terres_boisees_m2 BIGINT,
    surfaces_non_boisees_naturelles_m2 BIGINT,
    surfaces_non_boisees_artificialisees_m2 BIGINT,
    surfaces_non_boisees_m2 BIGINT,

    precision_des_surfaces TEXT,
    type_de_peuplement TEXT,
    nature TEXT,
    deces_ou_batiments_touches TEXT,
    nombre_de_deces INT,
    nb_batiments_totalement_detruits INT,
    nb_batiments_partiellement_detruits INT,
    precision_de_la_donnee TEXT,

    src_file_name TEXT,
    batch_id TEXT,
    loaded_at TIMESTAMP DEFAULT now()
);

-- Index utiles
CREATE INDEX IF NOT EXISTS idx_incendies_insee ON incendies(code_insee);
CREATE INDEX IF NOT EXISTS idx_incendies_annee ON incendies(annee);

-- Contrôles de cohérence simples
ALTER TABLE incendies
  ADD CONSTRAINT chk_surfaces_non_neg
  CHECK (
    COALESCE(surface_parcourue_m2,0) >= 0 AND
    COALESCE(surface_foret_m2,0) >= 0 AND
    COALESCE(surface_maquis_garrigues_m2,0) >= 0 AND
    COALESCE(autres_surfaces_naturelles_hors_foret_m2,0) >= 0 AND
    COALESCE(surfaces_agricoles_m2,0) >= 0 AND
    COALESCE(autres_surfaces_m2,0) >= 0 AND
    COALESCE(surface_autres_terres_boisees_m2,0) >= 0 AND
    COALESCE(surfaces_non_boisees_naturelles_m2,0) >= 0 AND
    COALESCE(surfaces_non_boisees_artificialisees_m2,0) >= 0 AND
    COALESCE(surfaces_non_boisees_m2,0) >= 0
  );