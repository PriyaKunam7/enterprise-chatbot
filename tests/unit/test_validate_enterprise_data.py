import pandas as pd

from validate_enterprise_data import (
    validate_cmdb,
    validate_incidents,
    validate_knowledge_docs,
)

VALID_CMDB_ROW = {
    "asset_id": "ASSET-000001",
    "hostname": "order-service-prod-0001.internal",
    "environment": "prod",
    "application": "order-service",
    "service_owner": "Platform Engineering",
    "business_unit": "Retail",
    "status": "active",
    "region": "us-east",
    "os_type": "linux",
    "lifecycle_state": "active",
}

VALID_INCIDENT_ROW = {
    "incident_id": "INC-000001",
    "service": "order-service",
    "severity": "SEV3",
    "status": "resolved",
    "opened_at": "2024-01-01T00:00:00",
    "resolved_at": "2024-01-01T01:00:00",
    "summary": "Some incident.",
    "root_cause": "Some cause.",
}


def make_cmdb(overrides_list):
    rows = [
        {**VALID_CMDB_ROW, "asset_id": f"ASSET-{i:06d}", **o}
        for i, o in enumerate(overrides_list, 1)
    ]
    return pd.DataFrame(rows)


def make_incidents(overrides_list):
    rows = [
        {**VALID_INCIDENT_ROW, "incident_id": f"INC-{i:06d}", **o}
        for i, o in enumerate(overrides_list, 1)
    ]
    return pd.DataFrame(rows)


def test_clean_cmdb_passes():
    df = make_cmdb([{}, {}])
    report = validate_cmdb(df)
    assert report["critical_violations"] == 0
    assert report["issues"] == []


def test_duplicate_asset_id_detected():
    df = make_cmdb([{"asset_id": "ASSET-000001"}, {"asset_id": "ASSET-000001"}])
    report = validate_cmdb(df)
    assert report["critical_violations"] > 0
    assert any(i["check"] == "duplicate_asset_id" for i in report["issues"])


def test_invalid_enum_detected_in_cmdb():
    df = make_cmdb([{"environment": "sandbox"}])
    report = validate_cmdb(df)
    assert any(i["check"] == "invalid_enum_values" for i in report["issues"])


def test_clean_incidents_pass_against_valid_applications():
    df = make_incidents([{}, {}])
    report = validate_incidents(df, valid_applications={"order-service"})
    assert report["critical_violations"] == 0


def test_broken_service_reference_detected():
    df = make_incidents([{"service": "does-not-exist"}])
    report = validate_incidents(df, valid_applications={"order-service"})
    assert report["critical_violations"] > 0
    assert any(i["check"] == "broken_service_reference" for i in report["issues"])


def test_duplicate_incident_id_detected():
    df = make_incidents([{"incident_id": "INC-000001"}, {"incident_id": "INC-000001"}])
    report = validate_incidents(df, valid_applications={"order-service"})
    assert any(i["check"] == "duplicate_incident_id" for i in report["issues"])


def test_invalid_severity_enum_detected():
    df = make_incidents([{"severity": "SEV9"}])
    report = validate_incidents(df, valid_applications={"order-service"})
    assert any(i["check"] == "invalid_enum_values" for i in report["issues"])


def test_missing_knowledge_doc_detected(tmp_path):
    (tmp_path / "order-service.md").write_text("# doc")
    report = validate_knowledge_docs(
        {"order-service", "payment-gateway"}, knowledge_dir=str(tmp_path)
    )
    assert any(i["check"] == "missing_knowledge_docs" for i in report["issues"])


def test_all_knowledge_docs_present(tmp_path):
    (tmp_path / "order-service.md").write_text("# doc")
    (tmp_path / "payment-gateway.md").write_text("# doc")
    report = validate_knowledge_docs(
        {"order-service", "payment-gateway"}, knowledge_dir=str(tmp_path)
    )
    assert report["issues"] == []
    assert report["doc_count"] == 2
