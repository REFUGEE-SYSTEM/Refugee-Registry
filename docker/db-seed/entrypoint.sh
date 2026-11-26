#!/bin/sh
set -e

EXPECTED_CALLER="refugee"

if [ -z "${AWE_CALLBACK_SECRET_ID}" ] || [ "${AWE_CALLBACK_SECRET_ID}" = "CHANGE_ME_UUID" ] || [ -z "${AWE_CALLBACK_CALLER_SERVICE}" ]; then
  echo "[db-seed-guard] FATAL: AWE_CALLBACK_SECRET_ID or AWE_CALLBACK_CALLER_SERVICE is unset/placeholder" >&2
  exit 1
fi

if [ "${AWE_CALLBACK_CALLER_SERVICE}" != "${EXPECTED_CALLER}" ]; then
  echo "[db-seed-guard] FATAL: caller mismatch (got caller=${AWE_CALLBACK_CALLER_SERVICE})" >&2
  exit 1
fi

echo "[db-seed-guard] AWE callback secret guard verified: id=${AWE_CALLBACK_SECRET_ID}, caller=${AWE_CALLBACK_CALLER_SERVICE}"
exec /seed/entrypoint.sh "$@"
