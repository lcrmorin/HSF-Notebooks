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
| `corr_from_lower_triangle(values, n)` | `03a_esg_risk_and_factors.ipynb`, `03b_pastor_pedersen_te.ipynb`, `11k_net_zero_core_satellite.ipynb` | Builds a symmetric n x n correlation matrix from its lower-triangular entries listed row by row (the MATLAB/GAUSS `xpnd` convention the `.m` source uses everywhere a correlation matrix is hand-specified). | A generic array-construction utility with no ESG content — the `xpnd`-style literal shows up throughout this book's `.m` source; reused as-is in `03b` and again in `11k` (the latter confirming the earlier note flagging `11a`'s locally-redefined `xpnd` as a duplicate — `11k` imports this one directly instead of redefining it a third time). | 🟡 |
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

## Chapter 10a-10c

No new candidates. `10a`'s `internal_rate_return`/`appraise` helpers are
tied to its own two illustrative cashflow schedules; `10b` and `10c` are
one-off charts against hardcoded data with no repeated structure within
the chapter so far.

## Chapter 10d

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `dwl_shift_diagram(shift, params1, params2, point_offsets, point_labels, curve_labels, legend_loc, use_latex_points)` | `10d_externality_comparative_statics.ipynb` | Given a fixed linear SMB or SMC curve and two versions (original/shifted) of the other, computes the 5 comparative-statics points (A/B/C/D/E per `chap10_externality4a-4e.m`'s construction) and renders the full labeled diagram with both deadweight-loss triangles shaded. | Used 5 times verbatim within `10d` alone (`4a`-`4e`) — the only difference between calls is curve parameters and label positions. Same "SMB/SMC linear market diagram" shape as `10a`-`10c`'s externality figures, though those don't share this exact comparative-statics point construction, so no cross-notebook merge yet. | 🔵 |

## Chapter 10e

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `weitzman_example(alpha_B, beta_B, alpha_C, beta_C, epsilon_i, p_i, check_numerical=False)` | `10e_weitzman_prices_vs_quantities.ipynb` | Given linear SMB/SMC curves and a discrete cost-shock distribution, computes the ex-post-optimal, quantity-instrument, and price-instrument quantities per state, their realized welfare, and the closed-form $\\Delta W$ — printing a summary table and diagnostics. | Used 3 times verbatim within `10e` (`5a`/`5b`/`5d`) — a clean, generic "compare a price vs. quantity instrument under linear SMB/SMC and discrete cost uncertainty" primitive that would directly serve any later chapter revisiting the Weitzman model with different parameters. | 🔵 |

## Chapter 11a

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `min_te_portfolio(b, Sigma, A_eq, b_eq, A_ub, b_ub, lb, ub)` | `11a_tracking_error_optimization_basics.ipynb`, reused as-is in `11h_net_zero_te_optimization.ipynb` (`net_zero4`/`net_zero6`) | Port of `compute_te_portfolio`'s gamma=0 (pure minimum-tracking-error) case: minimizes `(w-b)'Sigma(w-b)` subject to linear equality/inequality constraints and box bounds via `scipy.optimize.minimize(method="SLSQP")`, internally pruning rank-deficient equality rows first (see `_prune_redundant_rows` below). | This is the chapter's core solver. Confirmed reusable: `11h` reused it verbatim for both the base and green-intensity/carbon-momentum-extended equity glide-path optimizations. `chapter11_scoping.md`'s plan reuses it further across `11i`-`11l`. Promote to `quanttoolbox` once a second chapter needs it. | 🟡 |
| `_prune_redundant_rows(A, b, tol)` | `11a_tracking_error_optimization_basics.ipynb`, reused as-is in `11h_net_zero_te_optimization.ipynb` | Incrementally drops equality-constraint rows that don't increase the matrix's rank (via `np.linalg.matrix_rank` on the growing candidate set), returning an equivalent full-row-rank system. | Fixes a real scipy-specific gap: SLSQP's LSQ subproblem hits a singular Jacobian on a rank-deficient equality system (e.g. a budget-row + full-sector-partition equality set, where the partition rows already sum to the budget row) and silently returns the initial guess unchanged instead of erroring — caught in `11a`'s `basic1`/`basic2` scenarios via a "sigma=0, no constraint is binding" red flag in the printed tables. MATLAB's `quadprog` doesn't have this problem, so it's a translation-environment gap, not a math error, and it recurs anywhere a script passes a full sector/scope partition as equality constraints (confirmed again inside `11h`, packaged bundled with `min_te_portfolio` there). Worth packaging independently — it's a generic guard for *any* scipy SLSQP/QP call built from this codebase's `.m` source, not tracking-error-specific. | 🟡 |
| `quadratic_form_bond_portfolio2` reconstruction (the `Q = phi_AS*I + phi_MD*diag(MD)@M@diag(MD) + phi_DTS*diag(DTS)@M@diag(DTS)` derivation) | `11a_tracking_error_optimization_basics.ipynb` | Builds the AS/MD/DTS mixed tracking-error quadratic form for bond portfolios, matching `quadprog`'s `H,f` convention (`R_b = Q@b`). | Not found anywhere in the shipped archive — derived directly from `chap11_basic3.m`'s visible `R_Mix(w)` nonlinear objective and cross-checked to ~1e-8 against a direct SLSQP solve of that same nonlinear objective. `chapter11_scoping.md` plans to reuse this in `11b`/`11c` (the LP reformulation and quadratic-form verification notebooks) and possibly `11e`. Keep the "derived from usage, not a recovered original" caveat attached wherever it's reused. | 🔵 |

Note: `11a`'s `xpnd(rho_vec, n)` helper (lower-triangular-packed → symmetric
correlation matrix) duplicates the already-🟡-confirmed
`corr_from_lower_triangle` from `03a`/`03b` — later Chapter 11 notebooks
should import/reuse that existing helper directly rather than redefining
`xpnd` locally again.

## Chapter 11c

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `quadratic_form(x, Q, R, c)` | `11c_quadratic_form_verification.ipynb` | `0.5*x'Qx - x'R + c` — **note the minus sign**, confirmed by testing both sign conventions against `qf1.m`'s own shift identity (see `chapter11_scoping.md`'s Progress notes for the full derivation). | The chapter's most elementary building block, used directly or indirectly everywhere `quadratic_form_risk`/`quadratic_form_bond_portfolio1/2` appear. `chapter11_scoping.md` plans further reuse in later Chapter 11 notebooks. A wrong-sign copy elsewhere would silently produce plausible-looking but incorrect numbers (as the first draft here did), so this is worth packaging once reused a second time, specifically to prevent the sign bug from being reintroduced by hand. | 🔵 |
| `quadratic_form_risk(sector, X, X_star, z)` / `_sector_risk_matrices` | `11c_quadratic_form_verification.ipynb` | Builds `(Q,R,c)` for a quadratic penalty on a vector's per-sector weighted aggregate against a target `X_star`, and evaluates it. | Reused 3+ times per notebook wherever a chapter-11 script builds a sector-level MD/DTS/AS penalty (`qf2`-`qf4` here; `chapter11_scoping.md` plans reuse in `11f`-`11l`). | 🔵 |
| `quadratic_form_bond_portfolio1(sector, varphi_MD, MD, MD_star, varphi_DTS, DTS, DTS_star, gamma_carry, carry)` | `11c_quadratic_form_verification.ipynb` | Absolute-target (not benchmark-relative) mixed MD/DTS objective plus a linear carry term, evaluated directly on `w`. | The non-benchmark-relative sibling of `11a`'s `quadratic_form_bond_portfolio2` reconstruction — same status/reuse profile. | 🔵 |
| `quadratic_form_bond_portfolio2(sector, varphi_AS, varphi_MD, MD, MD_star, varphi_DTS, DTS, DTS_star, gamma_carry, carry, b)` | `11c_quadratic_form_verification.ipynb`, reused as-is in `11d_decarbonization_toy_examples.ipynb` | Generalizes `11a`'s benchmark-relative mixed AS/MD/DTS objective to an arbitrary per-sector target (not just implicit zero) plus a carry term; `MD_star`/`DTS_star=None` recovers `11a`'s basic3/basic4 case exactly. | Supersedes `11a`'s narrower version — later notebooks should import this one rather than `11a`'s. Confirmed reusable: `11d`'s `decarbonization3` reused it verbatim, no changes needed. `chapter11_scoping.md` plans further reuse in `11e`/`11f`-`11l`. | 🟡 |
| `bond_portfolio_metrics(sector, MD, DTS, b)` | `11c_quadratic_form_verification.ipynb` | Portfolio-level and per-sector weighted MD/DTS aggregates of a given weight vector. | A small, generic, chapter-11-wide utility (any script computing a benchmark's own sector MD/DTS profile needs this) — `chapter11_scoping.md` plans reuse throughout the net-zero notebooks. | 🔵 |

## Chapter 11d

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `solve_min_quadratic_form(Q, R, c, A_eq, b_eq, A_ub, b_ub, lb, ub, x0)` | `11d_decarbonization_toy_examples.ipynb` | Minimizes `quadratic_form(w,Q,R,c)` subject to linear equality/inequality constraints and box bounds via SLSQP (the Python equivalent of MATLAB's `quadprog(Q,-R,C,D,A,B,lb,ub,x0)`), reusing `_prune_redundant_rows`. | A thin, generic bridge between the `(Q,R,c)` triples `quadratic_form_bond_portfolio2`/`quadratic_form_bond_portfolio1` build and an actual constrained solve — needed anywhere a script calls `quadprog` directly on a pre-built `(Q,R)` pair rather than going through `compute_te_portfolio`'s own gamma/mu/sigma machinery (as `decarbonization3` and, per `chapter11_scoping.md`, several later net-zero scripts do). Complements `11a`'s `min_te_portfolio`, which is specific to the `(w-b)'Sigma(w-b)` case. | 🔵 |

## Chapter 11e

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `spline_curve(x_fit, y_fit, x_grid, scale)` | `11e_decarbonization_results.ipynb` | Ports the source's recurring `fit(...,'smoothingspline','SmoothingParam',~1)` + `missex(y, x>x_fit(end))` pattern: drops NaNs, fits a natural cubic spline through (nearly-)exact discrete points, evaluates on a finer grid, and masks any output beyond the fitted data's own range (no extrapolation). | Every one of Chapter 11's ~20+ "fit a smoothing spline to a discrete risk-vs-reduction curve and plot it" scripts follows this exact pattern (`decarbonization_bond1a`/`1b`, `equity2b`/`3e`/`4e`/`5b` all use it here alone) — a strong candidate given how many blocked-vs-buildable scripts in `chapter11_scoping.md` share this shape. | 🟡 |
| `plot_four_curves(ax, x, y, ylabel, ylim, yticks, ...)` | `11e_decarbonization_results.ipynb` | Renders the SC1/SC1-2/SC1-3up/SC1-3 4-curve comparison (fixed line styles/colors/labels, a vertical reference line at R=50%) onto a given axis. | Reused 6 times verbatim within `11e` alone; the same 4-curve box-severity comparison layout appears throughout this script family, including in scripts that remain blocked for now but would reuse this helper if a future data drop unblocks them. | 🟡 |

## Chapter 11f

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `pathway_benchmarks()` | `11f_net_zero_pathway_benchmarks.ipynb` | Returns the 4 normalized decarbonization-pathway curves (IEA, NZAOA, CTB, PAB), 2020-2050, each `csaps`-smoothed and rescaled to 100 at 2020. | Used by both `net_zero1b` (plot) and `net_zero1c` (table) here. **Correction**: `11h`'s `net_zero4-7` glide-path targets turned out to use only the closed-form CTB reduction rate directly (`glide_path`, see the new Chapter 11h section below) rather than calling this function — no reuse materialized. Still a candidate for `net_zero12`/`net_zero1d`'s sector-pathway consumers per `chapter11_scoping.md`. | 🔵 |

## Chapter 11g

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `carbon_budget_compound_reduction(t0, t, Delta_R, R_minus, CE_t0, g_Y=0)` / `estimate_delta_R(...)` | `11g_net_zero_carbon_budget.ipynb` | Cumulative-carbon-budget-under-compounding-reduction model, plus a bisection wrapper solving for the reduction rate hitting a target budget. | This chapter's lowest-confidence reconstruction (see `chapter11_scoping.md`'s Progress notes for the validation performed) — no other notebook currently plans to reuse it, but if a later net-zero notebook needs the same "compounding reduction rate -> cumulative budget" primitive, this is the version to reuse rather than re-deriving. | 🔵 |

## Chapter 11b

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `solve_mixed_norm_te(b, CI, MD, DTS, Sector, Reduction, varphi_AS, varphi_MD, varphi_DTS, lb, ub)` | `11b_l1_l2_norm_reformulation.ipynb` | Solves the L1-form mixed active-share/MD/DTS bond tracking-error objective under a budget constraint and a CI-reduction target, two ways: direct nonsmooth minimization (`scipy.optimize.minimize`, SLSQP) and an epigraph LP reformulation (`scipy.optimize.linprog`) with slack variables bounding each sector-level absolute-deviation term — returns both solutions plus a metrics dict for each. | Used 3 times verbatim within `11b` (`lp2`/`lp3`/`lp4`, differing only in universe size, `varphi_DTS`, reduction targets, and box bounds). This is the L1-sibling of `11a`'s `min_te_portfolio`/quadratic-form machinery. **Not reused verbatim by `11h`**: `net_zero5`/`net_zero7` need a duration-neutrality equality constraint and optional extra inequality rows that this signature doesn't support, so `11h` wrote a new, more general `solve_bond_l1_duration_neutral` (see below) rather than extending this one — worth reconciling the two into a single generalized L1-bond-objective solver if a later notebook needs a third variant. | 🔵 |

## Chapter 11h

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `glide_path(R_minus, Delta_R, t0, offsets, prepend_zero=True)` | `11h_net_zero_te_optimization.ipynb` | `R(t) = 1-(1-R_minus)*(1-Delta_R)^(t-t0)`, the same CTB-style compounding-reduction closed form as `11f`/`11g`, returned as a sequence of glide-path *targets* (optionally prepended with an unconstrained `R=0` point) for a loop of re-optimizations. | Every one of `net_zero4-7` builds this exact glide-path sequence before looping an optimizer over it — a strong candidate for `net_zero8`-onward net-zero notebooks that follow the same "re-solve at each point on a CTB glide path" pattern. | 🔵 |
| `solve_bond_l1_duration_neutral(b, CI, MD, DTS, Sector, R_target, varphi_DTS, extra_C, extra_D, ub_mask, x0)` | `11h_net_zero_te_optimization.ipynb`, reused as-is in `net_zero7` with `extra_C`/`extra_D`/`ub_mask` | Generalized LP builder for the L1 active-share+DTS bond objective (no MD penalty term, unlike `11b`'s `solve_mixed_norm_te`) subject to budget, duration-neutrality (`MD(w)=MD(b)`), a CI-reduction target, and optional extra inequality rows (used by `net_zero7` for the carbon-momentum ceiling / green-intensity floor) and an asset-level upper-bound mask (momentum exclusion). Returns `None` on LP infeasibility rather than raising, matching the source's own `if retcode2==1` guard. | Confirmed reusable within `11h` itself (`net_zero5` base case → `net_zero7`'s extended case via the same function, just passing `extra_C`/`extra_D`/`ub_mask`). The `None`-on-infeasible convention is deliberate and should be preserved by any caller — `11h`'s own `net_zero6`/`net_zero7` glide paths run into genuine infeasibility at the two highest targets, and silently returning a garbage solution instead of `None` would have hidden that. | 🟡 |
| `solve_bond_l1_duration_neutral_smooth(b, CI, MD, DTS, Sector, R_target, varphi_DTS, x0)` | `11h_net_zero_te_optimization.ipynb` | SLSQP-based (fmincon-equivalent) direct nonsmooth minimization of the same L1 objective/constraint set as `solve_bond_l1_duration_neutral`, used only as a cross-check against the LP solution in `net_zero5`. | Single-use so far (only `net_zero5` cross-checks against it; `net_zero7` is LP-only, matching the source). Kept alongside the LP version as the fmincon-equivalent cross-check pattern established in `11b`. | 🔵 |

## Chapter 11i

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `smoothing_spline_curve(x_fit, y_fit, x_grid, p, scale)` | `11i_net_zero_stock_level_results.ipynb`, reused as-is in `net_zero10c` and again in `11l_net_zero_barahhou_te_decomposition.ipynb` (all 4 of its plotting patterns) | Port of `fit(x,y,'smoothingspline','SmoothingParam',p)` + `missex` upper-range masking, using the `csaps` package directly at the source's actual `p` (here `0.9` — genuine smoothing, not near-interpolation). | Confirmed reusable across a second notebook (`11l`, called with `p` ranging from `0.9` down to exactly `1.0`, so it now covers the full range `11e`'s natural-cubic shortcut only approximated). **Related but distinct from `11e`'s `spline_curve`** — worth unifying into one `fit_smoothing_spline` helper that always calls `csaps` if a third notebook needs spline-fitting, now that this version has proven itself the more general one. | 🟡 |
| `packr(x, y)` | `11i_net_zero_stock_level_results.ipynb`, reused as-is in `11j_net_zero_taxonomy_and_thematic.ipynb` and `11l_net_zero_barahhou_te_decomposition.ipynb` | Drops any `(x,y)` pair where either is `NaN`, matching MATLAB's `packr`. | A trivial one-liner but confirmed reused verbatim in a 2nd and 3rd notebook — 11e's build script had its own inline NaN-dropping instead of a named `packr`; the name has stuck across the back half of the chapter. | 🟡 |

## Chapter 11j

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| GICS-tree `subdivide(y_boundaries, counts)` geometry | `11j_net_zero_taxonomy_and_thematic.ipynb` | Given `n` parent-slot boundaries and `n` child counts, splits each parent's vertical slot into equal-width child slots (top-down), returning the full child boundary array (trailing `0`). Chained 3 times (sector→group→industry→sub-industry) to build the whole GICS tree's line geometry. | Generic hierarchical-bracket/treemap-boundary primitive, not GICS-specific — any later chapter drawing a nested-category diagram (sector/industry trees recur throughout this book) could reuse it directly. Single-use so far. | 🔵 |

## Chapter 11l

| Function | Defined in | What it does | Why it's a candidate | Status |
|---|---|---|---|---|
| `spider_plot(ax, data, ax_max, labels, colors, linestyles, shaded_idx, shaded_color)` | `11l_net_zero_barahhou_te_decomposition.ipynb`, reused as-is for `net_zero_barahhou8` | A from-scratch `matplotlib` reimplementation of the third-party MATLAB `spider_plot` toolbox's core behavior: one axis per category, each independently normalized to its own max value across the plotted series (`AxesLimits`-equivalent), drawn on plain Cartesian unit-circle geometry (not `matplotlib`'s polar projection, which can't represent per-axis scales), with an optional shaded region between two named series. | The only radar/spider chart in the book so far, and the only place `spider_plot.m` (shipped in `0. Toolbox/external/`) gets exercised — worth promoting the moment a second chapter needs a per-axis-normalized radar chart, since re-deriving the Cartesian-geometry trick from scratch is the fiddliest part. Confirmed reusable within `11l` itself. | 🟡 |
| `indnv(query, table)` | `11l_net_zero_barahhou_te_decomposition.ipynb` | Exact-match index lookup: for each value in `query`, returns its position in `table`, or `NaN` if not found — the MATLAB/GAUSS `indnv` convention used throughout this book's `.m` source wherever a script looks up specific years/labels in a data axis. | The first notebook in this chapter to need `indnv`'s actual lookup semantics (earlier notebooks either didn't hit a missing-match case or used simpler direct indexing) — a generic utility, not chapter-11-specific, likely to recur anywhere else the `.m` source does a `indnv(selected_x, x)`-style lookup with a documented "fall back to the last available value" pattern. | 🔵 |
