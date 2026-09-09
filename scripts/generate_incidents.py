"""
Generates synthetic incident records, each referencing a real
application from the CMDB dataset (data/cmdb.csv) -- a genuine
foreign-key relationship enforced at generation time.

Usage:
    python scripts/generate_incidents.py
"""

import os

import numpy as np
import pandas as pd

SEED = 43
N_INCIDENTS = 2_000

CMDB_INPUT_PATH = "data/cmdb.csv"
INCIDENTS_OUTPUT_PATH = "data/incidents.csv"

SEVERITIES = ["SEV1", "SEV2", "SEV3", "SEV4"]
STATUSES = ["open", "mitigated", "resolved"]

CAUSE_PHRASES = [
    "a downstream dependency timeout",
    "database connection pool exhaustion",
    "a misconfigured deployment",
    "elevated traffic beyond provisioned capacity",
    "an expired credential",
    "a memory leak in a recent release",
    "network partition between regions",
    "an unhandled exception in a new code path",
]

ROOT_CAUSE_PHRASES = [
    "Insufficient connection pool sizing for peak load.",
    "A configuration change was deployed without a canary rollout.",
    "An upstream dependency exceeded its SLA during a regional failover.",
    "A credential rotation job failed silently.",
    "A memory leak introduced in the previous release caused gradual degradation.",
    "Capacity was not scaled ahead of a known traffic event.",
]


def load_applications(cmdb_path: str = CMDB_INPUT_PATH) -> list[str]:
    cmdb = pd.read_csv(cmdb_path)
    return sorted(cmdb["application"].unique())


def generate_incidents(
    applications: list[str], seed: int = SEED, n_incidents: int = N_INCIDENTS
) -> pd.DataFrame:
    if not applications:
        raise ValueError(
            "applications list is empty -- cannot generate incidents without a CMDB"
        )

    rng = np.random.default_rng(seed)

    incident_id = [f"INC-{i:06d}" for i in range(1, n_incidents + 1)]
    services = rng.choice(applications, size=n_incidents)
    severities = rng.choice(SEVERITIES, size=n_incidents, p=[0.05, 0.15, 0.35, 0.45])
    statuses = rng.choice(STATUSES, size=n_incidents, p=[0.1, 0.15, 0.75])

    start = pd.Timestamp("2024-01-01")
    end = pd.Timestamp("2025-12-31")
    seconds_range = int((end - start).total_seconds())
    open_offsets = rng.integers(0, seconds_range, size=n_incidents)
    opened_at = start + pd.to_timedelta(open_offsets, unit="s")

    duration_minutes = rng.uniform(15, 600, size=n_incidents)
    resolved_at = opened_at + pd.to_timedelta(duration_minutes, unit="m")

    causes = rng.choice(CAUSE_PHRASES, size=n_incidents)
    summaries = [
        f"Incident on {svc} triggered by {cause}."
        for svc, cause in zip(services, causes)
    ]

    root_causes = rng.choice(ROOT_CAUSE_PHRASES, size=n_incidents)

    df = pd.DataFrame(
        {
            "incident_id": incident_id,
            "service": services,
            "severity": severities,
            "status": statuses,
            "opened_at": opened_at,
            "resolved_at": resolved_at,
            "summary": summaries,
            "root_cause": root_causes,
        }
    )

    open_mask = df["status"] == "open"
    df.loc[open_mask, "resolved_at"] = pd.NaT
    df.loc[open_mask, "root_cause"] = None

    return df


def main() -> None:
    applications = load_applications()
    df = generate_incidents(applications)

    os.makedirs(os.path.dirname(INCIDENTS_OUTPUT_PATH), exist_ok=True)
    df.to_csv(INCIDENTS_OUTPUT_PATH, index=False)
    print(f"Generated {len(df):,} incidents -> {INCIDENTS_OUTPUT_PATH}")
    print(f"Referencing {len(applications)} applications from {CMDB_INPUT_PATH}")


if __name__ == "__main__":
    main()
