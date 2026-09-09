"""
Generates a synthetic CMDB (Configuration Management Database) asset
inventory and one Markdown knowledge/runbook document per application.

No real infrastructure names, hostnames, or identifiers are used
anywhere in this script -- everything is generated from fixed, fictional
vocabularies with a fixed random seed for reproducibility.

Usage:
    python scripts/generate_cmdb.py
"""

import os

import numpy as np
import pandas as pd

SEED = 42
N_ASSETS = 10_000

CMDB_OUTPUT_PATH = "data/cmdb.csv"
KNOWLEDGE_DIR = "data/knowledge"

ENVIRONMENTS = ["dev", "qa", "staging", "prod"]
STATUSES = ["active", "maintenance", "decommissioned"]
REGIONS = ["us-east", "us-west", "eu-west", "ap-southeast"]
OS_TYPES = ["linux", "windows", "macos"]
LIFECYCLE_STATES = ["provisioning", "active", "deprecated", "retired"]

BUSINESS_UNITS = ["Retail", "Logistics", "Finance", "Platform", "Customer Support"]

APPLICATIONS = [
    "order-service",
    "inventory-service",
    "payment-gateway",
    "shipping-tracker",
    "customer-portal",
    "notification-service",
    "auth-service",
    "billing-engine",
    "analytics-pipeline",
    "search-service",
    "recommendation-engine",
    "warehouse-management",
    "fraud-detection",
    "reporting-dashboard",
    "api-gateway",
]

SERVICE_OWNERS = [
    "Platform Engineering",
    "Payments Team",
    "Logistics Team",
    "Customer Experience Team",
    "Data Engineering",
    "Security Team",
    "SRE Team",
]

APP_OWNER_MAP = {
    "order-service": "Platform Engineering",
    "inventory-service": "Logistics Team",
    "payment-gateway": "Payments Team",
    "shipping-tracker": "Logistics Team",
    "customer-portal": "Customer Experience Team",
    "notification-service": "Platform Engineering",
    "auth-service": "Security Team",
    "billing-engine": "Payments Team",
    "analytics-pipeline": "Data Engineering",
    "search-service": "Platform Engineering",
    "recommendation-engine": "Data Engineering",
    "warehouse-management": "Logistics Team",
    "fraud-detection": "Security Team",
    "reporting-dashboard": "Data Engineering",
    "api-gateway": "SRE Team",
}

APP_BUSINESS_UNIT_MAP = {
    "order-service": "Retail",
    "inventory-service": "Logistics",
    "payment-gateway": "Finance",
    "shipping-tracker": "Logistics",
    "customer-portal": "Retail",
    "notification-service": "Platform",
    "auth-service": "Platform",
    "billing-engine": "Finance",
    "analytics-pipeline": "Platform",
    "search-service": "Retail",
    "recommendation-engine": "Retail",
    "warehouse-management": "Logistics",
    "fraud-detection": "Finance",
    "reporting-dashboard": "Platform",
    "api-gateway": "Platform",
}


def generate_cmdb(seed: int = SEED, n_assets: int = N_ASSETS) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    applications = rng.choice(APPLICATIONS, size=n_assets)
    environments = rng.choice(ENVIRONMENTS, size=n_assets, p=[0.35, 0.25, 0.15, 0.25])
    regions = rng.choice(REGIONS, size=n_assets)
    os_types = rng.choice(OS_TYPES, size=n_assets, p=[0.7, 0.25, 0.05])
    statuses = rng.choice(STATUSES, size=n_assets, p=[0.85, 0.1, 0.05])
    lifecycle_states = rng.choice(
        LIFECYCLE_STATES, size=n_assets, p=[0.1, 0.75, 0.1, 0.05]
    )

    asset_id = [f"ASSET-{i:06d}" for i in range(1, n_assets + 1)]
    hostname = [
        f"{app}-{env}-{i:04d}.internal"
        for i, (app, env) in enumerate(zip(applications, environments), start=1)
    ]
    service_owner = [APP_OWNER_MAP[app] for app in applications]
    business_unit = [APP_BUSINESS_UNIT_MAP[app] for app in applications]

    df = pd.DataFrame(
        {
            "asset_id": asset_id,
            "hostname": hostname,
            "environment": environments,
            "application": applications,
            "service_owner": service_owner,
            "business_unit": business_unit,
            "status": statuses,
            "region": regions,
            "os_type": os_types,
            "lifecycle_state": lifecycle_states,
        }
    )
    return df


def generate_knowledge_docs(
    applications: list[str], output_dir: str = KNOWLEDGE_DIR
) -> None:
    """Write one Markdown runbook per unique application."""
    os.makedirs(output_dir, exist_ok=True)

    for app in applications:
        owner = APP_OWNER_MAP[app]
        business_unit = APP_BUSINESS_UNIT_MAP[app]
        display_name = app.replace("-", " ").title()

        content = f"""# {display_name} Runbook

## Overview
{display_name} ({app}) is owned by {owner} and supports the {business_unit} business unit.

## Common Issues

### Elevated Error Rate
If {app} shows an elevated error rate, check recent deployments first and
review upstream dependency health before escalating.

### High Latency
Elevated latency in {app} is most often caused by downstream service
degradation or database connection pool exhaustion. Check connection
pool metrics before restarting the service.

## Support Procedures
1. Check the service dashboard for {app}.
2. Confirm whether the issue is isolated to one environment or region.
3. Review recent deployments and configuration changes.
4. If the issue persists, escalate to {owner}.

## Escalation
For unresolved incidents affecting {app}, escalate to {owner} via the
on-call channel for the {business_unit} business unit.
"""
        path = os.path.join(output_dir, f"{app}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)


def main() -> None:
    df = generate_cmdb()
    os.makedirs(os.path.dirname(CMDB_OUTPUT_PATH), exist_ok=True)
    df.to_csv(CMDB_OUTPUT_PATH, index=False)
    print(f"Generated {len(df):,} CMDB assets -> {CMDB_OUTPUT_PATH}")

    unique_applications = sorted(df["application"].unique())
    generate_knowledge_docs(unique_applications)
    print(f"Generated {len(unique_applications)} knowledge docs -> {KNOWLEDGE_DIR}/")


if __name__ == "__main__":
    main()
