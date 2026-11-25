#!/usr/bin/env python3
"""Idempotent Uganda-context demo-data loader for Refugee Registry.

Reads geography from the running Master Data Service via mds_client (never its DB),
inspects target columns from information_schema, and upserts 8 households (HH-DEMO-0001..0008),
25 refugees (RF-DEMO-0001..0025), and IdentityDocument/SpecificNeeds rows tagged with
created_by='demo-seeder' and record_status_reason='DEMO'.
"""

from __future__ import annotations

import os
import uuid
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


def _upsert_row(cur, table: str, cols_cache: dict[str, set[str]], row: dict) -> None:
    if table not in cols_cache:
        cols_cache[table] = _table_columns(cur, table)
    valid = cols_cache[table]
    filtered = {k: v for k, v in row.items() if k in valid}
    cols = list(filtered.keys())
    vals = [Json(v) if isinstance(v, (dict, list)) else v for v in filtered.values()]
    col_sql = ", ".join(f'"{c}"' for c in cols)
    ph_sql = ", ".join(["%s"] * len(cols))
    upd_sql = ", ".join(f'"{c}" = EXCLUDED."{c}"' for c in cols if c != "internal_record_id")
    sql = (
        f'INSERT INTO "{table}" ({col_sql}) VALUES ({ph_sql}) '
        f'ON CONFLICT ("internal_record_id") DO UPDATE SET {upd_sql}'
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


# (func_id, reg_date, entry_pt, reg_site, officer, district, settlement, zone, village,
#  income, earners, assist_cat, vuln, new_arr, new_end, progs, mod, mech, fdp, amt, cycle, pay_st, tx_ref, female_head, child_head)
HOUSEHOLDS = [
    ("HH-DEMO-0001", "2024-04-02", "ELEGU", "BIDIBIDI_RECEPTION", "OPM-OFF-014", "YUMBE", "BIDIBIDI", "ZONE_1", "BLOCK_A", "FARMING", 1, "NEW_ARRIVAL_FULL", 62, True, "2025-04-02", ["WFP_GFA", "OPM_NFI"], "IN_KIND_FOOD", "IN_KIND_FOOD", "BIDIBIDI_FDP_1", 180000.0, "2026-11", "COLLECTED", "TX-UG-202611-001", False, False),
    ("HH-DEMO-0002", "2025-01-22", "BUNAGANA", "NAKIVALE_RECEPTION", "OPM-OFF-021", "ISINGIRO", "NAKIVALE", "BASE_CAMP", "VILLAGE_1", "CASUAL_LABOUR", 1, "TARGETED_CASH", 74, True, "2026-01-22", ["UNHCR_CBI", "WFP_GFA"], "CASH", "MOBILE_MONEY", "NAKIVALE_FDP_BASE", 240000.0, "2026-11", "CREDITED", "TX-UG-202611-002", True, False),
    ("HH-DEMO-0003", "2023-09-05", "MPONDWE", "KYANGWALI_RECEPTION", "OPM-OFF-008", "KIKUUBE", "KYANGWALI", "ZONE_2", "BLOCK_B", "BUSINESS", 2, "TARGETED_FOOD", 48, False, None, ["WFP_GFA"], "IN_KIND_FOOD", "IN_KIND_FOOD", "KYANGWALI_FDP_1", 150000.0, "2026-11", "COLLECTED", "TX-UG-202611-003", False, False),
    ("HH-DEMO-0004", "2024-11-18", "CYANIKA", "NAKIVALE_RECEPTION", "OPM-OFF-022", "ISINGIRO", "NAKIVALE", "RUBONDO", "VILLAGE_2", "AID_ONLY", 0, "EXTREMELY_VULNERABLE", 88, True, "2025-11-18", ["UNHCR_CBI", "PROTECTION_ASSISTANCE"], "CASH", "AGENCY_BANKING", "NAKIVALE_FDP_BASE", 320000.0, "2026-11", "SENT", "TX-UG-202611-004", True, False),
    ("HH-DEMO-0005", "2025-02-28", "KAMPALA_DESK", "KAMPALA_OLD_KAMPALA", "OPM-OFF-003", "KAMPALA", "KAMPALA_URBAN", "URBAN_CENTRAL", "CLUSTER_1", "SALARY", 1, "SELF_RELIANT", 25, False, None, ["HEALTH_REFERRAL"], "CASH", "MOBILE_MONEY", "KAMPALA_CASH_POINT", 0.0, "2026-11", "NOT_COLLECTED", "TX-UG-202611-005", False, False),
    ("HH-DEMO-0006", "2024-06-19", "ORABA", "BIDIBIDI_RECEPTION", "OPM-OFF-015", "YUMBE", "BIDIBIDI", "ZONE_3", "BLOCK_C", "FARMING", 1, "TARGETED_CASH", 68, False, None, ["WFP_GFA", "EDUCATION_SUPPORT"], "MIXED", "MOBILE_MONEY", "BIDIBIDI_FDP_2", 210000.0, "2026-11", "COLLECTED", "TX-UG-202611-006", False, False),
    ("HH-DEMO-0007", "2025-03-12", "ELEGU", "ADJUMANI_RECEPTION", "OPM-OFF-031", "ADJUMANI", "ADJUMANI", "ZONE_4", "CLUSTER_2", "NONE", 0, "EXTREMELY_VULNERABLE", 92, True, "2026-03-12", ["WFP_GFA", "PROTECTION_ASSISTANCE"], "VOUCHER", "CASH_IN_HAND", "BIDIBIDI_FDP_1", 260000.0, "2026-11", "CREDITED", "TX-UG-202611-007", False, True),
    ("HH-DEMO-0008", "2024-09-25", "KAMPALA_DESK", "KAMPALA_OLD_KAMPALA", "OPM-OFF-005", "KAMPALA", "KAMPALA_URBAN", "URBAN_CENTRAL", "VILLAGE_3", "REMITTANCES", 1, "TRANSITIONAL", 42, False, None, ["UNHCR_CBI"], "CASH", "MOBILE_MONEY", "KAMPALA_CASH_POINT", 160000.0, "2026-11", "COLLECTED", "TX-UG-202611-008", True, False),
]

# (hh_idx, func_id, given, surname, gender, dob, dob_est, pob, origin, nat, marital, langs, arrival, rel, presence, legal, rsd_dt, screen, uasc, med, wg_see, wg_walk)
REFUGEES = [
    (0, "RF-DEMO-0001", "Deng", "GARANG", "MALE", "1986-04-12", False, "Juba, South Sudan", "SSD", "SSD", "MARRIED", ["JUBA_ARABIC", "DINKA", "ENGLISH"], "2024-03-15", "HEAD", "PRESENT", "RECOGNISED_REFUGEE", "2024-04-02", "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (0, "RF-DEMO-0002", "Nyabol", "GARANG", "FEMALE", "1990-09-21", False, "Bor, South Sudan", "SSD", "SSD", "MARRIED", ["DINKA", "JUBA_ARABIC"], "2024-03-15", "SPOUSE", "PRESENT", "RECOGNISED_REFUGEE", "2024-04-02", "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (0, "RF-DEMO-0003", "Akech", "GARANG", "FEMALE", "2012-06-11", False, "Juba, South Sudan", "SSD", "SSD", "SINGLE", ["DINKA", "ENGLISH"], "2024-03-15", "SON_DAUGHTER", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (0, "RF-DEMO-0004", "Lual", "GARANG", "MALE", "2016-02-03", True, "Yei, South Sudan", "SSD", "SSD", "SINGLE", ["DINKA"], "2024-03-15", "SON_DAUGHTER", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),

    (1, "RF-DEMO-0005", "Chantal", "MUKAMANA", "FEMALE", "1988-03-19", False, "Goma, North Kivu", "COD", "COD", "WIDOWED", ["KISWAHILI", "FRENCH", "LINGALA"], "2025-01-10", "HEAD", "PRESENT", "ASYLUM_SEEKER_PENDING_INTERVIEW", "2025-01-22", "CLEARED", "NO", False, "NO_DIFFICULTY", "SOME_DIFFICULTY"),
    (1, "RF-DEMO-0006", "Patrick", "HABIMANA", "MALE", "2010-11-08", False, "Goma, North Kivu", "COD", "COD", "SINGLE", ["KISWAHILI", "ENGLISH"], "2025-01-10", "SON_DAUGHTER", "PRESENT", "ASYLUM_SEEKER_PENDING_INTERVIEW", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (1, "RF-DEMO-0007", "Grace", "UWASE", "FEMALE", "2015-05-14", False, "Rutshuru, DRC", "COD", "COD", "SINGLE", ["KISWAHILI"], "2025-01-10", "SON_DAUGHTER", "PRESENT", "ASYLUM_SEEKER_PENDING_INTERVIEW", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),

    (2, "RF-DEMO-0008", "Jean-Baptiste", "NSENGIYUMVA", "MALE", "1983-07-25", False, "Bukavu, South Kivu", "COD", "COD", "MARRIED", ["FRENCH", "KISWAHILI", "LINGALA"], "2023-08-20", "HEAD", "PRESENT", "RECOGNISED_REFUGEE", "2023-09-05", "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (2, "RF-DEMO-0009", "Esperance", "NSENGIYUMVA", "FEMALE", "1987-01-18", False, "Bukavu, South Kivu", "COD", "COD", "MARRIED", ["KISWAHILI", "FRENCH"], "2023-08-20", "SPOUSE", "PRESENT", "RECOGNISED_REFUGEE", "2023-09-05", "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (2, "RF-DEMO-0010", "Divine", "NSENGIYUMVA", "FEMALE", "2008-12-01", False, "Bukavu, South Kivu", "COD", "COD", "SINGLE", ["KISWAHILI", "ENGLISH"], "2023-08-20", "SON_DAUGHTER", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (2, "RF-DEMO-0011", "Samuel", "NSENGIYUMVA", "MALE", "2014-08-17", False, "Kyangwali, Uganda", "COD", "COD", "SINGLE", ["KISWAHILI"], "2023-08-20", "SON_DAUGHTER", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),

    (3, "RF-DEMO-0012", "Claudine", "NDUWIMANA", "FEMALE", "1979-02-14", True, "Bujumbura, Burundi", "BDI", "BDI", "SEPARATED", ["KINYARWANDA", "FRENCH", "KISWAHILI"], "2024-11-01", "HEAD", "PRESENT", "RECOGNISED_REFUGEE", "2024-11-18", "CLEARED", "NO", True, "SOME_DIFFICULTY", "A_LOT_OF_DIFFICULTY"),
    (3, "RF-DEMO-0013", "Eric", "NDUWIMANA", "MALE", "2006-05-30", False, "Gitega, Burundi", "BDI", "BDI", "SINGLE", ["KINYARWANDA", "ENGLISH"], "2024-11-01", "SON_DAUGHTER", "TEMPORARILY_ABSENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (3, "RF-DEMO-0014", "Tharcisse", "NTIRANDEKURA", "MALE", "1952-10-10", True, "Ngozi, Burundi", "BDI", "BDI", "WIDOWED", ["KINYARWANDA"], "2024-11-01", "PARENT", "PRESENT", "RECOGNISED_REFUGEE", "2024-11-18", "CLEARED", "NO", True, "A_LOT_OF_DIFFICULTY", "A_LOT_OF_DIFFICULTY"),

    (4, "RF-DEMO-0015", "Abdirahman", "HASSAN", "MALE", "1991-06-09", False, "Mogadishu, Somalia", "SOM", "SOM", "SINGLE", ["SOMALI", "ENGLISH", "ARABIC"], "2025-02-14", "HEAD", "PRESENT", "ASYLUM_SEEKER_LODGED", "2025-02-28", "PENDING", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (4, "RF-DEMO-0016", "Hodan", "HASSAN", "FEMALE", "1996-09-22", False, "Mogadishu, Somalia", "SOM", "SOM", "SINGLE", ["SOMALI", "ENGLISH"], "2025-02-14", "SIBLING", "PRESENT", "ASYLUM_SEEKER_LODGED", "2025-02-28", "PENDING", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),

    (5, "RF-DEMO-0017", "Simon", "LOKU", "MALE", "1984-01-05", False, "Yei, South Sudan", "SSD", "SSD", "MARRIED", ["BARI", "JUBA_ARABIC", "ENGLISH"], "2024-06-05", "HEAD", "PRESENT", "RECOGNISED_REFUGEE", "2024-06-19", "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (5, "RF-DEMO-0018", "Rose", "LOKU", "FEMALE", "1989-11-28", False, "Yei, South Sudan", "SSD", "SSD", "MARRIED", ["BARI", "JUBA_ARABIC"], "2024-06-05", "SPOUSE", "PRESENT", "RECOGNISED_REFUGEE", "2024-06-19", "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (5, "RF-DEMO-0019", "Daniel", "LOKU", "MALE", "2013-03-19", False, "Yei, South Sudan", "SSD", "SSD", "SINGLE", ["BARI", "ENGLISH"], "2024-06-05", "SON_DAUGHTER", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),

    (6, "RF-DEMO-0020", "Gideon", "GATLUAK", "MALE", "2010-08-14", True, "Malakal, South Sudan", "SSD", "SSD", "SINGLE", ["NUER", "JUBA_ARABIC"], "2025-03-01", "HEAD", "PRESENT", "RECOGNISED_REFUGEE", "2025-03-12", "CLEARED", "UNACCOMPANIED", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (6, "RF-DEMO-0021", "Nyakan", "GATLUAK", "FEMALE", "2013-04-02", True, "Malakal, South Sudan", "SSD", "SSD", "SINGLE", ["NUER"], "2025-03-01", "SIBLING", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "SEPARATED", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (6, "RF-DEMO-0022", "Koang", "GATLUAK", "MALE", "2017-01-19", True, "Malakal, South Sudan", "SSD", "SSD", "SINGLE", ["NUER"], "2025-03-01", "SIBLING", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "SEPARATED", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),

    (7, "RF-DEMO-0023", "Halima", "FARAH", "FEMALE", "1982-07-11", False, "Hargeisa, Somalia", "SOM", "SOM", "DIVORCED", ["SOMALI", "ARABIC", "ENGLISH"], "2024-09-12", "HEAD", "PRESENT", "RECOGNISED_REFUGEE", "2024-09-25", "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (7, "RF-DEMO-0024", "Yasmin", "FARAH", "FEMALE", "2007-10-04", False, "Mogadishu, Somalia", "SOM", "SOM", "SINGLE", ["SOMALI", "ENGLISH"], "2024-09-12", "SON_DAUGHTER", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
    (7, "RF-DEMO-0025", "Ibrahim", "FARAH", "MALE", "2011-12-27", False, "Mogadishu, Somalia", "SOM", "SOM", "SINGLE", ["SOMALI", "ENGLISH"], "2024-09-12", "SON_DAUGHTER", "PRESENT", "RECOGNISED_REFUGEE", None, "CLEARED", "NO", False, "NO_DIFFICULTY", "NO_DIFFICULTY"),
]


def main() -> None:
    geo_units = _fetch_geo_units()
    conn = psycopg2.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ.get("PGDATABASE", "refugee_registry_db"),
        user=os.environ.get("PGUSER", "postgres"),
        password=os.environ.get("PGPASSWORD", "postgres"),
    )
    cols_cache: dict[str, set[str]] = {}
    hh_ids: list[str] = []
    ref_ids: list[str] = []
    head_ref_ids: list[str] = []

    try:
        with conn:
            with conn.cursor() as cur:
                # Precompute head refugee IDs per household
                hh_head_map = {}
                for hh_idx, func_id, *_rest in REFUGEES:
                    rel = _rest[11]
                    if rel == "HEAD" and hh_idx not in hh_head_map:
                        hh_head_map[hh_idx] = func_id

                # 1. Households
                for idx, hh in enumerate(HOUSEHOLDS):
                    (
                        func_id, reg_date, entry_pt, reg_site, officer,
                        district, settlement, zone, village, income, earners,
                        assist_cat, vuln, new_arr, new_end, progs, mod, mech,
                        fdp, amt, cycle, pay_st, tx_ref, female_head, child_head,
                    ) = hh
                    hh_id = _uid(func_id)
                    hh_ids.append(hh_id)
                    members = [r for r in REFUGEES if r[0] == idx]
                    group_size = len(members)
                    children = sum(1 for r in members if int(r[5][:4]) >= 2008)
                    dep_ratio = round(children / max(1, group_size - children), 2)
                    geo_id, geo_hier = geo_units[idx % len(geo_units)]
                    head_func = hh_head_map.get(idx, "")
                    _upsert_row(
                        cur,
                        "g2p_register_households",
                        cols_cache,
                        {
                            "internal_record_id": hh_id,
                            "functional_record_id": func_id,
                            "record_name": f"{func_id} {settlement} {district}",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"{func_id} {district} {settlement} {zone} {village} {assist_cat} {tx_ref} {DEMO_TAG}",
                            "registration_date": reg_date,
                            "entry_point": entry_pt,
                            "registration_site": reg_site,
                            "registering_officer_id": officer,
                            "head_of_household_id": head_func,
                            "group_size": group_size,
                            "dependency_ratio": dep_ratio,
                            "is_female_headed": female_head,
                            "is_child_headed": child_head,
                            "host_district": district,
                            "settlement_location": settlement,
                            "zone_cluster": zone,
                            "village_block": village,
                            "main_income_source": income,
                            "working_age_earners": earners,
                            "assistance_category": assist_cat,
                            "vulnerability_score": vuln,
                            "is_new_arrival": new_arr,
                            "new_arrival_end_date": new_end,
                            "programmes_enrolled": progs,
                            "enrolment_date": reg_date,
                            "delivery_modality": mod,
                            "delivery_mechanism": mech,
                            "primary_recipient_id": head_func,
                            "food_distribution_point": fdp,
                            "entitlement_amount": amt,
                            "entitlement_currency": "UGX",
                            "payment_cycle": cycle,
                            "payment_status": pay_st,
                            "transaction_reference": tx_ref,
                            "transaction_date": "2026-11-15",
                            "lifecycle_status": "ACTIVE",
                            "last_updated_at": NOW_TS,
                            "last_updated_by": SEEDER,
                            "geo_lowest_level_value_id": geo_id,
                            "geo_code_hierarchy_json": geo_hier,
                            "country_code": "UG",
                        },
                    )

                # 2. Refugees
                for idx, r in enumerate(REFUGEES):
                    (
                        hh_idx, func_id, given, surname, gender, dob, dob_est,
                        pob, origin, nat, marital, langs, arrival, rel, presence,
                        legal, rsd_dt, screen, uasc, med, wg_see, wg_walk,
                    ) = r
                    ref_id = _uid(func_id)
                    ref_ids.append(ref_id)
                    if rel == "HEAD":
                        head_ref_ids.append(ref_id)
                    hh_id = hh_ids[hh_idx]
                    progs = HOUSEHOLDS[hh_idx][15]
                    reg_date = HOUSEHOLDS[hh_idx][1]
                    rec_name = f"{given} {surname}"
                    search_txt = f"{func_id} {given} {surname} {gender} {origin} {nat} {legal} {' '.join(langs)} {pob} {DEMO_TAG}"
                    _upsert_row(
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
                            "first_name": given,
                            "given_name": given,
                            "last_name": surname,
                            "gender": gender,
                            "birth_date": dob,
                            "is_birth_date_estimated": dob_est,
                            "place_of_birth": pob,
                            "country_of_origin": origin,
                            "nationality": nat,
                            "marital_status": marital,
                            "languages_known": langs,
                            "arrival_date": arrival,
                            "relationship_to_group": rel,
                            "presence_status": presence,
                            "legal_status": legal,
                            "rsd_application_date": rsd_dt,
                            "security_screening_status": screen,
                            "unaccompanied_separated_status": uasc,
                            "has_serious_medical_condition": med,
                            "wg_seeing": wg_see,
                            "wg_hearing": "NO_DIFFICULTY",
                            "wg_walking": wg_walk,
                            "wg_remembering": "NO_DIFFICULTY",
                            "wg_self_care": "NO_DIFFICULTY",
                            "wg_communicating": "NO_DIFFICULTY",
                            "programmes_enrolled": progs,
                            "enrolment_date": reg_date,
                            "auth_result": "FINGERPRINT_OK",
                            "informed_consent_given": True,
                            "informed_consent_date": reg_date,
                            "partner_data_sharing_consent": ["OPM", "UNHCR", "WFP"],
                            "lifecycle_status": "ACTIVE",
                            "duplicate_check_result": "UNIQUE",
                            "last_updated_at": NOW_TS,
                            "last_updated_by": SEEDER,
                        },
                    )

                # 3. IdentityDocument
                doc_types = [
                    "REFUGEE_ID_CARD",
                    "REFUGEE_FAMILY_ATTESTATION",
                    "ASYLUM_REGISTRATION_CARD",
                    "ASYLUM_SEEKER_CERTIFICATE",
                ]
                for idx, ref_id in enumerate(ref_ids[:18]):
                    doc_id = _uid(f"doc-{idx}-1")
                    doc_type = doc_types[idx % len(doc_types)]
                    doc_num = f"UG-DOC-2025-{idx + 1001}"
                    _upsert_row(
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
                            "search_text": f"{doc_type} {doc_num} {DEMO_TAG}",
                            "document_type": doc_type,
                            "document_number": doc_num,
                            "issue_date": "2024-05-01",
                            "expiry_date": "2029-05-01",
                        },
                    )

                # 4. SpecificNeeds
                needs_data = [
                    (11, "SERIOUS_MEDICAL_CONDITION", "Ongoing hypertension and diabetes care"),
                    (13, "OLDER_PERSON_AT_RISK", "Mobility assistance and priority distribution"),
                    (13, "DISABILITY", "Walking aid required"),
                    (19, "UNACCOMPANIED_OR_SEPARATED_CHILD", "Unaccompanied minor in foster care"),
                    (20, "CHILD_AT_RISK", "Separated child under sibling care"),
                    (22, "WOMAN_AT_RISK", "Single female-headed household support"),
                ]
                for idx, (r_idx, cat, notes) in enumerate(needs_data):
                    _upsert_row(
                        cur,
                        "g2p_register_specific_needs",
                        cols_cache,
                        {
                            "internal_record_id": _uid(f"need-{idx}"),
                            "link_internal_record_id": ref_ids[r_idx],
                            "record_name": f"{cat}",
                            "record_status": "ACTIVE",
                            "record_status_reason": DEMO_TAG,
                            "created_by": SEEDER,
                            "created_at": NOW_TS,
                            "last_approved_by": SEEDER,
                            "last_approved_at": NOW_TS,
                            "search_text": f"{cat} {notes} {DEMO_TAG}",
                            "need_category": cat,
                            "date_identified": "2025-02-01",
                            "notes": notes,
                        },
                    )
    finally:
        conn.close()

    print(
        f"Seeded {len(hh_ids)} households, {len(ref_ids)} refugees, "
        f"18 identity documents, 6 specific needs (Uganda mandatory model)."
    )


if __name__ == "__main__":
    main()
