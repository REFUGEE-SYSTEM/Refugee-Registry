# Refugee Registry (OpenG2P Domain Extension)

A domain registry for refugee household and individual case management, built as an extension of the **OpenG2P Registry Platform** (`openg2p-registry-core`). It models the **55 non-biometric Mandatory attributes** of the Uganda Refugee Data Attributes specification across a category-per-tab Staff Portal UI.

---

## Registers & ID Prefixes

| Register | Purpose | Parent | Functional ID Prefix | Fixed UUID |
|---|---|---|---|---|
| `Household` | `REGISTER` | — | `HH-` (10-digit) | `a0000000-0000-0000-0000-000000000001` |
| `Refugee` | `REGISTER` | — | `RF-` (12-digit) | `a0000000-0000-0000-0000-000000000002` |
| `IdentityDocument` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000003` |
| `SpecificNeeds` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000005` |
| `DisplacementHistory` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000004` |
| `Relative` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000006` |
| `Address` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000007` |
| `EducationRecord` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000008` |
| `OccupationSkill` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000009` |

*(Only `Household`, `Refugee`, `IdentityDocument`, and `SpecificNeeds` are active in the UI; the remaining 5 legacy sub-registers are preserved in PostgreSQL and hidden from the UI.)*

---

## Architecture & Prerequisites

- **Pinned Platform Version (`RP_VERSION`)**: `0.0.0-develop.716` (configured in `docker/*/Dockerfile` and `.env.example`; override with `--build-arg RP_VERSION=<tag>` when rebuilding images).
- **Developer Stack Dependency**: Requires an OpenG2P developer stack (`openg2p-developer`) providing `infra` + `commons` services (PostgreSQL, MinIO, Docker network).
- **Isolated Refugee Services** (`deploy/local/docker-compose.refugee-services.yml`): Dedicated `refugee-postgres` (`5435`), `refugee-redis` (`6381`), `refugee-keycloak` (`8180`, realm `refugee`), `refugee-iam-staff-api` (`8120`), `refugee-awe` (`8130`), and `refugee-id-generator` (`8140`).

---

## Quick Start

1. **Copy configuration templates and set secrets** (replace every `CHANGE_ME` value):
   ```bash
   cp .env.example .env
   ```
2. **Install compose & env templates into `openg2p-developer`**:
   ```bash
   ./scripts/install-into-developer-stack.sh /path/to/openg2p-developer
   ```
   Copy the `*.example` files in `generated/refugee-registry/` to `*.env` / `*.yaml` / `*.json` with real local values.
3. **Build refugee images**:
   ```bash
   docker build -t openg2p-refugee-registry-staff-api:0.0.0-develop.716 -f docker/staff-api/Dockerfile .
   docker build -t openg2p-refugee-registry-celery:0.0.0-develop.716 -f docker/celery/Dockerfile .
   docker build -t openg2p-refugee-registry-db-seed:0.0.0-develop.716 -f docker/db-seed/Dockerfile .
   ```
4. **Start & seed**:
   ```bash
   export OPENG2P_DEVELOPER_DIR=/path/to/openg2p-developer
   ./scripts/start.sh
   # Provision Keycloak realm/clients/users and IAM roles/permissions:
   python3 scripts/init-refugee-keycloak.py
   python3 scripts/init-refugee-iam.py
   ```
   - Staff Portal UI: `http://localhost:3050/en`
   - Staff API OpenAPI: `http://localhost:8071/openapi.json`
   - Refugee Master Data API: `http://localhost:8049/openapi.json`
   - **Local demo only** users: `staff` (registrar), `alex.carter` (approver), `nina.patel` (registrar).

---

## Data Model & Codelists

- **Tab-by-Tab Data Model**: See [docs/DATA_MODEL.md](docs/DATA_MODEL.md) (8 Household category tabs; 10 Refugee category tabs).
- **Codelists**: 32 JSON codelists in [data/codelists/refugee/](data/codelists/refugee/). Regenerate via:
  ```bash
  python3 scripts/convert_uganda_codelists.py
  ```

---

## Tests

```bash
python3 -m compileall -q refugee-extension/src
PYTHONPATH=refugee-extension/src python3 -m unittest refugee-extension/tests/test_metadata_consistency.py -v
```

---

## Known Limitations & Roadmap

- See [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) for demo scope notes (biometrics `C01`/`C02`/`C05` out of scope, read-only security screening, plain consent fields, illustrative settlement/site lists).
- **Roadmap**: Helm chart packaging, GitHub Actions CI, automated sanity/E2E suite, biometric integration, Consent Manager / `data_scopes.json` enforcement, and Superset reporting views.

---

## Licence & Attribution

- Licensed under the **Mozilla Public License Version 2.0 (MPL-2.0)** — see [LICENSE](LICENSE).
- Built on the **OpenG2P Registry Platform**.
- Demo codelists under `data/codelists/refugee/` are illustrative and aligned to the Uganda demo model; they are **not** official UNHCR-approved reference tables.
