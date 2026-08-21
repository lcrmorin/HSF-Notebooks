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

## Chapter 2b

Built (2026-08-21). The Gini/selection/precision/ROC/performance/
discriminant/KS-curve and backtesting utilities were deliberately *not*
turned into named, reusable functions — they're one-off `.xlsx` readers
and plotting code tied to this chapter's specific figures (the curves
themselves come from data with no underlying formula in the MATLAB
source), not generic primitives. Only the q/z-score framework above
looked reusable enough to track.
