# Chapter 15 — Technical Appendix: Scoping

## Source

`HSF/15. Technical Appendix/` in the `hfs-archive` checkout. 9 exercise
scripts (`chap15_copula1-6.m`, `chap15_lasso1.m`, `chap15_lp1-3.m`), plus
7 toolbox self-test scripts (`test_copula1-6.m`, `test_smw1.m`) excluded
from the exercise count per this project's standing convention (`test_*`/
`init_*` files are toolbox scaffolding, not user-facing exercises — same
treatment as every earlier chapter).

No data files anywhere in this chapter — every script is either a pure
closed-form/toolbox exercise or works from a small inline data literal
(`chap15_lasso1`'s 15x6 matrix).

## Proposed notebook split

| Notebook | Scripts | Content | Notes | Status |
|---|---|---|---|---|
| `15a_copula_functions_and_diagrams` | `copula1-6` (6) | Marginal densities + a Gaussian-copula joint density; Fréchet-Hoeffding bounds; Frank-copula level curves; a shared 4-panel joint-density exercise (uniform/Normal/Student-t/Inverse-Gamma margins) repeated for Gaussian, Frank, and Gumbel copulas. | All copula CDF/PDF families already ported in `quanttoolbox.copula.families`; only the Frank-copula level-curve inversion (`copula3`) needed a from-scratch closed-form derivation (not itself in the toolbox). `copula4/5/6` collapsed into one parametrized `four_panel_copula_density` helper. | ✅ |
| `15b_lasso_regularization_path` | `lasso1` (1) | Lasso regression path (5 coefficients, standardized inline data) across a range of penalty values, replicating the classic "coefficient path vs. shrinkage fraction" diagram with degrees-of-freedom bands. | `regLasso2` (MATLAB, QP-based) replaced with `quanttoolbox.stats.regression.lasso.lasso_ccd` (coordinate descent, penalized form) looped over the lambda grid — same convex problem, verified to match at `lambda=0` (OLS) and to produce the expected monotonic path. | ✅ |
| `15c_linear_programming_duality` | `lp1-3` (3) | Bounded-variable LP feasibility (`lp1`); LP sensitivity analysis via shadow prices / dual values (`lp2`); primal-dual LP pair verifying strong duality (`lp3`). | MATLAB's `linprog` replaced with `scipy.optimize.linprog` (`method='highs'`). Dual-value sign conventions differ from MATLAB's and had to be verified empirically per constraint type (equality vs. inequality) rather than assumed — disclosed explicitly in the notebook. | ✅ |

## Working conventions (same as the rest of the series)

Same house conventions as every other chapter: `build_XXn.py` throwaway
build scripts (deleted after successful execution), 0 errors/0 stderr
warnings plus actual-output sanity-checking, transparent disclosure of
data quirks/discrepancies/dead code, near-duplicate scripts collapsed
into shared helpers, delivery + sync to the Mac via `SendUserFile` +
`device_commit_files`, and scoping-doc updates saved to the claude.ai
Project.

## Progress notes

**`15a_copula_functions_and_diagrams`** (`copula1-6`, 6 scripts) — built
and verified 0 errors / 0 stderr warnings, no data dependencies. One real
transcription bug caught and fixed while writing the build script:
`copula1`'s 4th panel (the copula-transformed joint density) pairs the
`t₃` grid with the **same `Beta(2,2)` grid** used in panel 2 (`cdfbeta`/
`pdfbeta` on `x2`), not a second normal margin as first (incorrectly)
transcribed — caught by re-reading the actual `.m` source line-by-line
rather than trusting a first-pass paraphrase, then fixed to build a
`t₃`/`Beta(2,2)` joint density via the Gaussian copula, matching the
source exactly. `copula2`'s dead-code block (`y1`/`y2`, computed but never
plotted) disclosed, not reproduced. `copula3` needed a from-scratch
closed-form Frank-copula level-curve inversion (verified via a round-trip
against `quanttoolbox`'s own `frank_cdf` for every `(θ,t)` combination in
each curve's valid domain — a first hand-rolled verification formula in
that check had its own sign-convention bug, caught and replaced with a
direct call to `frank_cdf` rather than re-deriving the algebra a second
time); also surfaced and disclosed a genuine mathematical domain
restriction (not a bug): a Frank-copula level curve `C(u1,u2)=t` has no
solution `u2∈[0,1]` for `u1<t`, since `C(u1,1)=u1` is every copula's
maximum value at fixed `u1` — correctly `NaN` there, matching what the
source script's own dashed guide lines visually demarcate. `copula4/5/6`
collapsed into one shared `four_panel_copula_density` helper (only the
copula family differs); `copula5`/`copula6`'s hard-coded `θ` values were
confirmed via `quanttoolbox.copula.dependence.frank_tau`/`gumbel_tau` to
correspond to exactly `τ=0.5`, as their unused `tau=0.5` source variable
implies. One genuine floating-point boundary singularity disclosed
(matching this project's established pattern, e.g. Chapter 13's `tau=0`/
`xi=1` cases): the `u2` grid for `copula4/5/6` hits exactly `1.0` at its
last point, where `Φ⁻¹(1)=+∞` blows up the Gaussian-copula panel at a
single cell — suppressed via `np.errstate`, not "fixed," since it's a
genuine singularity present in the source's own grid choice too. Added
sanity checks (all passed): Fréchet ordering `W≤Π≤M` holds pointwise
everywhere; every Frank level curve round-trips to its target `t` to
`1e-8`; all three copula densities integrate to their plotted-grid value
(~0.96-0.97, short of 1.0 purely from boundary-mass truncation on the
`[0.01,0.99/1.00]` grid, confirmed converging to 1.0 as the domain is
extended toward the true `[0,1]` boundary — the same boundary-
concentration phenomenon already established for the Vasicek density in
Chapter 13's `13j`).

**`15b_lasso_regularization_path`** (`lasso1`, 1 script) — built and
verified 0 errors / 0 stderr warnings. `regLasso2`'s (beta, tau, df,
complexity) API reproduced by looping `quanttoolbox`'s `lasso_ccd`
(penalized-form coordinate descent) over the lambda grid and computing
`tau`/`df`/`complexity` directly from each path point — verified exactly
matching OLS at `lambda=0` (a required boundary case for any correct
lasso implementation), with `tau` and `df` both confirmed monotonically
non-increasing in `lambda`, `R²` confirmed non-increasing (more shrinkage
can only fit the in-sample data worse), and the classic path diagram
showing all 5 coefficients converging to OLS at `s=1` and entering the
model one at a time (β3 first) as shrinkage relaxes — the expected lasso
path shape. One disclosed floating-point boundary case: `complexity=1/df`
divides by zero at the heaviest shrinkage level (`df=0`, every
coefficient shrunk out), giving `+inf`, matching MATLAB's own silent
behavior at the identical boundary rather than an error to fix.

**`15c_linear_programming_duality`** (`lp1-3`, 3 scripts) — built and
verified 0 errors / 0 stderr warnings, no data dependencies. `lp1`
surfaced a genuine finding, confirmed by hand-derivation rather than
trusted from the solver's status flag alone: tightening `lp1`'s second
scenario's first-inequality RHS from `10` to `1.4` makes the problem
**infeasible** — substituting the equality constraint into both
inequalities reduces them to `x1+2x2≥1.6` and `x1+2x2≤1.5` simultaneously,
a direct contradiction, so no feasible point can exist regardless of
solver or platform. `lp2`'s dual-value (shadow-price) sensitivity check
confirmed `scipy`'s `eqlin.marginals` needs **no** sign flip to match
MATLAB's `-lambda.eqlin` convention — verified by matching the actual
re-solved objective under 3 different RHS perturbations to the
shadow-price-predicted objective exactly, not assumed. `lp3`'s
primal/dual LP pair confirmed strong duality (primal max = dual min,
`65.9146` both ways) and, more sharply, that the primal's inequality
shadow prices (`-ineqlin.marginals`, needing the *opposite* sign
convention from `lp2`'s equality case — verified separately, not assumed
to carry over) exactly equal the dual's own optimal solution, and
vice versa — the classic complementary-shadow-price LP duality identity,
confirmed to numerical precision in both directions.

**Chapter 15 (Technical Appendix) is now complete: `15a`-`15c`, all 9
exercise scripts accounted for, 0 blocked.**
