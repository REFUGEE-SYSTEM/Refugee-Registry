INSERT INTO "public"."approval_stage" (
    "id",
    "policy_id",
    "stage_order",
    "name",
    "mode",
    "mode_value",
    "sla_hours",
    "parallel_group",
    "skip_if",
    "on_empty",
    "on_breach",
    "escalation_rules_json",
    "created_at",
    "updated_at"
)
SELECT v."id", v."policy_id", v."stage_order"::int, v."name", v."mode",
       v."mode_value"::int, v."sla_hours"::int, v."parallel_group"::int,
       v."skip_if"::json, v."on_empty", v."on_breach",
       v."escalation_rules_json"::json, v."created_at"::timestamptz, v."updated_at"::timestamptz
FROM (VALUES
    ('f2000000-0000-4000-8000-000000000001', 'f1000000-0000-4000-8000-000000000001', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('f2000000-0000-4000-8000-000000000002', 'f1000000-0000-4000-8000-000000000002', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('f2000000-0000-4000-8000-000000000003', '57f40743-266c-4e25-9a16-fd45483f904c', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW()),
    ('f2000000-0000-4000-8000-000000000004', 'fb51a862-d2ed-460d-8e1f-929cbeabdd01', 1, 'Stage 1 Officers', 'all', NULL, NULL, NULL, 'null', 'block', NULL, 'null', NOW(), NOW())
) AS v("id","policy_id","stage_order","name","mode","mode_value","sla_hours",
        "parallel_group","skip_if","on_empty","on_breach","escalation_rules_json",
        "created_at","updated_at")
WHERE EXISTS (SELECT 1 FROM "public"."approval_policy" p WHERE p.id = v."policy_id")
ON CONFLICT DO NOTHING;
