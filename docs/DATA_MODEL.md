# Refugee Registry — Data Model (Uganda Category-per-Tab Layout)

Generated from `refugee-extension/src/openg2p_registry_refugee_extension/register_domain/models/` and `meta_data/register-metadata/`.
Scope: Individual non-biometric `Mandatory` attributes from the Uganda Refugee Data Attributes specification (biometric templates `C01`, `C02`, `C05` out of scope; `record_image_document_id` photo upload supported in **Personal Identity**).

## 1. Registers (`g2p_register_definitions`)

| Register | Purpose | Parent | Functional ID Prefix | Fixed UUID | UI Status |
|---|---|---|---|---|---|
| `Refugee` | `REGISTER` | — | `RF-` (12-digit) | `a0000000-0000-0000-0000-000000000002` | Active (9 tabs) |
| `IdentityDocument` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000003` | Active (`refugee_documents_tab`) |
| `SpecificNeeds` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000005` | Active (`refugee_specific_needs_tab`) |
| `DisplacementHistory` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000004` | Hidden in UI (legacy DB preserved) |
| `Relative` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000006` | Hidden in UI (legacy DB preserved) |
| `Address` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000007` | Hidden in UI (legacy DB preserved) |
| `EducationRecord` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000008` | Hidden in UI (legacy DB preserved) |
| `OccupationSkill` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000009` | Hidden in UI (legacy DB preserved) |

## 2. Refugee Register (`g2p_register_refugees`, 9 Active Tabs)

| Order | Tab (`tab_id`) | Label | Section(s) | Attribute IDs & Fields | Codelist Bindings (`attribute_id`) |
|---|---|---|---|---|---|
| 1 | `refugee_overview_tab` | Personal Identity | `refugee_header_section_01`, `refugee_personal_info_section_01` | `B01` `last_name`, `B02` `given_name`, `B04` `gender`, `B05` `birth_date`, `B06` `is_birth_date_estimated`, `B07` `place_of_birth`, `B08` `country_of_origin`, `B09` `nationality`, `B10` `marital_status`, `B11` `languages_known`, `A03` `arrival_date`, `record_image_document_id` (`Photo`) | `gender` -> `REFUGEE_GENDER`, `country_of_origin` -> `COUNTRY_OF_ORIGIN`, `nationality` -> `NATIONALITY`, `marital_status` -> `REFUGEE_MARITAL_STATUS`, `languages_known` -> `LANGUAGE` |
| 2 | `refugee_documents_tab` | Identity Documents | `refugee_identity_document_section_01` (`IdentityDocument`) | `D01` `document_type`, `document_number`, `issue_date`, `expiry_date` | `document_type` -> `IDENTITY_DOCUMENT_TYPE` |
| 3 | `refugee_displacement_tab` | Legal Status & RSD | `refugee_legal_status_section_01` | `E01` `legal_status`, `E03` `rsd_application_date`, `E07` `security_screening_status` (RO) | `legal_status` -> `LEGAL_STATUS`, `security_screening_status` -> `SECURITY_SCREENING` |
| 4 | `refugee_specific_needs_tab` | Specific Needs & Protection | `refugee_specific_needs_section_01` (`SpecificNeeds`), `refugee_protection_uasc_section_01` | `I01` `need_category` + `date_identified` + `notes`, `I02` `unaccompanied_separated_status` | `need_category` -> `SPECIFIC_NEED_CATEGORY`, `unaccompanied_separated_status` -> `UNACCOMPANIED_CHILD` |
| 5 | `refugee_health_disability_tab` | Health & Disability | `refugee_health_disability_section_01` | `J01` `wg_seeing`, `wg_hearing`, `wg_walking`, `wg_remembering`, `wg_self_care`, `wg_communicating`; `J02` `has_serious_medical_condition` | `wg_*` -> `WASHINGTON_GROUP_ANSWER` |
| 6 | `refugee_targeting_tab` | Targeting & Eligibility | `refugee_targeting_section_01` | `M04` `programmes_enrolled`, `M05` `enrolment_date` + `exit_date` + `exit_reason` | `programmes_enrolled` -> `PROGRAMME`, `exit_reason` -> `EXIT_REASON` |
| 7 | `refugee_distribution_auth_tab` | Distribution (Authentication) | `refugee_distribution_auth_section_01` | `O02` `auth_result` | `auth_result` -> `AUTH_RESULT` |
| 8 | `refugee_consent_tab` | Consent & Data Protection | `refugee_consent_section_01` | `P01` `informed_consent_given` + `informed_consent_date`, `P02` `partner_data_sharing_consent` | `partner_data_sharing_consent` -> `PARTNER_CONSENT` |
| 9 | `refugee_lifecycle_tab` | Record Lifecycle | `refugee_lifecycle_section_01` | `Q01` `lifecycle_status`, `F07` `presence_status`, `Q03` `duplicate_check_result`, `Q04` `last_updated_at` (RO) + `last_updated_by` (RO) | `lifecycle_status` -> `REFUGEE_RECORD_STATUS`, `presence_status` -> `PRESENCE_STATUS`, `duplicate_check_result` -> `DUPLICATE_CHECK` |

## 3. Refugee Intake Form Order (`g2p_intake_form_ui_tab_sections`)

1. `refugee_personal_info_section_01` (Personal Identity — opens first by default, includes `Photo`)
2. `refugee_identity_document_section_01` (Identity Documents)
3. `refugee_legal_status_section_01` (Legal Status & RSD)
4. `refugee_specific_needs_section_01` (Specific Needs)
5. `refugee_protection_uasc_section_01` (Unaccompanied or Separated Child)
6. `refugee_health_disability_section_01` (Health & Disability)
7. `refugee_targeting_section_01` (Targeting & Eligibility)
8. `refugee_distribution_auth_section_01` (Distribution Authentication)
9. `refugee_consent_section_01` (Consent & Data Protection)
10. `refugee_lifecycle_section_01` (Record Lifecycle)
