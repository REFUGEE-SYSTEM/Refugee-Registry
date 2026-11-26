#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage: ./scripts/up.sh

Starts the standalone Refugee Registry stack, runs idempotent bootstrap
(MinIO buckets, Keycloak realm/users, IAM RBAC, AWE callback secret,
ID generator pools, Master Data ETH geo + Uganda refugee codelists, and
registry metadata + optional demo data).
EOF
  exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f .env ]]; then
  echo "[up] .env not found; running ./scripts/init-env.sh ..."
  ./scripts/init-env.sh
fi

# Always ensure login_providers.json matches current .env ports/secrets
./scripts/init-env.sh >/dev/null

echo "[up] Building and starting standalone services ..."
docker compose up -d --build --wait

echo "[up] Bootstrapping MinIO, Keycloak, IAM, AWE, and ID Generator ..."
docker compose --profile bootstrap run --rm --build bootstrap-core

echo "[up] Seeding Master Data (ETH geo + refugee codelists) ..."
docker compose --profile bootstrap run --rm --build mds-seed

echo "[up] Seeding Refugee Registry metadata & demo data ..."
docker compose --profile bootstrap run --rm --build db-seed

set -a
# shellcheck disable=SC1091
source .env
set +a

echo "[up] Refugee Registry is ready!"
echo "  Staff UI:      http://localhost:${REFUGEE_UI_PORT:-3150}/en"
echo "  Staff API:     http://localhost:${REFUGEE_STAFF_API_PORT:-8271}/docs"
echo "  Master Data:   http://localhost:${REFUGEE_MDS_API_PORT:-8249}/docs"
echo "  Keycloak:      http://localhost:${REFUGEE_KEYCLOAK_PORT:-8280}"
