# CPS ASEC Retirement Plan Access and Participation (2010–2024)

This repository provides a reproducible workflow for constructing annual measures of employer-sponsored retirement plan access and participation among private-sector workers ages 20–64 using the CPS Annual Social and Economic Supplement (ASEC). It was prepared as a data exercise for the Brookings Institution Retirement Security Project.

**Research question / task objective**
Measure how retirement plan access and participation evolve over time for private-sector wage-and-salary workers, and document the sample construction and weighting choices behind those estimates.

**Data source**
IPUMS CPS ASEC microdata (2010–2024). Raw microdata are not redistributed here. If you have access, place your extract in `data/raw/` as a CSV or CSV.GZ (the script expects the IPUMS extract to include `YEAR`, `AGE`, `EMPSTAT`, `CLASSWKR`, `PENSION`, and `ASECWT`).

**Repository structure**
- `code/` — replication scripts and notebook
- `data/raw/` — raw IPUMS extract (not included in public distribution)
- `data/processed/` — intermediate data products (optional)
- `output/figures/` — publication-ready figures
- `output/tables/` — analysis tables
- `writeup/` — LaTeX memo and bibliography

**Setup**
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`

**Run the full pipeline**
From the repo root:

```bash
python code/run_all.py
```

If the raw extract is not named `cps_00001.csv.gz`, pass it explicitly:

```bash
python code/run_all.py --raw-file data/raw/your_extract.csv.gz
```

**Outputs generated**
Tables (written to `output/tables/`):
- `retirement_access_participation_timeseries.csv`
- `retirement_access_participation_with_se.csv`
- `retirement_access_participation_with_se_rounded.csv`
- `final_annual_access_participation_table.csv`

Figures (written to `output/figures/`):
- `retirement_access_participation_timeseries.png`
- `retirement_access_participation_confidence_bands.png`
- `retirement_access_participation_main_figure.png`

**Notes on weighting and sample construction**
- Sample restrictions: ages 20–64, employed (EMPSTAT 10 or 12), and private-sector wage-and-salary workers (CLASSWKR 21, 22, or 23).
- Access and participation are derived from `PENSION` in the IPUMS extract (NIU values are treated as no access/participation to reproduce the existing outputs).
- Person-level weights use `ASECWT`.
- Standard errors are approximate and use population-weight formulas: `sqrt(p*(1-p)/sum(weights))`.

**Limitations**
- Standard errors are not design-based and do not incorporate CPS complex survey design.
- Question wording and survey design changes (notably around the mid-2010s redesign) may affect comparability.
- Results depend on IPUMS harmonization choices and the exact extract used.

**Citation**
If you use this repository, please cite it using the metadata in `CITATION.cff`.

**Author**
Alejandro De La Torre
