INSERT INTO "public"."approver_rule" (
    "id",
    "stage_id",
    "rule_type",
    "rule_value",
    "kind",
    "required",
    "created_at",
    "updated_at"
)
SELECT v."id", v."stage_id", v."rule_type", v."rule_value"::json, v."kind",
       v."required"::boolean, v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('f3000000-0000-4000-8000-000000000001', 'f2000000-0000-4000-8000-000000000001', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('f3000000-0000-4000-8000-000000000002', 'f2000000-0000-4000-8000-000000000002', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('f3000000-0000-4000-8000-000000000003', 'f2000000-0000-4000-8000-000000000003', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW()),
    ('f3000000-0000-4000-8000-000000000004', 'f2000000-0000-4000-8000-000000000004', 'user', '{"user_id": "alex.carter"}', 'approver', 'FALSE', NOW(), NOW())
) AS v("id","stage_id","rule_type","rule_value","kind","required","created_at","updated_at")
WHERE EXISTS (SELECT 1 FROM "public"."approval_stage" s WHERE s.id = v."stage_id")
ON CONFLICT DO NOTHING;
