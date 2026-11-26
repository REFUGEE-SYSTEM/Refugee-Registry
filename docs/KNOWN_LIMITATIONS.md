# Refugee Registry — Known Limitations (Standalone Uganda Demo Build)

1. **Standalone Local Stack**: Refugee Registry runs its own self-contained Docker Compose project (`refugee-registry`) with PostgreSQL (`5535`), Redis (`6481`), MinIO (`9100`/`9101`), Keycloak (`8280`, realm `refugee`), IAM Staff Portal API (`8220`), AWE (`8230`), ID Generator (`8240`), Master Data API (`8249`), Refugee Staff API (`8271`), Celery Worker & Beat, and Staff UI (`3150`).
2. **Individual-Only Scope**: The `Household` register and household-level attributes (including household settlement/location fields `host_district`, `settlement_location`, `zone_cluster`, `village_block`) have been removed; only the individual `Refugee` register and its sub-registers are active.
3. **Uganda Code Lists vs. Illustrative Lists**: Lists in `data/codelists/refugee/` are illustrative Uganda-context demo lists and not official UNHCR/OPM reference exports.
4. **Biometrics Out of Scope**: Mandatory biometric attributes `C01`, `C02`, and `C05` are out of scope (`TODO` in `register_domain/models/refugee.py`); a standard photo upload (`record_image_document_id`) is provided in **Personal Identity**.
5. **Security Screening (`E07`) Read-Only & Plain Consent (`P01`/`P02`)**: `security_screening_status` is read-only; `informed_consent_given`/`partner_data_sharing_consent` are stored on `G2PRefugee` without Consent Manager / `data_scopes.json`.
6. **Fictional Demo Data**: All 25 refugees (`RF-DEMO-0001..0025`) are fictional Uganda-context records.
