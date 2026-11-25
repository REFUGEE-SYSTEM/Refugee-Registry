-- Refugee Registry UI Tabs (idempotent)
-- Non-mandatory sub-register tabs hidden (is_active = FALSE) for Uganda mandatory demo
INSERT INTO "public"."g2p_register_ui_tabs" ("tab_id","register_id","tab_label","tab_order","is_active") VALUES
('household_overview_tab','a0000000-0000-0000-0000-000000000001','household_overview_tab',1,'TRUE'),
('refugee_overview_tab','a0000000-0000-0000-0000-000000000002','refugee_overview_tab',1,'TRUE'),
('refugee_household_link_tab','a0000000-0000-0000-0000-000000000002','refugee_household_link_tab',2,'TRUE'),
('refugee_documents_tab','a0000000-0000-0000-0000-000000000002','refugee_documents_tab',10,'TRUE'),
('refugee_displacement_tab','a0000000-0000-0000-0000-000000000002','refugee_displacement_tab',20,'FALSE'),
('refugee_specific_needs_tab','a0000000-0000-0000-0000-000000000002','refugee_specific_needs_tab',30,'TRUE'),
('refugee_relatives_tab','a0000000-0000-0000-0000-000000000002','refugee_relatives_tab',40,'FALSE'),
('refugee_addresses_tab','a0000000-0000-0000-0000-000000000002','refugee_addresses_tab',50,'FALSE'),
('refugee_education_tab','a0000000-0000-0000-0000-000000000002','refugee_education_tab',60,'FALSE'),
('refugee_occupation_tab','a0000000-0000-0000-0000-000000000002','refugee_occupation_tab',70,'FALSE')
ON CONFLICT ("tab_id") DO UPDATE SET
    "register_id" = EXCLUDED."register_id",
    "tab_label" = EXCLUDED."tab_label",
    "tab_order" = EXCLUDED."tab_order",
    "is_active" = EXCLUDED."is_active";
