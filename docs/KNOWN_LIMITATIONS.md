# Refugee Registry — Known Limitations (Isolated Uganda Demo Build)

1. **Isolated Identity & Workflow Services**: Refugee Registry runs its own dedicated `refugee-postgres` (`5435`), `refugee-redis` (`6381`), `refugee-keycloak` (`8180`, realm `refugee`), `refugee-iam-staff-api` (`8120`), `refugee-awe` (`8130`), and `refugee-id-generator` (`8140`).
2. **Remaining Shared Infra**: `refugee_registry_db` and `refugee_master_data_db` remain separate databases inside `openg2p-postgres` (`5433`), and `openg2p-minio` (`9000`) is shared for object storage buckets.
3. **Uganda Code Lists vs. Illustrative Lists**: Lists on the `Code Lists` sheet match `Uganda_Refugee_Data_Attributes.xlsx`; settlement/site/programme lists are illustrative Uganda-context demo lists.
4. **Biometrics Out of Scope**: Mandatory biometric attributes `C01`, `C02`, and `C05` are out of scope (`TODO` in `register_domain/models/refugee.py`).
5. **Security Screening (`E07`) Read-Only & Plain Consent (`P01`/`P02`)**: `security_screening_status` is read-only; `informed_consent_given`/`partner_data_sharing_consent` are stored on `G2PRefugee` without Consent Manager / `data_scopes.json`.
6. **Fictional Demo Data**: All 8 households (`HH-DEMO-0001..0008`) and 25 refugees (`RF-DEMO-0001..0025`) are fictional Uganda-context records.
