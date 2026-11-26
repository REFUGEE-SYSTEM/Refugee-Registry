#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <path-to-openg2p-developer>" >&2
  exit 1
fi

DEV_DIR="$(cd "$1" && pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TS="$(date +%Y%m%d%H%M%S)"

if [[ ! -d "$DEV_DIR/compose" ]]; then
  echo "ERROR: $DEV_DIR/compose does not exist. Provide a valid openg2p-developer path." >&2
  exit 1
fi

echo "Target developer stack: $DEV_DIR"
read -r -p "Install Refugee Registry compose and env templates into $DEV_DIR? [y/N] " REPLY
if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
  echo "Aborted."
  exit 0
fi

backup_and_copy() {
  local src="$1"
  local dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [[ -f "$dst" ]]; then
    cp "$dst" "${dst}.bak.${TS}"
    echo "Backed up $dst -> ${dst}.bak.${TS}"
  fi
  cp "$src" "$dst"
  echo "Copied $src -> $dst"
}

backup_and_copy "$PROJECT_DIR/deploy/local/docker-compose.refugee.yml" "$DEV_DIR/compose/docker-compose.refugee.yml"
backup_and_copy "$PROJECT_DIR/deploy/local/docker-compose.refugee-services.yml" "$DEV_DIR/compose/docker-compose.refugee-services.yml"
backup_and_copy "$PROJECT_DIR/deploy/local/id-generator.refugee.yaml" "$DEV_DIR/config/id-generator/refugee.yaml"

mkdir -p "$DEV_DIR/generated/refugee-registry/docker" "$DEV_DIR/generated/refugee-registry/isolated" "$DEV_DIR/generated/refugee-registry/iam-data"
for f in "$PROJECT_DIR/deploy/local/env/"*.env.example; do
  base="$(basename "$f" .example)"
  backup_and_copy "$f" "$DEV_DIR/generated/refugee-registry/docker/${base}.example"
done
backup_and_copy "$PROJECT_DIR/deploy/local/awe-config.yaml.example" "$DEV_DIR/generated/refugee-registry/isolated/awe-config.yaml.example"
backup_and_copy "$PROJECT_DIR/deploy/local/iam-data/login_providers.json.example" "$DEV_DIR/generated/refugee-registry/iam-data/login_providers.json.example"

echo ""
echo "=== Manual Steps for Shared Files ==="
echo "1. Copy *.example files to *.env / *.yaml / *.json and replace CHANGE_ME values."
echo "2. Add the following to $DEV_DIR/.env if not already present:"
cat "$PROJECT_DIR/deploy/local/developer-env.snippet"
echo ""
echo "3. If using the shared id-generator instead of refugee-id-generator, add to $DEV_DIR/config/id-generator/default.yaml:"
cat "$PROJECT_DIR/deploy/local/id-generator.refugee.snippet.yaml"
