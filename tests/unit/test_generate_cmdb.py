from generate_cmdb import (
    APP_BUSINESS_UNIT_MAP,
    APP_OWNER_MAP,
    APPLICATIONS,
    generate_cmdb,
    generate_knowledge_docs,
)


def test_generates_requested_row_count():
    df = generate_cmdb(seed=1, n_assets=500)
    assert len(df) == 500


def test_no_nulls():
    df = generate_cmdb(seed=1, n_assets=500)
    assert df.isnull().sum().sum() == 0


def test_no_duplicate_asset_ids():
    df = generate_cmdb(seed=1, n_assets=500)
    assert df["asset_id"].duplicated().sum() == 0


def test_reproducible_with_fixed_seed():
    df1 = generate_cmdb(seed=1, n_assets=200)
    df2 = generate_cmdb(seed=1, n_assets=200)
    import pandas as pd

    pd.testing.assert_frame_equal(df1, df2)


def test_all_applications_are_from_known_list():
    df = generate_cmdb(seed=1, n_assets=500)
    assert set(df["application"].unique()) <= set(APPLICATIONS)


def test_service_owner_matches_application_mapping():
    df = generate_cmdb(seed=1, n_assets=500)
    for app, owner in zip(df["application"], df["service_owner"]):
        assert owner == APP_OWNER_MAP[app]


def test_business_unit_matches_application_mapping():
    df = generate_cmdb(seed=1, n_assets=500)
    for app, bu in zip(df["application"], df["business_unit"]):
        assert bu == APP_BUSINESS_UNIT_MAP[app]


def test_enum_fields_only_contain_valid_values():
    df = generate_cmdb(seed=1, n_assets=500)
    assert set(df["environment"].unique()) <= {"dev", "qa", "staging", "prod"}
    assert set(df["status"].unique()) <= {"active", "maintenance", "decommissioned"}
    assert set(df["os_type"].unique()) <= {"linux", "windows", "macos"}


def test_generate_knowledge_docs_writes_one_file_per_application(tmp_path):
    apps = ["order-service", "payment-gateway"]
    generate_knowledge_docs(apps, output_dir=str(tmp_path))
    files = sorted(f.name for f in tmp_path.iterdir())
    assert files == ["order-service.md", "payment-gateway.md"]


def test_knowledge_doc_content_mentions_correct_owner(tmp_path):
    generate_knowledge_docs(["payment-gateway"], output_dir=str(tmp_path))
    content = (tmp_path / "payment-gateway.md").read_text()
    assert "Payments Team" in content
    assert "Finance" in content
