-- Refugee Registry Register Definitions (idempotent)
-- Fixed UUIDs match register_domain/constants.py
INSERT INTO "public"."g2p_register_definitions" ("register_id","register_mnemonic","register_subject","register_description","master_register_id","register_rank","functional_id_generation_required","register_purpose","program_id","program_mnemonic","register_icon","has_image","dedup_is_enabled","dedup_threshold_score","completion_score_required","outgest_applicable","requires_registrant_authentication","registrant_authentication_validity_days","registrant_re_auth_warning_days_before") VALUES
('a0000000-0000-0000-0000-000000000001','Household','Households','Refugee Household (Case/Group) Register',NULL,1,'TRUE','REGISTER',NULL,NULL,'','FALSE','TRUE',70,'FALSE','FALSE','FALSE',730,30),
('a0000000-0000-0000-0000-000000000002','Refugee','Refugees','Refugee Individual Register',NULL,2,'TRUE','REGISTER',NULL,NULL,'','TRUE','TRUE',70,'FALSE','FALSE','TRUE',730,30),
('a0000000-0000-0000-0000-000000000003','IdentityDocument','Identity Documents','Refugee Identity Documents Table','a0000000-0000-0000-0000-000000000002',10,'FALSE','TABLE',NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30),
('a0000000-0000-0000-0000-000000000004','DisplacementHistory','Displacement Histories','Refugee Displacement History Table','a0000000-0000-0000-0000-000000000002',20,'FALSE','TABLE',NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30),
('a0000000-0000-0000-0000-000000000005','SpecificNeeds','Specific Needs','Refugee Specific Needs Table','a0000000-0000-0000-0000-000000000002',30,'FALSE','TABLE',NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30),
('a0000000-0000-0000-0000-000000000006','Relative','Relatives','Refugee Relatives Table','a0000000-0000-0000-0000-000000000002',40,'FALSE','TABLE',NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30),
('a0000000-0000-0000-0000-000000000007','Address','Addresses','Refugee Addresses Table','a0000000-0000-0000-0000-000000000002',50,'FALSE','TABLE',NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30),
('a0000000-0000-0000-0000-000000000008','EducationRecord','Education Records','Refugee Education Records Table','a0000000-0000-0000-0000-000000000002',60,'FALSE','TABLE',NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30),
('a0000000-0000-0000-0000-000000000009','OccupationSkill','Occupation Skills','Refugee Occupation and Skills Table','a0000000-0000-0000-0000-000000000002',70,'FALSE','TABLE',NULL,NULL,NULL,'FALSE','FALSE',0,'FALSE','FALSE','FALSE',730,30)
ON CONFLICT ("register_id") DO UPDATE SET
    "register_mnemonic" = EXCLUDED."register_mnemonic",
    "register_subject" = EXCLUDED."register_subject",
    "register_description" = EXCLUDED."register_description",
    "master_register_id" = EXCLUDED."master_register_id",
    "register_rank" = EXCLUDED."register_rank",
    "functional_id_generation_required" = EXCLUDED."functional_id_generation_required",
    "register_purpose" = EXCLUDED."register_purpose",
    "program_id" = EXCLUDED."program_id",
    "program_mnemonic" = EXCLUDED."program_mnemonic",
    "register_icon" = EXCLUDED."register_icon",
    "has_image" = EXCLUDED."has_image",
    "dedup_is_enabled" = EXCLUDED."dedup_is_enabled",
    "dedup_threshold_score" = EXCLUDED."dedup_threshold_score",
    "completion_score_required" = EXCLUDED."completion_score_required",
    "outgest_applicable" = EXCLUDED."outgest_applicable",
    "requires_registrant_authentication" = EXCLUDED."requires_registrant_authentication",
    "registrant_authentication_validity_days" = EXCLUDED."registrant_authentication_validity_days",
    "registrant_re_auth_warning_days_before" = EXCLUDED."registrant_re_auth_warning_days_before";
