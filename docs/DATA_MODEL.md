# Refugee Registry — Data Model

Generated from `refugee-extension/src/openg2p_registry_refugee_extension/register_domain/models/` and `meta_data/register-metadata/g2p_register_sections.sql`.

## Registers Overview

| Register | Purpose | Parent | ID Prefix | Fixed UUID |
|---|---|---|---|---|
| `Household` | `REGISTER` | `NULL` | `HH-` | `a0000000-0000-0000-0000-000000000001` |
| `Refugee` | `REGISTER` | `NULL` | `RF-` | `a0000000-0000-0000-0000-000000000002` |
| `IdentityDocument` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000003` |
| `DisplacementHistory` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000004` |
| `SpecificNeeds` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000005` |
| `Relative` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000006` |
| `Address` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000007` |
| `EducationRecord` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000008` |
| `OccupationSkill` | `TABLE` | `Refugee` | — | `a0000000-0000-0000-0000-000000000009` |

## 1. Household (`g2p_register_households`)
- **Tab**: `household_overview_tab` ("Household Overview")
- **Sections**: `household_header_section_01`, `household_info_section_01`, `household_location_section_02`
- **Fields**:
  - `functional_record_id` (`str`, platform-minted `HH-...` Unique Group ID)
  - `group_size` (`int`, required)
  - `number_of_male` (`int`)
  - `number_of_female` (`int`)
  - `number_of_children` (`int`)
  - `date_of_arrival` (`date`)
  - `registration_date` (`date`)
  - `legal_status` (`LegalStatusEnum`, DS `LEGAL_STATUS`: `REFUGEE`, `ASYLUM_SEEKER`, `INTERNALLY_DISPLACED`, `RETURNEE`, `STATELESS`, `HOST_COMMUNITY`, `OTHER`)
  - `country_of_origin` (`str`, DS `COUNTRY_OF_ORIGIN`: `ETH`, `ERI`, `SOM`, `SDN`, `SSD`, `YEM`, `SYR`, `COD`, `UGA`, `KEN`, `DJI`)
  - `current_country_of_asylum_address` (`text`)
  - `phone_number` (`str`)
  - `consent_or_prohibition_to_share_information` (`bool`, label: "Consent recorded (information only)")
  - Inherited `G2PGeo`: `geo_lowest_level_value_id`, `geo_code_hierarchy_json`, `address_line_1`, `address_line_2`, `postal_code`, `country_code`, `latitude`, `longitude`, `altitude`, `plus_code`

## 2. Refugee (`g2p_register_refugees`)
- **Tabs**: `refugee_overview_tab`, `refugee_household_link_tab`, `refugee_documents_tab`, `refugee_displacement_tab`, `refugee_specific_needs_tab`, `refugee_relatives_tab`, `refugee_addresses_tab`, `refugee_education_tab`, `refugee_occupation_tab`
- **Fields**:
  - `functional_record_id` (`str`, platform-minted `RF-...` Unique Individual ID)
  - `link_internal_record_id` (`str`, lookup to `Household`)
  - `record_image_document_id` (`text`, photo)
  - Inherited `G2PPerson`: `prefix` (DS `PREFIX`: `MR`, `MRS`, `MISS`, `MS`), `first_name`, `middle_name`, `last_name`, `given_name`, `suffix`, `gender` (DS `REFUGEE_GENDER`: `MALE`, `FEMALE`, `OTHERS`, `UNKNOWN`), `birth_date`, `marital_status` (DS `MARITAL_STATUS`: `SINGLE`, `MARRIED`, `WIDOWED`, `DIVORCED`, `SEPARATED`, `UNKNOWN`)
  - `place_of_birth` (`str`)
  - `relationship_to_group` (`RelationshipToGroupEnum`, DS `REFUGEE_RELATIONSHIP_TO_GROUP`: `SELF`, `SPOUSE`, `CHILD`, `PARENT`, `SIBLING`, `OTHER_RELATIVE`, `NON_RELATIVE`)
  - `country_of_origin` (`str`, DS `COUNTRY_OF_ORIGIN`: 11 countries)
  - `fathers_name` (`str`), `mothers_name` (`str`)
  - `highest_education_level` (`HighestEducationLevelEnum`, DS `EDUCATION_LEVEL`: `ILLITERATE`, `CAN_READ_AND_WRITE`, `NON_FORMAL`, `NEVER_ATTEND`, `BASIC`, `PRIMARY`, `INTERMEDIARY`, `SECONDARY`, `TERTIARY`, `HIGHER_EDUCATION`)
  - `last_occupation` (`str`)
  - `religion` (`ReligionEnum`, DS `RELIGION`: `CHRISTIANITY`, `ISLAM`, `TRADITIONAL`, `HINDUISM`, `BUDDHISM`, `OTHER`, `NONE`, `PREFER_NOT_TO_SAY`)
  - `languages_known` (`JSONB list[str]`, DS `LANGUAGE`: `EN`, `AM`, `TI`, `SO`, `AR`, `OM`, `FR`, `SW`, `KU`, `APD`)

## 3. Sub-Register Tables (`master_register_id = Refugee`)
- **IdentityDocument (`g2p_register_identity_documents`)**: `document_type` (DS `IDENTITY_DOCUMENT_TYPE`: `NATIONAL_ID`, `PASSPORT`, `REFUGEE_ID`, `ASYLUM_SEEKER_CERTIFICATE`, `RESIDENCE_PERMIT`, `BIRTH_CERTIFICATE`, `DRIVING_LICENSE`, `TRAVEL_DOCUMENT`, `FAMILY_BOOKLET`, `OTHER`), `document_number` (`str`), `issuer_type` (DS `DOCUMENT_ISSUER_TYPE`: `NATIONAL_GOVERNMENT`, `REGIONAL_GOVERNMENT`, `IMMIGRATION_AUTHORITY`, `REFUGEE_AUTHORITY`, `UNHCR`, `EMBASSY`, `CONSULATE`, `POLICE`, `OTHER`), `issue_date` (`date`), `expiry_date` (`date`).
- **DisplacementHistory (`g2p_register_displacement_histories`)**: `reasons_for_unwillingness_or_inability_to_return` (`text`), `travel_details` (`text`), `departure_date` (`date`), `transit_countries` (`text`).
- **SpecificNeeds (`g2p_register_specific_needs`)**: `need_category` (DS `SPECIFIC_NEED_CATEGORY`: 14 values), `severity` (DS `SPECIFIC_NEED_SEVERITY`: `LOW`, `MODERATE`, `HIGH`, `CRITICAL`), `date_identified` (`date`), `support_required` (`text`), `notes` (`text`).
- **Relative (`g2p_register_relatives`)**: `relationship` (DS `RELATIONSHIP_TO_HEAD`: `SPOUSE`, `CHILD`, `PARENT`, `SIBLING`, `OTHER_RELATIVE`, `NON_RELATIVE`), `full_name` (`str`), `date_of_birth` (`date`), `location_or_status` (`text`).
- **Address (`g2p_register_addresses`)**: `address_type` (DS `REFUGEE_ADDRESS_TYPE`: `CAMP`, `SETTLEMENT`, `URBAN`, `RURAL`, `TEMPORARY_SHELTER`, `TRANSIT_CENTER`, `HOST_COMMUNITY`, `COUNTRY_OF_ASYLUM`, `COUNTRY_OF_ORIGIN`, `OTHER`), `address_line_1` (`str`), `address_line_2` (`str`), `country` (`str`, DS `COUNTRY`: 11 countries).
- **EducationRecord (`g2p_register_education_records`)**: `level` (DS `EDUCATION_LEVEL`), `institution` (`str`), `field_of_study` (`str`), `year_completed` (`int`).
- **OccupationSkill (`g2p_register_occupation_skills`)**: `occupation` (`str`), `skill` (`str`), `years_of_experience` (`int`).
