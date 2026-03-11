# CPS ASEC Retirement Plan Access and Participation (2010–2024)

This repository provides a concise, reproducible workflow for constructing annual measures of employer-sponsored retirement plan access and participation among private-sector workers ages 20–64 using the CPS Annual Social and Economic Supplement (ASEC). It was prepared as a data exercise for the Brookings Institution Retirement Security Project.

**Research Question**
How have retirement plan access and participation rates changed from 2010–2024 among private-sector wage-and-salary workers ages 20–64?

**Data Provenance and Access**
The analysis uses IPUMS CPS ASEC microdata (2010–2024). Raw microdata are not redistributed here. If you have access, place your extract in `data/raw/` as a CSV or CSV.GZ. The replication script expects the IPUMS extract to include `YEAR`, `AGE`, `EMPSTAT`, `CLASSWKR`, `PENSION`, and `ASECWT`.

**Repository Structure**
- `code/` — replication script and notebook
- `data/raw/` — raw IPUMS extract (not included in public distribution)
- `data/processed/` — intermediate data products (optional)
- `output/figures/` — publication-ready figures
- `output/tables/` — analysis tables
- `writeup/` — LaTeX memo and bibliography
- `.github/workflows/` — lightweight CI checks

**Setup**
1. `python -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -r requirements.txt`

**Run the Pipeline**
From the repo root:

```bash
python code/run_all.py
```

If your raw extract has a different filename:

```bash
python code/run_all.py --raw-file data/raw/your_extract.csv.gz
```

**Outputs Generated**
- Main figure: `output/figures/retirement_access_participation_main_figure.png`
- Final annual table: `output/tables/final_annual_access_participation_table.csv`
- Additional figures: `output/figures/retirement_access_participation_timeseries.png`, `output/figures/retirement_access_participation_confidence_bands.png`
- Additional tables: `output/tables/retirement_access_participation_timeseries.csv`, `output/tables/retirement_access_participation_with_se.csv`, `output/tables/retirement_access_participation_with_se_rounded.csv`

**Sample Construction Notes**
- Ages 20–64
- Employed (EMPSTAT 10 or 12)
- Private-sector wage-and-salary workers (CLASSWKR 21, 22, or 23)
- Access is defined as `PENSION` in {2, 3}
- Participation (unconditional) is defined as `PENSION == 3`
- NIU values for `PENSION` are treated as no access/participation to preserve a consistent denominator

**Weighting Notes**
- Person-level weights use `ASECWT`
- Standard errors are approximate and use population-weight formulas: `sqrt(p*(1-p)/sum(weights))`

**Limitations**
- Standard errors are not design-based and do not incorporate the CPS complex survey design
- The CPS ASEC redesign in the mid-2010s may affect comparability across years
- Results depend on IPUMS harmonization and the exact extract used

**Replication Entry Point**
The primary replication entry point is `code/run_all.py`. The notebook at `code/build/c1_asec.ipynb` documents exploratory steps and variable validation.

**Citation**
See `CITATION.cff` for recommended citation metadata.

**Author**
Alejandro De La Torre
