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

docker compose "${COMPOSE_FILES[@]}" --profile infra --profile commons stop \
  refugee-registry-staff-ui refugee-registry-celery-beat refugee-registry-celery-worker \
  refugee-registry-staff-api refugee-master-data-api \
  refugee-id-generator refugee-awe refugee-iam-staff-api refugee-keycloak refugee-redis refugee-postgres
