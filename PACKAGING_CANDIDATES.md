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
