#!/usr/bin/env bash
set -euo pipefail

PACK_DIR="/opt/openg2p-data/packs/ETH"
REFUGEE_CODELISTS_SRC="${REFUGEE_CODELISTS_SRC:-/data/codelists/refugee}"

if [[ -d "${REFUGEE_CODELISTS_SRC}" ]]; then
  mkdir -p "${PACK_DIR}/domains/refugee"
  cp -f "${REFUGEE_CODELISTS_SRC}"/*.json "${PACK_DIR}/domains/refugee/"
fi

export PGHOST="${MD_PGHOST:-postgres}"
export PGPORT="${MD_PGPORT:-5432}"
export PGUSER="${MD_PGUSER:-postgres}"
export PGPASSWORD="${MD_PGPASSWORD:?MD_PGPASSWORD is required}"
MD_DB="${MD_PGDATABASE:-refugee_master_data_db}"

echo "[mds-seed] Waiting for ${MD_DB} schema (g2p_geo_levels) ..."
for _ in $(seq 1 60); do
  if python3 -c "
import os, psycopg2
conn = psycopg2.connect(host=os.environ['PGHOST'], port=os.environ['PGPORT'], dbname='${MD_DB}', user=os.environ['PGUSER'], password=os.environ['PGPASSWORD'])
cur = conn.cursor()
cur.execute(\"SELECT 1 FROM information_schema.tables WHERE table_name = 'g2p_geo_levels'\")
assert cur.fetchone() is not None
conn.close()
" 2>/dev/null; then
    break
  fi
  sleep 2
done

echo "[mds-seed] Applying MDS schema migrations ..."
python3 - <<'PY'
import glob, os, psycopg2
conn = psycopg2.connect(
    host=os.environ["PGHOST"],
    port=os.environ["PGPORT"],
    dbname=os.environ.get("MD_PGDATABASE", "refugee_master_data_db"),
    user=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
)
conn.autocommit = True
with conn.cursor() as cur:
    for path in sorted(glob.glob("/opt/mds-seed/migrations/*.sql")):
        print(f"[mds-seed] Applying {os.path.basename(path)} ...")
        with open(path, encoding="utf-8") as f:
            cur.execute(f.read())
conn.close()
PY

echo "[mds-seed] Seeding ETH geo + refugee codelists into ${MD_DB} ..."
python3 /opt/mds-seed/load_geo_pack.py \
  --pack "${PACK_DIR}" \
  --db "${MD_DB}" \
  --load "geo,codelists" \
  --domains "refugee"

echo "[mds-seed] Publishing version 1 geo & codelist catalogues ..."
python3 - <<'PY'
import os, psycopg2
conn = psycopg2.connect(
    host=os.environ["PGHOST"],
    port=os.environ["PGPORT"],
    dbname=os.environ.get("MD_PGDATABASE", "refugee_master_data_db"),
    user=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
)
conn.autocommit = False
with conn, conn.cursor() as cur:
    cur.execute("SELECT 1 FROM g2p_geo_versions WHERE version_no = 1")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO g2p_geo_versions (version_no, country, status) VALUES (1, 'ETH', 'DRAFT')")
        cur.execute("""
            INSERT INTO g2p_geo_version_levels (version_no, level_id, level_mnemonic, parent_level_id, display, display_i18n)
            SELECT 1, level_id, level_mnemonic, parent_level_id, COALESCE(display_name, level_mnemonic), display_name_i18n
            FROM g2p_geo_levels
        """)
        cur.execute("""
            INSERT INTO g2p_geo_version_units (version_no, unit_id, level_id, name, name_i18n, parent_unit_id, status, valid_from, valid_to)
            SELECT 1, level_value_id, level_id, COALESCE(display_name, level_value_mnemonic, level_value_id),
                   display_name_i18n, parent_level_value_id, 'ACTIVE', valid_from, valid_to
            FROM g2p_geo_level_values
        """)
        cur.execute("""
            UPDATE g2p_geo_versions
            SET status = 'PUBLISHED', effective_from = NOW(), published_at = NOW()
            WHERE version_no = 1
        """)

    cur.execute("""
        INSERT INTO g2p_list_versions (list_id, version_no, list_code, display, display_i18n, is_hierarchical, status)
        SELECT attribute_id, 1, attribute_code, attribute_display,
               COALESCE(display_i18n, display_name_i18n), COALESCE(is_hierarchical, false), 'DRAFT'
        FROM g2p_attributes a
        WHERE NOT EXISTS (
            SELECT 1 FROM g2p_list_versions lv WHERE lv.list_id = a.attribute_id AND lv.version_no = 1
        )
    """)
    cur.execute("""
        INSERT INTO g2p_list_version_values (list_id, version_no, value_id, value_code, display, display_i18n, parent_value_code, sort_order, roles, status)
        SELECT av.attribute_id, 1, av.value_id, COALESCE(av.value_code, av.value_id), av.value_display,
               COALESCE(av.display_name_i18n, '{}'::jsonb), av.parent_value_id, av.sort_order, av.roles, 'ACTIVE'
        FROM g2p_attribute_values av
        JOIN g2p_list_versions lv ON lv.list_id = av.attribute_id AND lv.version_no = 1 AND lv.status = 'DRAFT'
        WHERE NOT EXISTS (
            SELECT 1 FROM g2p_list_version_values lvv
            WHERE lvv.list_id = av.attribute_id AND lvv.version_no = 1 AND lvv.value_id = av.value_id
        )
    """)
    cur.execute("""
        UPDATE g2p_list_versions
        SET status = 'PUBLISHED', effective_from = NOW(), published_at = NOW()
        WHERE version_no = 1 AND status = 'DRAFT'
    """)
    cur.execute("UPDATE g2p_attributes SET current_version_no = 1 WHERE current_version_no IS NULL")
conn.close()
PY
echo "[mds-seed] Master Data seed complete."
