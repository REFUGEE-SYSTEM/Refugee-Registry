#!/usr/bin/env python3
"""Provision isolated Keycloak realm 'refugee' on REFUGEE_KEYCLOAK_URL (default http://localhost:8180)."""

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request

KC = os.environ.get("REFUGEE_KEYCLOAK_URL", "http://localhost:8180")
REALM = os.environ.get("REFUGEE_KEYCLOAK_REALM", "refugee")
ADMIN_USER = os.environ.get("REFUGEE_KEYCLOAK_ADMIN", "admin")
ADMIN_PASS = os.environ["REFUGEE_KEYCLOAK_ADMIN_PASSWORD"]
IAM_SECRET = os.environ["KEYCLOAK_IAM_CLIENT_SECRET"]
AWE_SECRET = os.environ["KEYCLOAK_AWE_RESOLVER_CLIENT_SECRET"]
DEMO_USER_PASS = os.environ.get("REFUGEE_DEMO_USER_PASSWORD", "CHANGE_ME")

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


def req_json(url, method="GET", data=None, token=None):
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
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=15) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        if e.code == 409:
            return None
        raise RuntimeError(f"{method} {url} -> {e.code}: {e.read().decode()}") from e


def main():
    tok = req_json(
        f"{KC}/realms/master/protocol/openid-connect/token",
        method="POST",
        data={"grant_type": "password", "client_id": "admin-cli", "username": ADMIN_USER, "password": ADMIN_PASS},
    )["access_token"]

    try:
        req_json(f"{KC}/admin/realms/{REALM}", token=tok)
    except RuntimeError:
        req_json(
            f"{KC}/admin/realms",
            method="POST",
            data={"realm": REALM, "enabled": True, "sslRequired": "none"},
            token=tok,
        )

    clients_spec = [
        {
            "clientId": "iam-staff-portal",
            "enabled": True,
            "publicClient": False,
            "secret": IAM_SECRET,
            "directAccessGrantsEnabled": True,
            "standardFlowEnabled": True,
            "fullScopeAllowed": False,
            "redirectUris": ["http://localhost:8120/*", "http://localhost:3050/*"],
            "webOrigins": ["*"],
        },
        {
            "clientId": "refugee-registry-staff-portal",
            "enabled": True,
            "publicClient": True,
            "directAccessGrantsEnabled": True,
            "standardFlowEnabled": True,
            "fullScopeAllowed": False,
            "redirectUris": ["http://localhost:3050/*"],
            "webOrigins": ["*"],
        },
        {
            "clientId": "awe-admin-resolver",
            "enabled": True,
            "publicClient": False,
            "secret": AWE_SECRET,
            "serviceAccountsEnabled": True,
            "standardFlowEnabled": False,
            "directAccessGrantsEnabled": False,
            "fullScopeAllowed": False,
        },
    ]
    for c in clients_spec:
        req_json(f"{KC}/admin/realms/{REALM}/clients", method="POST", data=c, token=tok)

    all_clients = req_json(f"{KC}/admin/realms/{REALM}/clients", token=tok)
    cmap = {c["clientId"]: c["id"] for c in all_clients}
    rf_cid, iam_cid, awe_cid, rm_cid = (
        cmap["refugee-registry-staff-portal"],
        cmap["iam-staff-portal"],
        cmap["awe-admin-resolver"],
        cmap["realm-management"],
    )

    for rname in REFUGEE_ROLES:
        req_json(f"{KC}/admin/realms/{REALM}/clients/{rf_cid}/roles", method="POST", data={"name": rname}, token=tok)
    rf_roles_by_name = {r["name"]: r for r in req_json(f"{KC}/admin/realms/{REALM}/clients/{rf_cid}/roles", token=tok)}

    for rname in REFUGEE_ROLES:
        try:
            req_json(
                f"{KC}/admin/realms/{REALM}/clients/{iam_cid}/scope-mappings/clients/{rf_cid}",
                method="POST",
                data=[rf_roles_by_name[rname]],
                token=tok,
            )
        except RuntimeError:
            pass

    sa_user = req_json(f"{KC}/admin/realms/{REALM}/clients/{awe_cid}/service-account-user", token=tok)
    rm_roles = req_json(f"{KC}/admin/realms/{REALM}/clients/{rm_cid}/roles", token=tok)
    wanted_rm = [r for r in rm_roles if r["name"] in ("view-users", "query-users", "query-groups", "view-clients")]
    if wanted_rm:
        req_json(
            f"{KC}/admin/realms/{REALM}/users/{sa_user['id']}/role-mappings/clients/{rm_cid}",
            method="POST",
            data=wanted_rm,
            token=tok,
        )

    for uname, fn, ln, email in [
        ("staff", "Staff", "Registrar", "staff@refugee.local"),
        ("alex.carter", "Alex", "Carter", "alex.carter@refugee.local"),
        ("nina.patel", "Nina", "Patel", "nina.patel@refugee.local"),
    ]:
        req_json(
            f"{KC}/admin/realms/{REALM}/users",
            method="POST",
            data={
                "username": uname,
                "firstName": fn,
                "lastName": ln,
                "email": email,
                "enabled": True,
                "emailVerified": True,
                "credentials": [{"type": "password", "value": DEMO_USER_PASS, "temporary": False}],
            },
            token=tok,
        )
        uid = req_json(f"{KC}/admin/realms/{REALM}/users?username={uname}&exact=true", token=tok)[0]["id"]
        req_json(
            f"{KC}/admin/realms/{REALM}/users/{uid}/role-mappings/clients/{rf_cid}",
            method="POST",
            data=[rf_roles_by_name[r] for r in REFUGEE_ROLES],
            token=tok,
        )


if __name__ == "__main__":
    main()
