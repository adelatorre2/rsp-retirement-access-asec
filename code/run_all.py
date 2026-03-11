"""
End-to-end replication pipeline for the CPS ASEC retirement access analysis.

This script:
- locates the project root using pathlib
- loads the IPUMS CPS ASEC extract from data/raw
- constructs the analytic sample and annual estimates
- writes publication-ready tables and figures to output/
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

REQUIRED_COLUMNS = {
    "YEAR",
    "AGE",
    "EMPSTAT",
    "CLASSWKR",
    "PENSION",
    "ASECWT",
}


def find_repo_root(start: Path) -> Path:
    """Walk up from start until a repo root is found."""
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
        if (parent / "code").exists() and (parent / "data").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate the repository root. Expected a directory containing .git, code/, and data/."
    )


def find_raw_extract(
    raw_dir: Path,
    repo_root: Path,
    explicit_path: str | None = None,
) -> Path:
    """Resolve the raw IPUMS extract path, preferring an explicit path if provided."""
    if not raw_dir.exists():
        raise FileNotFoundError(
            f"Raw data directory not found: {raw_dir}. Expected data/raw/ under the repo root."
        )
    if explicit_path:
        candidate = Path(explicit_path)
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        if not candidate.exists():
            raise FileNotFoundError(
                f"Raw data file not found: {candidate}. Provide a valid path via --raw-file."
            )
        return candidate

    default = raw_dir / "cps_00001.csv.gz"
    if default.exists():
        return default

    candidates = sorted(raw_dir.glob("*.csv")) + sorted(raw_dir.glob("*.csv.gz"))
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) == 0:
        raise FileNotFoundError(
            "No raw CPS ASEC extract found. Place your IPUMS extract in data/raw/ (CSV or CSV.GZ)."
        )

    choices = "\n".join(f"- {path.name}" for path in candidates)
    raise FileNotFoundError(
        "Multiple raw extracts found in data/raw/. Specify one with --raw-file.\n" + choices
    )


def ensure_dirs(*paths: Path) -> None:
    """Create directories if they do not exist."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def load_raw_extract(path: Path) -> pd.DataFrame:
    """Load the raw IPUMS CPS ASEC extract with only the required columns."""
    df = pd.read_csv(path, usecols=sorted(REQUIRED_COLUMNS), low_memory=False)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(
            "Missing required columns in the raw extract: "
            f"{missing_list}. Update the IPUMS extract or adjust the script."
        )
    return df


def build_analytic_sample(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sample restrictions and construct access/participation measures.

    Sample definition:
    - ages 20–64
    - employed (EMPSTAT 10 or 12)
    - private-sector wage-and-salary workers (CLASSWKR 21, 22, 23)
    """
    df = df.copy()

    df = df[(df["YEAR"] >= 2010) & (df["YEAR"] <= 2024)]
    df = df[(df["AGE"] >= 20) & (df["AGE"] <= 64)]
    df = df[df["EMPSTAT"].isin([10, 12])]
    df = df[df["CLASSWKR"].isin([21, 22, 23])]
    df = df.copy()

    # Access = employer has a plan (PENSION 2 or 3).
    # NIU values are treated as no access/participation to match the existing outputs.
    df["access"] = np.where(df["PENSION"].isin([2, 3]), 1.0, 0.0)
    # Unconditional participation = included in a plan (PENSION 3).
    df["participation_unconditional"] = np.where(df["PENSION"] == 3, 1.0, 0.0)

    df = df.rename(columns={"YEAR": "year"})
    return df


def weighted_mean(x: pd.Series, w: pd.Series) -> float:
    """Compute a weighted mean."""
    return float((x * w).sum() / w.sum())


def weighted_se_binary(p: float, w: pd.Series) -> float:
    """Approximate standard error for a weighted binary proportion.

    Uses population weights: sqrt(p * (1 - p) / sum(w)).
    This is a simple approximation and not a design-based CPS standard error.
    """
    return float(np.sqrt(p * (1.0 - p) / w.sum()))


def compute_annual_estimates(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Compute annual rates, standard errors, and confidence intervals."""
    rows = []
    rows_se = []
    z = 1.96

    for year, g in df.groupby("year"):
        w = g["ASECWT"]
        access_rate = weighted_mean(g["access"], w)
        part_uncond = weighted_mean(g["participation_unconditional"], w)

        g_access = g[g["access"] == 1]
        part_cond = weighted_mean(
            g_access["participation_unconditional"], g_access["ASECWT"]
        ) if len(g_access) else np.nan

        access_se = weighted_se_binary(access_rate, w)
        part_uncond_se = weighted_se_binary(part_uncond, w)
        part_cond_se = weighted_se_binary(part_cond, g_access["ASECWT"]) if len(g_access) else np.nan

        rows.append(
            {
                "year": int(year),
                "access_rate": access_rate,
                "participation_unconditional": part_uncond,
                "participation_conditional": part_cond,
                "n_obs": int(len(g)),
            }
        )

        rows_se.append(
            {
                "year": int(year),
                "access_rate": access_rate,
                "access_se": access_se,
                "participation_unconditional": part_uncond,
                "participation_unconditional_se": part_uncond_se,
                "participation_conditional": part_cond,
                "participation_conditional_se": part_cond_se,
                "n_obs": int(len(g)),
                "access_ci_lower": access_rate - z * access_se,
                "access_ci_upper": access_rate + z * access_se,
                "participation_ci_lower": part_uncond - z * part_uncond_se,
                "participation_ci_upper": part_uncond + z * part_uncond_se,
            }
        )

    df_timeseries = pd.DataFrame(rows).sort_values("year")
    df_se = pd.DataFrame(rows_se).sort_values("year")

    df_se_rounded = df_se.copy()
    rate_cols = [
        "access_rate",
        "access_se",
        "participation_unconditional",
        "participation_unconditional_se",
        "participation_conditional",
        "participation_conditional_se",
        "access_ci_lower",
        "access_ci_upper",
        "participation_ci_lower",
        "participation_ci_upper",
    ]
    df_se_rounded[rate_cols] = df_se_rounded[rate_cols].round(4)
    df_se_rounded["n_obs"] = df_se_rounded["n_obs"].astype(int)

    return df_timeseries, df_se, df_se_rounded


def write_tables(
    df_timeseries: pd.DataFrame,
    df_se: pd.DataFrame,
    df_se_rounded: pd.DataFrame,
    tables_dir: Path,
) -> None:
    """Write all output tables."""
    df_timeseries.to_csv(tables_dir / "retirement_access_participation_timeseries.csv", index=False)
    df_se.to_csv(tables_dir / "retirement_access_participation_with_se.csv", index=False)
    df_se_rounded.to_csv(
        tables_dir / "retirement_access_participation_with_se_rounded.csv",
        index=False,
    )

    final_table = df_timeseries[[
        "year",
        "access_rate",
        "participation_unconditional",
        "n_obs",
    ]].copy()
    final_table = final_table.rename(
        columns={
            "year": "Year",
            "access_rate": "Access rate",
            "participation_unconditional": "Participation rate",
            "n_obs": "Sample size",
        }
    )
    final_table[["Access rate", "Participation rate"]] = final_table[[
        "Access rate",
        "Participation rate",
    ]].round(4)
    final_table.to_csv(tables_dir / "final_annual_access_participation_table.csv", index=False)


def plot_timeseries(df: pd.DataFrame, figures_dir: Path) -> None:
    """Generate the main time-series figures."""
    plt.style.use("seaborn-v0_8-whitegrid")

    # Simple time series
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(df["year"], df["access_rate"], label="Access rate", linewidth=2)
    ax.plot(df["year"], df["participation_unconditional"], label="Participation rate", linewidth=2)
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate")
    ax.set_ylim(0, 1)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(figures_dir / "retirement_access_participation_timeseries.png", dpi=300)
    plt.close(fig)


def plot_confidence_bands(df_se: pd.DataFrame, figures_dir: Path) -> None:
    """Generate a figure with 95% confidence bands."""
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(df_se["year"], df_se["access_rate"], label="Access rate", linewidth=2)
    ax.fill_between(
        df_se["year"],
        df_se["access_ci_lower"],
        df_se["access_ci_upper"],
        alpha=0.2,
    )

    ax.plot(
        df_se["year"],
        df_se["participation_unconditional"],
        label="Participation rate",
        linewidth=2,
    )
    ax.fill_between(
        df_se["year"],
        df_se["participation_ci_lower"],
        df_se["participation_ci_upper"],
        alpha=0.2,
    )

    ax.set_xlabel("Year")
    ax.set_ylabel("Rate")
    ax.set_ylim(0, 1)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(figures_dir / "retirement_access_participation_confidence_bands.png", dpi=300)
    plt.close(fig)


def plot_main_figure(df_se: pd.DataFrame, figures_dir: Path) -> None:
    """Generate the final presentation figure."""
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(df_se["year"], df_se["access_rate"], label="Access rate", linewidth=2.5)
    ax.plot(
        df_se["year"],
        df_se["participation_unconditional"],
        label="Participation rate",
        linewidth=2.5,
    )
    ax.set_xlabel("Year")
    ax.set_ylabel("Rate")
    ax.set_ylim(0, 1)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(figures_dir / "retirement_access_participation_main_figure.png", dpi=300)
    plt.close(fig)


def main() -> None:
    """Run the full pipeline."""
    parser = argparse.ArgumentParser(description="Run the CPS ASEC replication pipeline.")
    parser.add_argument(
        "--raw-file",
        type=str,
        default=None,
        help=(
            "Path to the IPUMS CPS ASEC extract (relative to the repo root). "
            "If omitted, the script searches data/raw/ for a single CSV or CSV.GZ."
        ),
    )
    args = parser.parse_args()

    try:
        repo_root = find_repo_root(Path(__file__).resolve().parent)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    data_dir = repo_root / "data"
    raw_dir = data_dir / "raw"
    output_dir = repo_root / "output"
    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables"

    ensure_dirs(figures_dir, tables_dir)

    try:
        raw_file = find_raw_extract(raw_dir, repo_root, args.raw_file)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading raw extract: {raw_file}")

    try:
        df_raw = load_raw_extract(raw_file)
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    df_sample = build_analytic_sample(df_raw)
    df_timeseries, df_se, df_se_rounded = compute_annual_estimates(df_sample)

    write_tables(df_timeseries, df_se, df_se_rounded, tables_dir)
    plot_timeseries(df_timeseries, figures_dir)
    plot_confidence_bands(df_se, figures_dir)
    plot_main_figure(df_se, figures_dir)

    print("Pipeline complete.")
    print(f"Tables written to: {tables_dir}")
    print(f"Figures written to: {figures_dir}")


if __name__ == "__main__":
    main()
