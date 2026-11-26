#!/usr/bin/env python3
"""Idempotently sync refugee-registry-staff-portal app, roles, and permissions into isolated iam_staff DB."""

import os
import psycopg2


def copy_rows(cs, cd, table, sql_select, conflict_col):
    cs.execute(sql_select)
    rows = cs.fetchall()
    cols = [d[0] for d in cs.description]
    col_sql = ", ".join(f'"{c}"' for c in cols)
    ph = ", ".join(["%s"] * len(cols))
    ins = f'INSERT INTO "{table}" ({col_sql}) VALUES ({ph}) ON CONFLICT ({conflict_col}) DO NOTHING'
    for r in rows:
        cd.execute(ins, r)
    print(f"{table}: synced {len(rows)} rows")


def main():
    pg_pw = os.environ["POSTGRES_PASSWORD"]
    src = psycopg2.connect(
        host=os.environ.get("SHARED_PGHOST", "localhost"),
        port=int(os.environ.get("SHARED_PGPORT", "5433")),
        dbname="iam_staff",
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=pg_pw,
    )
    dst = psycopg2.connect(
        host=os.environ.get("REFUGEE_PGHOST", "localhost"),
        port=int(os.environ.get("REFUGEE_PGPORT", "5435")),
        dbname="iam_staff",
        user=os.environ.get("POSTGRES_USER", "postgres"),
        password=pg_pw,
    )
    try:
        with src, dst:
            with src.cursor() as cs, dst.cursor() as cd:
                copy_rows(
                    cs, cd, "staff_portal_applications",
                    "SELECT * FROM staff_portal_applications WHERE application_mnemonic = 'refugee-registry-staff-portal'",
                    '"id"',
                )
                cs.execute("SELECT id FROM staff_portal_applications WHERE application_mnemonic = 'refugee-registry-staff-portal'")
                app_id = cs.fetchone()[0]
                copy_rows(cs, cd, "staff_application_permissions", f"SELECT * FROM staff_application_permissions WHERE application_id = '{app_id}'", '"id"')
                copy_rows(cs, cd, "staff_roles", f"SELECT * FROM staff_roles WHERE application_id = '{app_id}'", '"id"')
                copy_rows(cs, cd, "staff_role_permissions", f"SELECT * FROM staff_role_permissions WHERE role_id IN (SELECT id FROM staff_roles WHERE application_id = '{app_id}')", '"id"')
                issuer = os.environ.get("REFUGEE_KEYCLOAK_ISSUER", "http://localhost:8180/realms/refugee")
                cd.execute("UPDATE login_providers SET issuer = %s WHERE id = 1", (issuer,))
    finally:
        src.close()
        dst.close()


if __name__ == "__main__":
    main()
