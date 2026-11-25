# Refugee Registry — Data Model (Uganda Mandatory Attributes)

Generated from `refugee-extension/src/openg2p_registry_refugee_extension/register_domain/models/` and `meta_data/register-metadata/g2p_register_sections.sql`, aligned to the **Mandatory** attributes in `Uganda_Refugee_Data_Attributes.xlsx` (55 attributes implemented; 3 biometrics `C01, C02, C05` out of scope; Conditional/Recommended/Optional attributes omitted from forms while preserving legacy DB columns).

## Registers Overview

| Register | Purpose | Parent | ID Prefix | UI Status | Fixed UUID |
|---|---|---|---|---|---|
| `Household` | `REGISTER` | `NULL` | `HH-` | Active | `a0000000-0000-0000-0000-000000000001` |
| `Refugee` | `REGISTER` | `NULL` | `RF-` | Active | `a0000000-0000-0000-0000-000000000002` |
| `IdentityDocument` | `TABLE` | `Refugee` | — | Active | `a0000000-0000-0000-0000-000000000003` |
| `SpecificNeeds` | `TABLE` | `Refugee` | — | Active | `a0000000-0000-0000-0000-000000000005` |
| `DisplacementHistory` | `TABLE` | `Refugee` | — | Hidden (`is_active=FALSE`) | `a0000000-0000-0000-0000-000000000004` |
| `Relative` | `TABLE` | `Refugee` | — | Hidden (`is_active=FALSE`) | `a0000000-0000-0000-0000-000000000006` |
| `Address` | `TABLE` | `Refugee` | — | Hidden (`is_active=FALSE`) | `a0000000-0000-0000-0000-000000000007` |
| `EducationRecord` | `TABLE` | `Refugee` | — | Hidden (`is_active=FALSE`) | `a0000000-0000-0000-0000-000000000008` |
| `OccupationSkill` | `TABLE` | `Refugee` | — | Hidden (`is_active=FALSE`) | `a0000000-0000-0000-0000-000000000009` |

## 1. Household (`g2p_register_households`)
- **Tab**: `household_overview_tab` ("Household Composition")
- **Sections**: `household_header_section_01`, `household_info_section_01`, `household_location_section_02`
- **Uganda Mandatory Fields**:
  - `functional_record_id` (`A01`, `HH-...`), `registration_date` (`A02`), `entry_point` (`A04`, DS `ENTRY_POINT`), `registration_site` (`A05`, DS `REGISTRATION_SITE`), `registering_officer_id` (`A06`)
  - `head_of_household_id` (`F01`), `group_size` (`F03`), `dependency_ratio` (`F04`), `is_female_headed` (`F05`), `is_child_headed` (`F06`)
  - `host_district` (`G01`, DS `HOST_DISTRICT`), `settlement_location` (`G02`, DS `SETTLEMENT_LOCATION`), `zone_cluster` (`G03`, DS `ZONE_CLUSTER`), `village_block` (`G04`, DS `VILLAGE_BLOCK`)
  - `main_income_source` (`L01`, DS `INCOME_SOURCE`), `working_age_earners` (`L02`)
  - `assistance_category` (`M01`, DS `ASSISTANCE_CATEGORY`), `vulnerability_score` (`M02`, 0–100), `is_new_arrival` (`M03`), `new_arrival_end_date` (`M03`), `programmes_enrolled` (`M04`, DS `PROGRAMME`), `enrolment_date` / `exit_date` / `exit_reason` (`M05`, DS `EXIT_REASON`)
  - `delivery_modality` (`N01`, DS `DELIVERY_MODALITY`), `delivery_mechanism` (`N01`, DS `DELIVERY_MECHANISM`), `primary_recipient_id` (`N06`), `food_distribution_point` (`N08`, DS `FOOD_DISTRIBUTION_POINT`), `entitlement_amount` & `entitlement_currency` (`N09`, `UGX`/`USD`)
  - `payment_cycle` (`O01`, `YYYY-MM`), `payment_status` (`O03`, DS `PAYMENT_STATUS`), `transaction_reference` & `transaction_date` (`O04`)
  - `lifecycle_status` (`Q01`, DS `REFUGEE_RECORD_STATUS`), `last_updated_at` & `last_updated_by` (`Q04`)

## 2. Refugee (`g2p_register_refugees`)
- **Active Tabs**: `refugee_overview_tab` ("Personal Identity"), `refugee_household_link_tab`, `refugee_documents_tab`, `refugee_specific_needs_tab`
- **Uganda Mandatory Fields**:
  - `functional_record_id` (`D01`, `RF-...`), `link_internal_record_id` (Household lookup)
  - `last_name` (`B01`, uppercased), `given_name` (`B02`), `gender` (`B04`, DS `REFUGEE_GENDER`: `MALE`, `FEMALE`), `birth_date` (`B05`), `is_birth_date_estimated` (`B06`), `place_of_birth` (`B07`), `country_of_origin` (`B08`, DS `COUNTRY_OF_ORIGIN`), `nationality` (`B09`, DS `NATIONALITY`), `marital_status` (`B10`, DS `REFUGEE_MARITAL_STATUS`), `languages_known` (`B11`, DS `LANGUAGE`), `arrival_date` (`A03`)
  - `legal_status` (`E01`, DS `LEGAL_STATUS`), `rsd_application_date` (`E03`), `security_screening_status` (`E07`, DS `SECURITY_SCREENING`)
  - `relationship_to_group` (`F02`, DS `REFUGEE_RELATIONSHIP_TO_GROUP`), `presence_status` (`F07`, DS `PRESENCE_STATUS`)
  - `unaccompanied_separated_status` (`I02`, DS `UNACCOMPANIED_CHILD`)
  - Washington Group Short Set (`J01` x6, DS `WASHINGTON_GROUP_ANSWER`): `wg_seeing`, `wg_hearing`, `wg_walking`, `wg_remembering`, `wg_self_care`, `wg_communicating`; `has_serious_medical_condition` (`J02`)
  - `programmes_enrolled` (`M04`), `enrolment_date` / `exit_date` / `exit_reason` (`M05`)
  - `auth_result` (`O02`, DS `AUTH_RESULT`)
  - `informed_consent_given` & `informed_consent_date` (`P01`), `partner_data_sharing_consent` (`P02`, DS `PARTNER_CONSENT`)
  - `lifecycle_status` (`Q01`, DS `REFUGEE_RECORD_STATUS`), `duplicate_check_result` (`Q03`, DS `DUPLICATE_CHECK`), `last_updated_at` & `last_updated_by` (`Q04`)

## 3. Active Sub-Register Tables (`master_register_id = Refugee`)
- **IdentityDocument (`g2p_register_identity_documents`)**: `document_type` (DS `IDENTITY_DOCUMENT_TYPE`), `document_number` (`D01`), `issue_date`, `expiry_date`.
- **SpecificNeeds (`g2p_register_specific_needs`)**: `need_category` (`I01`, DS `SPECIFIC_NEED_CATEGORY` — 11 UNHCR categories), `date_identified`, `notes`.
