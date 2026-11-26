# Migration & Packaging Plan (`REFUGEE-PROJECT`)

This standalone project was created by copying (never moving or modifying) the Refugee Registry artifacts from the OpenG2P workspace and local developer harness.

## Source -> Target Mapping

| Source Path | Target Path | Notes |
|---|---|---|
| `$WS/refugee-registry` (git clone, branch `refugee-isolated-services`) | `$TARGET/` (branch `main`, remote removed) | Preserves full commit history (`ad8ccd3`..`51783f9`); `__pycache__`/`*.pyc` cleaned |
| `$WS/openg2p-data/packs/ETH/domains/refugee/*.json` (32 files) | `$TARGET/data/codelists/refugee/` | Uganda mandatory + illustrative codelists |
| `$ROOT/refugee_codelists/convert_codelists.py` | `$TARGET/data/source/convert_codelists.py` | Reference codelist converter script |
| `$WS/registry-platform/reference-extension/LICENSE` | `$TARGET/LICENSE` | Mozilla Public License 2.0 (MPL-2.0) |
| `$ROOT/openg2p-developer/compose/docker-compose.refugee.yml` | `$TARGET/deploy/local/docker-compose.refugee.yml` | Made portable (`${REFUGEE_ENV_DIR:-./env}`, no hardcoded secrets) |
| `$ROOT/openg2p-developer/compose/docker-compose.refugee-services.yml` | `$TARGET/deploy/local/docker-compose.refugee-services.yml` | Isolated Keycloak/IAM/AWE/ID-gen/Postgres/Redis |
| `$ROOT/openg2p-developer/config/id-generator/refugee.yaml` | `$TARGET/deploy/local/id-generator.refugee.yaml` | Isolated ID-generator config (`household: 10`, `refugee: 12`) |
| `$ROOT/openg2p-developer/config/id-generator/default.yaml` (refugee lines) | `$TARGET/deploy/local/id-generator.refugee.snippet.yaml` | Snippet only (shared file not copied) |
| `$ROOT/openg2p-developer/.env` (`MASTER_DATA_PACK_DOMAINS`) | `$TARGET/deploy/local/developer-env.snippet` | Snippet only |
| `$ROOT/openg2p-developer/generated/refugee-registry/docker/*.env` | `$TARGET/deploy/local/env/*.env.example` | Secrets/passwords replaced with `CHANGE_ME` |
| `$ROOT/openg2p-developer/generated/refugee-registry/isolated/*.env` | `$TARGET/deploy/local/env/isolated-*.env.example` | Secrets/passwords replaced with `CHANGE_ME` |
| `$ROOT/openg2p-developer/generated/refugee-registry/isolated/awe-config.yaml` | `$TARGET/deploy/local/awe-config.yaml.example` | `admin_client_secret` replaced with `CHANGE_ME` |
| `$ROOT/openg2p-developer/generated/refugee-registry/iam-data/login_providers.json` | `$TARGET/deploy/local/iam-data/login_providers.json.example` | `client_secret` replaced with `CHANGE_ME` |
| `$ROOT/openg2p-developer/scripts/init-refugee-keycloak.py` & `init-refugee-iam.py` | `$TARGET/scripts/` | Parameterized via env vars (`CHANGE_ME` defaults, no hardcoded secrets) |

## Intentionally Excluded
- `generated/refugee-registry/*.env`, `generated/refugee-registry/shared-backup/*.env`, and `.env` files with live credentials/secrets.
- `venv/`, `node_modules/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`, Docker volumes, logs, DB dumps, and other registries (`farmer-registry`, `livestock-registry`, `cropsown-registry`, `registry-platform`).
- `PRIMES_BIMS_refugee_attributes.xlsx` and `refugee_registry_demo_codelists_1.xlsx` (not present under `$HOME/work/OPENG2P`).
