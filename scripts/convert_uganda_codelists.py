#!/usr/bin/env python3
"""Generate Uganda Refugee Data Attributes codelists in OpenG2P Master Data pack format."""

import json
import os
from pathlib import Path

PACK_DIR = Path(
    os.environ.get(
        "REFUGEE_PACK_DIR",
        Path(__file__).resolve().parents[2] / "openg2p-data" / "packs" / "ETH" / "domains" / "refugee",
    )
)

COUNTRIES = [
    ("SSD", "South Sudan"),
    ("COD", "Democratic Republic of the Congo"),
    ("SOM", "Somalia"),
    ("BDI", "Burundi"),
    ("ETH", "Ethiopia"),
    ("ERI", "Eritrea"),
    ("SDN", "Sudan"),
    ("UGA", "Uganda"),
    ("KEN", "Kenya"),
    ("RWA", "Rwanda"),
    ("TZA", "Tanzania"),
    ("YEM", "Yemen"),
    ("SYR", "Syria"),
    ("DJI", "Djibouti"),
]

CODELISTS = {
    "legal_status": {
        "attribute_id": "LEGAL_STATUS",
        "attribute_display": "Legal Status",
        "values": [
            ("ASYLUM_SEEKER_LODGED", "Asylum-seeker - application lodged"),
            ("ASYLUM_SEEKER_PENDING_INTERVIEW", "Asylum-seeker - pending interview"),
            ("ASYLUM_SEEKER_PENDING_APPEAL", "Asylum-seeker - pending appeal"),
            ("RECOGNISED_REFUGEE", "Recognised refugee"),
            ("REJECTED", "Rejected"),
            ("EXCLUDED", "Excluded"),
            ("HOST_COMMUNITY", "Host community member (not applicable)"),
        ],
    },
    "identity_document_type": {
        "attribute_id": "IDENTITY_DOCUMENT_TYPE",
        "attribute_display": "Identity Document Type",
        "values": [
            ("ASYLUM_REGISTRATION_CARD", "Asylum Registration Card (Refugee Desk)"),
            ("ASYLUM_SEEKER_CERTIFICATE", "Asylum-seeker certificate (OPM, 3 months)"),
            ("ASYLUM_CERTIFICATE_PENDING_APPEAL", "Asylum Certificate Pending Review / Appeal"),
            ("REFUGEE_FAMILY_ATTESTATION", "Refugee Family Attestation"),
            ("REFUGEE_ID_CARD", "Refugee ID card (16+, 5 years)"),
            ("NIRA_BIRTH_CERTIFICATE", "NIRA birth certificate"),
            ("REFUGEE_TRAVEL_DOCUMENT", "Refugee travel document"),
            ("COUNTRY_OF_ORIGIN_PASSPORT_ID", "Country-of-origin passport / ID"),
            ("MARRIAGE_CERTIFICATE", "Marriage certificate"),
            ("OTHER", "Other as per government"),
        ],
    },
    "specific_need_category": {
        "attribute_id": "SPECIFIC_NEED_CATEGORY",
        "attribute_display": "Specific Needs Category",
        "values": [
            ("CHILD_AT_RISK", "Child at risk"),
            ("UNACCOMPANIED_OR_SEPARATED_CHILD", "Unaccompanied or separated child"),
            ("DISABILITY", "Disability"),
            ("SERIOUS_MEDICAL_CONDITION", "Serious medical condition"),
            ("OLDER_PERSON_AT_RISK", "Older person at risk"),
            ("SINGLE_PARENT_OR_CAREGIVER", "Single parent or caregiver"),
            ("WOMAN_AT_RISK", "Woman at risk"),
            ("SGBV_SURVIVOR", "SGBV survivor"),
            ("TORTURE_SURVIVOR", "Torture survivor"),
            ("SPECIFIC_LEGAL_PHYSICAL_PROTECTION_NEEDS", "Specific legal & physical protection needs"),
            ("FAMILY_UNITY", "Family unity"),
        ],
    },
    "refugee_relationship_to_group": {
        "attribute_id": "REFUGEE_RELATIONSHIP_TO_GROUP",
        "attribute_display": "Relationship to Head",
        "values": [
            ("HEAD", "Head"),
            ("SPOUSE", "Spouse"),
            ("SON_DAUGHTER", "Son / daughter"),
            ("STEPCHILD", "Stepchild"),
            ("PARENT", "Parent"),
            ("SIBLING", "Sibling"),
            ("GRANDCHILD", "Grandchild"),
            ("NIECE_NEPHEW", "Niece / nephew"),
            ("OTHER_RELATIVE", "Other relative"),
            ("FOSTER_CHILD", "Foster child"),
            ("UNRELATED", "Unrelated"),
        ],
    },
    "refugee_gender": {
        "attribute_id": "REFUGEE_GENDER",
        "attribute_display": "Sex",
        "values": [
            ("MALE", "Male"),
            ("FEMALE", "Female"),
        ],
    },
    "refugee_marital_status": {
        "attribute_id": "REFUGEE_MARITAL_STATUS",
        "attribute_display": "Marital Status",
        "values": [
            ("SINGLE", "Single"),
            ("MARRIED", "Married"),
            ("DIVORCED", "Divorced"),
            ("SEPARATED", "Separated"),
            ("WIDOWED", "Widowed"),
            ("ENGAGED", "Engaged"),
        ],
    },
    "country": {
        "attribute_id": "COUNTRY",
        "attribute_display": "Country",
        "values": COUNTRIES,
    },
    "country_of_origin": {
        "attribute_id": "COUNTRY_OF_ORIGIN",
        "attribute_display": "Country of Origin",
        "values": COUNTRIES,
    },
    "nationality": {
        "attribute_id": "NATIONALITY",
        "attribute_display": "Nationality / Citizenship",
        "values": COUNTRIES + [
            ("STATELESS", "Stateless"),
            ("UNDETERMINED", "Undetermined"),
        ],
    },
    "language": {
        "attribute_id": "LANGUAGE",
        "attribute_display": "Preferred Language(s)",
        "values": [
            ("JUBA_ARABIC", "Juba Arabic"),
            ("BARI", "Bari"),
            ("DINKA", "Dinka"),
            ("NUER", "Nuer"),
            ("KISWAHILI", "Kiswahili"),
            ("LINGALA", "Lingala"),
            ("KINYARWANDA", "Kinyarwanda"),
            ("FRENCH", "French"),
            ("ARABIC", "Arabic"),
            ("ENGLISH", "English"),
            ("SOMALI", "Somali"),
            ("TIGRINYA", "Tigrinya"),
        ],
    },
    "presence_status": {
        "attribute_id": "PRESENCE_STATUS",
        "attribute_display": "Physical Presence Status",
        "values": [
            ("PRESENT", "Present"),
            ("TEMPORARILY_ABSENT", "Temporarily absent"),
            ("LEFT", "Left"),
            ("DECEASED", "Deceased"),
        ],
    },
    "security_screening": {
        "attribute_id": "SECURITY_SCREENING",
        "attribute_display": "Security Screening Cleared",
        "values": [
            ("CLEARED", "Cleared"),
            ("PENDING", "Pending"),
            ("REFERRED", "Referred"),
        ],
    },
    "unaccompanied_child": {
        "attribute_id": "UNACCOMPANIED_CHILD",
        "attribute_display": "Unaccompanied or Separated Child",
        "values": [
            ("UNACCOMPANIED", "Unaccompanied"),
            ("SEPARATED", "Separated"),
            ("NO", "No"),
        ],
    },
    "washington_group_answer": {
        "attribute_id": "WASHINGTON_GROUP_ANSWER",
        "attribute_display": "Washington Group Difficulty Level",
        "values": [
            ("NO_DIFFICULTY", "No difficulty"),
            ("SOME_DIFFICULTY", "Some difficulty"),
            ("A_LOT_OF_DIFFICULTY", "A lot of difficulty"),
            ("CANNOT_DO_AT_ALL", "Cannot do at all"),
        ],
    },
    "income_source": {
        "attribute_id": "INCOME_SOURCE",
        "attribute_display": "Main Source of Income",
        "values": [
            ("FARMING", "Farming"),
            ("CASUAL_LABOUR", "Casual labour"),
            ("BUSINESS", "Business"),
            ("SALARY", "Salary"),
            ("REMITTANCES", "Remittances"),
            ("AID_ONLY", "Aid only"),
            ("NONE", "None"),
        ],
    },
    "delivery_modality": {
        "attribute_id": "DELIVERY_MODALITY",
        "attribute_display": "Delivery Modality",
        "values": [
            ("CASH", "Cash"),
            ("IN_KIND_FOOD", "In-kind food"),
            ("VOUCHER", "Voucher"),
            ("MIXED", "Mixed"),
        ],
    },
    "delivery_mechanism": {
        "attribute_id": "DELIVERY_MECHANISM",
        "attribute_display": "Delivery Mechanism",
        "values": [
            ("MOBILE_MONEY", "Mobile money"),
            ("AGENCY_BANKING", "Agency banking / bank account"),
            ("CASH_IN_HAND", "Cash in hand"),
            ("IN_KIND_FOOD", "In-kind food"),
        ],
    },
    "auth_result": {
        "attribute_id": "AUTH_RESULT",
        "attribute_display": "Authentication Method & Result",
        "values": [
            ("FINGERPRINT_OK", "Fingerprint OK"),
            ("IRIS_OK", "Iris OK"),
            ("MANUAL_OVERRIDE", "Manual override"),
            ("FAILED", "Failed"),
        ],
    },
    "payment_status": {
        "attribute_id": "PAYMENT_STATUS",
        "attribute_display": "Payment / Distribution Status",
        "values": [
            ("SENT", "Sent"),
            ("CREDITED", "Credited"),
            ("COLLECTED", "Collected"),
            ("FAILED", "Failed"),
            ("REVERSED", "Reversed"),
            ("NOT_COLLECTED", "Not collected"),
        ],
    },
    "refugee_record_status": {
        "attribute_id": "REFUGEE_RECORD_STATUS",
        "attribute_display": "Record Status",
        "values": [
            ("ACTIVE", "Active"),
            ("INACTIVE", "Inactive"),
            ("SUSPENDED", "Suspended"),
            ("CLOSED", "Closed"),
        ],
    },
    "duplicate_check": {
        "attribute_id": "DUPLICATE_CHECK",
        "attribute_display": "Duplicate Check Result",
        "values": [
            ("UNIQUE", "Unique"),
            ("POSSIBLE_DUPLICATE", "Possible duplicate"),
            ("CONFIRMED_DUPLICATE", "Confirmed duplicate"),
        ],
    },
    "partner_consent": {
        "attribute_id": "PARTNER_CONSENT",
        "attribute_display": "Consent for Data Sharing with Partners",
        "values": [
            ("OPM", "OPM"),
            ("UNHCR", "UNHCR"),
            ("WFP", "WFP"),
            ("FSPS", "FSPs"),
            ("IMPLEMENTING_PARTNERS", "Implementing partners"),
        ],
    },
    # Illustrative Uganda-context lists (government/settlement-specific in Uganda model)
    "entry_point": {
        "attribute_id": "ENTRY_POINT",
        "attribute_display": "Point of Entry / Reception Centre",
        "values": [
            ("ELEGU", "Elegu Border Point"),
            ("ORABA", "Oraba Border Point"),
            ("BUNAGANA", "Bunagana Border Point"),
            ("MPONDWE", "Mpondwe Border Point"),
            ("CYANIKA", "Cyanika Border Point"),
            ("KAMPALA_DESK", "Kampala Refugee Desk"),
            ("OTHER", "Other"),
        ],
    },
    "registration_site": {
        "attribute_id": "REGISTRATION_SITE",
        "attribute_display": "Registration Site / Office",
        "values": [
            ("BIDIBIDI_RECEPTION", "Bidibidi Reception Centre"),
            ("NAKIVALE_RECEPTION", "Nakivale Reception Centre"),
            ("KYANGWALI_RECEPTION", "Kyangwali Reception Centre"),
            ("KAMPALA_OLD_KAMPALA", "Old Kampala OPM Desk"),
            ("ADJUMANI_RECEPTION", "Adjumani Reception Centre"),
            ("OTHER", "Other"),
        ],
    },
    "host_district": {
        "attribute_id": "HOST_DISTRICT",
        "attribute_display": "Host District",
        "values": [
            ("YUMBE", "Yumbe"),
            ("ISINGIRO", "Isingiro"),
            ("KIKUUBE", "Kikuube"),
            ("KAMPALA", "Kampala"),
            ("ADJUMANI", "Adjumani"),
            ("TEREGO", "Terego"),
            ("MADI_OKOLLO", "Madi-Okollo"),
            ("KYEGEGWA", "Kyegegwa"),
            ("KAMWENGE", "Kamwenge"),
            ("KIRYANDONGO", "Kiryandongo"),
        ],
    },
    "settlement_location": {
        "attribute_id": "SETTLEMENT_LOCATION",
        "attribute_display": "Settlement or Urban Location",
        "values": [
            ("BIDIBIDI", "Bidibidi Settlement"),
            ("NAKIVALE", "Nakivale Settlement"),
            ("KYANGWALI", "Kyangwali Settlement"),
            ("KAMPALA_URBAN", "Kampala Urban"),
            ("ADJUMANI", "Adjumani Settlements"),
            ("RHINO_CAMP", "Rhino Camp"),
            ("IMVEPI", "Imvepi Settlement"),
            ("KYAKA_II", "Kyaka II Settlement"),
            ("RWAMWANJA", "Rwamwanja Settlement"),
            ("KIRYANDONGO", "Kiryandongo Settlement"),
        ],
    },
    "zone_cluster": {
        "attribute_id": "ZONE_CLUSTER",
        "attribute_display": "Zone / Cluster",
        "values": [
            ("ZONE_1", "Zone 1"),
            ("ZONE_2", "Zone 2"),
            ("ZONE_3", "Zone 3"),
            ("ZONE_4", "Zone 4"),
            ("ZONE_5", "Zone 5"),
            ("BASE_CAMP", "Base Camp"),
            ("RUBONDO", "Rubondo"),
            ("KASHONGA", "Kashonga"),
            ("URBAN_CENTRAL", "Urban Central"),
        ],
    },
    "village_block": {
        "attribute_id": "VILLAGE_BLOCK",
        "attribute_display": "Village / Block",
        "values": [
            ("BLOCK_A", "Block A"),
            ("BLOCK_B", "Block B"),
            ("BLOCK_C", "Block C"),
            ("VILLAGE_1", "Village 1"),
            ("VILLAGE_2", "Village 2"),
            ("VILLAGE_3", "Village 3"),
            ("CLUSTER_1", "Cluster 1"),
            ("CLUSTER_2", "Cluster 2"),
        ],
    },
    "assistance_category": {
        "attribute_id": "ASSISTANCE_CATEGORY",
        "attribute_display": "Assistance Category",
        "values": [
            ("NEW_ARRIVAL_FULL", "New Arrival - Full Ration"),
            ("EXTREMELY_VULNERABLE", "Extremely Vulnerable Household"),
            ("TARGETED_FOOD", "Targeted Food Assistance"),
            ("TARGETED_CASH", "Targeted Cash Assistance"),
            ("TRANSITIONAL", "Transitional Support"),
            ("SELF_RELIANT", "Self-Reliant / No Regular Ration"),
        ],
    },
    "programme": {
        "attribute_id": "PROGRAMME",
        "attribute_display": "Programme(s) Enrolled",
        "values": [
            ("WFP_GFA", "WFP General Food Assistance"),
            ("UNHCR_CBI", "UNHCR Cash-Based Intervention"),
            ("OPM_NFI", "OPM Core Relief Items"),
            ("HEALTH_REFERRAL", "Health & Medical Referral"),
            ("EDUCATION_SUPPORT", "Education Support"),
            ("PROTECTION_ASSISTANCE", "Protection Assistance"),
        ],
    },
    "exit_reason": {
        "attribute_id": "EXIT_REASON",
        "attribute_display": "Exit Reason",
        "values": [
            ("GRADUATED", "Graduated"),
            ("RELOCATED", "Relocated"),
            ("REPATRIATED", "Repatriated"),
            ("RESETTLED", "Resettled"),
            ("DECEASED", "Deceased"),
            ("INACTIVE", "Inactive"),
            ("INELIGIBLE", "Ineligible"),
        ],
    },
    "food_distribution_point": {
        "attribute_id": "FOOD_DISTRIBUTION_POINT",
        "attribute_display": "Food Distribution / Cash-Out Point",
        "values": [
            ("BIDIBIDI_FDP_1", "Bidibidi Zone 1 FDP"),
            ("BIDIBIDI_FDP_2", "Bidibidi Zone 2 FDP"),
            ("NAKIVALE_FDP_BASE", "Nakivale Base Camp FDP"),
            ("KYANGWALI_FDP_1", "Kyangwali Maratatu FDP"),
            ("KAMPALA_CASH_POINT", "Kampala Urban Cash-Out Point"),
        ],
    },
}


def main() -> None:
    PACK_DIR.mkdir(parents=True, exist_ok=True)
    for filename, spec in CODELISTS.items():
        attr_id = spec["attribute_id"]
        payload = {
            "attribute_id": attr_id,
            "attribute_code": attr_id,
            "attribute_display": spec["attribute_display"],
            "is_hierarchical": False,
            "values": [
                {
                    "value_id": code,
                    "value_code": code,
                    "value_display": label,
                    "sort_order": idx,
                    "display_i18n": {},
                }
                for idx, (code, label) in enumerate(spec["values"], start=1)
            ],
        }
        out_path = PACK_DIR / f"{filename}.json"
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(CODELISTS)} codelists to {PACK_DIR}")


if __name__ == "__main__":
    main()
