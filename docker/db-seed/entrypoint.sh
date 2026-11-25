#!/bin/sh
set -e

EXPECTED_SECRET_ID="00000000-0000-4000-8000-000000000005"
EXPECTED_CALLER="refugee"

if [ -z "${AWE_CALLBACK_SECRET_ID}" ] || [ -z "${AWE_CALLBACK_CALLER_SERVICE}" ]; then
  echo "[db-seed-guard] FATAL: AWE_CALLBACK_SECRET_ID or AWE_CALLBACK_CALLER_SERVICE is unset" >&2
  exit 1
fi

if [ "${AWE_CALLBACK_SECRET_ID}" != "${EXPECTED_SECRET_ID}" ] || [ "${AWE_CALLBACK_CALLER_SERVICE}" != "${EXPECTED_CALLER}" ]; then
  echo "[db-seed-guard] FATAL: mismatch (got id=${AWE_CALLBACK_SECRET_ID}, caller=${AWE_CALLBACK_CALLER_SERVICE})" >&2
  exit 1
fi

echo "[db-seed-guard] AWE callback secret guard verified: id=${AWE_CALLBACK_SECRET_ID}, caller=${AWE_CALLBACK_CALLER_SERVICE}"
exec /seed/entrypoint.sh "$@"
