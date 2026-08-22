# Packaging candidates

Functions defined inline in a notebook here — rather than ported into
`quanttoolbox` — that look clean and reusable enough to be worth
promoting into the toolbox later, if a second notebook ends up needing
the same thing. Tracked here instead of ported immediately, so notebook
work isn't gated on a `quanttoolbox` release cycle for every
reusable-looking helper; a function only earns a trip into the toolbox
once it's actually reused, not on the first plausible-looking use.

Status legend: 🔵 candidate (used once so far) · 🟡 confirmed reusable
(used in ≥2 notebooks) · ✅ packaged into `quanttoolbox`

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `expected_hitting_time(P, target_states)` | `02a_ratings_and_transitions.ipynb` | Expected number of steps to reach a target set of states from each state of a discrete-time Markov chain, via a direct linear solve. | A generic Markov-chain primitive, not ESG-specific — any future chapter analyzing rating/state transitions could reuse it as-is. | 🔵 |
| `qscore`/`zscore`/`aggregate`/`qz_score`/`zq_score`/`bz_score` | `02b_scoring_methodology.ipynb` | A small scoring-and-aggregation framework: rank-based, standardization-based, and Beta-shaped transforms of a raw criterion onto a common scale, plus weighted aggregation of already-computed scores. | Generic score-normalization primitives, not ESG-specific — any chapter combining multiple raw criteria into one indicator (which is most of the rest of this book) is a plausible reuse. Before porting: check whether `scikit-learn`'s `QuantileTransformer`/`scipy.stats.rankdata`-based recipes already cover this cleanly rather than adding bespoke functions. | 🔵 |
| `corr_from_lower_triangle(values, n)` | `03a_esg_risk_and_factors.ipynb`, `03b_pastor_pedersen_te.ipynb` | Builds a symmetric n x n correlation matrix from its lower-triangular entries listed row by row (the MATLAB/GAUSS `xpnd` convention the `.m` source uses everywhere a correlation matrix is hand-specified). | A generic array-construction utility with no ESG content — the `xpnd`-style literal shows up throughout this book's `.m` source; already reused as-is in a second notebook (`03b`, for `pastor6`'s and `te_param1`'s correlation matrices). | 🟡 |
| `beta_pi_alpha(x, mu, Sigma, r)` | `03b_pastor_pedersen_te.ipynb` | CAPM beta/pi/alpha decomposition of every asset against a given portfolio used as the pricing benchmark: `beta = (Sigma@x)/(x'Sigma x)`, `pi = beta*(mu(x)-r)`, `alpha = (mu-r) - pi`. | A generic portfolio-attribution primitive, not ESG-specific — reused three times within `03b` alone (sections 1.4, 1.5, 1.7); the same pattern also appeared inline (uncollected into a function) in `03a`'s Markowitz sections 3.6/3.7, so a second notebook reusing it as a named function is a near-certainty. | 🔵 |
| `stacked_issuance_outstanding(data, names, years, ...)` / `load_cbi_sheet(xlsx_name, sheet)` | `04b_gss_bond_market.ipynb` | Reads a "year-row + category-rows" wide time-series sheet (the Climate Bonds Initiative data layout used throughout Ch.4's bond-market data) and renders the standard issuance/cumulative-outstanding two-panel chart plus an end-of-sample share table. | Reused 6 times within `04b` alone across the green- and social-bond breakdowns; the same "wide time-series by category, cumulative stock chart" shape is plausible for other market-sizing data later in the book (e.g. carbon-market or transition-finance issuance in Ch.9-11). Not ESG-specific in its mechanics. | 🔵 |
| `bond_ytm(t, cashflows, price)` | `04c_the_greenium.ipynb` | Newton's-method solver for the yield-to-maturity implied by a cashflow schedule and price — general fixed-income primitive, not ESG-specific. | A basic building block (`compute_bond_ytm.m`'s Python counterpart) likely needed again anywhere the book prices a bond from first principles. | 🔵 |
| `blended_finance_simulation(N0, D_junior, Ni, Ri, ci, coupon_rate_senior, nt_default)` | `05a_impact_market_instruments.ipynb` | Two-tranche (junior/senior) cash-flow waterfall: given a portfolio default path, allocates cumulative losses and coupon income between tranches and returns each tranche's annualized return over time. | A generic structured-finance/blended-finance primitive, not ESG-specific — reused twice within `05a` (deterministic scenarios and a Monte Carlo simulation); any later chapter touching tranched/blended structures is a plausible second-notebook reuse. | 🔵 |
| `fit_power_law(fit_table, area_units)` | `05b_biodiversity_extinction_theory.ipynb` | Backs out a power-law exponent/intercept ($S = c\,A^z$) for each row of a table by averaging $\log(S/S_{\text{ref}})/\log(A/A_{\text{ref}})$ across columns, given one reference column. | A generic scaling-law fitting utility, not biodiversity-specific — any later figure that tabulates a quantity at several scales and wants the implied power-law exponent (not just this chapter's species-area curves) is a plausible reuse. | 🔵 |
| `species_abundance_distribution(n_i, brk)` / `species_area_relationship(...)` / `endemics_area_relationship(...)` / `hurlbert_rarefaction(n_i, m)` | `05c_biodiversity_abundance_models.ipynb` | Community-ecology primitives: abundance-frequency/octave binning, random-placement species-area and endemics-area curves, and Hurlbert's exact individual-based rarefaction formula. | Reimplementations of custom MATLAB toolbox functions not shipped in `hfs-archive`; reused repeatedly within `05c` across four different real datasets (Whittaker, Verneaux, Condit, plus synthetic examples) — any later chapter touching species counts/community diversity (e.g. more of the biodiversity case study) is a near-certain second-notebook reuse. | 🔵 |

## Chapter 2b

Built (2026-08-21). The Gini/selection/precision/ROC/performance/
discriminant/KS-curve and backtesting utilities were deliberately *not*
turned into named, reusable functions — they're one-off `.xlsx` readers
and plotting code tied to this chapter's specific figures (the curves
themselves come from data with no underlying formula in the MATLAB
source), not generic primitives. Only the q/z-score framework above
looked reusable enough to track.

## Chapter 3a

Built (2026-08-21). Almost everything this notebook needed already
existed in `quanttoolbox` (`portfolio.mean_variance`,
`sustainable_finance.esg`) from the initial toolbox port — the notebook
mostly just applies those functions to the book's worked examples, so
there was very little new inline computation to evaluate as a packaging
candidate. `factor_esg_minvar_comparison` (the CAPM-vs-two-factor,
unconstrained-vs-long-only comparison table builder) was *not* tracked:
it's a table-formatting wrapper tied to this notebook's specific
side-by-side presentation, not a reusable primitive.

## Chapter 3c

Built (2026-08-21). This notebook is almost entirely chart-building
code reproducing the book's illustrative bar/scatter figures from
hardcoded source values, plus thin `pandas.read_excel` reads for the
five real-data sections — `quanttoolbox.portfolio.tracking_error.
te_portfolio` (already existing) is the only optimizer call. The
helpers defined here (`plot_equity_alpha`, `lasso_beta_paths`,
`quintile_fit_plot`, `pillar_quintile_grid`, `q1_minus_q5_alpha`) are
all tied to this notebook's specific figure layouts and hardcoded data
shapes (e.g. `q1_minus_q5_alpha` expects the exact (quintile, period)
array shape used only in section 6) — same judgment as `03a`'s
`factor_esg_minvar_comparison`, none tracked as packaging candidates.

## Chapter 5d

Built (2026-08-21). Nine FAOSTAT/OECD/Global-Footprint-Network/FAO-FRA/
plastics-industry themes, all one-off `pandas.pivot_table`/`groupby`
reshaping tied to a specific source table's own column layout (crop
production groupings, food-balance element codes, FRA forest-database
ISO3 cross-referencing, etc.) — none of it is a generic primitive a later
notebook would plausibly reuse unchanged, unlike `05c`'s community-ecology
functions. Nothing tracked as a packaging candidate from this notebook.

## Chapter 5e

Built (2026-08-21). The reimplemented dose-response functions
(`drc_log_logistic`, `drc_log_normal`, `drc_weibull2`, `drc_hormetic1`,
`drc_hormetic2`) are generic ecotoxicology curve-family primitives, not
biodiversity-specific — but they stand in for the source's own missing
custom functions under an unverified sign/parameterization convention
(see the notebook's data-provenance note), so they're deliberately *not*
tracked here as reusable: promoting an unverified reimplementation into
the shared toolbox risks compounding the uncertainty into a later chapter.
If a later chapter needs dose-response curves again, re-derive from the
standard model family rather than reusing this notebook's version as-is.
Everything else in the notebook is a one-off table/chart tied to a
specific source dataset.

## Chapter 6

Built (2026-08-21). Everything here — the divestment/institutional-
ownership tables and the ShareAction voting-panel slices (by year, topic,
region, AUM-weighting) — is tied to this dataset's own specific column
layout (the per-year `Resolutions`/`Alphabetical` sheets, or the merged
multi-year panel's `Feuil1` layout), not a generic reusable primitive.
Nothing tracked as a packaging candidate from this notebook.

## Chapter 7

Built (2026-08-21). No `.m` source to translate (see `CHAPTERS.md`) — this
notebook is a one-off pair of UN SEEA survey-table reads and ranked bar
charts, not a generic primitive. Nothing tracked as a packaging candidate.

## Chapter 8 Part 1 (physical climate science)

Built (2026-08-22), Part 1 now complete: `08a_physics_energy_balance`,
`08b_physics_feedbacks_sensitivity`, `08c_physics_ice_albedo`,
`08d_physics_bifurcations_chaos`,
`08e_anthropogenic_temperature_carbon_budget`,
`08f_anthropogenic_shares_intensity_multigas`,
`08g_palaeoclimate_consensus`.

`08e`, `08f`, and `08g` are all data-driven rather than first-principles
and don't add any packaging candidates — their helpers (`ols_trend`,
`region_panel`, the deuterium-to-temperature OLS calibration, the
fuel-source cumulative-share and bibliometric-tabulation computations)
are all tied to specific dataset layouts (OWID/HadCRUT/NOAA/FAOSTAT
temperature panels, Global Carbon Budget columns, Vostok ice-core sheets,
the Highly-Cited-Researchers/Nature-Index tables), not generic reusable
primitives.

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `pdf_normal_ratio(z, mu_x, sigma_x, mu_y, sigma_y)` / `cdf_normal_ratio(t, mu_x, sigma_x, mu_y, sigma_y, lower=0.0)` | `08b_physics_feedbacks_sensitivity.ipynb` | Closed-form density/CDF (Hinkley 1969 / Marsaglia) of the ratio of two independent normal random variables — used here for equilibrium climate sensitivity ECS = ΔF/(-λ) where both ΔF and λ are stochastic. Reimplemented because the source toolbox's own `pdfNormalRatio`/`cdfNormalRatio` were not shipped in `hfs-archive`; treated as a standard textbook result, not a guess, but still unverified against the original source's exact convention. | A generic probability primitive with no climate content — any future chapter needing the distribution of a ratio of two normals (e.g. a valuation multiple, a leverage ratio) could reuse it as-is. | 🔵 |
| `bisection(f, a, b, tol=1e-10, max_iter=200)` | `08c_physics_ice_albedo.ipynb`, `08d_physics_bifurcations_chaos.ipynb` | Faithful port of `QuantToolbox/optim/bisection.m`, including its specific edge-case contract: returns `NaN` (not an error) when `f(a)` and `f(b)` don't bracket a sign change, rather than assuming a bracket is always valid. | A generic root-finder used throughout the `hfs-archive` MATLAB source wherever `bisection.m` is called. Now reused verbatim in a second notebook (`08d`, to find the cubic normal form's equilibrium in section 4) — the NaN-on-no-bracket behavior matters for correctness of any downstream sweep, so it's worth promoting to a shared `quanttoolbox` helper the next time Chapter 8 needs a root-finder (e.g. DICE equilibria in Part 2). | 🟡 |
| `ice_albedo(...)` / `ice_albedo_tau(...)` | `08c_physics_ice_albedo.ipynb` | Evaluate the bistable ice-albedo energy-balance model's equilibrium condition and its local relaxation timescale τ=\|c/λ\|, vectorized over a swept parameter. | Tied to this notebook's specific ice-albedo model form (smooth ice-line albedo × single-layer greenhouse) — a plausible reuse if a later Ch.8 notebook revisits the same bistable model (e.g. a coupled or extended version), but not a generic primitive the way `bisection` is. | 🔵 |
| `missex(x, cond)` | `08d_physics_bifurcations_chaos.ipynb` | Sets elements of `x` to `NaN` wherever `cond` is true, else leaves them unchanged — a direct port of GAUSS's own `missex` function, which the `.m`/GAUSS source uses throughout to split a swept parameter array into a "left of the bifurcation" and "right of the bifurcation" branch for plotting. | A trivial but exact-semantics utility (NaN-masking is easy to get backwards) that will keep recurring anywhere the `hfs-archive` source uses `missex` for branch-splitting — used four times within `08d` section 1 alone. | 🔵 |

## Chapter 9a

Built (2026-08-22): `09a_carbon_budget_accounting.ipynb`, covering all
7 `chap9_carbon_budget*` scripts (no data dependency — first-principles
carbon-budget accounting).

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `carbon_budget_Reduction(t0, t, CE_t0, R, mtd)` | `09a_carbon_budget_accounting.ipynb` | Closed-form carbon budget $\int_{t_0}^t CE(s)\,ds$ under one of three emission-decline paths (linear, compound/geometric, exponential), cross-checked against numerical `quad` integration. | Reimplementation of a `QuantToolbox` function not shipped in `hfs-archive`; reused 3 times within `09a` (once per `mtd`). A generic emissions-pathway integration primitive — any later chapter/notebook needing a closed-form declining-emissions budget (e.g. Ch.10 transition pathways) is a plausible reuse. | 🔵 |
| `carbon_budget_piecewise(t0, t, t_k, CE_k)` | `09a_carbon_budget_accounting.ipynb`, `09f_transition_pathways_pac_scoring.ipynb` | Piecewise-linear multi-period carbon budget via linear interpolation between knot emission rates and trapezoidal integration. | Also undocumented/unshipped in `hfs-archive`; its output split (originally `CB1`/`CB2`/`CB3` in `09a`, simplified to a single trapezoid-integrated value once reused in `09f` since the `quad`-vs-`trapezoid` cross-check isn't needed a second time) was *inferred* from `chap9_carbon_budget7.m`'s inline equivalent computation, not verified against an original function body — flagged as inferred-not-verified in both notebooks. Now used in 2 notebooks — promoted to 🟡. | 🟡 |

## Chapter 9b

Built (2026-08-22): `09b_ghg_protocol_worked_examples.ipynb`, covering
the archive's `chap9_carbon_scope1-5,10,11` scripts (`scope7` skipped as
a duplicate of `scope5`). All sections here are one-off worked-example
tables/prints or a single real-data chart, tied to this notebook's
specific inputs — nothing generic enough to track as a packaging
candidate (unlike `09a`'s two reimplemented carbon-budget functions).

## Chapter 9c

Built (2026-08-22): `09c_sector_carbon_intensity_trucost_msci.ipynb`, a
thin single-section notebook (`chap9_carbon_ci1.m` only — `ci2`/`ci4`
are data-blocked, see `chapter9_scoping.md`). The dollar-weighted
"WACI-style" vs. naive-weighted-average portfolio carbon-intensity
blending logic is fully inlined into one worked-example cell, not
factored into a named function — reused nowhere else in this notebook,
so nothing tracked as a packaging candidate here.

## Chapter 9d

Built (2026-08-22): `09d_gwp_radiative_forcing.ipynb`, covering all 7
`chap9_gwp*` scripts (`gwp2f` folded into `gwp2a`'s section). The
Bern-model decay/AGWP functions are tied to this notebook's specific
CO2/CH4 physical constants (radiative efficiencies, decay time
constants) taken directly from the source — a generic-looking shape,
but not worth abstracting into a named reusable function unless a later
chapter needs GWP physics for a *different* gas (N2O, HFCs), at which
point the constants (not the functional form) would need to change
anyway. Nothing tracked as a packaging candidate.

## Chapter 9e

Built (2026-08-22): `09e_emission_trend_forecasting.ipynb`, covering all
6 `chap9_carbon_trend*` scripts. This is the first Chapter 9 notebook to
draw on the real `quanttoolbox` package rather than defining everything
inline — `quanttoolbox.econometrics.kalman.StateSpaceModel`/
`kalman_filter` and `quanttoolbox.econometrics.whittle.
whittle_local_linear_trend` are used as-is (already ported, not
reimplemented here), so nothing new is tracked as a packaging candidate
from this notebook; the state-space machinery already lives where it
belongs.

## Chapter 9f

Built (2026-08-22): `09f_transition_pathways_pac_scoring.ipynb`,
covering `chap9_carbon_pac1-5` plus 3 orphaned addenda scripts
(`carbon_offsetting2`, `consolidation1`, `greenness_grs1`). Reuses
`carbon_budget_piecewise` from `09a` (see the Chapter 9a entry above,
now promoted to 🟡). Everything else — the sector rebasing table, the
trend/target/NZE comparison chart, the simplified PAC score-trajectory
panels, and the archetype radar charts — is tied to this notebook's own
illustrative figures/data, not a generic reusable primitive. Nothing
new tracked as a packaging candidate.

## Chapter 9g

Built (2026-08-22), completing Chapter 9: `09g_cdp_netzero_tracking.ipynb`
(`tale1-3`; `tale4`/`tale5` confirmed data-blocked — see
`chapter9_scoping.md`).

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `tale_chart(ax, raw, ylim, yticks)` | `09g_cdp_netzero_tracking.ipynb` | Renders the "track record / 2020 trend / targets / NZE scenario" comparison chart from a 5-row raw data matrix: normalizes to a 2013 baseline, splits into the 4 labeled curves, PCHIP-smooths each between its own real data points, and straight-line-extrapolates the 2020 trend. | A generic "actual vs. extrapolated-trend vs. target vs. scenario" chart shape — reused 3 times verbatim within `09g` alone (`tale1`/`tale2`/`tale3`). The identical pattern also appears in `09f`'s `pac2` figure (built manually there, not via this helper, since `pac2` only has one scenario per line rather than 5 raw series to reduce) — a plausible second-notebook consolidation if Chapter 10's transition-pathway content needs the same shape again. | 🔵 |

## Chapter 5f

Built (2026-08-21). This completes the Chapter 5 biodiversity case study
(05a-05f) and Chapter 5 overall. The `solve_ivp` right-hand-side functions
(logistic-with-harvest, theta-logistic, Lotka-Volterra variants,
4-species competition matrix) are each tied to this notebook's specific
illustrative parameter choices (the exact `r`, `K`, `epsilon`, interaction-
matrix values used to reproduce the source's own figures), not generic
reusable primitives in the way `05c`'s community-ecology functions were —
a later chapter modeling a different population-dynamics system would
more sensibly write its own right-hand side against `solve_ivp` directly
than import one of these. The fisheries/rhino/BII data sections are
one-off `pandas.read_excel` reads and charts tied to their specific source
layouts. Nothing tracked as a packaging candidate from this notebook.
