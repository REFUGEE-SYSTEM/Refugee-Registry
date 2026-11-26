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
('e0000000-0000-0000-0000-000000000004','d0000000-0000-0000-0000-000000000002','refugee_personal_info_section_01',10),
('e0000000-0000-0000-0000-000000000005','d0000000-0000-0000-0000-000000000002','refugee_identity_document_section_01',20),
('e0000000-0000-0000-0000-000000000020','d0000000-0000-0000-0000-000000000002','refugee_legal_status_section_01',30),
('e0000000-0000-0000-0000-000000000007','d0000000-0000-0000-0000-000000000002','refugee_specific_needs_section_01',40),
('e0000000-0000-0000-0000-000000000022','d0000000-0000-0000-0000-000000000002','refugee_protection_uasc_section_01',50),
('e0000000-0000-0000-0000-000000000023','d0000000-0000-0000-0000-000000000002','refugee_health_disability_section_01',60),
('e0000000-0000-0000-0000-000000000024','d0000000-0000-0000-0000-000000000002','refugee_targeting_section_01',70),
('e0000000-0000-0000-0000-000000000025','d0000000-0000-0000-0000-000000000002','refugee_distribution_auth_section_01',80),
('e0000000-0000-0000-0000-000000000026','d0000000-0000-0000-0000-000000000002','refugee_consent_section_01',90),
('e0000000-0000-0000-0000-000000000027','d0000000-0000-0000-0000-000000000002','refugee_lifecycle_section_01',100)
ON CONFLICT ("tab_section_id") DO UPDATE SET
    "tab_id" = EXCLUDED."tab_id",
    "section_id" = EXCLUDED."section_id",
    "section_order" = EXCLUDED."section_order";
