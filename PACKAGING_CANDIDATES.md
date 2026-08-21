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
