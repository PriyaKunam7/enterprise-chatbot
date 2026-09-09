import pandas as pd

from generate_incidents import generate_incidents

APPLICATIONS = ["order-service", "payment-gateway", "inventory-service"]


def test_generates_requested_row_count():
    df = generate_incidents(APPLICATIONS, seed=1, n_incidents=300)
    assert len(df) == 300


def test_no_duplicate_incident_ids():
    df = generate_incidents(APPLICATIONS, seed=1, n_incidents=300)
    assert df["incident_id"].duplicated().sum() == 0


def test_every_service_references_a_known_application():
    df = generate_incidents(APPLICATIONS, seed=1, n_incidents=300)
    assert set(df["service"].unique()) <= set(APPLICATIONS)


def test_raises_on_empty_application_list():
    import pytest

    with pytest.raises(ValueError):
        generate_incidents([], seed=1, n_incidents=10)


def test_reproducible_with_fixed_seed():
    df1 = generate_incidents(APPLICATIONS, seed=1, n_incidents=200)
    df2 = generate_incidents(APPLICATIONS, seed=1, n_incidents=200)
    pd.testing.assert_frame_equal(df1, df2)


def test_open_incidents_have_no_resolved_at_or_root_cause():
    df = generate_incidents(APPLICATIONS, seed=1, n_incidents=500)
    open_incidents = df[df["status"] == "open"]
    assert open_incidents["resolved_at"].isna().all()
    assert open_incidents["root_cause"].isna().all()


def test_non_open_incidents_have_resolved_at_and_root_cause():
    df = generate_incidents(APPLICATIONS, seed=1, n_incidents=500)
    non_open = df[df["status"] != "open"]
    assert non_open["resolved_at"].notna().all()
    assert non_open["root_cause"].notna().all()


def test_severity_values_are_valid():
    df = generate_incidents(APPLICATIONS, seed=1, n_incidents=300)
    assert set(df["severity"].unique()) <= {"SEV1", "SEV2", "SEV3", "SEV4"}
