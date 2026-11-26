#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage: ./scripts/status.sh

Displays container status and key HTTP endpoints for the standalone stack.
EOF
  exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

docker compose ps
echo ""
echo "Endpoints:"
echo "  Staff UI:      http://localhost:${REFUGEE_UI_PORT:-3150}/en"
echo "  Staff API:     http://localhost:${REFUGEE_STAFF_API_PORT:-8271}/ping"
echo "  Master Data:   http://localhost:${REFUGEE_MDS_API_PORT:-8249}/ping"
echo "  IAM API:       http://localhost:${REFUGEE_IAM_PORT:-8220}/ping"
echo "  AWE API:       http://localhost:${REFUGEE_AWE_PORT:-8230}/v1/awe/health"
echo "  ID Generator:  http://localhost:${REFUGEE_IDGEN_PORT:-8240}/v1/idgenerator/health"
echo "  Keycloak:      http://localhost:${REFUGEE_KEYCLOAK_PORT:-8280}/realms/${REFUGEE_KEYCLOAK_REALM:-refugee}/.well-known/openid-configuration"
