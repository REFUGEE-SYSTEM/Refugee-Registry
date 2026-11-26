#!/usr/bin/env python3
"""Idempotent standalone bootstrap for Keycloak, IAM, AWE, and ID Generator."""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import psycopg2

REFUGEE_ROLES = [
    "Intake Officer",
    "Intake Validator",
    "Data Editor",
    "Data Validator",
    "Data Supervisor",
    "Operations Administrator",
    "Technical Administrator",
    "Schema Designer",
    "Integration Specialist",
    "Integration Manager",
    "Reference Data Specialist",
]


def _req_json(url: str, method: str = "GET", data=None, token: str | None = None):
    headers = {}
    body = None
    if data is not None:
        if isinstance(data, dict) and url.endswith("/token"):
            body = urllib.parse.urlencode(data).encode()
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        if exc.code == 409:
            return None
        raise RuntimeError(f"{method} {url} -> {exc.code}: {exc.read().decode()}") from exc


def wait_for_table(dbname: str, table: str, timeout: int = 120) -> None:
    deadline = time.time() + timeout
    last_err: Exception | None = None
    while time.time() < deadline:
        conn = None
        try:
            conn = psycopg2.connect(
                host=os.environ.get("PGHOST", "postgres"),
                port=int(os.environ.get("PGPORT", "5432")),
                dbname=dbname,
                user=os.environ.get("POSTGRES_USER", "postgres"),
                password=os.environ["POSTGRES_PASSWORD"],
            )
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s",
                    (table,),
                )
                if cur.fetchone():
                    return
        except Exception as exc:
            last_err = exc
        finally:
            if conn is not None:
                conn.close()
        time.sleep(2)
    raise RuntimeError(f"Timed out waiting for {dbname}.{table}: {last_err}")


def bootstrap_keycloak() -> None:
    kc = os.environ.get("KEYCLOAK_INTERNAL_URL", "http://keycloak:8080")
    realm = os.environ.get("REFUGEE_KEYCLOAK_REALM", "refugee")
    admin_user = os.environ.get("REFUGEE_KEYCLOAK_ADMIN", "admin")
    admin_pass = os.environ["REFUGEE_KEYCLOAK_ADMIN_PASSWORD"]
    iam_secret = os.environ["KEYCLOAK_IAM_CLIENT_SECRET"]
    awe_secret = os.environ["KEYCLOAK_AWE_RESOLVER_CLIENT_SECRET"]
    demo_pass = os.environ["REFUGEE_DEMO_USER_PASSWORD"]
    ui_port = os.environ.get("REFUGEE_UI_PORT", "3150")
    iam_port = os.environ.get("REFUGEE_IAM_PORT", "8220")

    print(f"[bootstrap] Configuring Keycloak realm '{realm}' at {kc} ...")
    tok = _req_json(
        f"{kc}/realms/master/protocol/openid-connect/token",
        method="POST",
        data={
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": admin_user,
            "password": admin_pass,
        },
    )["access_token"]

    try:
        _req_json(f"{kc}/admin/realms/{realm}", token=tok)
    except RuntimeError:
        _req_json(
            f"{kc}/admin/realms",
            method="POST",
            data={"realm": realm, "enabled": True, "sslRequired": "none"},
            token=tok,
        )

    clients_spec = [
        {
            "clientId": "iam-staff-portal",
            "enabled": True,
            "publicClient": False,
            "secret": iam_secret,
            "directAccessGrantsEnabled": True,
            "standardFlowEnabled": True,
            "fullScopeAllowed": False,
            "redirectUris": [f"http://localhost:{iam_port}/*", f"http://localhost:{ui_port}/*"],
            "webOrigins": ["*"],
        },
        {
            "clientId": "refugee-registry-staff-portal",
            "enabled": True,
            "publicClient": True,
            "directAccessGrantsEnabled": True,
            "standardFlowEnabled": True,
            "fullScopeAllowed": False,
            "redirectUris": [f"http://localhost:{ui_port}/*"],
            "webOrigins": ["*"],
        },
        {
            "clientId": "awe-admin-resolver",
            "enabled": True,
            "publicClient": False,
            "secret": awe_secret,
            "serviceAccountsEnabled": True,
            "standardFlowEnabled": False,
            "directAccessGrantsEnabled": False,
            "fullScopeAllowed": False,
        },
    ]

    existing = {c["clientId"]: c for c in _req_json(f"{kc}/admin/realms/{realm}/clients", token=tok)}
    for spec in clients_spec:
        cid = spec["clientId"]
        if cid in existing:
            _req_json(f"{kc}/admin/realms/{realm}/clients/{existing[cid]['id']}", method="PUT", data=spec, token=tok)
        else:
            _req_json(f"{kc}/admin/realms/{realm}/clients", method="POST", data=spec, token=tok)

    cmap = {c["clientId"]: c["id"] for c in _req_json(f"{kc}/admin/realms/{realm}/clients", token=tok)}
    rf_cid = cmap["refugee-registry-staff-portal"]
    iam_cid = cmap["iam-staff-portal"]
    awe_cid = cmap["awe-admin-resolver"]
    rm_cid = cmap["realm-management"]

    for rname in REFUGEE_ROLES:
        _req_json(f"{kc}/admin/realms/{realm}/clients/{rf_cid}/roles", method="POST", data={"name": rname}, token=tok)
    rf_roles = {r["name"]: r for r in _req_json(f"{kc}/admin/realms/{realm}/clients/{rf_cid}/roles", token=tok)}

    for rname in REFUGEE_ROLES:
        try:
            _req_json(
                f"{kc}/admin/realms/{realm}/clients/{iam_cid}/scope-mappings/clients/{rf_cid}",
                method="POST",
                data=[rf_roles[rname]],
                token=tok,
            )
        except RuntimeError:
            pass

    sa_user = _req_json(f"{kc}/admin/realms/{realm}/clients/{awe_cid}/service-account-user", token=tok)
    rm_roles = _req_json(f"{kc}/admin/realms/{realm}/clients/{rm_cid}/roles", token=tok)
    wanted_rm = [r for r in rm_roles if r["name"] in ("view-users", "query-users", "query-groups", "view-clients")]
    if wanted_rm:
        _req_json(
            f"{kc}/admin/realms/{realm}/users/{sa_user['id']}/role-mappings/clients/{rm_cid}",
            method="POST",
            data=wanted_rm,
            token=tok,
        )

    for uname, fn, ln, email in [
        ("staff", "Staff", "Registrar", "staff@refugee.local"),
        ("alex.carter", "Alex", "Carter", "alex.carter@refugee.local"),
        ("nina.patel", "Nina", "Patel", "nina.patel@refugee.local"),
    ]:
        _req_json(
            f"{kc}/admin/realms/{realm}/users",
            method="POST",
            data={
                "username": uname,
                "firstName": fn,
                "lastName": ln,
                "email": email,
                "enabled": True,
                "emailVerified": True,
                "credentials": [{"type": "password", "value": demo_pass, "temporary": False}],
            },
            token=tok,
        )
        uid = _req_json(f"{kc}/admin/realms/{realm}/users?username={uname}&exact=true", token=tok)[0]["id"]
        _req_json(
            f"{kc}/admin/realms/{realm}/users/{uid}/role-mappings/clients/{rf_cid}",
            method="POST",
            data=[rf_roles[r] for r in REFUGEE_ROLES],
            token=tok,
        )
    print("[bootstrap] Keycloak realm, clients, roles, and users ready.")


async def _register_iam_app() -> None:
    from sqlalchemy.ext.asyncio import create_async_engine

    from iam_staff_portal_api.config import Settings
    from iam_staff_portal_api.controllers.user_access_controller import UserAccessController
    from iam_staff_portal_api.schemas import RegisterStaffPortalApplicationRequest
    from openg2p_fastapi_common.context import dbengine

    payload_data = json.loads(Path("/opt/bootstrap/iam_registration_payload.json").read_text(encoding="utf-8"))
    ui_port = os.environ.get("REFUGEE_UI_PORT", "3150")
    payload_data["application_url"] = f"http://localhost:{ui_port}"

    config = Settings.get_config(strict=False)
    existing_engine = dbengine.get()
    if existing_engine is not None:
        await existing_engine.dispose(close=False)
    dbengine.set(create_async_engine(config.db_datasource, echo=False))

    controller = UserAccessController()
    payload = RegisterStaffPortalApplicationRequest.model_validate(payload_data)
    response = await controller.register_staff_portal_application(None, payload)
    action = "created" if response.created else "updated"
    print(f"[bootstrap] IAM app {action}: refugee-registry-staff-portal ({response.permissions_count} perms, {response.roles_count} roles)")
    await dbengine.get().dispose(close=False)


def bootstrap_iam() -> None:
    print("[bootstrap] Running IAM DB migrations ...")
    subprocess.run([sys.executable, "-m", "iam_staff_portal_api.main", "migrate"], check=True)
    wait_for_table("iam_staff", "staff_portal_applications")
    wait_for_table("iam_staff", "login_providers")
    asyncio.run(_register_iam_app())

    kc_port = os.environ.get("REFUGEE_KEYCLOAK_PORT", "8280")
    iam_port = os.environ.get("REFUGEE_IAM_PORT", "8220")
    ui_port = os.environ.get("REFUGEE_UI_PORT", "3150")
    realm = os.environ.get("REFUGEE_KEYCLOAK_REALM", "refugee")
    issuer = f"http://localhost:{kc_port}/realms/{realm}"
    auth_ep = f"{issuer}/protocol/openid-connect/auth"
    cb_url = f"http://localhost:{iam_port}/auth/callback"
    redirect_uri = f"http://localhost:{ui_port}/"
    server_meta = f"http://keycloak:8080/realms/{realm}/.well-known/openid-configuration"
    iam_secret = os.environ["KEYCLOAK_IAM_CLIENT_SECRET"]

    conn = psycopg2.connect(
        host=os.environ.get("PGHOST", "postgres"),
        port=int(os.environ.get("PGPORT", "5432")),
        dbname="iam_staff",
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ["POSTGRES_PASSWORD"],
    )
    with conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE login_providers
            SET issuer = %s,
                authorization_endpoint = %s,
                oauth_callback_url = %s,
                default_redirect_uri = %s,
                server_metadata_url = %s,
                client_secret = %s
            WHERE id = 1
            """,
            (issuer, auth_ep, cb_url, redirect_uri, server_meta, iam_secret),
        )
    conn.close()
    print(f"[bootstrap] IAM login_providers updated (issuer={issuer}).")


def bootstrap_awe() -> None:
    print("[bootstrap] Waiting for AWE callback_secret table ...")
    wait_for_table("awe", "callback_secret")
    secret_id = os.environ["AWE_CALLBACK_SECRET_ID"]
    caller = os.environ.get("AWE_CALLBACK_CALLER_SERVICE", "refugee")
    hmac_secret = os.environ["AWE_CALLBACK_HMAC_SECRET"]

    conn = psycopg2.connect(
        host=os.environ.get("PGHOST", "postgres"),
        port=int(os.environ.get("PGPORT", "5432")),
        dbname="awe",
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=os.environ["POSTGRES_PASSWORD"],
    )
    with conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO public.callback_secret (
                id, caller_service, secret_hash, status, rotated_at, created_at, updated_at
            ) VALUES (%s, %s, %s, 'active', NOW(), NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET
                caller_service = EXCLUDED.caller_service,
                secret_hash = EXCLUDED.secret_hash,
                status = EXCLUDED.status,
                updated_at = NOW()
            """,
            (secret_id, caller, hmac_secret),
        )
    conn.close()
    print(f"[bootstrap] AWE callback_secret ready (id={secret_id}, caller={caller}).")


def wait_idgen_pools() -> None:
    url = os.environ.get("IDGEN_INTERNAL_URL", "http://id-generator:8000")
    print(f"[bootstrap] Waiting for ID Generator pools at {url} ...")
    deadline = time.time() + 90
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}/v1/idgenerator/health", timeout=5) as resp:
                if resp.status == 200:
                    conn = psycopg2.connect(
                        host=os.environ.get("PGHOST", "postgres"),
                        port=int(os.environ.get("PGPORT", "5432")),
                        dbname="idgenerator",
                        user=os.environ.get("POSTGRES_USER", "postgres"),
                        password=os.environ["POSTGRES_PASSWORD"],
                    )
                    with conn, conn.cursor() as cur:
                        cur.execute(
                            "SELECT id_type, COUNT(*) FROM id_pool WHERE status = 'AVAILABLE' GROUP BY id_type"
                        )
                        counts = dict(cur.fetchall())
                    conn.close()
                    if counts.get("household", 0) > 0 and counts.get("refugee", 0) > 0:
                        print(f"[bootstrap] ID Generator pools ready: {counts}")
                        return
        except Exception:
            pass
        time.sleep(3)
    raise RuntimeError("Timed out waiting for ID Generator pools (household, refugee)")


def bootstrap_minio() -> None:
    from minio import Minio

    endpoint = os.environ.get("MINIO_ENDPOINT", "minio:9000")
    access_key = os.environ.get("MINIO_ROOT_USER", "refugeeadmin")
    secret_key = os.environ["MINIO_ROOT_PASSWORD"]
    buckets = [
        os.environ.get("MINIO_BUCKET_NAME", "default_bucket"),
        "templates",
        "registrant-photos",
    ]
    client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)
    for bucket in buckets:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            print(f"[bootstrap] Created MinIO bucket '{bucket}'.")
        else:
            print(f"[bootstrap] MinIO bucket '{bucket}' already exists.")


def main() -> int:
    bootstrap_minio()
    bootstrap_keycloak()
    bootstrap_iam()
    bootstrap_awe()
    wait_idgen_pools()
    print("[bootstrap] Core bootstrap complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
