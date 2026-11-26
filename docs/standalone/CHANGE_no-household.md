# Phase 0 Inventory & Decision Table: Remove Household & Add Refugee Photo

## 1. Repository Inventory of `household` References

| Area | File(s) | Classification / Action |
|---|---|---|
| Register constants | `refugee-extension/src/openg2p_registry_refugee_extension/register_domain/constants.py` | Remove `"Household": "a0000000-...0001"` from `REGISTER_IDS` and docstring |
| ORM Models | `register_domain/models/household.py`, `models/__init__.py`, `models/refugee.py`, `models/enums.py` | Delete `models/household.py`; remove `Household` exports from `models/__init__.py`; remove `relationship_to_group` from `models/refugee.py`; remove `RelationshipToGroupEnum` and household-only enums (`IncomeSourceEnum`, `DeliveryModalityEnum`, `DeliveryMechanismEnum`, `PaymentStatusEnum`) from `models/enums.py` |
| Pydantic Schemas | `register_domain/schemas/household.py`, `schemas/__init__.py`, `schemas/refugee.py` | Delete `schemas/household.py`; remove `Household` exports from `schemas/__init__.py`; remove `relationship_to_group` from `schemas/refugee.py` |
| Domain Services | `register_domain/services/g2p_register_domain_service_household.py`, `services/__init__.py`, `services/g2p_register_domain_service_refugee.py` | Delete `g2p_register_domain_service_household.py`; remove `Household` export from `services/__init__.py`; remove `relationship_to_group` from `_enum_fields()` and `construct_search_text()` in `g2p_register_domain_service_refugee.py` |
| ID Generator | `register_domain/id_generator/g2p_id_generator_service.py` | Remove `if mnemonic == "household": return IdAffix(prefix="HH-", suffix="")` |
| App Initializer | `refugee-extension/src/openg2p_registry_refugee_extension/app.py` | Remove `G2PRegisterHousehold`, `G2PRegisterHistoryHousehold`, `G2PIntakeFormHousehold`, `G2PRegisterDomainServiceHousehold` imports, service init, and migration tuple entries |
| Ingestion Enrichers | `ingestion_pipeline/enricher_services/g2p_household_enricher_services.py`, `enricher_services/__init__.py` | Delete `g2p_household_enricher_services.py`; remove its imports from `enricher_services/__init__.py` |
| Score Compute | `score_compute/services/poverty.py` | Update docstring/log message to reference `record` instead of `household` (keep generic `G2PScoreComputeServicePoverty` class) |
| Register Metadata SQL | `meta_data/register-metadata/g2p_register_definitions.sql`, `g2p_register_schemas.sql`, `g2p_register_sections.sql`, `g2p_register_ui_tabs.sql`, `g2p_register_ui_tab_sections.sql`, `g2p_intake_form_definitions.sql`, `g2p_intake_form_ui_tabs.sql`, `g2p_intake_form_ui_tab_sections.sql` | Remove all `a0000000-...0001` (Household), `c0000000-...0001`, `d0000000-...0001`, `e0000000-...0001..0019` rows; remove `refugee_household_link_tab`, `refugee_household_lookup_section_01`, `refugee_household_rel_section_01`; move `presence_status` into `refugee_lifecycle_section_01`; add photo widget to `refugee_personal_info_section_01`; reorder Refugee detail tabs and intake sections so Personal Identity is first |
| AWE Policies | `awe_meta_data/10_approval_policy.sql`, `meta_data/awe-integration/g2p_registry_awe_policy_configurations.sql` | Remove `registry.change_request.household` and `registry.intake_form.household` rows |
| Language / Translations | `translation/domain.json`, `meta_data/registry-configurations/g2p_registry_languages.sql`, `registry_languages.sql` | Remove household-only translation keys; rename `functional_record_id` label from `"Household / Case Number"` to `"Individual Registration No."`; add `"photo": "Photo"` |
| IAM & Bootstrap | `docker/bootstrap/bootstrap.py`, `docker/bootstrap/iam_registration_payload.json` | Remove `household` ID pool check in `wait_idgen_pools()` in `bootstrap.py` (IAM payload already has 0 household hits) |
| ID Pool Config | `docker/config/id-generator.yaml` | Remove `household: id_length: 10` under `id_types` |
| Codelists | `data/codelists/refugee/*.json`, `scripts/convert_uganda_codelists.py` | Delete 12 household-only codelists (`assistance_category`, `delivery_mechanism`, `delivery_modality`, `entry_point`, `food_distribution_point`, `host_district`, `income_source`, `payment_status`, `registration_site`, `settlement_location`, `village_block`, `zone_cluster`) + `refugee_relationship_to_group.json` (13 total removed, 23 retained) |
| Demo Data Loader | `docker/db-seed/load_sample_data.py` | Remove `HOUSEHOLDS` and `g2p_register_households` seeding; seed 25 `REFUGEES` (no `link_internal_record_id` or `relationship_to_group`), 18 `IdentityDocument` rows, and 6 `SpecificNeeds` rows |
| Tests & Smoke Script | `refugee-extension/tests/test_metadata_consistency.py`, `scripts/smoke-test.sh` | Update unit tests (remove household enum/idgen/model checks, assert no Household in `REGISTER_IDS`); update `smoke-test.sh` (drop household IDGen/count checks, assert `Household` absent from `g2p_register_definitions` and `refugee` ID pool allocates 12-digit IDs) |
| Docs | `README.md`, `docs/DATA_MODEL.md`, `docs/DEMO_SCRIPT.md`, `docs/KNOWN_LIMITATIONS.md` | Update in Phase 5 |

*(Note: `docker/mds-seed/load_geo_pack.py` and `docker/mds-seed/migrations/002_codelists.sql` are upstream platform MDS seed scripts for generic country packs and are left untouched unless needed; we will verify final grep scope.)*

---

## 2. Refugee Register Decision Table (Household-Related Elements)

| Field / Section / Tab | Type | Decision | Destination / Notes |
|---|---|---|---|
| `refugee_household_link_tab` | UI Tab | **DELETE** | Removed from `g2p_register_ui_tabs.sql` and `g2p_register_ui_tab_sections.sql` |
| `refugee_household_lookup_section_01` (`link_internal_record_id` lookup) | Section & Widget | **DELETE** | Removed from `g2p_register_sections.sql`, `g2p_register_ui_tab_sections.sql`, `g2p_intake_form_ui_tab_sections.sql` (base column `link_internal_record_id` remains unused on `G2PRegister`) |
| `refugee_household_rel_section_01` ("Household Relationship & Presence") | Section | **DELETE** | Removed from `g2p_register_sections.sql`, `g2p_register_ui_tab_sections.sql`, `g2p_intake_form_ui_tab_sections.sql` |
| `relationship_to_group` (F02) & `REFUGEE_RELATIONSHIP_TO_GROUP` | Field, Enum, Codelist | **DELETE** | Removed from `models/refugee.py`, `schemas/refugee.py`, `models/enums.py`, `g2p_register_domain_service_refugee.py`, `load_sample_data.py`, and `data/codelists/refugee/refugee_relationship_to_group.json` |
| `presence_status` (F07) & `PRESENCE_STATUS` | Field, Enum, Codelist | **KEEP** | Moved to `refugee_lifecycle_section_01` (tab `refugee_lifecycle_tab`, "Record Lifecycle"), alongside `lifecycle_status` |

### Geography / Location Note
- `G2PRegisterRefugee` inherits `G2PGeo` (`geo_lowest_level_value_id`, `geo_code_hierarchy_json`, `country_code`) and has the hidden `Address` sub-register (`a0000000-0000-0000-0000-000000000007`), neither of which is exposed on the active Uganda Refugee UI tabs.
- The Uganda settlement/location fields (`host_district`, `settlement_location`, `zone_cluster`, `village_block`) existed only on `G2PHousehold`. Per the decision rule, no new location fields are invented on `Refugee`.

---

## 3. Schema Creation & Existing Database Behaviour

- **Table creation (`app.py`)**: `Initializer.migrate_database()` runs `await model.create_migrate()` (SQLAlchemy `create_all`, which creates missing tables only) followed by `await add_missing_columns(model)` (`ALTER TABLE ... ADD COLUMN IF NOT EXISTS ...`). It never drops removed tables (`g2p_register_households`, `g2p_register_history_households`, `g2p_intake_form_households`) or removed columns (`relationship_to_group`).
- **Metadata SQL**: All metadata SQL files use `INSERT ... ON CONFLICT (...) DO UPDATE` or `DO NOTHING`. Removing `Household` rows from seed SQL does **not** delete existing `Household` rows from `g2p_register_definitions`, `g2p_register_schemas`, `g2p_register_sections`, `g2p_register_ui_tabs`, `g2p_register_ui_tab_sections`, `g2p_intake_form_*`, `approval_policy`, or `g2p_registry_awe_policy_configurations` in an already-initialized database.
- Therefore, existing databases must follow the reset upgrade procedure documented in `docs/standalone/UPGRADE_remove-household.md`.
