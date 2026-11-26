#!/usr/bin/env bash
set -euo pipefail

DEV_DIR="${OPENG2P_DEVELOPER_DIR:?Set OPENG2P_DEVELOPER_DIR to your openg2p-developer path}"
cd "$DEV_DIR"

COMPOSE_FILES=(
  -f compose/docker-compose.infra.yml
  -f compose/docker-compose.commons.yml
  -f compose/docker-compose.refugee-services.yml
  -f compose/docker-compose.refugee.yml
)

docker compose "${COMPOSE_FILES[@]}" --profile infra --profile commons up -d --no-deps \
  refugee-postgres refugee-redis refugee-keycloak refugee-iam-staff-api refugee-awe refugee-id-generator \
  refugee-master-data-api refugee-registry-staff-api refugee-registry-celery-worker refugee-registry-celery-beat refugee-registry-staff-ui
