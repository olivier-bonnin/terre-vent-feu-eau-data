import os, sys, csv, glob, re
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Set

import psycopg2
from dotenv import load_dotenv
from unidecode import unidecode

BASE_DIR  = Path(__file__).resolve().parent.parent
DATA_GLOB = str(BASE_DIR / "data" / "Incendies_*.csv")

CSV_TO_TARGET = {
    "annee": "annee",
    "numero": "numero",
    "code_insee": "code_insee",
    "nom_de_la_commune": "nom_commune",
    "nom_de_commune": "nom_commune",
    "nom_commune": "nom_commune",
    "departement": "departement",
    "date_de_premiere_alerte": "date_premiere_alerte",
    "date_premiere_alerte": "date_premiere_alerte",
    "surface_parcourue_m2": "surface_parcourue_m2",
    "surface_foret_m2": "surface_foret_m2",
    "surface_maquis_garrigues_m2": "surface_maquis_garrigues_m2",
    "autres_surfaces_naturelles_hors_foret_m2": "autres_surfaces_naturelles_hors_foret_m2",
    "surfaces_agricoles_m2": "surfaces_agricoles_m2",
    "autres_surfaces_m2": "autres_surfaces_m2",
    "surface_autres_terres_boisees_m2": "surface_autres_terres_boisees_m2",
    "surfaces_non_boisees_naturelles_m2": "surfaces_non_boisees_naturelles_m2",
    "surfaces_non_boisees_artificialisees_m2": "surfaces_non_boisees_artificialisees_m2",
    "surfaces_non_boisees_m2": "surfaces_non_boisees_m2",
    "precision_des_surfaces": "precision_des_surfaces",
    "type_de_peuplement": "type_de_peuplement",
    "nature": "nature",
    "deces_ou_batiments_touches": "deces_ou_batiments_touches",
    "nombre_de_deces": "nombre_de_deces",
    "nombre_de_batiments_totalement_detruits": "nb_batiments_totalement_detruits",
    "nb_batiments_totalement_detruits": "nb_batiments_totalement_detruits",
    "nombre_de_batiments_partiellement_detruits": "nb_batiments_partiellement_detruits",
    "nb_batiments_partiellement_detruits": "nb_batiments_partiellement_detruits",
    "precision_de_la_donnee": "precision_de_la_donnee",
}

def normalize_headers(cols: List[str]) -> List[str]:
    out = []
    for c in cols:
        cc = unidecode(str(c)).lower().strip()
        cc = cc.replace("(", "").replace(")", "").replace("’", "'")
        cc = re.sub(r"\s+", " ", cc).replace(" ", "_")
        cc = re.sub(r"__+", "_", cc)
        out.append(cc)
    return out

def normalize_insee(code: str) -> str | None:
    """Retourne un code INSEE normalisé :
       - None si vide
       - garde 2A/2B tels quels
       - si uniquement chiffres et len<5 -> left-pad à 5 (ex 7033 -> 07033)
       - sinon renvoie tel quel
    """
    if code is None:
        return None
    s = str(code).strip()
    if not s:
        return None

    s = s.replace(" ", "")

    if re.match(r"^(2A|2B)\d{3}$", s, re.IGNORECASE):
        return s.upper()

    if re.match(r"^\d+$", s):
        if len(s) < 5:
            return s.zfill(5)
        return s

    return s

def open_conn(db_url: str):
    return psycopg2.connect(db_url)

def ensure_communes_exist(db_url: str, codes: Set[str]):
    """Insère dans communes les codes manquants (placeholders)."""
    if not codes:
        return
    conn = open_conn(db_url)
    conn.autocommit = False
    cur = conn.cursor()
    try:

        cur.execute("DROP TABLE IF EXISTS tmp_codes;")
        cur.execute("CREATE TEMP TABLE tmp_codes(code_insee TEXT PRIMARY KEY);")

        copy_sql = "COPY tmp_codes (code_insee) FROM STDIN WITH (FORMAT CSV)"
        with conn.cursor() as c2:
            c2.copy_expert(copy_sql, io:=__import__("io").StringIO("\n".join(sorted(codes))))

        cur.execute("""
            INSERT INTO communes(code_insee)
            SELECT t.code_insee
            FROM tmp_codes t
            WHERE NOT EXISTS (
                SELECT 1 FROM communes c WHERE c.code_insee = t.code_insee
            );
        """)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        try:
            cur.close(); conn.close()
        except Exception:
            pass

def main():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL manquant dans .env")
        sys.exit(1)

    files = sorted(glob.glob(DATA_GLOB))
    print(f"Pattern : {DATA_GLOB}")
    print(f"Fichiers : {[Path(f).name for f in files]}")
    if not files:
        print("Aucun fichier trouvé. Vérifie le nom (Incendies_*.csv) et le dossier data/.")
        sys.exit(1)

    all_codes: Set[str] = set()
    for path in files:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=";")
            header = next(reader)
            header = normalize_headers(header)
            if "code_insee" not in header:
                continue
            idx = header.index("code_insee")
            for row in reader:
                if idx < len(row):
                    code = normalize_insee(row[idx])
                    if code:
                        all_codes.add(code)

    print(f"Codes INSEE détectés (uniques) : {len(all_codes):,}")
    ensure_communes_exist(db_url, all_codes)
    print("Communes manquantes insérées (placeholders).")

    conn = open_conn(db_url); conn.autocommit = False
    cur = conn.cursor()

    total_inserted = 0

    try:
        for path in files:
            base = Path(path).name
            batch_id = Path(base).stem

            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.reader(f, delimiter=";")
                header_raw = next(reader)
            header_norm = normalize_headers(header_raw)

            csv_known = [c for c in header_norm if c in CSV_TO_TARGET]
            if not csv_known:
                raise RuntimeError(f"Aucune colonne reconnue dans {base} (header={header_norm})")

            cur.execute("DROP TABLE IF EXISTS tmp_bdiff_stage;")
            cols_def = ", ".join([f"{c} TEXT" for c in csv_known])
            cur.execute(f"CREATE TEMP TABLE tmp_bdiff_stage ({cols_def});")

            col_list = ", ".join(csv_known)
            copy_sql = f"""
                COPY tmp_bdiff_stage ({col_list})
                FROM STDIN WITH (FORMAT CSV, HEADER TRUE, DELIMITER ';', QUOTE '\"')
            """
            with open(path, "r", encoding="utf-8") as f:
                cur.copy_expert(copy_sql, f)

            cur.execute("SELECT COUNT(*) FROM tmp_bdiff_stage;")
            stage_count = cur.fetchone()[0]

            def src(col): 
                return col if col in csv_known else "NULL"

            code_src = src("code_insee")
            code_norm_expr = (
                f"CASE "
                f"WHEN {code_src} IS NULL OR {code_src} = '' THEN NULL "
                f"WHEN {code_src} ~ '^(2A|2B)\\d{{3}}$' THEN upper({code_src}) "
                f"WHEN {code_src} ~ '^\\d+$' AND length({code_src}) < 5 THEN lpad({code_src}, 5, '0') "
                f"ELSE {code_src} "
                f"END"
            )

            def as_bigint(col):
                c = src(col)
                return f"CASE WHEN {c} ~ '^-?\\d+$' THEN ({c})::bigint ELSE NULL END"

            def as_text(col):
                c = src(col)
                return f"NULLIF({c}, '')"

            date_src = f"COALESCE({src('date_de_premiere_alerte')}, {src('date_premiere_alerte')})"

            fr_prepared = f"""
            CASE
            WHEN {date_src} ~ '^\\d{{2}}/\\d{{2}}/\\d{{4}} \\d{{1,2}}:\\d{{2}}$'
                THEN {date_src} || ':00'     -- ajoute :SS si manquent
            ELSE {date_src}
            END
            """

            fr_padded = f"""
            regexp_replace(
            {fr_prepared},
            '^(\\d{{2}}/\\d{{2}}/\\d{{4}}) (\\d):',  -- heure à 1 chiffre
            '\\1 0\\2:'                              -- pad à 2 chiffres
            )
            """

            date_sql = f"""
            CASE
            WHEN {date_src} IS NULL OR {date_src} = '' THEN NULL::timestamp
            WHEN POSITION('/' IN {date_src}) > 0 THEN
                to_timestamp({fr_padded}, 'DD/MM/YYYY HH24:MI:SS')
            WHEN POSITION('-' IN {date_src}) > 0 THEN
                CASE
                    WHEN {date_src} ~ '^\\d{{4}}-\\d{{2}}-\\d{{2}}$'
                        THEN to_timestamp({date_src}, 'YYYY-MM-DD')
                    WHEN {date_src} ~ '^\\d{{4}}-\\d{{2}}-\\d{{2}} \\d{{2}}:\\d{{2}}$'
                        THEN to_timestamp({date_src}, 'YYYY-MM-DD HH24:MI')
                    ELSE to_timestamp({date_src}, 'YYYY-MM-DD HH24:MI:SS')
                END
            ELSE NULL::timestamp
            END
            """

            insert_sql = f"""
                INSERT INTO incendies (
                    annee, numero, code_insee, nom_commune, departement, date_premiere_alerte,
                    surface_parcourue_m2, surface_foret_m2, surface_maquis_garrigues_m2,
                    autres_surfaces_naturelles_hors_foret_m2, surfaces_agricoles_m2, autres_surfaces_m2,
                    surface_autres_terres_boisees_m2, surfaces_non_boisees_naturelles_m2,
                    surfaces_non_boisees_artificialisees_m2, surfaces_non_boisees_m2,
                    precision_des_surfaces, type_de_peuplement, nature, deces_ou_batiments_touches,
                    nombre_de_deces, nb_batiments_totalement_detruits, nb_batiments_partiellement_detruits,
                    precision_de_la_donnee, src_file_name, batch_id, loaded_at
                )
                SELECT
                    {as_bigint("annee")},
                    {as_text("numero")},
                    {code_norm_expr},
                    COALESCE({as_text("nom_de_la_commune")}, {as_text("nom_de_commune")}, {as_text("nom_commune")}),
                    {as_text("departement")},
                    {date_sql},
                    {as_bigint("surface_parcourue_m2")},
                    {as_bigint("surface_foret_m2")},
                    {as_bigint("surface_maquis_garrigues_m2")},
                    {as_bigint("autres_surfaces_naturelles_hors_foret_m2")},
                    {as_bigint("surfaces_agricoles_m2")},
                    {as_bigint("autres_surfaces_m2")},
                    {as_bigint("surface_autres_terres_boisees_m2")},
                    {as_bigint("surfaces_non_boisees_naturelles_m2")},
                    {as_bigint("surfaces_non_boisees_artificialisees_m2")},
                    {as_bigint("surfaces_non_boisees_m2")},
                    {as_text("precision_des_surfaces")},
                    {as_text("type_de_peuplement")},
                    {as_text("nature")},
                    {as_text("deces_ou_batiments_touches")},
                    {as_bigint("nombre_de_deces")},
                    {as_bigint("nb_batiments_totalement_detruits")},
                    {as_bigint("nb_batiments_partiellement_detruits")},
                    {as_text("precision_de_la_donnee")},
                    %s, %s, %s
                FROM tmp_bdiff_stage;
            """
            cur.execute(
                insert_sql,
                (base, batch_id, datetime.now(timezone.utc).replace(tzinfo=None)),
            )

            cur.execute("SELECT COUNT(*) FROM incendies WHERE batch_id = %s;", (batch_id,))
            inserted = cur.fetchone()[0]
            if inserted != stage_count:
                raise RuntimeError(f"Insertion incomplète pour {base}: staging={stage_count}, inserees={inserted}")

            total_inserted += inserted
            conn.commit()
            print(f"{base}: {inserted} lignes insérées")

            cur.execute("DROP TABLE IF EXISTS tmp_bdiff_stage;")

        print(f"\n Import terminé : {total_inserted} lignes insérées (tous fichiers).")

    except Exception as e:
        conn.rollback()
        print(f"\n ERREUR: {e}\n")
        try:
            cur.execute("SELECT COUNT(*) FROM tmp_bdiff_stage;")
            print("(debug) lignes en staging:", cur.fetchone()[0])
        except Exception:
            pass
        sys.exit(2)
    finally:
        try:
            cur.close(); conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()
