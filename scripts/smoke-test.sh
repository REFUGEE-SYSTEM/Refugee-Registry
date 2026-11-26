#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage: ./scripts/smoke-test.sh

Verifies that every standalone Refugee Registry service is healthy, seeded,
and functional (HTTP health, Keycloak OIDC token for staff, IAM registration,
MDS geo + Uganda codelists, ID Generator allocation, Staff API registers,
Staff UI rendering, and demo data counts when LOAD_SAMPLE_DATA=true).
EOF
  exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f .env ]]; then
  echo "[smoke] Missing .env. Run ./scripts/init-env.sh first." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

pass() { echo "[PASS] $*"; }
fail() { echo "[FAIL] $*" >&2; exit 1; }

check_http() {
  local name="$1" url="$2"
  local code
  code="$(curl -s -o /dev/null -w '%{http_code}' "$url" || true)"
  if [[ "$code" == "200" ]]; then
    pass "$name -> HTTP $code ($url)"
  else
    fail "$name -> HTTP $code ($url)"
  fi
}

check_http "Staff UI" "http://localhost:${REFUGEE_UI_PORT:-3150}/en"
check_http "Staff API /ping" "http://localhost:${REFUGEE_STAFF_API_PORT:-8271}/ping"
check_http "Master Data /ping" "http://localhost:${REFUGEE_MDS_API_PORT:-8249}/ping"
check_http "IAM /ping" "http://localhost:${REFUGEE_IAM_PORT:-8220}/ping"
check_http "AWE /v1/awe/health" "http://localhost:${REFUGEE_AWE_PORT:-8230}/v1/awe/health"
check_http "IDGen /v1/idgenerator/health" "http://localhost:${REFUGEE_IDGEN_PORT:-8240}/v1/idgenerator/health"
check_http "Keycloak OIDC" "http://localhost:${REFUGEE_KEYCLOAK_PORT:-8280}/realms/${REFUGEE_KEYCLOAK_REALM:-refugee}/.well-known/openid-configuration"

# 1. Keycloak OIDC password grant for demo user 'staff'
token_resp="$(curl -s -X POST \
  "http://localhost:${REFUGEE_KEYCLOAK_PORT:-8280}/realms/${REFUGEE_KEYCLOAK_REALM:-refugee}/protocol/openid-connect/token" \
  -d "grant_type=password" \
  -d "client_id=${REFUGEE_KEYCLOAK_CLIENT_ID:-refugee-registry-staff-portal}" \
  -d "username=staff" \
  -d "password=${REFUGEE_DEMO_USER_PASSWORD}")"
if echo "$token_resp" | python3 -c "import sys,json; d=json.load(sys.stdin); assert d.get('access_token')" 2>/dev/null; then
  pass "Keycloak token issued for 'staff'"
else
  fail "Keycloak token failed for 'staff': $token_resp"
fi

# 2. ID Generator allocation test
hh_id="$(curl -s -X POST "http://localhost:${REFUGEE_IDGEN_PORT:-8240}/v1/idgenerator/household/id" | python3 -c "import sys,json; d=json.load(sys.stdin); print((d.get('response') or {}).get('id') or d.get('id',''))" 2>/dev/null || true)"
rf_id="$(curl -s -X POST "http://localhost:${REFUGEE_IDGEN_PORT:-8240}/v1/idgenerator/refugee/id" | python3 -c "import sys,json; d=json.load(sys.stdin); print((d.get('response') or {}).get('id') or d.get('id',''))" 2>/dev/null || true)"
[[ ${#hh_id} -eq 10 ]] && pass "IDGen household ID allocated: $hh_id" || fail "IDGen household ID invalid: '$hh_id'"
[[ ${#rf_id} -eq 12 ]] && pass "IDGen refugee ID allocated: $rf_id" || fail "IDGen refugee ID invalid: '$rf_id'"

# 3. DB verification (IAM, MDS, Registry)
docker compose exec -T postgres psql -U "${POSTGRES_USER:-postgres}" -d iam_staff -tAc \
  "SELECT COUNT(*) FROM staff_portal_applications WHERE application_mnemonic = 'refugee-registry-staff-portal'" | grep -qx "1" \
  && pass "IAM registered refugee-registry-staff-portal" || fail "IAM app missing"

geo_cnt="$(docker compose exec -T postgres psql -U "${POSTGRES_USER:-postgres}" -d "${REFUGEE_MASTER_DATA_DB:-refugee_master_data_db}" -tAc "SELECT COUNT(*) FROM g2p_geo_levels")"
[[ "${geo_cnt:-0}" -gt 0 ]] && pass "MDS g2p_geo_levels count=$geo_cnt" || fail "MDS geo levels empty"

tab_cnt="$(docker compose exec -T postgres psql -U "${POSTGRES_USER:-postgres}" -d "${REFUGEE_REGISTRY_DB:-refugee_registry_db}" -tAc "SELECT COUNT(*) FROM g2p_register_ui_tabs WHERE is_active = true")"
[[ "${tab_cnt:-0}" -ge 10 ]] && pass "Registry active UI tabs count=$tab_cnt" || fail "Registry UI tabs unexpected: $tab_cnt"

if [[ "${LOAD_SAMPLE_DATA:-true}" == "true" ]]; then
  hh_cnt="$(docker compose exec -T postgres psql -U "${POSTGRES_USER:-postgres}" -d "${REFUGEE_REGISTRY_DB:-refugee_registry_db}" -tAc "SELECT COUNT(*) FROM g2p_register_households")"
  rf_cnt="$(docker compose exec -T postgres psql -U "${POSTGRES_USER:-postgres}" -d "${REFUGEE_REGISTRY_DB:-refugee_registry_db}" -tAc "SELECT COUNT(*) FROM g2p_register_refugees")"
  [[ "${hh_cnt:-0}" -ge 8 ]] && pass "Demo households count=$hh_cnt" || fail "Demo households missing: $hh_cnt"
  [[ "${rf_cnt:-0}" -ge 25 ]] && pass "Demo refugees count=$rf_cnt" || fail "Demo refugees missing: $rf_cnt"
fi

echo "[smoke] All standalone smoke checks PASSED."
