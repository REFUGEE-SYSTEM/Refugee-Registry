# Upgrade Guide: Removing the Household Register

This guide applies to **existing** Refugee Registry databases created before the Household register was removed (`feature/no-household-photo`).

## Why a Reset Is Required

1. **Seed SQL uses upserts (`ON CONFLICT DO UPDATE` / `DO NOTHING`)**: removing `Household` rows from `g2p_register_definitions.sql`, `g2p_register_ui_tabs.sql`, `g2p_register_sections.sql`, `g2p_intake_form_*.sql`, `10_approval_policy.sql`, and `g2p_registry_awe_policy_configurations.sql` does **not** delete existing `Household` rows from an already-seeded database.
2. **ORM migrations are additive (`create_migrate()` + `add_missing_columns()`)**: removing `G2PRegisterHousehold` and `relationship_to_group` from Python models does **not** drop `g2p_register_households`, `g2p_register_history_households`, `g2p_intake_form_households`, or the `relationship_to_group` column on `g2p_register_refugees`.
3. **ID Generator & Master Data**: the `household` ID pool and household-only codelists remain in the existing Postgres volumes until reset.

## Upgrade Steps (Destructive Reset)

```bash
# 1. Stop the running stack (never use `docker compose down -v` directly)
./scripts/down.sh

# 2. Reset ONLY this project's Docker volumes (asks for confirmation)
./scripts/reset.sh

# 3. Start and re-seed the stack
./scripts/up.sh

# 4. Verify
./scripts/smoke-test.sh
```

### What Is Kept vs. Deleted by `./scripts/reset.sh`

- **Kept**: `.env` (your secrets, ports, and `LOAD_SAMPLE_DATA` setting) and all source/config files in the repository.
- **Deleted**: ONLY this project's Docker volumes (`refugee_postgres_data`, `refugee_minio_data`, `refugee_redis_data`), which wipes all existing database records, uploaded MinIO objects, and Keycloak/IAM/AWE state so they are freshly seeded without `Household`.
