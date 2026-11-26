-- Refugee Registry UI Tab Sections (idempotent, Uganda category-per-tab layout)
DELETE FROM "public"."g2p_register_ui_tab_sections"
WHERE "tab_section_id" IN (
    'b0000000-0000-0000-0000-000000000008',
    'b0000000-0000-0000-0000-000000000010',
    'b0000000-0000-0000-0000-000000000011',
    'b0000000-0000-0000-0000-000000000012',
    'b0000000-0000-0000-0000-000000000013'
);

INSERT INTO "public"."g2p_register_ui_tab_sections" ("tab_section_id","register_id","tab_id","section_id","section_order") VALUES
('b0000000-0000-0000-0000-000000000004','a0000000-0000-0000-0000-000000000002','refugee_overview_tab','refugee_header_section_01',5),
('b0000000-0000-0000-0000-000000000005','a0000000-0000-0000-0000-000000000002','refugee_overview_tab','refugee_personal_info_section_01',10),
('b0000000-0000-0000-0000-000000000007','a0000000-0000-0000-0000-000000000002','refugee_documents_tab','refugee_identity_document_section_01',10),
('b0000000-0000-0000-0000-000000000020','a0000000-0000-0000-0000-000000000002','refugee_displacement_tab','refugee_legal_status_section_01',10),
('b0000000-0000-0000-0000-000000000009','a0000000-0000-0000-0000-000000000002','refugee_specific_needs_tab','refugee_specific_needs_section_01',10),
('b0000000-0000-0000-0000-000000000022','a0000000-0000-0000-0000-000000000002','refugee_specific_needs_tab','refugee_protection_uasc_section_01',20),
('b0000000-0000-0000-0000-000000000023','a0000000-0000-0000-0000-000000000002','refugee_health_disability_tab','refugee_health_disability_section_01',10),
('b0000000-0000-0000-0000-000000000024','a0000000-0000-0000-0000-000000000002','refugee_targeting_tab','refugee_targeting_section_01',10),
('b0000000-0000-0000-0000-000000000025','a0000000-0000-0000-0000-000000000002','refugee_distribution_auth_tab','refugee_distribution_auth_section_01',10),
('b0000000-0000-0000-0000-000000000026','a0000000-0000-0000-0000-000000000002','refugee_consent_tab','refugee_consent_section_01',10),
('b0000000-0000-0000-0000-000000000027','a0000000-0000-0000-0000-000000000002','refugee_lifecycle_tab','refugee_lifecycle_section_01',10)
ON CONFLICT ("tab_section_id") DO UPDATE SET
    "register_id" = EXCLUDED."register_id",
    "tab_id" = EXCLUDED."tab_id",
    "section_id" = EXCLUDED."section_id",
    "section_order" = EXCLUDED."section_order";
