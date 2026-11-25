-- Refugee Registry UI Tabs (idempotent, Uganda category-per-tab layout)
INSERT INTO "public"."g2p_register_ui_tabs" ("tab_id","register_id","tab_label","tab_order","is_active") VALUES
('household_overview_tab','a0000000-0000-0000-0000-000000000001','household_overview_tab',1,'TRUE'),
('household_case_registration_tab','a0000000-0000-0000-0000-000000000001','household_case_registration_tab',2,'TRUE'),
('household_location_tab','a0000000-0000-0000-0000-000000000001','household_location_tab',3,'TRUE'),
('household_livelihoods_tab','a0000000-0000-0000-0000-000000000001','household_livelihoods_tab',4,'TRUE'),
('household_targeting_tab','a0000000-0000-0000-0000-000000000001','household_targeting_tab',5,'TRUE'),
('household_payment_tab','a0000000-0000-0000-0000-000000000001','household_payment_tab',6,'TRUE'),
('household_distribution_tab','a0000000-0000-0000-0000-000000000001','household_distribution_tab',7,'TRUE'),
('household_lifecycle_tab','a0000000-0000-0000-0000-000000000001','household_lifecycle_tab',8,'TRUE'),
('refugee_overview_tab','a0000000-0000-0000-0000-000000000002','refugee_overview_tab',1,'TRUE'),
('refugee_documents_tab','a0000000-0000-0000-0000-000000000002','refugee_documents_tab',2,'TRUE'),
('refugee_displacement_tab','a0000000-0000-0000-0000-000000000002','refugee_displacement_tab',3,'TRUE'),
('refugee_household_link_tab','a0000000-0000-0000-0000-000000000002','refugee_household_link_tab',4,'TRUE'),
('refugee_specific_needs_tab','a0000000-0000-0000-0000-000000000002','refugee_specific_needs_tab',5,'TRUE'),
('refugee_health_disability_tab','a0000000-0000-0000-0000-000000000002','refugee_health_disability_tab',6,'TRUE'),
('refugee_targeting_tab','a0000000-0000-0000-0000-000000000002','refugee_targeting_tab',7,'TRUE'),
('refugee_distribution_auth_tab','a0000000-0000-0000-0000-000000000002','refugee_distribution_auth_tab',8,'TRUE'),
('refugee_consent_tab','a0000000-0000-0000-0000-000000000002','refugee_consent_tab',9,'TRUE'),
('refugee_lifecycle_tab','a0000000-0000-0000-0000-000000000002','refugee_lifecycle_tab',10,'TRUE'),
('refugee_relatives_tab','a0000000-0000-0000-0000-000000000002','refugee_relatives_tab',40,'FALSE'),
('refugee_addresses_tab','a0000000-0000-0000-0000-000000000002','refugee_addresses_tab',50,'FALSE'),
('refugee_education_tab','a0000000-0000-0000-0000-000000000002','refugee_education_tab',60,'FALSE'),
('refugee_occupation_tab','a0000000-0000-0000-0000-000000000002','refugee_occupation_tab',70,'FALSE')
ON CONFLICT ("tab_id") DO UPDATE SET
    "register_id" = EXCLUDED."register_id",
    "tab_label" = EXCLUDED."tab_label",
    "tab_order" = EXCLUDED."tab_order",
    "is_active" = EXCLUDED."is_active";
