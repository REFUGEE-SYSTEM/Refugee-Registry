INSERT INTO "public"."g2p_registry_awe_policy_configurations" (
    "awe_policy_config_id",
    "policy_scope",
    "register_id",
    "intake_form_id",
    "section_id",
    "policy_type",
    "policy_key",
    "context_field_names"
) VALUES
    ('f4000000-0000-4000-8000-000000000001', 'REGISTER', 'a0000000-0000-0000-0000-000000000002', '', '', 'registry.change_request', 'registry.change_request.refugee', 'null'),
    ('f4000000-0000-4000-8000-000000000002', 'INTAKE_FORM', 'a0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000002', '', 'registry.intake_form', 'registry.intake_form.refugee', 'null')
ON CONFLICT ("awe_policy_config_id") DO NOTHING;
