# Optional: Migrating from a Shared OpenG2P Developer Stack

`Refugee-Registry` is now fully standalone via its root `docker-compose.yml` and `scripts/up.sh`. You do **not** need a shared developer stack.

If you previously ran the Refugee extension inside a shared OpenG2P developer workspace:
1. Keep your existing shared stack untouched on its original ports (`3000-3050`, `5432-5435`, `6379-6381`, `8020-8180`, `9000-9011`).
2. Run this standalone project on its own non-colliding default ports (`3150`, `5535`, `6481`, `8220`, `8230`, `8240`, `8249`, `8271`, `8280`, `9100`, `9101`) using:
   ```bash
   ./scripts/init-env.sh
   ./scripts/up.sh
   ./scripts/smoke-test.sh
   ```
3. All database schemas, Keycloak realm (`refugee`), IAM RBAC (`refugee-registry-staff-portal`), Master Data (`ETH` geo + `data/codelists/refugee/`), AWE policies, and demo records are bootstrapped automatically inside the standalone stack's own named volumes.
