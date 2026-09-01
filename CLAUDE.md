# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

Bidirectional synchronization API that integrates a Microsoft SQL Server database (`ggs_stud`) with Bitrix24 CRM. Syncs entities (houses, persons, organizations, contracts, equipment, work operations) from the local DB into Bitrix24 custom SmartProcess (SPA) entities.

## Running the Server

```powershell
# Create and activate venv
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and fill in environment variables
cp .env.example .env

# Start development server (auto-reload)
fastapi dev app/app.py
```

Server: `http://localhost:8000` -- Swagger UI: `http://localhost:8000/docs`

No test suite exists. No lint configuration exists.

## Environment Variables (`.env`)

| Variable | Description |
|---|---|
| `RUN_MODE` | `DEV` or production flag |
| `BITRIX_WEBHOOK` | Bitrix24 webhook URL (`https://domain/rest/132/{SECRET}/`) |
| `DB_ENGINE_STRING` | SQLAlchemy connection string for SQL Server via ODBC |
| `*_ENTITY_TYPE_ID` | Bitrix SPA entity type IDs for each entity |
| `*_ENTITY_ID` | Specific entity IDs within Bitrix |

## Architecture

```
app/
  app.py              -- FastAPI app, router registration
  settings.py         -- Pydantic Settings, reads .env
  routes/
    forward_sync.py   -- 7 sync endpoints (one per entity type)
    admin_tasks.py    -- Debug/setup endpoints, CRM field discovery
  db/
    engine.py         -- SQLAlchemy engine and session factory
    query_*.py        -- One module per entity; return dicts
  models/
    *.py              -- 37 SQLAlchemy ORM models (snake_case attrs)
  utils/
    *.py              -- Payload builders (DB dict -> Bitrix API payload)
  enums/
    *.py              -- Field name mappings: DB column <-> Bitrix field key
  bitrix/
    forward_sync.py   -- Low-level Bitrix API calls (add_item / update_item)
  legacy_modules/     -- Deprecated code, do not use
```

> **Note on AI Context:** 
> For domain understanding (Context Engineering), refer to **[DOMAIN.md](DOMAIN.md)**. It contains the business-level descriptions of all entities and their relationships.


## Sync Data Flow

For each entity, the sync follows this pattern:

1. **Route** (`routes/forward_sync.py`) receives `POST /forward_sync/{entity}/{id}`
2. **Query** (`db/query_*.py`) fetches entity data from SQL Server as a dict
3. **Dependency check** -- if a referenced parent entity has no CRM ID yet, the route recursively syncs the parent first (using `called_by_*` boolean flags to prevent infinite loops)
4. **Payload build** (`utils/*.py`) maps DB fields to Bitrix field names using enums
5. **Bitrix call** (`bitrix/forward_sync.py`) calls `add_item()` (new) or `update_item()` (existing) via `fast_bitrix24`
6. **ID store** -- the returned Bitrix CRM ID is written back to the SQL Server row

## Key Patterns

- **`called_by_*` flags** on sync endpoints: when `True`, the endpoint was triggered recursively by another sync, not directly by a client. Used to skip re-syncing parents that are already being processed.
- **Query modules** always return a single dict (one entity) or list of dicts; never ORM model instances.
- **Enum modules** (`enums/`) are the authoritative source for which Bitrix field key corresponds to which DB column. Change mappings there first.
- **`admin_tasks/build_table_crm_fields`** introspects Bitrix to discover all custom field names for a given entity type -- run this when Bitrix fields are added or renamed.

## Database

- Target DB: `ggs_stud` on SQL Server
- `prepare.sql` adds CRM ID tracking columns to existing tables and creates `zm.gro` and `zm.district` lookup tables
- Run `prepare.sql` once on initial setup against the target database

## E2E Tests

Tests are run on the remote machine (the only environment with access to both Bitrix24 and SQL Server).

**Setup:**
```powershell
pip install -r requirements-test.txt
cp tests/.env.test.example tests/.env.test
# edit tests/.env.test -- set TEST_HOUSE_ID and TEST_API_BASE_URL
# .env must also be present and configured (same as running the app)
```

**Run:**
```powershell
pytest tests/ -v          # all tests
pytest tests/test_sync_house.py -v   # single entity
```

**Test structure:**
- `tests/conftest.py` -- session fixtures: `api_client` (httpx), `bitrix` (fast_bitrix24), `test_settings`; module fixture: `house_sync_result` (runs the first sync once, shared across tests in the module)
- `tests/helpers.py` -- `assert_payload_matches_bitrix()` handles datetime/int/list type coercion when comparing payload values to Bitrix API response values
- `tests/test_sync_house.py` -- four assertions per entity: HTTP 200, crm_ids stored in DB, all custom fields in Bitrix match DB values, second sync is update (crm_ids unchanged)

**Adding tests for a new entity:** create `tests/test_sync_{entity}.py` following the same pattern -- build the expected payload using the app's utils functions, fetch from Bitrix with `crm.item.get`, call `assert_payload_matches_bitrix`.

## Entities and Their Route/Query/Model/Util Mapping

| Entity | Route path | Query module | Util module |
|---|---|---|---|
| House (Object KS) | `/forward_sync/house/{id}` | `query_house.py` | `object_ks_gs.py` |
| Person | `/forward_sync/person/{id}` | `query_person.py` | `contact.py` |
| Organization | `/forward_sync/organization/{id}` | `query_organization.py` | `company.py` |
| Contract | `/forward_sync/contract/{id}` | `query_contract.py` | `contract.py` |
| Equipment | `/forward_sync/house_equip/{house_equip_id}` | `query_house_equip.py` | `equip.py` |
| Work operation | `/forward_sync/work_operation/{id}` | `query_work.py` | `work_operation.py` |
| Ground | `/forward_sync/ground/{id}` | `query_net.py` | `ground.py` |
