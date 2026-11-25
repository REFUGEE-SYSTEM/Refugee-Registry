-- Refugee Registry Intake Form UI Tab Sections (idempotent)
DELETE FROM "public"."g2p_intake_form_ui_tab_sections"
WHERE "tab_section_id" IN (
    'e0000000-0000-0000-0000-000000000006',
    'e0000000-0000-0000-0000-000000000008',
    'e0000000-0000-0000-0000-000000000009',
    'e0000000-0000-0000-0000-000000000010',
    'e0000000-0000-0000-0000-000000000011'
);

INSERT INTO "public"."g2p_intake_form_ui_tab_sections" ("tab_section_id","tab_id","section_id","section_order") VALUES
('e0000000-0000-0000-0000-000000000001','d0000000-0000-0000-0000-000000000001','household_info_section_01',10),
('e0000000-0000-0000-0000-000000000002','d0000000-0000-0000-0000-000000000001','household_location_section_02',20),
('e0000000-0000-0000-0000-000000000003','d0000000-0000-0000-0000-000000000002','refugee_household_lookup_section_01',10),
('e0000000-0000-0000-0000-000000000004','d0000000-0000-0000-0000-000000000002','refugee_personal_info_section_01',20),
('e0000000-0000-0000-0000-000000000005','d0000000-0000-0000-0000-000000000002','refugee_identity_document_section_01',30),
('e0000000-0000-0000-0000-000000000007','d0000000-0000-0000-0000-000000000002','refugee_specific_needs_section_01',50)
ON CONFLICT ("tab_section_id") DO UPDATE SET
    "tab_id" = EXCLUDED."tab_id",
    "section_id" = EXCLUDED."section_id",
    "section_order" = EXCLUDED."section_order";
