# Chapter 10 (Transition Risk) — scoping & roadmap

Chapter 10 ships 32 `chap10_*.m` exercise scripts (confirmed by direct
`ls`, not filename-pattern estimation — the earlier placeholder note in
`CHAPTERS.md` guessed 43, which was wrong) plus one shared helper
function in the chapter's own folder (`internal_rate_return.m`, not
part of the `hfs-archive` toolbox) and a `Data/` folder of real-world
carbon-pricing/stranded-asset datasets.

Content-wise this chapter is welfare/public economics applied to
climate transition: cost-benefit analysis, externalities and Pigouvian
taxation, the Weitzman "prices vs. quantities" instrument-choice result,
real-world carbon-pricing coverage, and stranded fossil-fuel assets —
a natural companion to Chapter 9's carbon-accounting content, this time
from an economics-of-policy-instruments angle rather than a
measurement angle.

## Planned notebook split

| Notebook | Scripts | Topic | Status |
|---|---|---|---|
| `10a_cost_benefit_analysis` | `cba1`, `cba2` (2) | Welfare-weighted cost-benefit analysis (utilitarian/Rawlsian/Kaldor-Hicks weightings) and project appraisal (NPV/BCR/PI/IRR) worked examples, including a break-even discount-rate search. No data dependency. | ✅ |
| `10b_decarbonization_investment_pathways` | `decarbonization_pathway1`, `pathway3`, `pathway4`, `sector1` (4) | Sector-level CO2/CH4 emission-source shares, the 2030 critical-minerals-for-clean-energy investment-flow pie chart (`pathway3` and `sector1` share the same underlying investment-flow data — `sector1` extends it with a GSS-labelled-vs-not sub-split, so both are kept, not deduplicated), and a critical-minerals supply/demand-gap small-multiples chart (`pathway4`). No data dependency. | ✅ |
| `10c_externalities_and_pigouvian_tax` | `externality1`, `externality2a`, `externality2b`, `externality3` (4) | Textbook supply/demand deadweight-loss diagrams (market equilibrium vs. a quantity restriction), the externality/social-marginal-cost DWL diagram (consumer/producer surplus, external cost, overproduction), and the Pigouvian-tax-correction diagram. No data dependency. | ✅ |
| `10d_externality_comparative_statics` | `externality4a`-`4e` (5) | Five comparative-statics variants of the same linear-supply/demand DWL diagram (SMC shift vs. SMB shift, in both directions) — built via one shared parametrized helper function since the structure is identical across all 5. No data dependency. | ✅ |
| `10e_weitzman_prices_vs_quantities` | `externality5a`, `5b`, `5d`, `5e` buildable (4); `5c` near-duplicate of `5b`, skipped | Weitzman's classic "prices vs. quantities" result: choosing a price instrument (tax) vs. a quantity instrument (cap) for pollution control under marginal-abatement-cost uncertainty. `5a`/`5b`/`5d` are worked-example print-outs at different uncertainty distributions/slope parameters (`5c` confirmed byte-for-byte-identical *inputs* to `5b`, just a condensed re-run without the numerical-integration check — skipped per the near-duplicate convention); `5e` sweeps the marginal-cost slope and plots where each instrument's expected welfare dominates, crossing exactly at $\\beta_C=\\beta_B$. No data dependency. | ✅ |
| `10f_carbon_pricing_landscape` | `pricing1`, `pricing2a`, `pricing2b`, `pricing3`, `pricing4` buildable (5); `pricing5`, `pricing6`, `pricing7` blocked (3) | Real-world carbon pricing: World Bank 2025 carbon tax and ETS price/coverage tables by country/instrument, the EU ETS carbon price time series (bar chart, two source vintages spliced at a pivot date), voluntary carbon market (Ecosystem Marketplace) prices by project category, and the top-15 carbon-pricing schemes by revenue/coverage share. | ✅ |
| `10g_stranded_fossil_assets` | `stranded1`-`4` (4) | Stranded fossil-fuel reserves: a circle-packing "carbon bubble" chart at 50%/80% warming-budget probabilities (self-contained hardcoded data), a simple worked example on reserve categories vs. a budget constraint, a full stranded-asset valuation model (production/price/marginal-cost paths under baseline vs. climate scenarios, discounted at 4 rates) using real data, and a Hansen-style stranded-value table by fuel type and discount rate. | ✅ |

Total: 2 + 4 + 4 + 5 + 5 + 5 + 4 = 29 buildable scripts + 3 blocked = 32,
matching the archive's confirmed file count exactly.

**Chapter 10 is now complete (2026-08-22)**: all 7 notebooks (`10a`-`10g`)
built, verified (0 errors/0 stderr warnings, every figure visually
checked), delivered, and tracked. 29 of the chapter's 32 exercise
scripts are built faithfully (`5c` additionally folded into `5b` as a
confirmed near-duplicate, not counted separately); the other 3
(`pricing5`/`6`/`7`) are explicitly flagged as blocked on MCOS-opaque
MATLAB `table` serialization with no `.xlsx` fallback anywhere in the
archive, rather than skipped silently or faked. Two disclosed
simplifications: `10b`'s `sector1` section doesn't reproduce the
source's hand-tuned per-slice pie-label offsets, and `10g`'s `stranded1`
"carbon bubble" chart uses per-axes legend text instead of the source's
absolute figure-fraction `annotation()` placement — in both cases all
underlying data, colors, and chart semantics are faithful, only exact
pixel layout differs.

## Data-blocked scripts (3 of 32)

Unlike Chapter 9's data-blocking (missing files entirely), Chapter 10's
blockers are a **format** problem: `pricing5`, `pricing6`, and
`pricing7` all ultimately depend on `chap10_eutl_2023.mat` and/or
`chap10_cdp_icp_2023.mat`/`chap10_coverage_carbon_pricing_2022.mat` —
`.mat` files whose payload is a MATLAB `table` object serialized as an
**MCOS opaque type** (`scipy.io.loadmat` loads the file without error,
but the actual variable comes back as an unparseable
`MatlabOpaque`/`MCOS`/`table` blob, not usable data — confirmed by
direct inspection, not assumed). This is a different failure mode from
Chapter 8's "check `scipy.io.loadmat` vs. `h5py`/`mat73` for v7.3 files"
caveat: it isn't a v5-vs-v7.3 format issue that a different reader
would fix, it's that MATLAB's own `table` class serialization has no
standard non-MATLAB deserializer. No `.xlsx`/`.csv` fallback exists for
either `chap10_eutl_2023` or `chap10_cdp_icp_2023` anywhere in the
archive (`chap10_cdp_icp_2023.m`'s own prep script reads from a
`chap10_cdp_icp_2023.xlsx` that was apparently never actually shipped
into `Data/` — checked directly, not present). `pricing5`
(`chap10_coverage_carbon_pricing_2022`) cascades from the same
`eutl_2023` blocker since its own prep script derives from it.
Two source data files (`chap10_carbon_tracker_2011.xlsx`,
`chap10_welsby_2021.xlsx`) are present in `Data/` but not referenced by
any of the 32 scripts — orphaned, left unused.

## Progress notes

- **`10a`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 6
  cells, no figures (table-only). `internal_rate_return` ported
  faithfully as described above; break-even discount rate between the
  two illustrative projects came out to 4.37%.
- **`10b`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  11 cells, 4 figures all visually confirmed correct (sector CO2/CH4
  grouped bar chart; investment-flow pie with correct >10% exploding;
  6-mineral supply/demand small-multiples grid; 16-slice GSS/non-GSS
  split pie). One disclosed simplification: `sector1`'s hand-tuned
  per-slice `pie_delta` label offsets were not reproduced — matplotlib's
  default label placement is used instead, with the same data, sort
  order, and two-tone GSS/non-GSS coloring scheme.
- **`10c`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  10 cells, 3 figures all visually confirmed correct (market-equilibrium
  DWL-from-quantity-restriction diagram; externality/overproduction DWL
  diagram with consumer/producer surplus, external costs, and points
  A/B/C; Pigouvian-tax diagram showing the taxed equilibrium landing
  exactly on the untaxed social optimum) plus one numeric worked-example
  table (`externality2b`, net social benefit maximized at $q=6$,
  confirming the graphical social optimum from Section 2). Fixed a
  matplotlib-specific issue during the build: with both axis spines
  pinned to the origin (to mirror MATLAB's `XAxisLocation`/
  `YAxisLocation = 'origin'`), `ax.set_xlabel`/`set_ylabel`'s default
  placement collides with the origin-anchored `q*`/`p*`/`q'`/`p'`
  annotations — fixed by placing the axis titles as free-floating
  `ax.text()` calls at explicit offsets instead, matching the source's
  own explicit label `Position` overrides.
- **`10d`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  12 cells, 5 figures all visually confirmed correct. Built via one
  shared `dwl_shift_diagram(shift, params1, params2, ...)` helper
  (packaging candidate, see `PACKAGING_CANDIDATES.md`'s "Chapter 10d"
  section) parametrized by `shift='cost'` (SMC shifts, `4a`/`4d`) or
  `shift='benefit'` (SMB shifts, `4b`/`4c`/`4e`). Caught and fixed a
  color-mapping bug during the build: a first draft plotted the SMB and
  SMC/SMC1 curves in swapped colors for the `shift='cost'` branch
  (SMC1 came out blue and the fixed SMB came out green, versus the
  source's blue=SMB/green=SMC1/red=SMC2 convention) — caught by visual
  inspection of the first rendered figure (blue line was upward-sloping,
  which is wrong for a demand-side SMB curve) and fixed before
  finalizing.
- **`10e`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  10 cells, 1 figure visually confirmed correct (the two expected-
  welfare curves cross exactly at $\\beta_C=\\beta_B=4$, with correct
  red/teal shading on each side). Built via one shared
  `weitzman_example(...)` helper (packaging candidate, see
  `PACKAGING_CANDIDATES.md`'s "Chapter 10e" section) covering `5a`
  (with the numerical-vs-analytical welfare check via `scipy.integrate.
  quad`, matching MATLAB's `integral` to ~1e-14), `5b`, and `5d`; `5c`
  confirmed as a near-duplicate of `5b` (identical inputs) and skipped.
  All closed-form Delta(W) values reproduced the direct numeric
  computation exactly, cross-checked by hand before building.
- **`10f`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  12 cells, 1 figure visually confirmed correct (EU ETS price series
  shows the historically accurate trajectory — ~20-25 EUR in 2008,
  crashing to single digits 2012-2017 during the oversupply era, then
  rising steadily post-2018 to a ~90-95 EUR peak in 2022-2023) plus 4
  data tables (top-33 carbon tax schemes, top-33 ETS schemes, voluntary
  carbon market prices by category, top-15 schemes by coverage share
  and by revenue). Source `.mat` files (`chap10_world_bank_carbon_
  price_2025.mat`, `chap10_ecosystem_marketplace_2025.mat`,
  `chap10_eu_ets_carbon_price.mat`) were bypassed entirely — every one
  has a readable `.xlsx` sibling that the source's own prep scripts
  were themselves built from, copied into `data/` and read directly via
  `pandas.read_excel`. Diagnostic totals (28.58% of global GHG emissions
  covered by carbon pricing; \\$102.19bn total 2024 revenue, across all
  91/92 schemes not just the top 15 shown) both fall in the range of
  publicly known figures — a plausibility check, not a guarantee of
  exact match to any single published estimate.
- **`10g`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  10 cells, 1 figure visually confirmed correct (the "carbon bubble"
  nested-circle chart: 6 bottom-aligned circles per probability
  scenario, correctly showing no 1.5°C-compatible reserve at all under
  80% confidence) plus 3 worked-example/table sections (`stranded2`'s
  budget-allocation logic, `stranded3`'s full discounted stranded-value
  model showing total stranded value declining from \\$53.4bn at 0%
  discount to \\$22.2bn at 10%, and `stranded4`'s Hansen-table
  percentage-of-total breakdown). This completes Chapter 10 — all 7
  notebooks (`10a`-`10g`) built and verified.

## Custom/missing-function inventory

- **`internal_rate_return(cf)`** — ships as a plain `.m` file directly
  inside the chapter's own folder (not `hfs-archive`'s shared toolbox),
  so its source is fully visible: finds the roots of the cashflow
  polynomial, converts to a rate via `1/root - 1`, keeps only real
  roots, and returns the largest if multiple exist (or `NaN` if none).
  A direct `numpy.roots`-based port, used in `10a`.
- **`bisection`** — already ported (from Chapter 8, reused in `08d`);
  Chapter 10 doesn't call it directly in any script read so far, but is
  available if a later section needs a general root-finder.
- No other custom/undocumented functions were found across all 32
  scripts — Chapter 10 is unusually self-contained compared to
  Chapters 8/9, leaning on closed-form economics formulas rather than
  bespoke toolbox functions.

## Working conventions (same as the rest of the series)

- Faithful `.m`-to-Python translation via the `build_XXn.py` throwaway-
  script pattern; execute with `nbclient`, confirm 0 errors/0 stderr
  warnings, visually spot-check every figure before finalizing.
- Missing custom toolbox functions get reimplemented transparently with
  an explicit data-provenance caveat in the notebook markdown.
- Near-duplicate/superseded scripts get noted and skipped rather than
  rebuilt; scripts sharing underlying data but adding genuinely new
  content (like `10b`'s `pathway3`/`sector1` pair) are both kept.
- Missing/unreadable data dependencies get explicitly flagged rather
  than faked with synthetic data.
- Never run git directly — hand exact `git add`/`commit`/`push`
  commands to the user.
- Confirm the archive's actual file list directly (`ls`) before
  finalizing a script-count table, rather than trusting a filename-
  pattern guess (the lesson from Chapter 9's `09b`/`09c` corrections,
  applied here from the start — Chapter 10's count came out right on
  the first pass as a result).
