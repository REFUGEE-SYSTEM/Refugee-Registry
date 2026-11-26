-- Refugee Registry UI Tabs (idempotent, Uganda category-per-tab layout only)
DELETE FROM "public"."g2p_register_ui_tabs"
WHERE "tab_id" IN (
    'refugee_relatives_tab',
    'refugee_addresses_tab',
    'refugee_education_tab',
    'refugee_occupation_tab'
);

INSERT INTO "public"."g2p_register_ui_tabs" ("tab_id","register_id","tab_label","tab_order","is_active") VALUES
('refugee_overview_tab','a0000000-0000-0000-0000-000000000002','refugee_overview_tab',1,'TRUE'),
('refugee_documents_tab','a0000000-0000-0000-0000-000000000002','refugee_documents_tab',2,'TRUE'),
('refugee_displacement_tab','a0000000-0000-0000-0000-000000000002','refugee_displacement_tab',3,'TRUE'),
('refugee_specific_needs_tab','a0000000-0000-0000-0000-000000000002','refugee_specific_needs_tab',4,'TRUE'),
('refugee_health_disability_tab','a0000000-0000-0000-0000-000000000002','refugee_health_disability_tab',5,'TRUE'),
('refugee_targeting_tab','a0000000-0000-0000-0000-000000000002','refugee_targeting_tab',6,'TRUE'),
('refugee_distribution_auth_tab','a0000000-0000-0000-0000-000000000002','refugee_distribution_auth_tab',7,'TRUE'),
('refugee_consent_tab','a0000000-0000-0000-0000-000000000002','refugee_consent_tab',8,'TRUE'),
('refugee_lifecycle_tab','a0000000-0000-0000-0000-000000000002','refugee_lifecycle_tab',9,'TRUE')
ON CONFLICT ("tab_id") DO UPDATE SET
    "register_id" = EXCLUDED."register_id",
    "tab_label" = EXCLUDED."tab_label",
    "tab_order" = EXCLUDED."tab_order",
    "is_active" = EXCLUDED."is_active";
