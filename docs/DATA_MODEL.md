# Refugee Registry — Data Model (Uganda Category-per-Tab Layout)

Generated from `refugee-extension/src/openg2p_registry_refugee_extension/register_domain/models/` and `meta_data/register-metadata/`.
Scope: **55 non-biometric `Mandatory` attributes** from `Uganda_Refugee_Data_Attributes.xlsx` (`C01`, `C02`, `C05` biometrics out of scope).

## 1. Registers (`g2p_register_definitions`)

| Register | Purpose | Parent | Functional ID Prefix | Fixed UUID | UI Status |
|---|---|---|---|---|---|
| `Household` | `REGISTER` | — | `HH-` (10-digit) | `a0000000-0000-0000-0000-000000000001` | Active (8 tabs) |
| `Refugee` | `REGISTER` | — | `RF-` (12-digit) | `a0000000-0000-0000-0000-000000000002` | Active (10 tabs) |
| `IdentityDocument` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000003` | Active (`refugee_documents_tab`) |
| `SpecificNeeds` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000005` | Active (`refugee_specific_needs_tab`) |
| `DisplacementHistory` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000004` | Hidden in UI (legacy DB preserved) |
| `Relative` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000006` | Hidden in UI (legacy DB preserved) |
| `Address` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000007` | Hidden in UI (legacy DB preserved) |
| `EducationRecord` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000008` | Hidden in UI (legacy DB preserved) |
| `OccupationSkill` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000009` | Hidden in UI (legacy DB preserved) |

## 2. Household Register (`g2p_register_households`, 8 Active Tabs)

| Order | Tab (`tab_id`) | Label | Section(s) | Attribute IDs & Fields | Codelist Bindings (`attribute_id`) |
|---|---|---|---|---|---|
| 1 | `household_overview_tab` | Household Composition | `household_header_section_01`, `household_info_section_01` | `F01` `head_of_household_id`, `F03` `group_size` (RO), `F04` `dependency_ratio` (RO), `F05` `is_female_headed` (RO), `F06` `is_child_headed` (RO) | — |
| 2 | `household_case_registration_tab` | Case & Registration | `household_case_registration_section_01` | `A01` `functional_record_id` (RO), `A02` `registration_date`, `A04` `entry_point`, `A05` `registration_site`, `A06` `registering_officer_id` (RO) | `entry_point` -> `ENTRY_POINT`, `registration_site` -> `REGISTRATION_SITE` |
| 3 | `household_location_tab` | Location & Settlement | `household_location_section_02` | `G01` `host_district`, `G02` `settlement_location`, `G03` `zone_cluster`, `G04` `village_block`, core `geo_hierarchy` | `host_district` -> `HOST_DISTRICT`, `settlement_location` -> `SETTLEMENT_LOCATION`, `zone_cluster` -> `ZONE_CLUSTER`, `village_block` -> `VILLAGE_BLOCK` |
| 4 | `household_livelihoods_tab` | Livelihoods | `household_livelihoods_section_01` | `L01` `main_income_source`, `L02` `working_age_earners` | `main_income_source` -> `INCOME_SOURCE` |
| 5 | `household_targeting_tab` | Targeting & Eligibility | `household_targeting_section_01` | `M01` `assistance_category`, `M02` `vulnerability_score` (RO), `M03` `is_new_arrival` + `new_arrival_end_date`, `M04` `programmes_enrolled`, `M05` `enrolment_date` + `exit_date` + `exit_reason` | `assistance_category` -> `ASSISTANCE_CATEGORY`, `programmes_enrolled` -> `PROGRAMME`, `exit_reason` -> `EXIT_REASON` |
| 6 | `household_payment_tab` | Payment & Delivery | `household_payment_section_01` | `N01` `delivery_modality` + `delivery_mechanism`, `N06` `primary_recipient_id`, `N08` `food_distribution_point`, `N09` `entitlement_amount` (RO) + `entitlement_currency` (RO) | `delivery_modality` -> `DELIVERY_MODALITY`, `delivery_mechanism` -> `DELIVERY_MECHANISM`, `food_distribution_point` -> `FOOD_DISTRIBUTION_POINT` |
| 7 | `household_distribution_tab` | Distribution & Transactions | `household_distribution_section_01` | `O01` `payment_cycle`, `O03` `payment_status`, `O04` `transaction_reference` + `transaction_date` | — (enum-backed `PaymentStatusEnum`) |
| 8 | `household_lifecycle_tab` | Record Lifecycle | `household_lifecycle_section_01` | `Q01` `lifecycle_status`, `Q04` `last_updated_at` (RO) + `last_updated_by` (RO) | — (enum-backed `RefugeeRecordStatusEnum`) |

## 3. Refugee Register (`g2p_register_refugees`, 10 Active Tabs)

| Order | Tab (`tab_id`) | Label | Section(s) | Attribute IDs & Fields | Codelist Bindings (`attribute_id`) |
|---|---|---|---|---|---|
| 1 | `refugee_overview_tab` | Personal Identity | `refugee_header_section_01`, `refugee_personal_info_section_01` | `B01` `last_name`, `B02` `given_name`, `B04` `gender`, `B05` `birth_date`, `B06` `is_birth_date_estimated`, `B07` `place_of_birth`, `B08` `country_of_origin`, `B09` `nationality`, `B10` `marital_status`, `B11` `languages_known`, `A03` `arrival_date` | Enum/schema-backed (`RefugeeGenderEnum`, `RefugeeMaritalStatusEnum`) |
| 2 | `refugee_documents_tab` | Identity Documents | `refugee_identity_document_section_01` (`IdentityDocument`) | `D01` `document_type`, `document_number`, `issue_date`, `expiry_date` | `document_type` -> `IDENTITY_DOCUMENT_TYPE` |
| 3 | `refugee_displacement_tab` | Legal Status & RSD | `refugee_legal_status_section_01` | `E01` `legal_status`, `E03` `rsd_application_date`, `E07` `security_screening_status` (RO) | Enum-backed (`LegalStatusEnum`, `SecurityScreeningEnum`) |
| 4 | `refugee_household_link_tab` | Household Relationship | `refugee_household_lookup_section_01`, `refugee_household_rel_section_01` | `link_internal_record_id`, `F02` `relationship_to_group`, `F07` `presence_status` | Enum-backed (`RelationshipToGroupEnum`, `PresenceStatusEnum`) |
| 5 | `refugee_specific_needs_tab` | Specific Needs & Protection | `refugee_specific_needs_section_01` (`SpecificNeeds`), `refugee_protection_uasc_section_01` | `I01` `need_category` + `date_identified` + `notes`, `I02` `unaccompanied_separated_status` | `need_category` -> `SPECIFIC_NEED_CATEGORY`, `unaccompanied_separated_status` -> `UNACCOMPANIED_CHILD` |
| 6 | `refugee_health_disability_tab` | Health & Disability | `refugee_health_disability_section_01` | `J01` `wg_seeing`, `wg_hearing`, `wg_walking`, `wg_remembering`, `wg_self_care`, `wg_communicating`; `J02` `has_serious_medical_condition` | Enum-backed (`WashingtonGroupAnswerEnum`) |
| 7 | `refugee_targeting_tab` | Targeting & Eligibility | `refugee_targeting_section_01` | `M04` `programmes_enrolled`, `M05` `enrolment_date` + `exit_date` + `exit_reason` | Enum/list-backed (`ExitReasonEnum`) |
| 8 | `refugee_distribution_auth_tab` | Distribution (Authentication) | `refugee_distribution_auth_section_01` | `O02` `auth_result` | `auth_result` -> `AUTH_RESULT` |
| 9 | `refugee_consent_tab` | Consent & Data Protection | `refugee_consent_section_01` | `P01` `informed_consent_given` + `informed_consent_date`, `P02` `partner_data_sharing_consent` | — |
| 10 | `refugee_lifecycle_tab` | Record Lifecycle | `refugee_lifecycle_section_01` | `Q01` `lifecycle_status`, `Q03` `duplicate_check_result`, `Q04` `last_updated_at` (RO) + `last_updated_by` (RO) | Enum-backed (`RefugeeRecordStatusEnum`, `DuplicateCheckEnum`) |

## 4. Differences from the Earlier 9-Register Design

1. **UI Sub-Register Consolidation (9 DB tables -> 4 UI-active registers)**:
   - The earlier PRIMES/BIMS-derived design exposed all 7 child `TABLE` registers as separate tabs (`IdentityDocument`, `DisplacementHistory`, `SpecificNeeds`, `Relative`, `Address`, `EducationRecord`, `OccupationSkill`).
   - Under the Uganda Mandatory-only scope, `DisplacementHistory`, `Relative`, `Address`, `EducationRecord`, and `OccupationSkill` have no mandatory attributes; their PostgreSQL tables, ORM classes, and schemas are preserved for platform convention compatibility, while their UI tabs (`refugee_relatives_tab`, `refugee_addresses_tab`, `refugee_education_tab`, `refugee_occupation_tab`, and the old displacement-history section) are removed/hidden from `g2p_register_ui_tabs`.
2. **Category-per-Tab Layout (18 active tabs)**:
   - Replaced the earlier monolithic single-tab Household (`Household Composition`) and Refugee (`Personal Identity`) forms with 8 Household category tabs and 10 Refugee category tabs.
3. **Uganda Mandatory Attribute Model (55 fields)**:
   - Added Uganda-specific fields across `Household` (`entry_point`, `registration_site`, `registering_officer_id`, `host_district`, `settlement_location`, `zone_cluster`, `village_block`, `main_income_source`, `working_age_earners`, `assistance_category`, `vulnerability_score`, `is_new_arrival`, `new_arrival_end_date`, `programmes_enrolled`, `enrolment_date`, `exit_date`, `exit_reason`, `delivery_modality`, `delivery_mechanism`, `primary_recipient_id`, `food_distribution_point`, `entitlement_amount`, `entitlement_currency`, `payment_cycle`, `payment_status`, `transaction_reference`, `transaction_date`, `lifecycle_status`, `last_updated_at`, `last_updated_by`) and `Refugee` (`rsd_application_date`, `security_screening_status`, `presence_status`, `unaccompanied_separated_status`, `wg_seeing..wg_communicating`, `has_serious_medical_condition`, `auth_result`, `informed_consent_given`, `informed_consent_date`, `partner_data_sharing_consent`, `duplicate_check_result`, `lifecycle_status`, `last_updated_at`, `last_updated_by`).
   - Excluded non-mandatory (Conditional/Recommended/Optional) fields and biometrics (`C01`, `C02`, `C05`) from UI forms while keeping legacy DB columns intact.
4. **Refugee Domain Codelists (`data/codelists/refugee/`)**:
   - Replaced the earlier generic codelists with Uganda-aligned domain packs (`ENTRY_POINT`, `REGISTRATION_SITE`, `HOST_DISTRICT`, `SETTLEMENT_LOCATION`, `ZONE_CLUSTER`, `VILLAGE_BLOCK`, `INCOME_SOURCE`, `ASSISTANCE_CATEGORY`, `PROGRAMME`, `EXIT_REASON`, `DELIVERY_MODALITY`, `DELIVERY_MECHANISM`, `FOOD_DISTRIBUTION_POINT`, `IDENTITY_DOCUMENT_TYPE`, `SPECIFIC_NEED_CATEGORY`, `UNACCOMPANIED_CHILD`, `AUTH_RESULT`, `WASHINGTON_GROUP_ANSWER`, `LEGAL_STATUS`, `LANGUAGE`, etc.).
