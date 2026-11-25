# Refugee Registry — 5-Minute Live Demo Script

## Prerequisites
- Staff Portal URL: `http://localhost:3050`
- Demo Login: `alex.carter` / `pass` (also approver for AWE Stage 1)

## Walkthrough
1. **Sign In (0:00–0:30)**
   - Open `http://localhost:3050`, click Sign In, authenticate as `alex.carter` / `pass`.
   - Show the **Refugee Registry** home screen listing **Households** and **Refugees**.
2. **Browse Households & Geography (0:30–1:30)**
   - Open **Households**. Point out the 8 seeded demo households (`HH-DEMO-0001` through `HH-DEMO-0008`).
   - Open `HH-DEMO-0001` (`SSD`, `REFUGEE`, Gambella Camp).
   - Show group counts (`group_size=4`), `Legal Status`, `Country of Origin`, `Consent recorded (information only)`, and the Ethiopia **Location Hierarchy** (`country > region > zone > woreda`) resolved from Master Data.
3. **Browse Refugee Record & Sub-Registers (1:30–3:00)**
   - Open **Refugees**, search for `Deng` or `RF-DEMO-0001` (`Deng Garang`).
   - Walk through the tabs:
     - **Refugee Overview**: Personal Info (`MALE`, `SELF`, `SSD`, `SECONDARY`, `CHRISTIANITY`, `EN`/`AR`).
     - **Identity Documents**: `REFUGEE_ID` (`DOC-2025-1001`, issued by `UNHCR`).
     - **Displacement History**: Reasons for inability to return, departure date, travel details.
     - **Addresses**: Both `COUNTRY_OF_ASYLUM` (`ETH`) and `COUNTRY_OF_ORIGIN` (`SSD`).
     - **Education** & **Occupation & Skills** tabs.
4. **Show Specific Needs & Dropdowns (3:00–4:00)**
   - Search `RF-DEMO-0012` (`Omer Al-Amin`, Sudan, `APD` Sudanese Arabic) or `RF-DEMO-0003` (`Akech Garang`) to show **Specific Needs** (`CHRONIC_ILLNESS` / `UNACCOMPANIED_CHILD`).
   - Click **New Intake** (or Edit) to show live Master Data dropdowns (`Gender` with `OTHERS`, `Relationship to Group` with `SELF`, `Languages Known` with `APD`, `Legal Status`, `Country of Origin`).
5. **Approval Workflow (4:00–5:00)**
   - Submit a change request or intake form, then open **My Tasks / Approvals** as `alex.carter` to approve in one stage.

## 5 Likely Questions & Honest Answers
1. **Are these official UNHCR proGres codelists?**
   No. The 10 domain codelists are illustrative demo lists aligned to proGres concepts; they can be swapped in `openg2p-data/packs/ETH/domains/refugee/` without changing code.
2. **How is the Farmer Registry on this same machine affected?**
   It is completely isolated: separate databases (`farmer_custom_registry_db` vs `refugee_registry_db`), separate Master Data DB, separate ports (`3040` vs `3050`), and separate AWE callback secret (`...0004` vs `...0005`).
3. **Why is biometrics not shown?**
   Biometrics (fingerprints, iris, face templates, BIMS flags) are deferred from Step 3 and marked as a `TODO` in `refugee.py`.
4. **How is consent enforced?**
   The household consent checkbox is currently an informational boolean (`Consent recorded (information only)`). Full partner-level consent enforcement uses `data_scopes.json` and the Consent Manager, which are out of scope for this demo.
5. **What happens when a new Refugee is approved — does it mint an `RF-` ID?**
   `Household` mints `HH-` from the existing `id_pool_household`. `Refugee` uses `id_pool_refugee`, which is configured in `config/id-generator/default.yaml` and requires restarting the shared `openg2p-id-generator` container to initialize its pool.
