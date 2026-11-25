# Refugee Registry — Known Limitations (Local Demo)

1. **Illustrative Codelists**: The 12 codelists under `openg2p-data/packs/ETH/domains/refugee/` are illustrative demo lists, not official UNHCR proGres v4 reference tables.
2. **Biometrics Deferred**: Fingerprints, iris, face templates, and BIMS duplicate/history flags are not implemented (`TODO` in `register_domain/models/refugee.py`).
3. **Consent Field is Informational Only**: `Household.consent_or_prohibition_to_share_information` is stored as a plain boolean ("Consent recorded (information only)"). Platform `data_scopes.json` and Consent Manager enforcement are not configured.
4. **No Production Deployment Artifacts**: Helm charts, CI pipelines, published container images, reporting views/Superset dashboards, and Beneficiary Portal are not included.
5. **Fictional Demo Data**: All 8 households (`HH-DEMO-0001..0008`) and 25 refugees (`RF-DEMO-0001..0025`) are fictional, placed at real Ethiopia woreda/geo units from Master Data.
6. **Shared `openg2p-id-generator` Pool Reload**: `refugee: id_length: 12` was added to `openg2p-developer/config/id-generator/default.yaml`, but the shared `openg2p-id-generator` container was not restarted (per safety rules), so `id_pool_refugee` does not exist yet until `docker restart openg2p-id-generator` is run.
7. **UI Image Reuse**: `refugee-registry-staff-ui` reuses the pre-built `openg2p-farmer-custom-staff-ui:0.0.0-develop.716` Next.js image configured at runtime via environment variables (`APPLICATION_MNEMONIC=refugee-registry-staff-portal`, `BACKEND_API_URL`, `MASTERDATA_BACKEND_API_URL`), with all domain labels served from `registry_languages.domain_translation`.
