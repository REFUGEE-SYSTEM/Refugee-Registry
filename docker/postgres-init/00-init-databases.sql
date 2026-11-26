-- Standalone Refugee Registry databases (runs once on first Postgres start).

SELECT 'CREATE DATABASE keycloak OWNER postgres'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'keycloak')\gexec

SELECT 'CREATE DATABASE iam_staff OWNER postgres'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'iam_staff')\gexec

SELECT 'CREATE DATABASE awe OWNER postgres'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'awe')\gexec

SELECT 'CREATE DATABASE idgenerator OWNER postgres'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'idgenerator')\gexec

SELECT 'CREATE DATABASE refugee_registry_db OWNER postgres'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'refugee_registry_db')\gexec

SELECT 'CREATE DATABASE refugee_master_data_db OWNER postgres'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'refugee_master_data_db')\gexec

\c refugee_registry_db
CREATE EXTENSION IF NOT EXISTS pg_trgm;

\c refugee_master_data_db
CREATE EXTENSION IF NOT EXISTS pg_trgm;

\c awe
CREATE EXTENSION IF NOT EXISTS pg_trgm;
