#!/usr/bin/env python3
"""Idempotent demo-data loader for Refugee Registry.

Reads geography from the running Master Data Service via mds_client (never its DB),
inspects target columns from information_schema, and inserts 8 households,
25 refugees, and sub-register rows tagged with created_by='demo-seeder' and
record_status_reason='DEMO'.
"""

from __future__ import annotations

import os
import sys
import uuid
from datetime import date
from pathlib import Path

import psycopg2
from psycopg2.extras import Json

try:
    import mds_client
except ImportError:
    mds_client = None

DEMO_TAG = "DEMO"
SEEDER = "demo-seeder"
NOW_TS = "2026-11-25 10:00:00"


def _uid(key: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"refugee-demo:{key}"))


def _table_columns(cur, table: str) -> set[str]:
    cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_schema = current_schema() AND table_name = %s",
        (table,),
    )
    return {r[0] for r in cur.fetchall()}


def _insert_row(cur, table: str, cols_cache: dict[str, set[str]], row: dict) -> None:
    if table not in cols_cache:
        cols_cache[table] = _table_columns(cur, table)
    valid = cols_cache[table]
    filtered = {k: v for k, v in row.items() if k in valid}
    cols = list(filtered.keys())
    vals = [Json(v) if isinstance(v, (dict, list)) else v for v in filtered.values()]
    col_sql = ", ".join(f'"{c}"' for c in cols)
    ph_sql = ", ".join(["%s"] * len(cols))
    sql = (
        f'INSERT INTO "{table}" ({col_sql}) VALUES ({ph_sql}) '
        f'ON CONFLICT ("internal_record_id") DO NOTHING'
    )
    cur.execute(sql, vals)


def _fetch_geo_units() -> list[tuple[str, dict]]:
    if mds_client is None:
        raise SystemExit("mds_client module is not available")
    mds = mds_client.MdsClient.from_env(required=True)
    levels = mds_client.order_levels(mds.geo_levels())
    if not levels:
        raise SystemExit("MDS has no geography levels")
    lowest = levels[-1]
    level_id = lowest.get("level_id") or lowest.get("id") or lowest.get("level_mnemonic")
    units = mds.geo_units(level=level_id)
    if not units and len(levels) > 1:
        # Fallback to parent level if lowest has no units
        parent_id = levels[-2].get("level_id") or levels[-2].get("id")
        units = mds.geo_units(level=parent_id)
    if not units:
        raise SystemExit("MDS has no geography units")
    result = []
    for u in units[:16]:
        uid = u.get("unit_id") or u.get("level_value_id") or u.get("id") or u.get("value_id")
        if not uid:
            continue
        hier = mds.geo_hierarchy_json(uid) or {}
        result.append((uid, hier))
    if not result:
        raise SystemExit("Could not resolve any geography hierarchy from MDS")
    return result


HOUSEHOLDS = [
    ("HH-DEMO-0001", "REFUGEE", "SSD", "2024-03-15", "2024-04-02", "Gambella Camp Zone A, Plot 12", "+251911000101", True),
    ("HH-DEMO-0002", "ASYLUM_SEEKER", "ERI", "2025-01-10", "2025-01-22", "Addis Ababa Urban, Bole Subcity", "+251911000102", True),
    ("HH-DEMO-0003", "REFUGEE", "SOM", "2023-08-20", "2023-09-05", "Dollo Ado Camp, Block 4", "+251911000103", False),
    ("HH-DEMO-0004", "REFUGEE", "SDN", "2024-11-01", "2024-11-18", "Assosa Camp, Sector 2", "+251911000104", True),
    ("HH-DEMO-0005", "INTERNALLY_DISPLACED", "ETH", "2025-02-14", "2025-02-28", "Mekelle IDP Site, Shelter 9", "+251911000105", True),
    ("HH-DEMO-0006", "STATELESS", "SYR", "2024-06-05", "2024-06-19", "Addis Ababa Urban, Kirkos", "+251911000106", False),
    ("HH-DEMO-0007", "RETURNEE", "ETH", "2025-03-01", "2025-03-12", "Jijiga Reception Center", "+251911000107", True),
    ("HH-DEMO-0008", "REFUGEE", "YEM", "2024-09-12", "2024-09-25", "Addis Ababa Urban, Yeka", "+251911000108", True),
]

# (hh_idx, func_id, first, last, gender, dob, rel, marital, origin, edu, occ, religion, langs, pob)
REFUGEES = [
    # HH 1 (SSD, 4)
    (0, "RF-DEMO-0001", "Deng", "Garang", "MALE", "1984-05-12", "SELF", "MARRIED", "SSD", "SECONDARY", "Farmer", "CHRISTIANITY", ["EN", "AR"], "Juba"),
    (0, "RF-DEMO-0002", "Nyibol", "Garang", "FEMALE", "1988-09-20", "SPOUSE", "MARRIED", "SSD", "PRIMARY", "Trader", "CHRISTIANITY", ["EN"], "Bor"),
    (0, "RF-DEMO-0003", "Akech", "Garang", "FEMALE", "2012-03-11", "CHILD", "SINGLE", "SSD", "PRIMARY", "Student", "CHRISTIANITY", ["EN"], "Juba"),
    (0, "RF-DEMO-0004", "Bol", "Garang", "MALE", "2015-07-04", "CHILD", "SINGLE", "SSD", "NEVER_ATTEND", None, "CHRISTIANITY", ["EN"], "Juba"),
    # HH 2 (ERI, 3)
    (1, "RF-DEMO-0005", "Tesfay", "Berhe", "MALE", "1990-02-18", "SELF", "MARRIED", "ERI", "TERTIARY", "Electrician", "CHRISTIANITY", ["TI", "EN"], "Asmara"),
    (1, "RF-DEMO-0006", "Selam", "Berhe", "FEMALE", "1993-11-05", "SPOUSE", "MARRIED", "ERI", "SECONDARY", "Tailor", "CHRISTIANITY", ["TI", "AM"], "Keren"),
    (1, "RF-DEMO-0007", "Robel", "Berhe", "MALE", "2018-01-22", "CHILD", "SINGLE", "ERI", "NEVER_ATTEND", None, "CHRISTIANITY", ["TI"], "Asmara"),
    # HH 3 (SOM, 4)
    (2, "RF-DEMO-0008", "Abdi", "Hassan", "MALE", "1979-08-30", "SELF", "MARRIED", "SOM", "BASIC", "Pastoralist", "ISLAM", ["SO", "AR"], "Baidoa"),
    (2, "RF-DEMO-0009", "Halima", "Hassan", "FEMALE", "1983-04-14", "SPOUSE", "MARRIED", "SOM", "NON_FORMAL", "Weaver", "ISLAM", ["SO"], "Baidoa"),
    (2, "RF-DEMO-0010", "Fartun", "Hassan", "FEMALE", "2010-12-01", "CHILD", "SINGLE", "SOM", "PRIMARY", "Student", "ISLAM", ["SO"], "Baidoa"),
    (2, "RF-DEMO-0011", "Yusuf", "Hassan", "MALE", "2014-06-19", "CHILD", "SINGLE", "SOM", "PRIMARY", "Student", "ISLAM", ["SO"], "Dollo"),
    # HH 4 (SDN, 3)
    (3, "RF-DEMO-0012", "Omer", "Al-Amin", "MALE", "1986-07-07", "SELF", "MARRIED", "SDN", "HIGHER_EDUCATION", "Teacher", "ISLAM", ["APD", "AR", "EN"], "Khartoum"),
    (3, "RF-DEMO-0013", "Muna", "Al-Amin", "FEMALE", "1991-03-25", "SPOUSE", "MARRIED", "SDN", "TERTIARY", "Nurse", "ISLAM", ["APD", "EN"], "Omdurman"),
    (3, "RF-DEMO-0014", "Tariq", "Al-Amin", "MALE", "2017-10-10", "CHILD", "SINGLE", "SDN", "NEVER_ATTEND", None, "ISLAM", ["APD"], "Khartoum"),
    # HH 5 (ETH, 3)
    (4, "RF-DEMO-0015", "Dawit", "Gebre", "MALE", "1981-01-15", "SELF", "WIDOWED", "ETH", "SECONDARY", "Mason", "CHRISTIANITY", ["TI", "AM"], "Adigrat"),
    (4, "RF-DEMO-0016", "Hana", "Gebre", "FEMALE", "2011-05-09", "CHILD", "SINGLE", "ETH", "PRIMARY", "Student", "CHRISTIANITY", ["TI"], "Adigrat"),
    (4, "RF-DEMO-0017", "Yonas", "Gebre", "OTHERS", "2004-09-12", "SIBLING", "SINGLE", "ETH", "SECONDARY", "Mechanic", "NONE", ["TI", "EN"], "Adigrat"),
    # HH 6 (SYR, 3)
    (5, "RF-DEMO-0018", "Khaled", "Mansour", "MALE", "1975-11-28", "SELF", "MARRIED", "SYR", "TERTIARY", "Carpenter", "ISLAM", ["AR", "EN"], "Aleppo"),
    (5, "RF-DEMO-0019", "Layla", "Mansour", "FEMALE", "1980-06-03", "SPOUSE", "MARRIED", "SYR", "SECONDARY", "Baker", "ISLAM", ["AR"], "Aleppo"),
    (5, "RF-DEMO-0020", "Nadia", "Mansour", "FEMALE", "2006-04-17", "CHILD", "SINGLE", "SYR", "SECONDARY", "Student", "ISLAM", ["AR", "EN"], "Damascus"),
    # HH 7 (ETH, 2)
    (6, "RF-DEMO-0021", "Amina", "Mohamed", "FEMALE", "1987-08-21", "SELF", "SEPARATED", "ETH", "CAN_READ_AND_WRITE", "Vendor", "ISLAM", ["SO", "AM"], "Jijiga"),
    (6, "RF-DEMO-0022", "Bilal", "Mohamed", "MALE", "2016-02-28", "CHILD", "SINGLE", "ETH", "NEVER_ATTEND", None, "ISLAM", ["SO"], "Jijiga"),
    # HH 8 (YEM, 3)
    (7, "RF-DEMO-0023", "Ali", "Al-Harbi", "MALE", "1982-12-09", "SELF", "MARRIED", "YEM", "TERTIARY", "Pharmacist", "ISLAM", ["AR", "EN"], "Aden"),
    (7, "RF-DEMO-0024", "Fatima", "Al-Harbi", "FEMALE", "1985-03-16", "SPOUSE", "MARRIED", "YEM", "SECONDARY", "Teacher", "ISLAM", ["AR"], "Aden"),
    (7, "RF-DEMO-0025", "Zainab", "Al-Harbi", "FEMALE", "1955-01-05", "PARENT", "WIDOWED", "YEM", "ILLITERATE", None, "ISLAM", ["AR"], "Taiz"),
]


def main() -> None:
    geo_units = _fetch_geo_units()
    conn = psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=os.environ.get("PGDATABASE", "refugee_registry_db"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", "postgres"),
    )
    cols_cache: dict[str, set[str]] = {}
    hh_ids: list[str] = []
    ref_ids: list[str] = []

    try:
        with conn:
            with conn.cursor() as cur:
                # 1. Households
                for idx, (func_id, status, origin, arrival, reg_date, addr, phone, consent) in enumerate(HOUSEHOLDS):
                    hh_id = _uid(func_id)
                    hh_ids.append(hh_id)
                    members = [r for r in REFUGEES if r[0] == idx]
                    male_cnt = sum(1 for r in members if r[4] == "MALE")
                    female_cnt = sum(1 for r in members if r[4] == "FEMALE")
                    child_cnt = sum(1 for r in members if int(r[5][:4]) >= 2009)
                    geo_id, geo_hier = geo_units[idx % len(geo_units)]
                    rec_name = f"{func_id} {origin} {status}"
                    search_txt = f"{func_id} {rec_name} {origin} {status} {addr} {phone} {DEMO_TAG}"
                    _insert_row(
                        cur,
                        "g2p_register_households",
                        cols_cache,
                        {
                            "internal_record_id": hh_id,
                            "functional_record_id": func_id,
                            "record_name": rec_name,
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": search_txt,
                            "group_size": len(members),
                            "number_of_male": male_cnt,
                            "number_of_female": female_cnt,
                            "number_of_children": child_cnt,
                            "date_of_arrival": arrival,
                            "registration_date": reg_date,
                            "legal_status": status,
                            "current_country_of_asylum_address": addr,
                            "country_of_origin": origin,
                            "phone_number": phone,
                            "consent_or_prohibition_to_share_information": consent,
                            "geo_lowest_level_value_id": geo_id,
                            "geo_code_hierarchy_json": geo_hier,
                            "country_code": "ET",
                            "address_line_1": addr,
                            "latitude": 9.03 + idx * 0.05,
                            "longitude": 38.74 + idx * 0.05,
                        },
                    )

                # 2. Refugees
                head_ref_ids: list[str] = []
                for idx, (hh_idx, func_id, first, last, gender, dob, rel, marital, origin, edu, occ, religion, langs, pob) in enumerate(REFUGEES):
                    ref_id = _uid(func_id)
                    ref_ids.append(ref_id)
                    if rel == "SELF":
                        head_ref_ids.append(ref_id)
                    hh_id = hh_ids[hh_idx]
                    rec_name = f"{first} {last}"
                    search_txt = f"{func_id} {first} {last} {gender} {origin} {rel} {religion} {' '.join(langs)} {pob} {DEMO_TAG}"
                    _insert_row(
                        cur,
                        "g2p_register_refugees",
                        cols_cache,
                        {
                            "internal_record_id": ref_id,
                            "functional_record_id": func_id,
                            "link_internal_record_id": hh_id,
                            "record_name": rec_name,
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": search_txt,
                            "first_name": first,
                            "last_name": last,
                            "gender": gender,
                            "birth_date": dob,
                            "marital_status": marital,
                            "relationship_to_group": rel,
                            "country_of_origin": origin,
                            "fathers_name": f"Father of {first}",
                            "mothers_name": f"Mother of {first}",
                            "highest_education_level": edu,
                            "last_occupation": occ,
                            "religion": religion,
                            "languages_known": langs,
                            "place_of_birth": pob,
                        },
                    )

                # 3. IdentityDocument (1-2 per adult/most refugees)
                for idx, ref_id in enumerate(ref_ids[:18]):
                    doc_id = _uid(f"doc-{idx}-1")
                    doc_type = ["REFUGEE_ID", "NATIONAL_ID", "PASSPORT", "ASYLUM_SEEKER_CERTIFICATE"][idx % 4]
                    issuer = "UNHCR" if doc_type == "REFUGEE_ID" else "NATIONAL_GOVERNMENT"
                    doc_num = f"DOC-2025-{idx + 1001}"
                    _insert_row(
                        cur,
                        "g2p_register_identity_documents",
                        cols_cache,
                        {
                            "internal_record_id": doc_id,
                            "link_internal_record_id": ref_id,
                            "record_name": f"{doc_type} {doc_num}",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"{doc_type} {doc_num} {issuer} {DEMO_TAG}",
                            "document_type": doc_type,
                            "document_number": doc_num,
                            "issuer_type": issuer,
                            "issue_date": "2024-05-01",
                            "expiry_date": "2029-05-01",
                        },
                    )

                # 4. DisplacementHistory (each household head)
                for idx, ref_id in enumerate(head_ref_ids):
                    _insert_row(
                        cur,
                        "g2p_register_displacement_histories",
                        cols_cache,
                        {
                            "internal_record_id": _uid(f"disp-{idx}"),
                            "link_internal_record_id": ref_id,
                            "record_name": f"2024-01-10 Displacement {idx + 1}",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"Armed conflict and insecurity transit {DEMO_TAG}",
                            "reasons_for_unwillingness_or_inability_to_return": "Ongoing conflict and lack of physical safety in area of origin",
                            "travel_details": "Crossed border on foot and by bus to reception center",
                            "departure_date": "2024-01-10",
                            "transit_countries": "Border transit",
                        },
                    )

                # 5. SpecificNeeds (~6 rows)
                needs = [
                    (2, "UNACCOMPANIED_CHILD", "HIGH", "Child protection case management"),
                    (6, "SEPARATED_CHILD", "MODERATE", "Family tracing support"),
                    (11, "CHRONIC_ILLNESS", "HIGH", "Regular medication and clinic referral"),
                    (16, "PHYSICAL_DISABILITY", "MODERATE", "Mobility aid and accessible shelter"),
                    (20, "SINGLE_PARENT", "MODERATE", "Livelihood and childcare support"),
                    (24, "OLDER_PERSON", "CRITICAL", "Home-based care and food assistance"),
                ]
                for idx, (r_idx, cat, sev, sup) in enumerate(needs):
                    _insert_row(
                        cur,
                        "g2p_register_specific_needs",
                        cols_cache,
                        {
                            "internal_record_id": _uid(f"need-{idx}"),
                            "link_internal_record_id": ref_ids[r_idx],
                            "record_name": f"{cat} {sev}",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"{cat} {sev} {sup} {DEMO_TAG}",
                            "need_category": cat,
                            "severity": sev,
                            "date_identified": "2025-02-01",
                            "support_required": sup,
                            "notes": "Demo specific needs assessment",
                        },
                    )

                # 6. Relative (~10 rows)
                for idx in range(10):
                    r_idx = idx % len(ref_ids)
                    rel_type = ["SPOUSE", "CHILD", "PARENT", "SIBLING"][idx % 4]
                    rel_name = f"Relative {idx + 1} Demo"
                    _insert_row(
                        cur,
                        "g2p_register_relatives",
                        cols_cache,
                        {
                            "internal_record_id": _uid(f"rel-{idx}"),
                            "link_internal_record_id": ref_ids[r_idx],
                            "record_name": f"{rel_name} {rel_type}",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"{rel_name} {rel_type} {DEMO_TAG}",
                            "relationship": rel_type,
                            "full_name": rel_name,
                            "date_of_birth": "1995-04-12",
                            "location_or_status": "Residing in same household",
                        },
                    )

                # 7. Address (2 per refugee for 5 refugees)
                for idx in range(5):
                    ref_id = ref_ids[idx]
                    origin = REFUGEES[idx][8]
                    for addr_type, line1, ctry in (
                        ("COUNTRY_OF_ASYLUM", f"Camp Block {idx + 1}", "ETH"),
                        ("COUNTRY_OF_ORIGIN", f"Home District {idx + 1}", origin),
                    ):
                        _insert_row(
                            cur,
                            "g2p_register_addresses",
                            cols_cache,
                            {
                                "internal_record_id": _uid(f"addr-{idx}-{addr_type}"),
                                "link_internal_record_id": ref_id,
                                "record_name": f"{addr_type} {ctry}",
                                "record_status": "ACTIVE",
                                "record_status_reason": DEMO_TAG,
                                "created_by": SEEDER,
                                "created_at": NOW_TS,
                                "last_approved_by": SEEDER,
                                "last_approved_at": NOW_TS,
                                "search_text": f"{addr_type} {line1} {ctry} {DEMO_TAG}",
                                "address_type": addr_type,
                                "address_line_1": line1,
                                "address_line_2": "Sector 1",
                                "country": ctry,
                            },
                        )

                # 8. EducationRecord (6 rows)
                for idx, r_idx in enumerate((0, 4, 11, 12, 17, 22)):
                    lvl = REFUGEES[r_idx][9]
                    _insert_row(
                        cur,
                        "g2p_register_education_records",
                        cols_cache,
                        {
                            "internal_record_id": _uid(f"edu-{idx}"),
                            "link_internal_record_id": ref_ids[r_idx],
                            "record_name": f"{lvl} Demo Institute",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"{lvl} Demo Institute {DEMO_TAG}",
                            "level": lvl,
                            "institution": f"National Institute {idx + 1}",
                            "field_of_study": "General Studies",
                            "year_completed": 2010 + idx,
                        },
                    )

                # 9. OccupationSkill (6 rows)
                for idx, r_idx in enumerate((0, 4, 5, 11, 17, 22)):
                    occ = REFUGEES[r_idx][10] or "General Labor"
                    _insert_row(
                        cur,
                        "g2p_register_occupation_skills",
                        cols_cache,
                        {
                            "internal_record_id": _uid(f"occ-{idx}"),
                            "link_internal_record_id": ref_ids[r_idx],
                            "record_name": f"{occ}",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"{occ} Vocational {DEMO_TAG}",
                            "occupation": occ,
                            "skill": f"{occ} Operations",
                            "years_of_experience": 3 + idx,
                        },
                    )
    finally:
        conn.close()

    print(
        f"[refugee-demo] Seeded {len(hh_ids)} households and {len(ref_ids)} refugees "
        f"using {len(geo_units)} MDS geo unit(s)."
    )


if __name__ == "__main__":
    main()
