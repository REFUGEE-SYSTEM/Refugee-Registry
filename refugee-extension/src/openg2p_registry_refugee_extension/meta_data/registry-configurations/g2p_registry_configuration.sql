INSERT INTO
    "public"."g2p_registry_configuration" (
        "configuration_id",
        "registry_name",
        "registry_logo",
        "registry_favicon",
        "registry_theme_id",
        "registry_language_id"
    )
VALUES
    (
        'f5000000-0000-4000-8000-000000000001',
        'Refugee Registry',
        NULL,
        NULL,
        '68721343-ea47-4675-94da-0437d688e9fe',
        'ccbcb97b-c4df-415d-9e4d-ec4985cf04e9'
    )
ON CONFLICT ("configuration_id") DO UPDATE SET
    "registry_name" = EXCLUDED."registry_name",
    "registry_theme_id" = EXCLUDED."registry_theme_id",
    "registry_language_id" = EXCLUDED."registry_language_id";
