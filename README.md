# Retirement Plan Access and Participation Using CPS ASEC

This repository contains the code and analysis used to construct annual measures of employer-sponsored retirement plan access and participation among private-sector workers ages 20–64 using the CPS Annual Social and Economic Supplement (ASEC).

The project was completed as part of a data exercise for the Brookings Institution Retirement Security Project.

## Contents

- `code/` – Jupyter notebook used to construct the analytic dataset and produce estimates
- `output/figures/` – final figures used in the write-up
- `output/tables/` – annual estimates exported from the analysis
- `writeup/` – LaTeX memo summarizing the analysis

## Data

The analysis uses CPS ASEC microdata from IPUMS CPS. Due to licensing restrictions, the raw data are not included in this repository.

To replicate the analysis:

1. Download CPS ASEC data from https://cps.ipums.org
2. Place the extract in the `data/` directory
3. Run `code/c1_asec.ipynb`

## Methods

The analysis constructs:

- Retirement plan access
- Conditional participation
- Unconditional participation

among private-sector wage-and-salary workers ages 20–64 from 2010–2024.

All estimates are weighted using the CPS ASEC person weight (`ASECWT`).

## Author

Alejandro De La Torre