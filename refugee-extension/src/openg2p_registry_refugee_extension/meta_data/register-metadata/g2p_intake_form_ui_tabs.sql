-- Refugee Registry Intake Form UI Tabs (idempotent)
INSERT INTO "public"."g2p_intake_form_ui_tabs" ("tab_id","form_id","tab_label","tab_order") VALUES
('d0000000-0000-0000-0000-000000000001','c0000000-0000-0000-0000-000000000001','household_intake_tab',10),
('d0000000-0000-0000-0000-000000000002','c0000000-0000-0000-0000-000000000002','refugee_intake_tab',10)
ON CONFLICT ("tab_id") DO UPDATE SET
    "form_id" = EXCLUDED."form_id",
    "tab_label" = EXCLUDED."tab_label",
    "tab_order" = EXCLUDED."tab_order";
