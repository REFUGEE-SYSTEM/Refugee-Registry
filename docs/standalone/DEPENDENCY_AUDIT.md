# Standalone Dependency Audit

Generated during Phase 1 of standalone packaging for `Refugee-Registry`.

## 1. Container Images & Registry Pullability

All images below were verified with `docker manifest inspect` (no `:latest` tags; immutable digests or pinned tags only):

| Service | Pinned Image | Status | Notes |
| --- | --- | --- | --- |
| Postgres | `postgres:16` | PUBLISHED | Standard official image |
| Redis | `redis:7-alpine` | PUBLISHED | Standard official image |
| MinIO | `cgr.dev/chainguard/minio@sha256:2136d593beacf4461187035eca949fe49abd589d5079735025c711ca58fee0c8` | PUBLISHED | Digest-pinned (`minio/minio` dated tags returned `NOT_FOUND` on Docker Hub) |
| MinIO Client | `cgr.dev/chainguard/minio-client@sha256:d8a93c5d335509ff353774eefec8f82fa2a2a975e800139702232d8be3dbe6b9` | PUBLISHED | Digest-pinned |
| Keycloak | `quay.io/keycloak/keycloak:26.0` | PUBLISHED | `linux/amd64` |
| IAM Staff API | `openg2p/iam-staff-portal-api:1.3.0` | PUBLISHED | |
| AWE | `openg2p/openg2p-awe:develop` | PUBLISHED | |
| ID Generator | `openg2p/openg2p-id-generator:1.0.0` | PUBLISHED | `linux/amd64` |
| Master Data API | `openg2p/master-data-api:develop` | PUBLISHED | |
| Staff API (base) | `openg2p/openg2p-registry-staff-api:0.0.0-develop.716` | PUBLISHED | Extended by `./docker/staff-api/Dockerfile` |
| Celery (base) | `openg2p/openg2p-registry-celery:0.0.0-develop.716` | PUBLISHED | Extended by `./docker/celery/Dockerfile` |
| DB Seed (base) | `openg2p/openg2p-registry-db-seed:0.0.0-develop.716` | PUBLISHED | Extended by `./docker/db-seed/Dockerfile` |
| Staff UI | `openg2p/openg2p-registry-staff-ui:0.0.0-develop.716` | PUBLISHED | Replaces local-only `openg2p/openg2p-farmer-custom-staff-ui:0.0.0-develop.716` |

## 2. External Workspace References Found in Repo

References to `openg2p-developer` / `openg2p-workspace` currently in `Refugee-Registry`:
- `README.md`, `LOCAL_WIRING_PLAN.md`, `CHANGES_OUTSIDE_REPO.md`, `docs/MOVE_PLAN.md`: developer-stack documentation.
- `deploy/local/*`, `scripts/install-into-developer-stack.sh`, `scripts/start.sh`, `scripts/stop.sh`, `.env.example`: developer-stack compose/wiring helpers (kept or superseded by root standalone `docker-compose.yml` + `scripts/up.sh`).
- `scripts/init-refugee-iam.py`: previously synced `iam_staff` from shared `openg2p-postgres:5433`. Replaced for standalone mode by self-contained IAM application/role/permission registration (`docker/bootstrap/iam_registration_payload.json` + `docker/bootstrap/init_iam.py`).
- `refugee-extension/tests/test_metadata_consistency.py`: had an optional fallback path to `OPENG2P/openg2p-workspace/openg2p-data/packs/ETH`. Updated so standalone tests run without any external workspace path.

## 3. External Data Dependencies & Self-Contained Strategy

- **ETH Country Pack (`openg2p-data` `packs/ETH`)**:
  - Source repo: `https://github.com/OpenG2P/openg2p-data.git`
  - Pinned commit SHA: `122275845b38729e508480539cf35dd67b4c804e`
  - Strategy: A dedicated `mds-seed` bootstrap image (`docker/mds-seed/Dockerfile`) performs a shallow sparse checkout of `packs/ETH` at pinned SHA `122275845b38729e508480539cf35dd67b4c804e`, overlays `./data/codelists/refugee/`, and runs `load_geo_pack.py` (extracted/ported cleanly) into `refugee_master_data_db`. Nothing from `openg2p-data` is vendored into git.
- **Refugee Codelists (12 Uganda JSONs)**:
  - Already committed in-repo under `data/codelists/refugee/`.
- **IAM RBAC Catalog (11 roles, 72 permissions)**:
  - Self-contained in `docker/bootstrap/iam_registration_payload.json` (no secrets), registered via `iam_staff_portal_api` `UserAccessController.register_staff_portal_application` during bootstrap.
- **Keycloak Realm (`refugee`), Clients, Roles, Demo Users**:
  - Self-contained in `docker/bootstrap/init_keycloak.py` (reads generated secrets from `.env`).
- **AWE Callback Secret**:
  - Self-contained SQL/Python seed in `docker/bootstrap/init_awe.py` (reads `AWE_CALLBACK_SECRET_ID` and `AWE_CALLBACK_HMAC_SECRET` from `.env`).
- **ID Generator Pools (`household: 10`, `refugee: 12`)**:
  - Configured in `docker/config/id-generator.yaml` and verified/warmed by `docker/bootstrap/wait_idgen.py` before `db-seed` / `staff-api` use.

## 4. Non-Colliding Default Host Ports

Chosen so the standalone stack does not collide with `openg2p-developer` (`3000-3050`, `5432-5435`, `6379-6381`, `8020-8180`, `9000-9011`) or `mds-standalone`:

- `REFUGEE_UI_PORT=3150`
- `REFUGEE_STAFF_API_PORT=8271`
- `REFUGEE_MDS_API_PORT=8249`
- `REFUGEE_POSTGRES_PORT=5535`
- `REFUGEE_REDIS_PORT=6481`
- `REFUGEE_KEYCLOAK_PORT=8280`
- `REFUGEE_IAM_PORT=8220`
- `REFUGEE_AWE_PORT=8230`
- `REFUGEE_IDGEN_PORT=8240`
- `REFUGEE_MINIO_PORT=9100`
- `REFUGEE_MINIO_CONSOLE_PORT=9101`
