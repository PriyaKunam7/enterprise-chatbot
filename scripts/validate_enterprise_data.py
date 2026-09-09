"""
Validates data/cmdb.csv and data/incidents.csv for structural
integrity: duplicates, nulls in required fields, invalid enum values,
and broken foreign-key-style references between incidents and CMDB
applications.

Writes a JSON report to reports/enterprise_data_validation.json.

Usage:
    python scripts/validate_enterprise_data.py
"""

import json
import os
from datetime import datetime, timezone

import pandas as pd

CMDB_PATH = "data/cmdb.csv"
INCIDENTS_PATH = "data/incidents.csv"
KNOWLEDGE_DIR = "data/knowledge"
REPORT_PATH = "reports/enterprise_data_validation.json"

VALID_ENVIRONMENTS = {"dev", "qa", "staging", "prod"}
VALID_STATUSES_CMDB = {"active", "maintenance", "decommissioned"}
VALID_REGIONS = {"us-east", "us-west", "eu-west", "ap-southeast"}
VALID_OS_TYPES = {"linux", "windows", "macos"}
VALID_LIFECYCLE_STATES = {"provisioning", "active", "deprecated", "retired"}

VALID_SEVERITIES = {"SEV1", "SEV2", "SEV3", "SEV4"}
VALID_STATUSES_INCIDENT = {"open", "mitigated", "resolved"}

CMDB_REQUIRED_COLUMNS = [
    "asset_id",
    "hostname",
    "environment",
    "application",
    "service_owner",
    "business_unit",
    "status",
    "region",
    "os_type",
    "lifecycle_state",
]
INCIDENT_REQUIRED_COLUMNS = [
    "incident_id",
    "service",
    "severity",
    "status",
    "opened_at",
    "resolved_at",
    "summary",
    "root_cause",
]


def validate_cmdb(cmdb: pd.DataFrame) -> dict:
    issues = []

    missing_columns = [c for c in CMDB_REQUIRED_COLUMNS if c not in cmdb.columns]
    if missing_columns:
        issues.append(
            {"check": "required_columns", "detail": f"Missing: {missing_columns}"}
        )

    dup_count = int(cmdb["asset_id"].duplicated().sum())
    if dup_count:
        issues.append(
            {"check": "duplicate_asset_id", "detail": f"{dup_count} duplicates"}
        )

    required_non_null = [c for c in CMDB_REQUIRED_COLUMNS if c in cmdb.columns]
    null_counts = cmdb[required_non_null].isnull().sum()
    fields_with_nulls = {k: int(v) for k, v in null_counts.items() if v > 0}
    if fields_with_nulls:
        issues.append({"check": "null_required_fields", "detail": fields_with_nulls})

    enum_checks = {
        "environment": VALID_ENVIRONMENTS,
        "status": VALID_STATUSES_CMDB,
        "region": VALID_REGIONS,
        "os_type": VALID_OS_TYPES,
        "lifecycle_state": VALID_LIFECYCLE_STATES,
    }
    invalid_enum_counts = {}
    for col, valid_values in enum_checks.items():
        if col not in cmdb.columns:
            continue
        invalid = (~cmdb[col].isin(valid_values)).sum()
        if invalid > 0:
            invalid_enum_counts[col] = int(invalid)
    if invalid_enum_counts:
        issues.append({"check": "invalid_enum_values", "detail": invalid_enum_counts})

    return {
        "row_count": len(cmdb),
        "unique_applications": (
            sorted(cmdb["application"].unique().tolist())
            if "application" in cmdb.columns
            else []
        ),
        "issues": issues,
        "critical_violations": len(missing_columns) + (1 if dup_count else 0),
    }


def validate_incidents(incidents: pd.DataFrame, valid_applications: set[str]) -> dict:
    issues = []

    missing_columns = [
        c for c in INCIDENT_REQUIRED_COLUMNS if c not in incidents.columns
    ]
    if missing_columns:
        issues.append(
            {"check": "required_columns", "detail": f"Missing: {missing_columns}"}
        )

    dup_count = int(incidents["incident_id"].duplicated().sum())
    if dup_count:
        issues.append(
            {"check": "duplicate_incident_id", "detail": f"{dup_count} duplicates"}
        )

    always_required = [
        "incident_id",
        "service",
        "severity",
        "status",
        "opened_at",
        "summary",
    ]
    always_required = [c for c in always_required if c in incidents.columns]
    null_counts = incidents[always_required].isnull().sum()
    fields_with_nulls = {k: int(v) for k, v in null_counts.items() if v > 0}
    if fields_with_nulls:
        issues.append({"check": "null_required_fields", "detail": fields_with_nulls})

    enum_checks = {
        "severity": VALID_SEVERITIES,
        "status": VALID_STATUSES_INCIDENT,
    }
    invalid_enum_counts = {}
    for col, valid_values in enum_checks.items():
        if col not in incidents.columns:
            continue
        invalid = (~incidents[col].isin(valid_values)).sum()
        if invalid > 0:
            invalid_enum_counts[col] = int(invalid)
    if invalid_enum_counts:
        issues.append({"check": "invalid_enum_values", "detail": invalid_enum_counts})

    broken_refs = 0
    if "service" in incidents.columns:
        broken_refs = int((~incidents["service"].isin(valid_applications)).sum())
        if broken_refs > 0:
            issues.append(
                {
                    "check": "broken_service_reference",
                    "detail": f"{broken_refs} incidents reference an unknown application",
                }
            )

    return {
        "row_count": len(incidents),
        "issues": issues,
        "critical_violations": len(missing_columns)
        + (1 if dup_count else 0)
        + (1 if broken_refs else 0),
    }


def validate_knowledge_docs(
    applications: set[str], knowledge_dir: str = KNOWLEDGE_DIR
) -> dict:
    issues = []
    if not os.path.isdir(knowledge_dir):
        return {
            "doc_count": 0,
            "issues": [{"check": "knowledge_dir_missing", "detail": knowledge_dir}],
        }

    doc_files = {f[:-3] for f in os.listdir(knowledge_dir) if f.endswith(".md")}
    missing_docs = applications - doc_files
    if missing_docs:
        issues.append(
            {
                "check": "missing_knowledge_docs",
                "detail": f"No doc for: {sorted(missing_docs)}",
            }
        )

    return {"doc_count": len(doc_files), "issues": issues}


def main() -> None:
    cmdb = pd.read_csv(CMDB_PATH)
    incidents = pd.read_csv(INCIDENTS_PATH)

    cmdb_report = validate_cmdb(cmdb)
    valid_applications = set(cmdb_report["unique_applications"])
    incidents_report = validate_incidents(incidents, valid_applications)
    knowledge_report = validate_knowledge_docs(valid_applications)

    total_critical = (
        cmdb_report["critical_violations"] + incidents_report["critical_violations"]
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cmdb": cmdb_report,
        "incidents": incidents_report,
        "knowledge_docs": knowledge_report,
        "total_critical_violations": total_critical,
        "passed": total_critical == 0,
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(
        f"CMDB: {cmdb_report['row_count']:,} rows, {len(cmdb_report['issues'])} issue type(s)"
    )
    print(
        f"Incidents: {incidents_report['row_count']:,} rows, {len(incidents_report['issues'])} issue type(s)"
    )
    print(
        f"Knowledge docs: {knowledge_report['doc_count']} found, {len(knowledge_report['issues'])} issue type(s)"
    )
    print(f"Total critical violations: {total_critical}")
    print(f"Report written to {REPORT_PATH}")


if __name__ == "__main__":
    main()
