# Data Dictionary — Enterprise CMDB, Incidents & Knowledge Docs

Describes `data/cmdb.csv`, `data/incidents.csv`, and `data/knowledge/*.md`. All data is synthetically generated; no real infrastructure names, hostnames, or identifiers are used anywhere.

## `data/cmdb.csv` (10,000 rows)

| Field | Type | Valid Values | Nullable | Business Meaning |
|---|---|---|---|---|
| `asset_id` | string | `ASSET-000001` ... unique | No | Primary key. Unique identifier for the asset. |
| `hostname` | string | `{application}-{environment}-{n}.internal` | No | Synthetic internal hostname. Never a real or resolvable address. |
| `environment` | string (enum) | `dev`, `qa`, `staging`, `prod` | No | Deployment environment the asset belongs to. |
| `application` | string (enum) | one of 15 fictional application names (e.g. `order-service`, `payment-gateway`) | No | The application this asset supports. Foreign key target for `incidents.service`. |
| `service_owner` | string (enum) | one of 7 fictional team names | No | Team responsible for the application. Derived deterministically from `application`. |
| `business_unit` | string (enum) | `Retail`, `Logistics`, `Finance`, `Platform`, `Customer Support` | No | Business unit the application serves. Derived deterministically from `application`. |
| `status` | string (enum) | `active`, `maintenance`, `decommissioned` | No | Current operational status of the asset. |
| `region` | string (enum) | `us-east`, `us-west`, `eu-west`, `ap-southeast` | No | Deployment region. |
| `os_type` | string (enum) | `linux`, `windows`, `macos` | No | Operating system family. |
| `lifecycle_state` | string (enum) | `provisioning`, `active`, `deprecated`, `retired` | No | Asset lifecycle stage, independent of `status`. |

## `data/incidents.csv` (2,000 rows)

| Field | Type | Valid Values | Nullable | Business Meaning |
|---|---|---|---|---|
| `incident_id` | string | `INC-000001` ... unique | No | Primary key. |
| `service` | string | must exist in `cmdb.csv`'s `application` column | No | **Foreign key** to `cmdb.application`. Every incident must reference a real, existing application. |
| `severity` | string (enum) | `SEV1`, `SEV2`, `SEV3`, `SEV4` | No | Incident severity, `SEV1` = most severe. |
| `status` | string (enum) | `open`, `mitigated`, `resolved` | No | Current incident status. |
| `opened_at` | datetime (ISO 8601) | 2024-01-01 to 2025-12-31 | No | When the incident was detected/opened. |
| `resolved_at` | datetime (ISO 8601) | after `opened_at` | **Yes, for `status = open`** | When the incident was resolved. Deliberately null for still-open incidents rather than fabricating a resolution time. |
| `summary` | string | free text | No | One-sentence synthetic summary of the incident. |
| `root_cause` | string | free text | **Yes, for `status = open`** | Root cause description. Null for incidents that haven't been resolved yet, since a root cause hasn't been confirmed. |

## `data/knowledge/*.md`

One Markdown runbook per unique application in `cmdb.csv` (15 files). Each follows a consistent structure: `Overview`, `Common Issues` (with named subsections), `Support Procedures` (numbered steps), and `Escalation` (naming the owning team, matching `cmdb.service_owner` for that application).

## Notes

- **The `service` -> `application` relationship is a genuine foreign key**, enforced at generation time: `generate_incidents.py` reads the actual application list out of `data/cmdb.csv` before generating any incidents, so every `service` value is guaranteed to exist in the CMDB. This is validated independently by `scripts/validate_enterprise_data.py`, which checks the relationship again after the fact rather than only trusting how the data was generated.
- **`service_owner` and `business_unit` in the CMDB are derived, not independently random** -- every asset for a given `application` always has the same owner and business unit, which is what makes cross-referencing (e.g. "which team owns `payment-gateway`?") consistent throughout the dataset.
- No field in any of these files is derived from or represents any real company, system, or infrastructure.