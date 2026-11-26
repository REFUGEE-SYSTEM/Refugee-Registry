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
echo "[mds-seed] Master Data seed complete."
