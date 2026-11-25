# Baseline State (Before Refugee Registry Wiring)

Recorded: 2026-11-25T12:57+05:30

## Running Containers (`docker ps`)
- **Shared Infra**:
  - `openg2p-postgres` (`postgres:16`) — `0.0.0.0:5433->5432/tcp` (healthy)
  - `openg2p-redis` (`redis:7-alpine`) — `0.0.0.0:6380->6379/tcp` (healthy)
  - `openg2p-minio` (`minio/minio:latest`) — `0.0.0.0:9000-9001->9000-9001/tcp` (healthy)
  - `openg2p-keycloak` (`quay.io/keycloak/keycloak:26.0`) — `0.0.0.0:8080->8080/tcp` (healthy)
- **Shared Platform**:
  - `openg2p-iam-staff-api` — `0.0.0.0:8020->8000/tcp` (healthy)
  - `openg2p-awe-api` — `0.0.0.0:8030->8000/tcp` (healthy)
  - `openg2p-awe-ui` — `0.0.0.0:8031->8080/tcp` (healthy)
  - `openg2p-id-generator` — `0.0.0.0:8040->8000/tcp` (healthy)
  - `openg2p-staff-portal-ui` — `0.0.0.0:3000->3000/tcp`
  - `openg2p-superset` — `0.0.0.0:8088->8088/tcp` (healthy)
  - `openg2p-dev-consent-stub` — `0.0.0.0:8095->8000/tcp`
  - `openg2p-dev-keycloak-proxy` — `8000/tcp`
- **Farmer Custom Registry (must remain unaffected)**:
  - `openg2p-farmer-custom-staff-ui` — `0.0.0.0:3040->3000/tcp`
  - `openg2p-farmer-custom-staff-api` — `0.0.0.0:8061->8000/tcp`
  - `openg2p-farmer-custom-partner-api` — `0.0.0.0:8062->8000/tcp`
  - `openg2p-farmer-custom-master-data-api` — `0.0.0.0:8048->8000/tcp`
  - `openg2p-farmer-custom-celery-worker`, `openg2p-farmer-custom-celery-beat`
- **Livestock Registry**:
  - `openg2p-livestock-registry-staff-ui` (`3020`), `staff-api` (`8041`), `partner-api` (`8042`), `master-data-api` (`8044`), celery worker/beat
- **Crop Sown Registry**:
  - `openg2p-cropsown-registry-staff-ui` (`3030`), `staff-api` (`8051`), `master-data-api` (`8046`), celery worker/beat
- **Other**:
  - `mds-standalone-*` (`3005`, `8045`, `5434`, `9010-9011`)
  - `central-*` (ODK Central, `8081`, `7443`)

## Ports in Use (relevant range)
- UI ports: `3000`, `3005`, `3020`, `3030`, `3040`
- API ports: `8020`, `8030`, `8031`, `8040`, `8041`, `8042`, `8044`, `8045`, `8046`, `8048`, `8051`, `8061`, `8062`, `8080`, `8081`, `8088`, `8095`
- DB/Redis/MinIO: `5433`, `5434`, `6380`, `9000`, `9001`, `9010`, `9011`

## Farmer Registry Baseline Check
- `curl -sI http://localhost:3040` returned `HTTP/1.1 307 Temporary Redirect` (`location: /en`).
