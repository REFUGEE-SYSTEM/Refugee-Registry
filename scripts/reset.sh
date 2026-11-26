#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage: ./scripts/reset.sh --yes

Wipes standalone containers and named volumes (refugee_postgres_data,
refugee_redis_data, refugee_minio_data), then runs ./scripts/up.sh.
EOF
  exit 0
fi

if [[ "${1:-}" != "--yes" ]]; then
  echo "This will destroy all standalone Refugee Registry volumes and re-seed from scratch." >&2
  echo "Re-run with --yes to confirm." >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

docker compose --profile bootstrap down -v
exec ./scripts/up.sh
