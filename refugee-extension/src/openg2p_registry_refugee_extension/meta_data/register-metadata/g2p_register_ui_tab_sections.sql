-- Refugee Registry UI Tab Sections (idempotent)
INSERT INTO "public"."g2p_register_ui_tab_sections" ("tab_section_id","register_id","tab_id","section_id","section_order") VALUES
('b0000000-0000-0000-0000-000000000001','a0000000-0000-0000-0000-000000000001','household_overview_tab','household_header_section_01',5),
('b0000000-0000-0000-0000-000000000002','a0000000-0000-0000-0000-000000000001','household_overview_tab','household_info_section_01',10),
('b0000000-0000-0000-0000-000000000003','a0000000-0000-0000-0000-000000000001','household_overview_tab','household_location_section_02',20),
('b0000000-0000-0000-0000-000000000004','a0000000-0000-0000-0000-000000000002','refugee_overview_tab','refugee_header_section_01',5),
('b0000000-0000-0000-0000-000000000005','a0000000-0000-0000-0000-000000000002','refugee_overview_tab','refugee_personal_info_section_01',10),
('b0000000-0000-0000-0000-000000000006','a0000000-0000-0000-0000-000000000002','refugee_household_link_tab','refugee_household_lookup_section_01',10),
('b0000000-0000-0000-0000-000000000007','a0000000-0000-0000-0000-000000000002','refugee_documents_tab','refugee_identity_document_section_01',10),
('b0000000-0000-0000-0000-000000000008','a0000000-0000-0000-0000-000000000002','refugee_displacement_tab','refugee_displacement_history_section_01',10),
('b0000000-0000-0000-0000-000000000009','a0000000-0000-0000-0000-000000000002','refugee_specific_needs_tab','refugee_specific_needs_section_01',10),
('b0000000-0000-0000-0000-000000000010','a0000000-0000-0000-0000-000000000002','refugee_relatives_tab','refugee_relative_section_01',10),
('b0000000-0000-0000-0000-000000000011','a0000000-0000-0000-0000-000000000002','refugee_addresses_tab','refugee_address_section_01',10),
('b0000000-0000-0000-0000-000000000012','a0000000-0000-0000-0000-000000000002','refugee_education_tab','refugee_education_record_section_01',10),
('b0000000-0000-0000-0000-000000000013','a0000000-0000-0000-0000-000000000002','refugee_occupation_tab','refugee_occupation_skill_section_01',10)
ON CONFLICT ("tab_section_id") DO UPDATE SET
    "register_id" = EXCLUDED."register_id",
    "tab_id" = EXCLUDED."tab_id",
    "section_id" = EXCLUDED."section_id",
    "section_order" = EXCLUDED."section_order";
