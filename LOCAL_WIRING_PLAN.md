# Local Wiring Plan — Refugee Registry

## 1. Allocated Ports, DBs, and Identifiers (Conflict-Free)
- **UI Port**: `3050` (verified free via `ss -tlnp`; Farmer Custom is `3040`)
- **Staff API Port**: `8071` (verified free; Farmer Custom is `8061`)
- **Master Data API Port**: `8049` (verified free; Farmer Custom is `8048`)
- **Databases** (in `openg2p-postgres`):
  - `refugee_registry_db` (with `pg_trgm`)
  - `refugee_master_data_db` (with `pg_trgm`)
- **Keycloak Client & IAM Application**: `refugee-registry-staff-portal` (`http://localhost:3050`)
- **Worker Queue & Redis DB**: `refugee_registry_worker_queue`, `redis://redis:6379/7`
- **AWE Callback Secret**: `00000000-0000-4000-8000-000000000005` (`caller_service = refugee`)

## 2. Files Created Inside `refugee-registry/`
- `.openg2p-extension.yaml` (extension manifest for `openg2p-developer`)
- `translation/domain.json` (English labels for every `widget-label` / `widget-data-add-label` / enum code)
- `refugee-extension/src/openg2p_registry_refugee_extension/awe_meta_data/`:
  - `10_approval_policy.sql`, `20_approval_stage.sql`, `30_approver_rule.sql`, `40_callback_secret.sql.tpl`
- `refugee-extension/src/openg2p_registry_refugee_extension/meta_data/`:
  - `awe-integration/g2p_registry_awe_policy_configurations.sql`
  - `registry-configurations/g2p_registry_configuration.sql`, `registry_themes.sql`, `registry_languages.sql` (embedding `translation/domain.json`), `g2p_input_mechanisms.sql`
- `docker/`:
  - `staff-api/Dockerfile` (extends `openg2p/openg2p-registry-staff-api:0.0.0-develop.716`)
  - `celery/Dockerfile` (extends `openg2p/openg2p-registry-celery:0.0.0-develop.716`)
  - `db-seed/Dockerfile` (extends `openg2p/openg2p-registry-db-seed:0.0.0-develop.716`)
  - `db-seed/entrypoint.sh` (AWE callback secret guard + delegates to `/seed/entrypoint.sh`)
  - `db-seed/load_sample_data.py` (idempotent demo data loader: 8 households, ~25 refugees, sub-register rows, MDS geo lookup)

## 3. Files Added/Updated Outside `refugee-registry/` (logged in `CHANGES_OUTSIDE_REPO.md`)
- `openg2p-developer/compose/docker-compose.refugee.yml` (NEW compose file for `refugee-master-data-api`, `refugee-registry-staff-api`, `refugee-registry-celery-worker`, `refugee-registry-celery-beat`, `refugee-registry-staff-ui`, `refugee-registry-db-seed`)
- `openg2p-developer/config/id-generator/default.yaml` (ADD `refugee: id_length: 12` under `id_types:`)
- `openg2p-developer/generated/refugee-registry/docker/*.env` (generated env files)
- `openg2p-postgres` (`refugee_registry_db`, `refugee_master_data_db`, IAM app `refugee-registry-staff-portal` in `iam_staff`, Keycloak client `refugee-registry-staff-portal`)

## 4. Build, Seed, and Start Commands
1. Create `refugee_registry_db` and `refugee_master_data_db` with `pg_trgm` in `openg2p-postgres`.
2. Seed `refugee_master_data_db` using `load_geo_pack.py --pack .../packs/ETH --db refugee_master_data_db --load geo,codelists --domains refugee`.
3. Provision Keycloak client `refugee-registry-staff-portal` and IAM `staff_portal_applications` / `staff_roles` / `staff_role_permissions`.
4. Build `openg2p-refugee-registry-{staff-api,celery,db-seed}:0.0.0-develop.716`.
5. Run `refugee-registry-db-seed` (`LOAD_SAMPLE_DATA=false` first, then run `load_sample_data.py` or `LOAD_SAMPLE_DATA=true`).
6. Start `refugee-master-data-api`, `refugee-registry-staff-api`, `refugee-registry-celery-worker`, `refugee-registry-celery-beat`, `refugee-registry-staff-ui` (reusing `openg2p-farmer-custom-staff-ui:0.0.0-develop.716` with refugee env).
