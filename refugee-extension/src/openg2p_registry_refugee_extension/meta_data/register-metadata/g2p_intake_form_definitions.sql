-- Refugee Registry Intake Form Definitions (idempotent)
INSERT INTO "public"."g2p_intake_form_definitions" ("form_id","register_id","form_mnemonic","form_description","number_of_verifications","used_only_in_ingestion_pipeline") VALUES
('c0000000-0000-0000-0000-000000000001','a0000000-0000-0000-0000-000000000001','household_intake','Refugee Household Intake Form',1,'FALSE'),
('c0000000-0000-0000-0000-000000000002','a0000000-0000-0000-0000-000000000002','refugee_intake','Refugee Individual Intake Form',1,'FALSE')
ON CONFLICT ("form_id") DO UPDATE SET
    "register_id" = EXCLUDED."register_id",
    "form_mnemonic" = EXCLUDED."form_mnemonic",
    "form_description" = EXCLUDED."form_description",
    "number_of_verifications" = EXCLUDED."number_of_verifications",
    "used_only_in_ingestion_pipeline" = EXCLUDED."used_only_in_ingestion_pipeline";
