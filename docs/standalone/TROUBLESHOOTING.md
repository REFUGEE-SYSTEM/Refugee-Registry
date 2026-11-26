# Standalone Troubleshooting

## 1. Port Already in Use
- Default standalone ports are `3150`, `5535`, `6481`, `8220`, `8230`, `8240`, `8249`, `8271`, `8280`, `9100`, `9101`.
- Override any colliding port in `.env` and re-run `./scripts/up.sh` (which automatically regenerates `docker/generated/iam-data/login_providers.json` and updates Keycloak/IAM URLs).

## 2. `iam-staff-api` Login or 403 Permission Errors
- Ensure `./scripts/up.sh` completed `bootstrap-core` cleanly.
- Re-run just the core bootstrap:
  ```bash
  docker compose --profile bootstrap run --rm bootstrap-core
  ```
- Verify `login_providers` has `issuer = http://localhost:${REFUGEE_KEYCLOAK_PORT}/realms/refugee` and `staff_portal_applications` contains `refugee-registry-staff-portal`.

## 3. Master Data (`mds-seed`) Failed to Fetch `openg2p-data`
- `docker/mds-seed/Dockerfile` performs a shallow sparse checkout of `OpenG2P/openg2p-data` at pinned SHA `122275845b38729e508480539cf35dd67b4c804e`.
- Ensure outbound GitHub HTTPS access during image build, then re-run:
  ```bash
  docker compose --profile bootstrap run --rm --build mds-seed
  ```

## 4. Clean Reset
- To wipe all standalone containers and volumes and re-seed from scratch:
  ```bash
  ./scripts/reset.sh --yes
  ```
