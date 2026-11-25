# Refugee Registry — Data Model (Uganda Category-per-Tab Layout)

Generated from `refugee-extension/src/openg2p_registry_refugee_extension/register_domain/models/` and `meta_data/register-metadata/`. Scope: 55 non-biometric `Mandatory` attributes from `Uganda_Refugee_Data_Attributes.xlsx` (`C01`, `C02`, `C05` biometrics out of scope). Legacy DB columns and non-mandatory sub-registers (`DisplacementHistory`, `Relative`, `Address`, `EducationRecord`, `OccupationSkill`) are preserved in PostgreSQL and hidden in the UI.

## Household Register (`g2p_register_households`, `a0000000-0000-0000-0000-000000000001`)

| Order | Tab (`tab_id`) | Label | Section(s) | Attribute IDs & Fields |
|---|---|---|---|---|
| 1 | `household_overview_tab` | Household Composition | `household_header_section_01`, `household_info_section_01` | `F01` `head_of_household_id`, `F03` `group_size` (RO), `F04` `dependency_ratio` (RO), `F05` `is_female_headed` (RO), `F06` `is_child_headed` (RO) |
| 2 | `household_case_registration_tab` | Case & Registration | `household_case_registration_section_01` | `A01` `functional_record_id` (RO), `A02` `registration_date`, `A04` `entry_point`, `A05` `registration_site`, `A06` `registering_officer_id` (RO) |
| 3 | `household_location_tab` | Location & Settlement | `household_location_section_02` | `G01` `host_district`, `G02` `settlement_location`, `G03` `zone_cluster`, `G04` `village_block`, core `geo_hierarchy` |
| 4 | `household_livelihoods_tab` | Livelihoods | `household_livelihoods_section_01` | `L01` `main_income_source`, `L02` `working_age_earners` |
| 5 | `household_targeting_tab` | Targeting & Eligibility | `household_targeting_section_01` | `M01` `assistance_category`, `M02` `vulnerability_score` (RO), `M03` `is_new_arrival` + `new_arrival_end_date`, `M04` `programmes_enrolled`, `M05` `enrolment_date` + `exit_date` + `exit_reason` |
| 6 | `household_payment_tab` | Payment & Delivery | `household_payment_section_01` | `N01` `delivery_modality` + `delivery_mechanism`, `N06` `primary_recipient_id`, `N08` `food_distribution_point`, `N09` `entitlement_amount` (RO) + `entitlement_currency` (RO) |
| 7 | `household_distribution_tab` | Distribution & Transactions | `household_distribution_section_01` | `O01` `payment_cycle`, `O03` `payment_status`, `O04` `transaction_reference` + `transaction_date` |
| 8 | `household_lifecycle_tab` | Record Lifecycle | `household_lifecycle_section_01` | `Q01` `lifecycle_status`, `Q04` `last_updated_at` (RO) + `last_updated_by` (RO) |

## Refugee Register (`g2p_register_refugees`, `a0000000-0000-0000-0000-000000000002`)

| Order | Tab (`tab_id`) | Label | Section(s) | Attribute IDs & Fields |
|---|---|---|---|---|
| 1 | `refugee_overview_tab` | Personal Identity | `refugee_header_section_01`, `refugee_personal_info_section_01` | `B01` `last_name`, `B02` `given_name`, `B04` `gender`, `B05` `birth_date`, `B06` `is_birth_date_estimated`, `B07` `place_of_birth`, `B08` `country_of_origin`, `B09` `nationality`, `B10` `marital_status`, `B11` `languages_known`, `A03` `arrival_date` |
| 2 | `refugee_documents_tab` | Identity Documents | `refugee_identity_document_section_01` (`IdentityDocument`) | `D01` `document_type`, `document_number`, `issue_date`, `expiry_date` |
| 3 | `refugee_displacement_tab` | Legal Status & RSD | `refugee_legal_status_section_01` | `E01` `legal_status`, `E03` `rsd_application_date`, `E07` `security_screening_status` (RO) |
| 4 | `refugee_household_link_tab` | Household Relationship | `refugee_household_lookup_section_01`, `refugee_household_rel_section_01` | `link_internal_record_id`, `F02` `relationship_to_group`, `F07` `presence_status` |
| 5 | `refugee_specific_needs_tab` | Specific Needs & Protection | `refugee_specific_needs_section_01` (`SpecificNeeds`), `refugee_protection_uasc_section_01` | `I01` `need_category` + `date_identified` + `notes`, `I02` `unaccompanied_separated_status` |
| 6 | `refugee_health_disability_tab` | Health & Disability | `refugee_health_disability_section_01` | `J01` `wg_seeing`, `wg_hearing`, `wg_walking`, `wg_remembering`, `wg_self_care`, `wg_communicating`; `J02` `has_serious_medical_condition` |
| 7 | `refugee_targeting_tab` | Targeting & Eligibility | `refugee_targeting_section_01` | `M04` `programmes_enrolled`, `M05` `enrolment_date` + `exit_date` + `exit_reason` |
| 8 | `refugee_distribution_auth_tab` | Distribution (Authentication) | `refugee_distribution_auth_section_01` | `O02` `auth_result` |
| 9 | `refugee_consent_tab` | Consent & Data Protection | `refugee_consent_section_01` | `P01` `informed_consent_given` + `informed_consent_date`, `P02` `partner_data_sharing_consent` |
| 10 | `refugee_lifecycle_tab` | Record Lifecycle | `refugee_lifecycle_section_01` | `Q01` `lifecycle_status`, `Q03` `duplicate_check_result`, `Q04` `last_updated_at` (RO) + `last_updated_by` (RO) |
