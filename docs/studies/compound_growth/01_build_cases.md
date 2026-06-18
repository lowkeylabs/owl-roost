---
_quarto-vars:
  var_report_title: generic title from \_variables
engines:
- path: /opt/quarto/share/extension-subtrees/julia-engine/\_extensions/julia-engine/julia-engine.js
title: Build cases
toc-title: Table of contents
---

# Abstract

This module builds the case(s) for this study.

::: {.cell execution_count="1"}
``` {.python .cell-code}
from io import StringIO
import owlplanner as owl

CASE_FOLDER = "./cases"
SAVE_FILE_NAME = f"{CASE_FOLDER}/example1"

# Create the plan
plan = owl.Plan(['Jack'], ['1996-01-01'], [100],"Compound Growth Example")
plan.setLogstreams(False,logstreams=[StringIO(),StringIO()])

# Basic information
plan.setDescription("Jack is a millenial, born in 1996, and expects to live to 100.")
plan.setSexes(["M"])

# balance information and asset allocation information
plan.setAccountBalances(
    taxable=[0],
    taxDeferred=[0],
    taxFree=[10],
    startDate='2026-01-01',
)
plan.setAllocationRatios(
    'individual',
    generic = [
        [ [ 100.0, 0.0, 0.0, 0.0,], [ 100.0, 0.0, 0.0, 0.0,],],
    ]
)

# Spending profiles
#plan.setInterpolationMethod("linear")
plan.setSpendingProfile("flat")
#plan.setRates("user",values=[6.0,0,0,2.8])

# Rates
plan.setRates("default")
plan.setDefaultPlots(value="today")

# Do a quick run, then save
options = {'netSpending': 0.0, 'withMedicare': "none"}
plan.solve('maxBequest', options=options)
plan.saveConfig( SAVE_FILE_NAME )
```
:::

::: {.cell execution_count="2"}
``` {.python .cell-code}
from owlroost.catalog.context import build_catalog_context
from owlroost.display.loaders import load_case_rows
from owlroost.display.materializers.compare import materialize_compare_table
from owlroost.display.materializers.materialize import materialize_view
from owlroost.display.renderers.markdown_table import render_markdown_table

(
    schema_registry,
    metrics_registry,
    display_registry,
    catalog_rows,
    catalog_index,
) = build_catalog_context()
rows = load_case_rows(CASE_FOLDER, metrics_registry=metrics_registry)

diff_only = False
explain_facets = "variables"   # variables, values, sources, provenence, etc.

table = materialize_compare_table(
    rows,
    registry=display_registry,
    catalog_index=catalog_index,
    diff_only=False,
    explain_facets=explain_facets,
)
output = render_markdown_table( table )
```
:::

``` {.python .cell-code}
print(output)
```

  Field       case_example1.toml        Explanation
  ----------- ------------------------- -----------------------
  case_name   Compound Growth Example   Name of the case/plan

| **BASIC_INFO** \| \| \|
|   status \| single \| Filing status. Valid values: "single", "married"
  \|
|   names \| \[Jack\] \| Names of the individuals in the plan. Must
  contain 1 or 2 names. Length determines N_i \|
|   date_of_birth \| \[1996-01-01\] \| Date of birth for each individual
  in ISO format (e.g., "1967-01-15"). Defaults to "1965-01-15" if not
  specified \|
|   life_expectancy \| \[100\] \| Life expectancy in years for each
  individual \|
|   sexes \| \[M\] \| *(Optional)* Biological sex for each individual.
  Valid values: "M" or "F". Defaults to \["F"\] for single and
  \["M","F"\] for married when omitted. Recommended to set explicitly,
  especially when using longevity-risk sampling in stochastic spending
  \|
|   start_date \| 2026-01-01 \| Start date of the plan (e.g., "01-01",
  "01/01", "2026-01-01"). Only the month and day are used; the plan
  always starts in the current year. Defaults to "today" if not
  specified \|
|   state \| \| *(Optional)* Two-letter US state abbreviation for state
  income tax calculations (e.g., "MN", "CA"). Omit or set to "" for
  federal-only (no state tax) \|

| **SAVINGS_ASSETS** \| \| \|
|   taxable_savings_balances \| \[0\] \| Initial balance in taxable
  accounts for each individual (in thousands of dollars) \|
|   tax_deferred_savings_balances \| \[0\] \| Initial balance in
  tax-deferred accounts (e.g., 401k, traditional IRA) for each
  individual (in thousands of dollars) \|
|   tax_free_savings_balances \| \[10\] \| Initial balance in tax-free
  accounts (e.g., Roth IRA, Roth 401k) for each individual (in thousands
  of dollars) \|
|   hsa_savings_balances \| \[0\] \| *(Optional)* Initial balance in
  Health Savings Accounts (HSA) for each individual (in thousands of
  dollars). Defaults to \[0.0\] (or \[0.0, 0.0\] for married). HSA
  contributions must stop at Medicare enrollment (\~age 65); see HSA
  ctrb column in the HFP file \|

| **HOUSEHOLD_FINANCIAL_PROFILE** \| \| \|
|   HFP_file_name \| None \| Filename of the HFP workbook (typically
  .xlsx). Resolved relative to the directory of the case TOML when
  loading. Use "None" if the case has no HFP (wages and contributions
  are then zero unless set another way). \|

| **FIXED_INCOME** \| \| \|
|   pension_monthly_amounts \| \[0\] \| Monthly pension amount for each
  individual (in dollars). Use 0 if no pension \|
|   pension_ages \| \[65\] \| Age at which pension starts for each
  individual \|
|   pension_indexed \| \[False\] \| Whether each pension is indexed for
  inflation \|
|   pension_survivor_fraction \| \[0\] \| Fraction of pension (0--1)
  continuing to surviving spouse. 0 = single-life. Typical: 0, 0.5,
  0.75, 1.0 \|
|   social_security_pia_amounts \| \[0\] \| Primary Insurance Amount
  (PIA) for Social Security for each individual (in dollars) \|
|   social_security_ages \| \[67\] \| Age at which Social Security
  benefits start for each individual \|

| **RATES_SELECTION** \| \| \|
|   heirs_rate_on_tax_deferred_estate \| 30 \| Tax rate (as percentage,
  e.g., 30.0 for 30%) that heirs will pay on inherited tax-deferred and
  HSA accounts. Non-spouse HSA beneficiaries must include the full
  inherited HSA balance as ordinary income (IRC §223(f)(8)(B)) \|
|   dividend_rate \| 1.72 \| Dividend rate as a percentage (e.g., 1.72
  for 1.72%) \|
|   obbba_expiration_year \| 2032 \| Year when the OBBBA (One Big
  Beautiful Bill Act) provisions expire. Default is 2032 \|
|   method \| default \| Method for determining rates. Valid values:
  "trailing-30", "optimistic", "conservative", "user", "historical",
  "historical average", "gaussian", "histogaussian", "lognormal",
  "histolognormal", "bootstrap_sor", "var", "garch_dcc",
  "historical_copula", "gmm", "hmm", "dataframe" \|
|   from \| 1928 \| Starting year for historical data range (must be
  between 1928 and 2025). Default is 1928 \|
|   to \| 2025 \| Ending year for historical data range (must be between
  1928 and 2025, and greater than from). Default is 2025. garch_dcc
  requires at least 15 years of data (to - from ≥ 15) \|
|   reverse_sequence \| false \| If true, reverse the rate sequence
  along the time axis (e.g. last year first). Default is false. Ignored
  for fixed/constant rate methods. Used for both single-scenario and
  Historical Range runs. \|
|   roll_sequence \| 0 \| Number of years to roll (shift) the rate
  sequence; positive shifts toward the end, values wrap. Default is 0.
  Ignored for fixed/constant rate methods. Used for both single-scenario
  and Historical Range runs. \|

| **ASSET_ALLOCATION** \| \| \|
|   interpolation_method \| linear \| Method for gliding the allocation
  from initial to final values over time. "linear" = straight-line
  transition (equal steps each year). "s-curve" = smooth sigmoid (slow
  change at first, fast in the middle, slow again at the end),
  controlled by interpolation_center and interpolation_width. \|
|   type \| individual \| How the allocation is defined. "individual"
  --- each person has their own set of ratios applied identically to all
  their accounts. "account" --- separate ratios for each account type
  (taxable, tax-deferred, tax-free, HSA), allowing more aggressive
  allocation in tax-free accounts. "spouses" --- a single shared set of
  ratios applied across all accounts and both spouses simultaneously,
  reducing the number of parameters needed. *(Note: "spouses" is only
  available via the Python API, not the Streamlit UI.)* \|
|   generic \| \[100, 0, 0, 0\]`<br>`{=html}\[100, 0, 0, 0\] \| A single
  \[initial, final\] allocation pair shared by both spouses and applied
  uniformly across all their accounts. Structure: \[\[s0, b0, t0, c0\],
  \[sf, bf, tf, cf\]\]. Simpler to configure than "individual" when both
  spouses follow the same investment strategy. \|

| **OPTIMIZATION_PARAMETERS** \| \| \|
|   spending_profile \| flat \| Type of spending profile. Valid values:
  "flat", "smile" \|
|   surviving_spouse_spending_percent \| 60 \| Percentage of spending
  amount for the surviving spouse (0-100). Default is 60 \|
|   objective \| maxBequest \| Optimization objective. Valid values:
  "maxSpending", "maxBequest" \|

| **SOLVER_OPTIONS** \| \| \|
|   netSpending \| 0 \| Target net spending amount in today's dollars
  (in units). Used when objective = "maxBequest". \|
|   withMedicare \| none \| Medicare Part B and Part D IRMAA handling.
  Valid values: "none", "loop", "optimize" (expert). When not "none",
  Part B and Part D premiums (including IRMAA) are included; Part D can
  be disabled or given a base premium via the options below. \|

| **RESULTS** \| \| \|
|   default_plots \| today \| Default plot display mode. Valid values:
  "nominal" (nominal dollars), "today" (today's dollars) \|
|   worksheet_show_ages \| false \| When true (default false), adds
  per-person **age** columns next to year in both the on-screen tables
  and the saved Excel workbook. Each value is the individual's integer
  age on **December 31** of that row's calendar year. The cell is blank
  for years after that person's plan horizon. \|
|   worksheet_hide_zero_columns \| false \| When true (default false),
  the Streamlit **Worksheets** page omits numeric columns where every
  value is zero (within a small tolerance). The year and age columns are
  never removed. Applies to the **on-screen display only** --- the saved
  Excel workbook always retains all columns. \|
|   worksheet_real_dollars \| false \| When true (default false), all
  currency values in both the on-screen tables and the saved Excel
  workbook are divided by the cumulative inflation factor gamma_n,
  converting nominal dollars to today's (real) dollars. The saved Excel
  filename gains a \_real suffix to distinguish it from the nominal
  version. \|
