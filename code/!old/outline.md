# Component 1: CPS Data Exercise — Plan of Attack

## Objective
Construct annual measures of **retirement plan access** and **retirement plan participation** among **private-sector workers ages 20–64** for **2010–2024** using **CPS ASEC** data.

The final deliverables for Component 1 are:
1. A clearly formatted **figure** showing retirement plan access and/or participation over time.
2. A clearly formatted **table** showing the retirement plan access rate and sample size for each year.
3. A **1–2 page write-up** documenting:
   - sample construction,
   - the exact survey questions used,
   - weights used and why,
   - treatment of missing/ambiguous responses,
   - and how the 2015 CPS redesign may affect comparability over time.

---

## What this task is asking in plain English
We need to use CPS ASEC microdata to answer:

> Among working-age private-sector workers, what share had access to a retirement plan in each year, and what share participated in one?

This means we must:
- identify the relevant CPS ASEC variables,
- define the sample consistently across years,
- construct annual weighted rates,
- and document all choices clearly enough that someone else could reproduce the analysis.

---

## Key concepts to define

### 1. Retirement plan access
This likely means whether a worker's employer **offers or makes available** a retirement plan.

Open task:
- Find the exact CPS ASEC question and variable that captures employer-sponsored retirement plan access.

### 2. Retirement plan participation
This likely means whether a worker **actually participates in** the employer-sponsored retirement plan available to them.

Open task:
- Find the exact CPS ASEC question and variable that captures participation.

### 3. Annual measure
An "annual measure" likely means:
- for each survey year from 2010 through 2024,
- calculate the weighted share of the target population with access,
- and the weighted share with participation.

### 4. Target population
The target population is:
- age 20–64,
- employed,
- private-sector workers.

Open task:
- determine exactly how to identify "private-sector workers" in CPS ASEC,
- determine whether to include only wage-and-salary workers and exclude self-employed and government workers.

---

## Working assumptions (to verify)
These are initial assumptions only and must be checked against CPS documentation:

1. **Age restriction:** include respondents ages 20–64.
2. **Employment restriction:** include respondents who are employed at the time relevant to the retirement plan questions.
3. **Private-sector restriction:** include private wage-and-salary workers; likely exclude:
   - federal government workers,
   - state/local government workers,
   - self-employed workers,
   - unpaid family workers.
4. **Weights:** use the appropriate CPS ASEC person-level weight so annual estimates are nationally representative.
5. **Missing values:** document clearly whether missing / “don’t know” / “not in universe” responses are excluded, recoded, or treated as zero.
6. **Comparability:** the 2015 CPS redesign may create a break in the time series, so we need to be cautious when interpreting trends across that boundary.

---

## Concrete workflow

### Step 1: Identify the exact CPS ASEC variables
We need to find variables for:
- year,
- age,
- employment status,
- class of worker / sector,
- retirement plan access,
- retirement plan participation,
- survey weights.

Questions to answer:
- What is the exact wording of the retirement plan questions?
- Are the same questions asked in every year 2010–2024?
- Did variable names or response categories change after the 2015 redesign?

### Step 2: Define the analytic sample
Construct a person-level sample restricted to:
- ages 20–64,
- employed workers,
- private-sector workers.

Questions to answer:
- What CPS variable best identifies employment?
- What CPS variable best identifies private-sector status?
- Are there edge cases (e.g., incorporated self-employed) that need to be handled explicitly?

### Step 3: Construct outcome variables
For each eligible worker, construct:
- `access` = 1 if worker has access to a retirement plan, 0 otherwise
- `participation` = 1 if worker participates in a retirement plan, 0 otherwise

Need to document:
- exact coding rules,
- handling of missing / inapplicable responses,
- whether participation is conditional on access or measured directly.

### Step 4: Compute annual weighted estimates
For each year 2010–2024:
- weighted access rate,
- weighted participation rate,
- unweighted sample size.

### Step 5: Produce outputs
- Figure: annual retirement plan access and/or participation rates
- Table: annual access rate and sample size
- Save clean intermediate data and outputs for reproducibility.

### Step 6: Write up methodology
The write-up should explain:
- how the sample was constructed,
- what each retirement measure means,
- what weights were used,
- how missing values were treated,
- and how the 2015 redesign affects interpretation.

---

## Immediate next task
Before writing analysis code, the first priority is:

> Build a variable crosswalk for 2010–2024 that identifies the CPS ASEC variables for age, employment, class of worker, retirement plan access, retirement plan participation, and weights.

Once that crosswalk is complete, sample construction and coding decisions will be much easier to justify and explain.

---

## Open questions to resolve before analysis
1. What exact CPS ASEC variables correspond to retirement plan access and participation?
2. Are those measures fully comparable from 2010–2024?
3. What is the correct private-sector restriction?
4. Which weight should be used for annual nationally representative estimates?
5. How should “not in universe,” missing, and ambiguous responses be treated?
6. Should the figure show both access and participation, or just access with participation discussed separately?