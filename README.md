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

- **Pinned Platform Version (`RP_VERSION`)**: `0.0.0-develop.716` (configured in `docker/*/Dockerfile` and `.env.example`).
- **Standalone Stack**: Self-contained root `docker-compose.yml` runs PostgreSQL, Redis, MinIO, Keycloak (realm `refugee`), IAM Staff Portal API, AWE, ID Generator, Master Data API, Refugee Staff API, Celery Worker & Beat, and Staff UI — with zero dependency on `openg2p-developer` or external workspaces.
- See [docs/standalone/ARCHITECTURE.md](docs/standalone/ARCHITECTURE.md), [docs/standalone/DEPENDENCY_AUDIT.md](docs/standalone/DEPENDENCY_AUDIT.md), and [docs/standalone/TROUBLESHOOTING.md](docs/standalone/TROUBLESHOOTING.md) for details.

---

## Quick Start (Standalone)

Requires only **Docker** (with Compose v2) and **git**.

1. **Generate `.env` with random secrets**:
   ```bash
   ./scripts/init-env.sh
   ```
2. **Start, bootstrap, and seed the full stack** (set `LOAD_SAMPLE_DATA=false` in `.env` to skip demo records):
   ```bash
   ./scripts/up.sh
   ```
3. **Verify everything is healthy**:
   ```bash
   ./scripts/smoke-test.sh
   ```
   - Staff Portal UI: `http://localhost:3150/en` (demo login: `staff`, password in `.env` `REFUGEE_DEMO_USER_PASSWORD`)
   - Staff API OpenAPI: `http://localhost:8271/docs`
   - Master Data API OpenAPI: `http://localhost:8249/docs`
   - Keycloak Admin: `http://localhost:8280`
4. **Stop or reset**:
   - `./scripts/down.sh` — stop containers (keeps data volumes)
   - `./scripts/reset.sh --yes` — wipe volumes and re-seed from scratch
   - `./scripts/status.sh` / `./scripts/logs.sh [service]` — inspect status and logs
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
