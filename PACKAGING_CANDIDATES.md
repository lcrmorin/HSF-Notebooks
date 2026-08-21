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

## Chapter 2b (planned)

Scoring-methodology functions — Gini curve, KS statistic/curve,
performance/selection/discriminant curves, classifier-backtesting
utilities — will be defined inline in `02b_scoring_methodology.ipynb`
per an explicit decision (2026-08-21) not to port them into
`quanttoolbox` yet, since it's not yet clear which are genuinely reused
elsewhere versus specific to this chapter's presentation. Entries get
added here once that notebook exists.
