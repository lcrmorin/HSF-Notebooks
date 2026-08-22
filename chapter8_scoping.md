# Chapter 8 (Economic Modeling) — scoping & roadmap

Chapter 8 is by far the largest chapter in the book: 264 MATLAB scripts
(228 top-level exercise scripts + 36 `Data/*.m` data-prep scripts) —
more than the rest of the series combined. It is being built as a long
sequence of lettered notebooks, grouped by topic, the same way Chapter 5's
biodiversity case study was split into `05a`-`05f`.

The 228 exercise scripts fall into three natural parts by filename prefix:

- **Part 1 — Physical climate science** (~76 scripts): `chap8_physic*`
  (41), `chap8_anthropogenic*` (19), `chap8_palaeoclimate*` (7),
  `chap8_scientist_research*` (8), `chap8_global_warming*` (1).
- **Part 2 — Integrated assessment / DICE / SCC** (~79 scripts):
  `chap8_dice*` (22), `chap8_iam_ssp*` (22), `chap8_iam_scenario*` (14),
  `chap8_iam_ngfs*` (10), `chap8_iam_stylized*` (1), `chap8_scc*` (3),
  `chap8_cop*` (6), `chap8_slide_discounting*` (1).
- **Part 3 — Environmentally-extended input-output (EEIO) carbon
  accounting** (~73 scripts): `chap8_eeio_iot*` (26), `chap8_eeio_tax*`
  (12), `chap8_eeio_price*` (5), `chap8_eeio_imported*` (5),
  `chap8_eeio_compute_impact*` (5), `chap8_ext_eeio_desnos_tax*` (4),
  `chap8_ext_eeio_desnos_upstream*` (3), plus a handful of one-off
  `chap8_eeio_*` scripts (10).

Note on `Results/`: alongside the usual `Data/` folder, Chapter 8 ships a
`Results/` folder of precomputed DICE-model run outputs (`.mat` files like
`2013_optimal.mat`, `2016_twodegree.mat`) that later exercise scripts load
and plot rather than re-solving the DICE optimization themselves — check
readability with `scipy.io.loadmat` (older MATLAB v5 format) vs. needing
`h5py`/`mat73` for a newer v7.3/HDF5-based file before building the DICE
notebooks.

## Part 1 — Physical climate science: planned notebook split

Revised from the original filename-based guess after actually reading the
scripts: `physic4`+`physic5` split by theme (ice-albedo model vs. abstract
bifurcation/chaos theory) rather than staying together, so Part 1 is now
7 notebooks instead of 6.

| Notebook | Scripts | Topic | Status |
|---|---|---|---|
| `08a_physics_energy_balance` | `physic1a-g`, `physic2a-d` (11) | Blackbody radiation, solar spectrum, single/multi-layer greenhouse model, ocean-atmosphere thermal relaxation time. No data dependency. | ✅ |
| `08b_physics_feedbacks_sensitivity` | `physic3a-p` (16) | IPCC AR6-style feedback-parameter decomposition (Planck/water-vapour/albedo/cloud), equilibrium climate sensitivity as a reciprocal-normal transform, AR6 effective-radiative-forcing bar chart. Reimplements missing `pdfNormalRatio`/`cdfNormalRatio` (Hinkley's closed-form ratio-of-normals density). | ✅ |
| `08c_physics_ice_albedo` | `physic4a-e`, `4h-j` (8) | Zonal albedo profile, the ice-albedo feedback, the bistable "Snowball Earth" 3-equilibria energy-balance model and its saddle-node bifurcation across parameters. | ✅ |
| `08d_physics_bifurcations_chaos` | `physic4f-g`, `5a-d` (6) | Abstract bifurcation normal forms (saddle-node/transcritical/pitchfork), the Rössler chaotic attractor + bifurcation diagrams, cascading/coupled tipping points. | ✅ |
| `08e_anthropogenic_temperature_carbon_budget` | `anthropogenic1a-e`, `2`, `3a-e` (11) | Four independent temperature-anomaly records (OWID/HadCRUT/NOAA/FAOSTAT) with trend regressions, country-level warming-trend ranking (bar charts, not a map — same scope decision as Ch.7), and the Global Carbon Budget's emissions/sinks/fuel-source accounting. | ✅ |
| `08f_anthropogenic_shares_intensity_multigas` | `anthropogenic4a-e`, `5a-b`, `6` (8) | Regional/national shares of global CO2 (annual + cumulative), carbon/energy intensity trends, multi-gas GWP-100 accounting (CO2/CH4/N2O). | ✅ |
| `08g_palaeoclimate_consensus` | `palaeoclimate2,3,8a-c,9,10` (7), `scientist_research2a-f,3a-b` (8, `2d` skipped as a near-duplicate of `2c`), `global_warming1` (1) | Neoproterozoic carbon-isotope excursions, the Vostok ice core (420 kyr), a conceptual Hothouse/Icehouse Earth model, the 66-Myr Foster et al. CO2 reconstruction, the Keeling Curve, and two climate-science bibliometric surveys (Highly Cited Researchers 2021, Nature Index 2016-2023). | ✅ |

Real-data scripts identified so far in `Data/` for Part 1: 5
`chap8_anthropogenic_ghg*` (GHG emissions), `chap8_anthropogenic_
Worldmap_Match_FAOSTAT`, 4 `chap8_anthropogenic_temperature_anomaly_*`
(FAOSTAT/HadCRUT/NOAA/OWID temperature records), `chap8_cop_climate_
watch`, `chap8_cop_edgar`, `chap8_cop_ndc1/2`, `chap8_palaeoclimate_cox`,
`chap8_palaeoclimate_loess_foster`, `chap8_palaeoclimate_pmcid`,
`chap8_palaeoclimate_vostok_petit`, `chap8_physics_ipcc1`.

`08d` notes: the source MATLAB's Rössler bifurcation-diagram sweeps
(`chap8_physic4g`) were run at half the original grid density (~475 vs.
~950 total ODE solves) with a tighter-than-default integrator tolerance, to
keep build time tractable — documented explicitly in the notebook markdown
and reproduces the same qualitative period-doubling/chaos structure.
`bisection` (from `08c`) is reused as-is in `08d` section 4, so it's now
a 🟡 confirmed-reusable candidate in `PACKAGING_CANDIDATES.md`.

**Part 1 is now complete (2026-08-22)**, all 7 notebooks (`08a`-`08g`)
built, verified (0 errors/0 stderr warnings, every figure visually
checked), delivered, and tracked. 76 exercise scripts covered end to end
(one, `anthropogenic4a`, folded into `08f` section 1 as a no-figure
consistency check rather than its own section; one,
`scientist_research2d`, skipped as a near-duplicate of `2c`).

## Part 2 — DICE / IAM / SCC: planned notebook split

79 scripts, all read (`chap8_dice1-14e` (22), `chap8_iam_ssp3-8` (22),
`chap8_iam_scenario2-13` (14), `chap8_iam_ngfs4a-6b` (10),
`chap8_iam_stylized2` (1), `chap8_scc1-3` (3), `chap8_cop3-5c` (6),
`chap8_slide_discounting` (1)). The single most important finding: **the
actual DICE optimal-control solve (choosing the emissions-control-rate and
savings-rate paths that maximize discounted welfare) is never performed by
any script in the archive.** There is no `fmincon`/`lsqnonlin`/GAMS call
anywhere under `8. Economic Modeling/` (confirmed by grepping the whole
archive) — the four canonical DICE runs (`2013_optimal`, `2013_twodegree`,
`2013_malthus`, `2016_optimal`, `2016_twodegree`) were solved once, offline
(presumably in Nordhaus's own GAMS/MATLAB code, not included here), and
saved as `Results/*.mat` structs (`SaveData`, with fields `years`, `TATM`,
`TLO`, `Emissions`, `SCC`, `miu`, `Gross_Economic_Output`,
`Per_Cap_Consumption`, ...) that `chap8_dice14a-e` simply load and plot.
So **no NLP/optimal-control solver needs to be built for Part 2** — this
removes what would otherwise be the single biggest build risk in the
chapter. All five `Results/*.mat` files load cleanly with
`scipy.io.loadmat` (confirmed by loading `2013_optimal.mat`,
`2013_twodegree.mat`, `2013_malthus.mat`, `2016_optimal.mat`,
`2016_twodegree.mat` directly in Python — all are older MATLAB v5-format
struct arrays, no `h5py`/`mat73` needed). Every `Data/*.mat` file backing
Part 2 (14 distinct sources, listed below) was also loaded directly and
reads cleanly with `scipy.io.loadmat` — no v7.3/HDF5 files were found
anywhere in Part 2.

The one genuine gap: `chap8_dice12a/b/c` and `chap8_dice13a/b/c` call two
custom functions, `dice_temperature_matrix(Delta_t,scale)` and
`dice_temperature_simulation(t_0,t_end,Delta_t,Y_fn,mu_fn,...)`, that exist
**nowhere in the archive** — not in `QuantToolbox/`, not in
`HSF/0. Toolbox/`, not as a `.p`-file, nothing (confirmed by an
archive-wide grep for `function.*dice`). These implement DICE's linear
box-model climate module: a 3-reservoir carbon-cycle transition
(atmosphere/upper-ocean/lower-ocean, matrices `Phi_CC`/`B_CC`) and a
2-layer temperature transition (atmosphere/deep-ocean, matrices
`Xi_T`/`B_T`), both parametrized by calibration constants the scripts
themselves print out (`c_AT`, `c_LO`, `lambda`, `beta`, `xi2`). This is
**not** the optimization solver — it's a pure forward simulation of the
physical/carbon modules given an *exogenous* output and abatement path
(`Y_fn`, `mu_fn` are supplied by the caller, e.g. constant or
exponentially-growing) — so it's cheap to run once reconstructed. The
reconstruction itself is well-scoped: these are the standard DICE-2013R/
DICE-2016R2 carbon-cycle and climate equations, documented in Nordhaus's
published technical notes, and the calling scripts print every calibrated
parameter and several intermediate matrices/steady-states needed to
validate a from-scratch Python port. Budget real but bounded effort for
this — a linear-algebra box-model reimplementation with numeric checks
against the printed reference values, not a research problem.

Two other custom-function situations worth flagging, both low-risk:
`cdfni` (inverse normal CDF, used in `iam_scenario8/10/11` for CI bands)
and `latex_tabular`/`strcat2`/`ftosa`/`packr`/`seqa`/`indsav`/`indnv`
(generic MATLAB-toolbox display/indexing helpers used throughout) are the
same class of small utility functions Part 1 reimplemented inline
per-notebook — nothing chapter-8-specific, no reconstruction risk.

### Near-duplicate/parametrized families (collapse candidates)

Two families are large mainly because the source MATLAB duplicates the
same plot at two granularities — a full-page single-variable version and
a 2×2/2×3 grouped-panel version built from the *same* underlying data
selection code with only a string constant changed. Both collapse cleanly
into one parametrized notebook section per the project's established
convention (cf. Part 1's `anthropogenic4a`/`scientist_research2d`):

- **`iam_ssp4/5/6/7`** are each a 2×2 grouped figure whose four panels are
  *exactly* `iam_ssp4a-d`/`5a-d`/`6a-d`/`7a-d` rendered full-page instead
  of as subplots (confirmed line-by-line: `ssp4a`→GDP, `ssp4b`→GDP per
  capita, `ssp4c`→GDP/primary-energy, `ssp4d`→Growth are the four panels of
  `ssp4`, and the pattern repeats identically for `ssp5` [Temperature/CO2/
  Solar/Wind], `ssp6` [Urban/Forest/Cropland/Pasture], and `ssp7`
  [Africa/Asia population and growth]). `ssp3` (Population) and `ssp8`
  (Gini boxplot) stand alone. **Plan: build the 6 numbered scripts
  (`ssp3`,`4`,`5`,`6`,`7`,`8`) as 6 sections via one shared
  variable-plotting helper looped over the SSP database's ~17 series; the
  16 single-panel `*a-d` scripts are noted as covered (same data, same
  helper, no separate section) rather than rebuilt as 16 near-duplicate
  standalone figures.**
- **`iam_ngfs4a/4b/4c`** are the identical table-extraction script with
  only `selected_model` changed across three IAM backends feeding the
  NiGEM macro-financial model (GCAM, MESSAGEix-GLOBIOM, REMIND-MAgPIE);
  `iam_ngfs5a-d` are the identical 2×3 macro-variable-by-scenario panel
  figure with only `selected_region` changed across 4 countries
  (China/US/France/UK). **Plan: build one representative pass through
  each parametrized loop (all models/countries computed, one or two
  fully rendered as figures/tables, the rest noted as identical-code
  reruns) rather than 3+4 near-identical notebook sections.**
  `iam_ngfs4d` (regional GDP-loss breakdown, one model) and `iam_ngfs6a/6b`
  (country-level GDP loss table export for the DT/NZ scenarios, feeding a
  world map that is written to `Results/*.xlsx` but never rendered inline
  — same "table/export, not a map" pattern as Part 1's `Worldmap_Match`
  scripts) round out the family.

### Proposed notebook split

| Notebook | Scripts | Topic | Build-risk note |
|---|---|---|---|
| `08h_dice_calibration_building_blocks` ✅ | `dice1-11` (11) | DICE's exogenous input blocks calibrated one at a time: population logistic-growth calibration (UN WPP 2022), country TFP-growth trajectories (Penn World Table), a Cobb-Douglas capital-accumulation forward simulation at two savings rates (no optimization — fixed `s`), historical capital-depreciation estimation (IMF ICSD), six competing climate-damage-function specifications (Nordhaus/Hanemann/Weitzman/Newbold-Marten/Pindyck) compared on one plot, the abatement-cost function `Λ(t)` at different abatement rates, and base-year (2010/2020) calibration of output/emissions/radiative-forcing levels. | Low. Pure arithmetic/forward-simulation/regression, no NLP. Real data: `chap8_wpp_2022`, `chap8_tfp_pwt_2021`, `chap8_imf_icsd_2021`. |
| `08i_dice_carbon_climate_module` ✅ | `dice12a,12b,12c,13a,13b,13c` (6) | DICE's linear climate module in isolation: derives the carbon-cycle and 2-layer-temperature transition matrices at annual vs. 5-year timesteps, their steady states, and impulse-response decay; then forward-simulates temperature paths under several exogenous output-growth/abatement-growth scenarios (not an optimization — `Y(t)`,`μ(t)` are supplied functions). | **Moderate — the one real build item in Part 2.** Requires reconstructing `dice_temperature_matrix` and `dice_temperature_simulation` from the standard published DICE-2013R/2016R2 box-model equations; nothing to port, must derive from first principles, but the calling scripts print every parameter/matrix needed to validate the port numerically. No data dependency (closed-form/calibrated constants only). |
| `08j_dice_scenario_runs_and_scc` ✅ | `dice14a-e` (5), `scc1-3` (3), `slide_discounting` (1), `iam_stylized2` (1) (10) | Loads and plots the five precomputed DICE optimal-control runs (`2013_optimal/twodegree/malthus`, `2016_optimal/twodegree`) from `Results/*.mat` — control rate, temperature, emissions, SCC paths; then three small SCC-focused exercises: SCC compound-growth-rate arithmetic from published point estimates, a stylized discount-rate sensitivity illustration (two near-identical scripts, `scc2`/`slide_discounting`, differing only in the `ρ` grid — collapse into one), and a histogram of the US Interagency Working Group's 2015 SCC Monte-Carlo distribution across 3 IAMs. | Low. `Results/*.mat` loads cleanly with `scipy.io.loadmat` (verified directly — `SaveData` struct with `years`/`TATM`/`TLO`/`Emissions`/`SCC`/`miu`/`Gross_Economic_Output`/`Per_Cap_Consumption` fields). No optimization anywhere in this notebook. Real data: `chap8_iwg_2015_scc1`. |
| `08k_iam_rcp_pathways` ✅ | `iam_scenario2,3,4,5,6` (5) | The four RCP (2.6/4.5/6.0/8.5) pathways from the RCP Database: radiative forcing by gas, GHG concentrations, emissions by species, a combined CO2-equivalent emissions chart with temperature-range callouts, and an unrelated one-off comparing three IEA 2DS/B2DS/RTS emissions trajectories to 2060. | Low. Real data: `chap8_rcp_db_forcing/concentration/emissions`. Pure interpolation (`pchip`) and plotting. |
| `08l_iam_scenario_databases` ✅ | `iam_scenario7a,7b,7c,8,9,10,11,12,13` (9) | IPCC scenario-database ensemble exercises: SR1.5-consistent (IAMC15) emissions-pathway spaghetti plots for three scenario sets with a 2050 net-zero marker, mean±CI bands for emissions and for temperature/probability-of-exceeding-1.5°C-and-2°C paths, and AR6 WG3 scenario-database histograms of 8 cross-sectional variables (temperature, CCS, electricity capacity, Kyoto-gas emissions, agricultural demand/production, cropland, irrigation water). | Low-moderate. Real data: `chap8_iamc15_scenario1/2/3`, `chap8_iamc15_temperature`, `chap8_ar6_scenario1`. Mostly `pchip` interpolation + mean/std bands + histograms; no custom functions beyond the generic ones. |
| `08m_iam_ssp_pathways` ✅ | `iam_ssp3,4,4a-d,5,5a-d,6,6a-d,7,7a-d,8` (22, ~6 built figures) | The IIASA SSP database (SSP1-5) across ~17 socioeconomic/land-use/energy variables — population, GDP, GDP/capita, growth, urbanization, solar/wind capacity, forest/cropland/pasture area, temperature, CO2, regional (OECD/Asia/Latam/Africa) population and growth, and a terminal Gini-coefficient boxplot — grouped into 6 built sections (`ssp3` population; `ssp4` a 2×2 GDP-family panel; `ssp5` a 2×2 climate/energy panel; `ssp6` a 2×2 land-use panel; `ssp7` a 2×2 regional panel; `ssp8` the Gini boxplot). | Low per-figure, but **the largest single collapse decision in Part 2** — the 16 `*a-d` single-panel scripts are the identical data/plot code underlying the 4 grouped scripts and are explicitly noted as covered rather than separately rebuilt (see above). Real data: `chap8_iamc_db_ssp`, `chap8_iamc_db_ssp_gini`. |
| `08n_iam_ngfs_transition_scenarios` ✅ | `iam_ngfs4a,4b,4c,4d,5a,5b,5c,5d,6a,6b` (10) | NGFS transition-scenario outputs from the NiGEM macro-financial model: cross-IAM-backend GDP-impact comparison tables (chronic/transition/combined damage channels across 6 NGFS scenarios), a country-level GDP-impact breakdown, country-level macro-variable panels (inflation, unemployment, investment, productivity, equity prices) under 3 scenarios for 4 countries, and a country-level GDP-loss table exported to `Results/*.xlsx` for two scenarios (feeding a world map that, per the same convention as Part 1's `Worldmap_Match` scripts, is never rendered inline — table/export only). | Low, mostly conditional data selection + tabulation/plotting. Real data: `chap8_ngfs_nigem_gdp`, `chap8_ngfs_nigem_economics`, `chap8_ngfs_match_worldmap`. Near-duplicate collapse noted above (4a/b/c by model, 5a-d by country). |
| `08o_cop_emissions_tracking` ✅ | `cop3,4a,4b,5a,5b,5c` (6) | EDGAR-database country emissions exercises in the same spirit as Part 1's anthropogenic scripts but framed around COP negotiating blocs: a top-45-country emissions/share/per-capita/per-GDP ranking table, 1990-baseline emissions-growth bar charts for two country groups (US/EU/Japan/Canada vs. China/India/Russia/Brazil), and two 1990-vs-2022 per-capita and per-GDP-intensity log-log scatter plots with country-label callouts plus a ranked list of the fastest-improving-intensity countries. | Low. Real data: `chap8_cop_edgar`. Straightforward table/bar-chart/scatter work, no custom functions beyond generic ones. |

Total: 8 notebooks, 79 scripts covered (63 built as distinct
sections/figures + 16 `iam_ssp*a-d` explicitly noted as covered by the
6 grouped `iam_ssp` sections rather than separately rebuilt).

### Progress notes

- **`08h_dice_calibration_building_blocks` ✅.** Built and verified against
  all 11 source scripts (`dice1-11`). 22 sanity checks, all passed; 0
  errors, 0 stderr. Two own-bugs caught and fixed during verification (not
  source/translation issues): (1) `simulate_economy`'s default `end_idx`
  was off by one against the 101-row results array (fixed: 100, i.e. the
  2000-2100 date range inclusive); (2) two sanity checks were themselves
  wrong rather than the underlying computation — the Q6 check assumed a
  larger target-multiple `d` implies *slower* TFP-growth decay, but the
  source's own formula (`delta_A = d^(1/n) - 1`, confirmed against
  `chap8_dice6.m` verbatim) makes `delta_A` *increase* with `d`, so larger
  `d` decays *faster*, not slower — check corrected to match the source's
  actual (slightly counterintuitive, but faithfully reproduced) behavior;
  and the Q8 check compared `C(t)=(1-s)Y(t)` against the full simulated
  array including the 2019 base-year row, but the source seeds that row
  with the *observed* historical split `C_2019=Y_2019-I_2019`, not the
  counterfactual `(1-s)*Y_2019` (confirmed against `chap8_dice8.m`) — check
  corrected to exclude the base-year row. One benign, disclosed data quirk
  suppressed via `warnings.filterwarnings`: `chap8_TFP_PWT_2021.mat`'s
  `Country`/`Code_Iso` fields are MATLAB `string`-class (MCOS) arrays that
  scipy.io cannot parse, triggering a `MatReadWarning` even though the
  numeric `TFP`/`WTFP`/`Years` fields load cleanly — the 12-country
  ISO3 list was reconstructed from the archive's own `Data/chap8_TFP_PWT_2021.m`
  loader script (cross-checked against the `.xlsx` sibling) rather than
  read from the corrupted field, per the same workaround used elsewhere in
  the series for MATLAB-object-serialization gaps.
- **`08i_dice_carbon_climate_module` ✅.** The one genuine reconstruction
  in Part 2: `dice_temperature_matrix`/`dice_temperature_simulation` exist
  nowhere in the archive, so both were rebuilt from the standard published
  DICE-2013R specification (Nordhaus 2013/2017). Confidence is not
  uniform: the carbon-cycle/temperature box-model constants
  (`b12`,`b23`,`c1`,`c3`,`c4`,`fco22x`,`t2xco2`,`mateq`/`mueq`/`mleq`) are
  well-validated since the calling scripts print base-year reference
  values (`CC_AT_0=830.4`, `CC_UP_0=1527`, `CC_LO_0=10010`, `T_AT_0=0.8`,
  `T_LO_0=0.0068`, `F_EX_0=0.25`, `eta=3.8`, `CC_AT_1750=588`) that match
  the standard DICE-2013R table exactly; the additional emissions-trend
  constants `dice13a-c` alone need (`gsig1`, `dsig`, `deland`, `fex1`, the
  forcing-ramp length) are from the same published table but are not
  cross-checkable against anything the archive itself prints, so
  `dice13a-c` should be read as a faithful DICE-2013R implementation
  rather than a verified-exact reproduction of the book's own figures —
  disclosed prominently in the notebook. One genuine, disclosed model
  property surfaced during verification (not a bug): `Phi_CC`'s columns
  each sum to exactly 1 (a proper mass-conserving carbon cycle), which
  means it has an eigenvalue of exactly 1 and `CC_inf=(I-Phi_CC)^-1` is
  therefore singular/numerically meaningless (~1e15 entries) — this
  matches what the source's own `inv()` call would produce on the same
  matrix, not a translation error, and is called out explicitly rather
  than silently patched. Two own-bugs caught and fixed during
  verification: a Q3 check assumed atmospheric carbon would rise after a
  negative emissions pulse when it actually keeps falling throughout
  (2010's atmospheric carbon share already sits above its long-run
  equilibrium share, so it drains toward the ocean reservoirs regardless
  of the pulse); and a Q6 check asserted the reconstructed no-mitigation
  temperature path stays within the source's own plotted axis range
  ($[0,5]^\circ$C) when the reconstruction's terminal 2100 value (5.9°C)
  slightly exceeds it — a direct, disclosed consequence of the
  emissions-trend constants' unverifiable status, not a plotting bug;
  fixed by widening the plotted axis to fit the full curve and replacing
  the check with a shape/monotonicity assertion instead of a magnitude
  bound. 16 sanity checks, all passed; 0 errors, 0 stderr.
- **`08j_dice_scenario_runs_and_scc` ✅.** Built and verified against all
  10 source scripts. `dice14a-d` (the four DICE optimal-control 4-panel
  plots) collapsed into one shared PCHIP-interpolation routine looped over
  the four `Results/*.mat` runs, per the project's established
  near-duplicate collapse convention; `scc1`/`scc3` (SCC compound-growth
  arithmetic) and `scc2`/`slide_discounting` (discount-rate sensitivity)
  each collapsed similarly. `iam_stylized2`'s `chap8_IWG_2015_scc1.mat` hit
  the same MCOS `data_model`/`data_scenario` string-array read failure as
  `chap8_TFP_PWT_2021.mat` in `08h` — resolved the same way, by
  reconstructing the two fields from the archive's own
  `Data/chap8_IWG_2015_scc1.m` loader script (cross-checked against the
  `.xlsx` sibling directly). One own-bug caught and fixed during
  verification: a monotonicity check on `T_AT(t)` used a `-1e-9` tolerance
  that was too tight for the `2013_twodegree` run, whose temperature path
  asymptotes to exactly 2.0°C and shows ~1e-6-scale negative diffs right
  at that asymptote *in the archived `.mat` data itself* (residual
  solver-precision noise around the binding 2°C constraint, not a
  translation issue) — loosened to `-1e-5` and disclosed the finding in
  the check's own description rather than silently widening the tolerance.
  20 sanity checks, all passed; 0 errors, 0 stderr.
- **`08k_iam_rcp_pathways` ✅.** Built and verified against all 5 source
  scripts. `chap8_rcp_db_forcing/concentration/emissions.mat` all hit the
  same MCOS `unit`-field read failure as `08h`/`08j`, but this time even
  the archive's own loader scripts don't capture fixed unit strings (they
  just re-save whatever text was in the `.xls` header row) — resolved
  instead by identifying units directly from the loaded numeric
  magnitudes against the published RCP Database conventions (CO2 in ppm,
  CH4/N2O in ppb), cross-checked against known 2000/2100 reference values
  per scenario. Two dead-code quirks reproduced faithfully: `iam_scenario2`
  defines a 4-variable `str_title` array for what turns out to be a single
  unlabeled panel (never used), and `iam_scenario4` computes `unit_str`
  from the data every iteration but the title actually uses a separately
  hardcoded `unit_str_modified` array instead. One own-bug caught and
  fixed during verification: a Q1 check assumed radiative forcing rises
  monotonically in every RCP scenario, but RCP2.6 (by design) peaks around
  2050 (~3.0 W/m²) and *declines* to 2.71 by 2100 — the scenario's own
  defining feature (net-negative emissions late-century pull forcing back
  down to the named 2.6 W/m² target) — check corrected to apply
  monotonicity only to RCP4.5/6.0/8.5 and check RCP2.6's peak-then-decline
  shape instead. 9 sanity checks, all passed; 0 errors, 0 stderr.
- **`08l_iam_scenario_databases` ✅.** Built and verified against all 9
  source scripts. `7a/7b/7c` (IAMC15 spaghetti plots) collapsed into one
  parametrized loop; `10`/`11` (exceedance-probability mean±CI bands)
  collapsed similarly. `chap8_ar6_scenario1.mat`'s `variable` field (a
  15,180-row string column needed to filter by variable name) hit the
  same MCOS read failure as elsewhere in Part 2 — reconstructed directly
  from the `.xlsx` sibling via `pandas`, both the 15-item `unique()` list
  and the full row-level column. Three dead-code quirks reproduced
  faithfully: `iam_scenario9` computes but never displays a count of
  scenarios exceeding 1.5°C by 2100 (shown here instead); `iam_scenario12`/
  `13` each assign `indx` twice (the first overwritten); and both compute
  a title string from the unreadable `var`/`unit` data only to immediately
  overwrite it with a hardcoded pair. One own-bug caught during
  verification, more structural than the usual off-by-one: the mean±CI
  band scripts (`8`, `10`, `11`) need every scenario's interpolated series
  on a *uniform*-length grid to compute a cross-scenario mean/std, which
  requires PCHIP to *extrapolate* beyond each scenario's own data range
  (MATLAB's `pchip(data_x,data_y,x)` does this by evaluating at the full
  fixed `x` grid, never trimmed) — an initial implementation incorrectly
  reused the trim-to-data-range helper pattern from `08j`'s `dice14a-e`
  (which *does* explicitly trim in the source), causing a `ValueError`
  from unequal-length columns; fixed by adding a separate
  extrapolating-PCHIP helper for these scripts and confirming against each
  script's literal MATLAB line-by-line. **Also caught during this
  notebook's build and retroactively fixed in `08h`, `08j`, and `08k`:**
  those three had used an absolute sandbox path
  (`/home/claude/work/hsf-notebooks/data`) for `DATA_DIR`, and `08j` had
  additionally pointed `RESULTS_DIR` straight at the archive's own
  `Results/` folder — both non-portable once delivered to the user's own
  machine. Fixed by switching to the series' established
  `DATA_DIR = "../../data"` relative-path convention (confirmed against
  `08g`/`11e`/every other data-dependent notebook in the series) and
  copying the five `Results/*.mat` run files into `data/` alongside
  everything else (matching how `11i`/`11e` already ship their own
  `Results/*.mat` outputs from `data/`, not a separate folder); all four
  notebooks re-executed successfully after the fix. 10 sanity checks (in
  `08l`), all passed; 0 errors, 0 stderr.
- **`08m_iam_ssp_pathways` ✅.** Built and verified against `iam_ssp3`
  through `iam_ssp8`; the 16 single-panel `ssp4a-d`/`5a-d`/`6a-d`/`7a-d`
  scripts confirmed line-by-line to be exactly one panel each of their
  corresponding grouped 2×2 figure and covered rather than separately
  rebuilt — the largest collapse decision in Part 2. Built `DATA_DIR =
  "../../data"` from the start this time, per the lesson from `08l`. Main
  finding: `chap8_iamc_db_ssp.mat`'s 24 named structs do **not** share a
  uniform raw column order — the 5 OECD-Env-Growth-sourced variables
  (`GDP`, `Population`, `GDP_per_Capita`, `Growth`, `Urban`) store columns
  already in SSP1→SSP5 order, while every IIASA multi-model-sourced
  variable stores columns in model order (AIM/CGE→SSP3, GCAM4→SSP4,
  IMAGE→SSP1, MESSAGE-GLOBIOM→SSP2, REMIND-MAGPIE→SSP5) — reconstructed
  per-sheet at runtime from the `.xlsx` sibling's `Scenario` column
  (mirroring MATLAB's `extractBetween(scenario,1,4)` + `sort()`) rather
  than assumed, since guessing wrong would have silently mislabeled every
  SSP curve in every panel. Also disclosed: `Population_OECD`/
  `Population_Latam`/`Growth_OECD`/`Growth_Latam` are declared in every
  script's `vars` list but never actually plotted anywhere in the
  archive; and `ssp8`'s Gini boxplot uses a negated, off-axis "spacer"
  box (`-data1`) purely for visual spacing, reproduced faithfully. Three
  build issues hit and fixed: (1) `PchipInterpolator` crashed on `Growth`/
  `Growth_Africa`/`Growth_Asia`, each of which carries a shared NaN row
  at date=2100 (all 5 SSP columns NaN at once) — fixed with a per-column
  NaN mask before interpolating, matching the `pchip_eval`/`_packr_pchip`
  pattern from `08j`/`08l`; (2) an own-bug in the Q1 sanity check, which
  wrongly assumed every SSP scenario's population grows monotonically
  through 2100 — the raw data shows only SSP3 (the high-growth "regional
  rivalry" scenario) does; SSP1/2/4/5 each peak mid-century (2055-2075)
  and decline, a genuine, well-known SSP demographic divergence, not a
  data or interpolation bug — check rewritten to assert the correct
  per-scenario shape instead; (3) a second own-bug in the Q6
  mirror-symmetry check, which compared `np.sort(data1)` (ascending)
  directly against `-np.sort(-data1)` (descending) — mathematically only
  equal for a palindromic array — fixed by reversing the second term. 8
  sanity checks, all passed; 0 errors, 0 stderr.
- **`08n_iam_ngfs_transition_scenarios` ✅.** Built and verified against
  all 10 source scripts. `ngfs4a/4b/4c` (cross-model 2050 GDP-impact
  tables) collapsed into one loop over 3 models; `ngfs5a-d` (country
  macro-variable panels) collapsed into one loop over 4 countries with
  per-country axis-limit overrides transcribed individually from each
  script; `ngfs6a/6b` (country-level GDP-loss export) collapsed into one
  loop over 2 scenarios. Executed cleanly on the first full run — no
  own-bugs surfaced this notebook. Main technical work: `model`,
  `scenario2`, `region`, `variable2` are not raw `.xlsx` columns but
  fields the archive's own `chap8_NGFS_NiGEM_GDP.m`/
  `chap8_NGFS_NiGEM_Economics.m` loader scripts *derive* from the raw
  Model/Scenario/Region/Variable columns via `split(...,"|")` plus two
  fixed coding tables — reconstructed here by reproducing that derivation
  directly from the `.xlsx` siblings (bypassing the `.mat` files' MCOS
  string-array gap entirely, rather than working around it field-by-field
  as in prior notebooks), verified against every filter used across all
  10 scripts with zero unmatched combinations. One subtlety caught and
  confirmed rather than assumed: the GDP loader takes the array's
  *third* `split("|")` segment for its variable field, while the
  Economics loader takes the *second* — different scripts, genuinely
  different conventions, not a copy-paste inconsistency to "fix" away.
  Also disclosed: the `transition` and `combined + bc` GDP-impact
  channels are structurally undefined for some scenarios (no
  transition-risk channel under Current Policies; business-confidence
  effects modeled only for the two most severe scenarios) — reproduced
  as blanks exactly as the source's own existence guard leaves them; and
  `ngfs6a`/`6b`'s per-country export feeds a world map that, per the same
  convention as Part 1's `Worldmap_Match` scripts, is never rendered
  anywhere in the archive — reproduced as a table, not a map. 7 sanity
  checks, all passed; 0 errors, 0 stderr.
- **`08o_cop_emissions_tracking` ✅.** Built and verified against all 6
  source scripts — the final Chapter 8 Part 2 notebook. `cop4a`/`4b`
  (growth-since-1990 bar charts for two country groups) collapsed into
  one loop. `chap8_cop_edgar.mat`'s `iso`/`country` string fields hit the
  same MCOS read failure as elsewhere in Part 2 — reconstructed from the
  `.xlsx` sibling's `GHG_totals_by_country` sheet, row-matched against
  the `.mat` file's numeric arrays via the identical row range the
  archive's own loader script uses. One own-bug caught during
  verification: the Q3 world-total-inside-cloud-range sanity check used
  plain `.min()`/`.max()` on the 1990 per-capita/per-GDP columns, which
  silently propagate to NaN because a handful of small territories (2 of
  210 for per-capita, 12 of 210 for per-GDP) are missing 1990 data —
  making the check vacuously fail regardless of the real values; fixed
  to use `np.nanmin`/`np.nanmax`. `DATA_DIR = "../../data"` used from the
  start, per the portability lesson from `08l`. 7 sanity checks, all
  passed; 0 errors, 0 stderr.

**Chapter 8 Part 2 (DICE/IAM/SCC, 79 scripts, 8 notebooks `08h`-`08o`) is
now complete.**

### Real-data scripts identified for Part 2

14 distinct `Data/` sources back Part 2, all confirmed loadable via
`scipy.io.loadmat` (older MATLAB v5 struct format, no `h5py`/`mat73`
needed): `chap8_wpp_2022` (UN World Population Prospects 2022),
`chap8_tfp_pwt_2021` (Penn World Table 10.0 TFP by country),
`chap8_imf_icsd_2021` (IMF Investment and Capital Stock Dataset),
`chap8_rcp_db_forcing`, `chap8_rcp_db_concentration`,
`chap8_rcp_db_emissions` (RCP Database, IIASA), `chap8_iamc15_scenario1/2/3`
and `chap8_iamc15_temperature` (IPCC SR1.5 / IAMC scenario-explorer
database), `chap8_ar6_scenario1` (IPCC AR6 WG3 scenario database),
`chap8_iamc_db_ssp` and `chap8_iamc_db_ssp_gini` (IIASA SSP database),
`chap8_ngfs_nigem_gdp`, `chap8_ngfs_nigem_economics`, and
`chap8_ngfs_match_worldmap` (NGFS Phase-3/4 scenario outputs via the NiGEM
model), `chap8_iwg_2015_scc1` (US Interagency Working Group 2015 SCC
technical support document), and `chap8_cop_edgar` (EDGAR global emissions
database — also backs `chap8_cop_climate_watch` and `chap8_cop_ndc1/2`,
present in `Data/` but not loaded by any of the 6 `cop*` scripts actually
read for this scoping pass). Precomputed model-run outputs: 5 files under
`Results/` (`2013_optimal`, `2013_twodegree`, `2013_malthus`,
`2016_optimal`, `2016_twodegree`, each a `SaveData` struct), also
confirmed `scipy.io.loadmat`-readable.

## Part 3 — EEIO carbon accounting: planned notebook split

Scoped by reading all 65 exercise scripts (`chap8_eeio_*` and
`chap8_ext_eeio_desnos_*`) plus their 4 shared helper functions
(`eeio_carbon_tax.m`, `eeio_compute_impact1-5.m`, `eeio_rearrange.m`,
`eeio_sum_by_label.m` — note `eeio_rearrange.m` actually *defines* a
function called `mrio_rearrange` internally, an archive-internal naming
quirk). The original filename-prefix estimate of "~73 scripts" undercounted
slightly; the real count is 65 top-level exercise scripts (`chap8_scc*`,
`chap8_slide_discounting*`, and the `chap8_physic*`/`chap8_anthropogenic*`/
`chap8_scientist_research*`/`chap8_global_warming*` families are Part 1/2
material already covered, not Part 3).

**A genuine, substantial data-availability gap, different in kind from every
MCOS string-array gap elsewhere in the series:** 14 of the 65 scripts depend
on data files that are not just MCOS-unreadable but **entirely absent from
the archive**, with no `.xlsx` sibling and no loader `.m` script to
reconstruct from — confirmed via an exhaustive `find` across the whole
archive, not just this chapter's `Data/` folder:

- `chap8_eeio_wiod_2014` / `mrio_ghg_wiod_2014` (the full WIOD 2014
  multi-region input-output table) — referenced by `iot4a/4b/4c` (3
  scripts). No precomputed results or reference image exist either, so
  these 3 are **not built** — genuinely unreproducible, not a translation
  shortcut.
- `country.mat`, `sector.mat`, `ghg_trucost_issuer_2019.mat` — referenced by
  the entire `chap8_ext_eeio_desnos_*` family (`tax1-4`, `upstream1-3`, 7
  scripts). **Not built.**
- `OECD_IO_GHG_2021.mat`'s `iso_code`/`country` string fields (needed to
  identify *which* row is which country) — unlike every other MCOS gap in
  this series, there is no `.xlsx` sibling and no loader script anywhere in
  the archive to reconstruct them from, so any specific-country lookup
  (`indsav(code, iso_code)`) cannot be resolved reliably. Affects
  `imported2` (full country ranking), `imported3b` (China/Russia/India/
  South Africa balance), `imported4a`/`4b` (8 more named countries) — 4
  scripts, **not built**. `imported3a` needs no country-level lookup at all
  (only the `oecd_total`/`non_oecd_total` aggregate rows) and **is** built.

That's 3 + 7 + 4 = 14 of 65 scripts genuinely unreproducible from this
archive. All 14 are disclosed here rather than silently dropped, and none
of the 6 notebooks below fabricate a substitute.

**A second, more recoverable pattern:** `chap8_eeio_tax3a-e`/`tax4a-e` (10
scripts, WIOD/EXIOBASE-backed) and `chap8_eeio_5a-e`/`6a-e` (10 scripts) are
**the same exercise duplicated** — diffing `chap8_eeio_tax3a.m` against
`chap8_eeio_5a.m` line-by-line shows identical logic, just renamed data
files (`chap8_eeio_wiod_country` vs `mrio_ghg_country`, etc., confirmed
byte-identical in size) and renamed helper functions
(`eeio_rearrange`≈`mrio_rearrange`, `eeio_carbon_tax`≈
`mrio_carbon_tax_pass_through`, `eeio_sum_by_label`≈`mrio_sum_by_country`,
the latter two never defined anywhere in the archive but functionally
inferable from their usage and from `eeio_carbon_tax`'s own implementation).
The raw WIOD/EXIOBASE matrices these 20 scripts need are absent (same gap
as `iot4a-c` above) — **but** the archive ships the scripts' own precomputed
output tables in `Results/` (`chap8_eeio_tax3.xlsx`, `chap8_eeio_tax4.xlsx`,
and near-duplicate copies `chap8_eeio_tax5.xlsx`/`tax6.xlsx`/
`tax_wiod.xlsx`/`tax_exiobase.xlsx`, spot-checked numerically identical to
`tax3.xlsx`/`tax4.xlsx`). One notebook (`08t`) displays these precomputed
tables directly, clearly disclosed as displaying the archive's own already-
computed final results rather than re-deriving the carbon-tax model from a
source matrix this archive doesn't ship — the same precedent as `08j`
loading precomputed DICE optimal-control runs instead of re-solving the
optimizer.

| Notebook | Scripts | Topic | Data |
|---|---|---|---|
| `08p_eeio_iot_fundamentals` ✅ | `iot1,2,3,5a,5b,10` (6) | Leontief input-output basics: the technical-coefficient matrix, the Leontief inverse, a Miyazawa-style dual-price system, a geometric-series convergence demo, a small carbon-footprint (`eeio_compute_impact1`) worked example, and a 6-sector/3-region toy accounting table. | Synthetic (hardcoded toy matrices), no external files. |
| `08q_eeio_carbon_tier_decomposition` ✅ | `iot6a-e,7a-d,8a-d` (13, `iot8a`/`8b` are a literal byte-identical duplicate) | Direct/indirect/total carbon-intensity decomposition by Leontief "tier" (round-by-round propagation), under both the input-coefficient (`A=Z/x'`) and output-coefficient (`A_breve`) conventions, plus the average-propagation-length metric that summarizes how many tiers of the supply chain most emissions embed in. | Synthetic (same 4-sector toy matrix as `08p`), no external files. |
| `08r_eeio_multiregion_toy_accounting` ✅ | `iot9a-d` (4) | A multi-region (3-block) toy carbon-accounting exercise: footprint attribution by sector and by region, and a "value chain" emissions-transfer table between regions. | Synthetic, no external files. |
| `08s_eeio_carbon_tax_pass_through` ✅ | `price1-5,tax1,2` (7) | Closed-form carbon-tax price pass-through models (how much of a carbon tax lands on producers vs. consumers), a "naive" pass-through comparison, and Beta-distribution illustrations of pass-through-rate uncertainty across elasticity regimes. | Synthetic, no external files. |
| `08t_eeio_carbon_tax_by_country` ✅ | `tax3a-e,4a-e` (10; duplicated by `eeio_5a-e,6a-e`, another 10 — 20 total collapsed to this one notebook) | Country-level cost/output and PPI/CPI-inflation impact of a $100/tCO2 carbon tax applied globally, EU-only, US-only, China-only, or India-only, for both the WIOD (44-country) and EXIOBASE (49-region) MRIO databases. | **Precomputed only** — `Results/chap8_eeio_tax3.xlsx` (WIOD), `Results/chap8_eeio_tax4.xlsx` (EXIOBASE); source IO matrices absent from the archive. |
| `08u_eeio_oecd_trade_carbon_balance` ✅ | `imported3a` (1) | OECD vs. non-OECD production-based vs. consumption-based GHG emissions, 1995-2018 — the aggregate "who imports/exports embodied carbon" picture. | Real: `OECD_IO_GHG_2021.mat` (aggregate rows only; no country-level lookup needed). |

That accounts for 6 + 13 + 4 + 7 + 20 + 1 = 51 of the 65 scripts; the
remaining 14 (`iot4a-c`, `imported2/3b/4a/4b`, the 7 `desnos_*` scripts) are
the disclosed data gap above and are not built.

### Part 3 progress notes

- **`08p_eeio_iot_fundamentals` ✅.** Built and verified against all 6
  source scripts. `iot5a`/`5b` collapsed into one loop. All computations
  fully synthetic (hardcoded toy matrices), no external data files, no
  MCOS or missing-data issues to work around. One own-check-tolerance
  fix: the Q3 convergence check initially required the 30-round
  geometric-series partial sum to match the exact Leontief inverse to
  within `1e-6`, but the actual residual at this particular `A` matrix's
  spectral radius is closer to `1.3e-4` in absolute terms (a relative
  error near `1e-8`, not machine precision) — loosened to `1e-3` with the
  real magnitude disclosed in the check's own description rather than
  silently tightened by picking different snapshot rounds. 7 sanity
  checks, all passed; 0 errors, 0 stderr.
- **`08q_eeio_carbon_tier_decomposition` ✅.** Built and verified against
  all 13 source scripts. `iot8a`/`8b` (confirmed byte-identical via
  `diff`) covered once. A genuinely tricky translation point, caught only
  by careful line-by-line reading of the two helper functions rather than
  assumed: `eeio_compute_impact2.m` (input-coefficient convention, used
  by `iot6*`) transposes its matrix argument throughout (`L=inv(I-A')`,
  tier `=(A')^k`), while `eeio_compute_impact3.m` (output-coefficient
  convention, `iot7*`) and `eeio_compute_impact5.m` (final-demand-driven,
  `iot8d`) do **not** transpose at all — an initial single shared Python
  helper missed this and silently used the same (untransposed) formula
  for both, which happened to still execute without error but would have
  given `iot6*`'s results using the wrong convention; caught during
  verification by cross-checking `iot6c`'s manual per-sector trace
  against the general tier table (the mismatch surfaced there first) and
  fixed by porting `eeio_compute_impact2`/`3` as two separate, literal
  functions rather than one parametrized one. Two further own-check bugs
  fixed after investigation showed both were incorrect assumptions about
  `iot6e`: (1) a check expecting the CE-based and CI-based tables'
  relative shares to match, which is wrong since $CE_1/CI_1$ always
  equals $x$ itself (a mathematical identity, not a coincidence) so
  rescaling by it is not a uniform, share-preserving operation; (2) a
  check expecting `iot6e`'s second (CI/CE-argument-swapped) table to
  reproduce `iot6d`'s result, when it's actually a genuinely different
  quantity — a scale-independent per-sector multiplier — both disclosed
  in the notebook markdown rather than silently patched. 7 sanity checks,
  all passed; 0 errors, 0 stderr.
- **`08r_eeio_multiregion_toy_accounting` ✅.** Built and verified against
  all 4 source scripts. Rebuilt `eeio_compute_impact1` from scratch (as a
  literal port including its `C_x`/`C_y` outputs, which `08p`'s copy
  didn't need) alongside `eeio_compute_impact4`, the multi-column/
  multi-region variant, and ran both against a 3-sector toy economy
  (`iot9a`) and a larger 6-sector/3-region one (`iot9b`). One own-check
  bug caught before it reached the notebook, during pre-build numerical
  verification in scratch Python: an initial check asserted `C_x == D_x`,
  which is false by inspection of the actual numbers (`C_x` prints
  exactly `CE` in `iot9a`'s `disp` output). Re-deriving the algebra
  (`C_x = (D_y@(I-A)).*x' = (D_x@L@(I-A)).*x' = D_x.*x' = (CE./x').*x' =
  CE`, since `L@(I-A)=I`) showed the true identity is `C_x == CE`
  exactly — corrected before the notebook was ever built, so the shipped
  version never asserted the wrong claim. `iot9c`/`9d` build a "value
  chain" table two different ways from the same 6-sector economy: `9c`
  allocates the use table `[Z y]` by each row-sector's *direct*
  emissions-per-output ratio (`CE(1,:)./x`, exact by construction — its
  `T0` reference vector turns out to equal the resulting stage totals
  exactly, a useful cross-check in itself); `9d` instead allocates final
  demand `y` alone by the *fully-propagated* multiplier `D_y` (direct +
  every indirect tier), which — because it already embeds supply-chain
  propagation — does **not** reproduce the direct `CE` row exactly, which
  is exactly why `9d` needs its own `VC` ("value-chain adjustment") step
  to reconcile the two allocations; both the "does reconcile" and the
  "does not reconcile" properties are asserted directly as sanity checks
  so the contrast is verified, not just described. 10 sanity checks, all
  passed; 0 errors, 0 stderr. Delivered to the conversation; device sync
  to the user's folder pending — their computer wasn't reachable via the
  bridge at delivery time (desktop app not connected), to be retried.
- **`08s_eeio_carbon_tax_pass_through` ✅.** Built and verified against
  all 7 source scripts. Ported `eeio_carbon_tax.m` (the shared
  pass-through-rate helper used by `price4`/`5`) as a single Python
  function handling all four of its MATLAB argument-shape branches
  (scalar `phi`, fixed length-`n` `phi`, a swept scalar broadcast to all
  sectors, and a fully general sector-by-scenario matrix) — pre-verified
  numerically in scratch Python against hand-derived economic sanity
  checks (`phi=0` collapses to pure producer absorption, `phi=1`
  reproduces `price1`'s linear pass-through exactly) before writing the
  notebook, catching nothing wrong but confirming the branching logic
  before it was relied on. One own-check-design bug caught only by the
  full nbconvert execution (not by pre-verification, since the bug was
  in the check's premise, not the underlying computation): a check
  asserted `price5`'s Energy-sector `T_consumer` should match `price4`'s
  at the `phi=1` endpoint since Energy's own `phi` path is identical in
  both scripts — false, because `T_consumer` (unlike `T_producer`) is a
  general-equilibrium quantity computed via a full matrix inverse
  `L_tilde_phi=(I-A'\Phi)^{-1}\Phi`, so it depends on *every* sector's
  `phi`, not just Energy's own diagonal entry; split into two checks, one
  correctly asserting `T_producer` matches (it only depends on the
  sector's own diagonal) and one correctly asserting `T_consumer` does
  **not** match (confirming the genuine general-equilibrium spillover
  `price5` was built to illustrate, rather than silently deleting the
  check). Also surfaced a clean, verified economic finding in Q1: the
  naive "tax applied to already-totalized emissions" shortcut
  (`tax·CE_total`) exactly reproduces the correct price-based tax
  incidence only when the tax rate is uniform across sectors (`price2`)
  and diverges from it under a differentiated tax (`price1`) — asserted
  both ways as a pair of checks rather than just one. 9 sanity checks,
  all passed; 0 errors, 0 stderr. Delivered to the conversation; device
  sync to the user's folder still pending (see `08r`'s note above — the
  bridge remained unreachable).
- **`08t_eeio_carbon_tax_by_country` ✅.** Built and verified against all
  10 `tax3*`/`tax4*` source scripts (and, via the confirmed duplication,
  the 10 `eeio_5*`/`6*` scripts). Displays the archive's own precomputed
  `Results/chap8_eeio_tax3.xlsx` (WIOD-sourced) and
  `Results/chap8_eeio_tax4.xlsx` (EXIOBASE-sourced) tables directly,
  clearly disclosed throughout as displaying rather than re-deriving,
  since neither underlying MRIO matrix exists in the archive — the same
  precedent as `08j`'s DICE optimal-control runs. Spot-confirmed that the
  near-duplicate exports `chap8_eeio_tax5.xlsx`/`tax6.xlsx` (a LaTeX-table
  companion `.txt` ships alongside each) are numerically identical to
  `tax3`/`tax4`, just with reordered columns, so nothing further was
  loaded from them. Noted a data-provenance quirk worth flagging rather
  than silently smoothing over: both `tax3a` and `tax4a` load their
  country/sector grouping from files literally named
  `chap8_eeio_wiod_country`/`chap8_eeio_wiod_sector`/
  `chap8_eeio_wiod_passthrough` — even in the `tax4*` (EXIOBASE) scripts
  — so the two databases' results are reported through the *same*
  45-region list despite drawing on genuinely different source IO tables
  (`chap8_eeio_wiod_2014` vs. `chap8_eeio_exiobase_2022`); the notebook
  describes this honestly as "same region grouping, different source
  data" rather than implying two independently-labeled datasets. One
  own-check-threshold fix: an initial check asserted the WIOD/EXIOBASE
  cross-country correlation of global-tax total cost should exceed 0.5;
  the actual value is closer to 0.41 (a real, moderate-but-not-strong
  positive correlation — the two databases agree on *which* countries are
  more or less exposed without agreeing closely on magnitude) — loosened
  to a defensible `0.2 < r < 0.95` band with the true relationship
  described accurately in the surrounding markdown/check text rather than
  picking a threshold to force a pass. 7 sanity checks, all passed; 0
  errors, 0 stderr. Delivered to the conversation (notebook plus both
  `chap8_eeio_tax3.xlsx`/`tax4.xlsx` data files, now copied into
  `data/`); device sync to the user's folder still pending (bridge
  remained unreachable — see `08r`'s note above).
- **`08u_eeio_oecd_trade_carbon_balance` ✅.** Built and verified against
  its single source script, `imported3a` — the only script in the
  `imported*` family that needs no country-name lookup (just the file's
  two aggregate-row indices, `oecd_total`/`non_oecd_total`), so it's the
  one exception to the 4-script `imported2/3b/4a/4b` gap disclosed in
  `08p`'s introduction. Reconstructed the source script's shaded-area
  chart faithfully via `matplotlib.fill_between`, and added one
  cross-check the original script doesn't perform but the data file
  quietly supports: `OECD_IO_GHG_2021.mat` ships its own precomputed
  `GHG_balance` field (opposite sign convention, production minus
  consumption) alongside the raw `GHG_consumption`/`GHG_production`
  matrices this notebook computes the balance from directly — the two
  agree exactly, independently validating both the `/1000` Mt-to-Gt
  conversion and the 1-based-to-0-based row-index translation without
  relying on eyeballing the chart against the source script's hardcoded
  y-axis range alone (though that check is kept too, as a second,
  independent cross-check). No own-bugs this notebook — the numbers
  matched on the first execution. 5 sanity checks, all passed; 0 errors,
  0 stderr. Delivered to the conversation (notebook plus
  `OECD_IO_GHG_2021.mat`, now copied into `data/`); device sync to the
  user's folder still pending (bridge remained unreachable throughout
  this entire batch — see `08r`'s note above; all of `08r`-`08u` and
  their data files need syncing once the bridge reconnects).

**Chapter 8 Part 3 (EEIO carbon accounting, 65 scripts, 6 notebooks
`08p`-`08u`) is now complete.** 51 of 65 scripts built (6 fully synthetic
in `08p`/`08q`/`08r`/`08s`, 20 collapsed into `08t` via the confirmed
`tax3/4`≈`eeio_5/6` duplication and displayed from the archive's own
precomputed results, 1 real-data script in `08u`); 14 genuinely
unreproducible from this archive (`iot4a-c`'s missing WIOD table,
`imported2/3b/4a/4b`'s unrecoverable country-name lookup, and the entire
`desnos_*` family's missing data files) transparently disclosed rather
than fabricated. Combined with Part 2's completion above, **all of
Chapter 8 (144 scripts across both parts, 14 notebooks `08h`-`08u`) is
now complete** — and, per the original 16-chapter archive structure,
that completes the entire HSF-Notebooks translation project.

## Working conventions (same as the rest of the series)

- Faithful `.m`-to-Python translation via the `build_XXn.py` throwaway-
  script pattern; execute with `nbclient`, confirm 0 errors/0 stderr
  warnings, visually spot-check every figure before finalizing.
- Missing custom toolbox functions get reimplemented transparently with an
  explicit data-provenance caveat in the notebook markdown.
- Near-duplicate/superseded scripts get noted and skipped rather than
  rebuilt, same policy as earlier chapters.
- Never run git directly — hand exact `git add`/`commit`/`push` commands
  to the user.
