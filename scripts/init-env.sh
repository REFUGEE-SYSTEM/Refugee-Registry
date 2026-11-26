#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage: ./scripts/init-env.sh [--force]

Creates .env from .env.example (with generated random secrets) and renders
docker/generated/iam-data/login_providers.json for iam-staff-api.
  --force   Overwrite an existing .env file.
EOF
  exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

FORCE=false
if [[ "${1:-}" == "--force" ]]; then
  FORCE=true
fi

gen_secret() {
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -hex 24
  else
    python3 -c "import secrets; print(secrets.token_hex(24))"
  fi
}

if [[ ! -f .env || "$FORCE" == "true" ]]; then
  cp .env.example .env
  python3 - <<'PY'
import secrets
import uuid
from pathlib import Path

env_path = Path(".env")
lines = []
for line in env_path.read_text(encoding="utf-8").splitlines():
    if "=CHANGE_ME_UUID" in line:
        key = line.split("=", 1)[0]
        lines.append(f"{key}={uuid.uuid4()}")
    elif "=CHANGE_ME" in line:
        key = line.split("=", 1)[0]
        if key == "REFUGEE_DEMO_USER_PASSWORD":
            val = secrets.token_urlsafe(12)
        else:
            val = secrets.token_hex(24)
        lines.append(f"{key}={val}")
    else:
        lines.append(line)
env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
  echo "[init-env] Generated .env with random secrets."
else
  echo "[init-env] .env already exists (pass --force to regenerate)."
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

mkdir -p docker/generated/iam-data
cat > docker/generated/iam-data/login_providers.json <<EOF
[
  {
    "id": 1,
    "provider_name": "Keycloak Refugee",
    "description": "Standalone Refugee Keycloak realm",
    "client_id": "iam-staff-portal",
    "client_secret": "${KEYCLOAK_IAM_CLIENT_SECRET}",
    "token_endpoint_auth_method": "client_secret_post",
    "server_metadata_url": "http://keycloak:8080/realms/${REFUGEE_KEYCLOAK_REALM:-refugee}/.well-known/openid-configuration",
    "authorization_endpoint": "http://localhost:${REFUGEE_KEYCLOAK_PORT:-8280}/realms/${REFUGEE_KEYCLOAK_REALM:-refugee}/protocol/openid-connect/auth",
    "issuer": "http://localhost:${REFUGEE_KEYCLOAK_PORT:-8280}/realms/${REFUGEE_KEYCLOAK_REALM:-refugee}",
    "oauth_callback_url": "http://localhost:${REFUGEE_IAM_PORT:-8220}/auth/callback",
    "default_redirect_uri": "http://localhost:${REFUGEE_UI_PORT:-3150}/",
    "scope": "openid profile email",
    "enable_pkce": true,
    "active": true,
    "audiences": "[]",
    "adapter_name": "keycloak"
  }
]
EOF
echo "[init-env] Rendered docker/generated/iam-data/login_providers.json."
