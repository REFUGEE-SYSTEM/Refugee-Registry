INSERT INTO "public"."approval_policy" (
    "id",
    "policy_key",
    "version",
    "name",
    "description",
    "status",
    "artifact_type",
    "created_by",
    "forbid_self_approval",
    "forbid_repeat_approvers",
    "created_at",
    "updated_at"
) VALUES
    ('f1000000-0000-4000-8000-000000000001', 'registry.change_request.refugee', 1, 'Policy for Refugee Change Request', NULL, 'active', 'registry.change_request', 'seed', 'FALSE', 'FALSE', NOW(), NOW()),
    ('f1000000-0000-4000-8000-000000000002', 'registry.intake_form.refugee', 1, 'Policy for Refugee Intake Form', NULL, 'active', 'registry.intake_form', 'seed', 'FALSE', 'FALSE', NOW(), NOW())
ON CONFLICT DO NOTHING;
