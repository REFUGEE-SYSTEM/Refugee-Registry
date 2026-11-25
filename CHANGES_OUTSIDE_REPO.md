# Changes Outside `refugee-registry` Repo

All changes outside `$WS/refugee-registry` for the isolated refugee services:

1. **`openg2p-developer/compose/docker-compose.refugee-services.yml`** (new file):
   - Dedicated refugee-only containers: `refugee-postgres` (`5435`), `refugee-redis` (`6381`), `refugee-keycloak` (`8180`, realm `refugee`), `refugee-iam-staff-api` (`8120`), `refugee-awe` (`8130`), `refugee-id-generator` (`8140`).
2. **`openg2p-developer/config/id-generator/refugee.yaml`** (new file):
   - Dedicated ID generator pool config (`household: id_length 10`, `refugee: id_length 12`).
3. **`openg2p-developer/generated/refugee-registry/iam-data/login_providers.json`** & **`isolated/{iam-staff-portal-api.env,awe-api.env,awe-config.yaml}`** (new files):
   - Isolated IAM login provider (`http://refugee-keycloak:8080/realms/refugee`), AWE config, and IAM API env.
4. **`openg2p-developer/scripts/init-refugee-keycloak.py`** & **`scripts/init-refugee-iam.py`** (new files):
   - Provisions `refugee` realm, scoped clients (`iam-staff-portal`, `refugee-registry-staff-portal`, `awe-admin-resolver`), 11 refugee roles, and users (`staff`, `alex.carter`, `nina.patel`) with `fullScopeAllowed=false`.
   - `init-refugee-iam.py` idempotently syncs `staff_portal_applications` (`refugee-registry-staff-portal`, `1` row), `staff_application_permissions` (`72` rows), `staff_roles` (`11` rows), `staff_role_permissions` (`165` rows), and `login_providers.issuer` (`http://localhost:8180/realms/refugee`) into `refugee-postgres/iam_staff`.
5. **`openg2p-developer/generated/refugee-registry/shared-backup/`** (new backup) & **`generated/refugee-registry/docker/*.env`** (edited):
   - Pointed refugee stack env files to `refugee-keycloak`, `refugee-iam-staff-api`, `refugee-awe`, `refugee-id-generator`, and `refugee-redis`.
6. **`openg2p-developer/compose/docker-compose.refugee.yml`** (edited):
   - Switched `depends_on` and inline env overrides to `refugee-redis`, `refugee-keycloak`, `refugee-iam-staff-api`, `refugee-awe`, and `refugee-postgres` (for `AWE_PGHOST`).
7. **`openg2p-data/packs/ETH/domains/refugee/`** (32 codelists on branch `uganda-attributes`):
   - Uganda mandatory refugee codelists (no shared `ETH/codelists/` files modified).
