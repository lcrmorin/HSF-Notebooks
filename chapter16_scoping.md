# Chapter 16 — Exercise Solution: Scoping

## Source

`HSF/16. Exercise Solution/` in the `hfs-archive` checkout. 10 scripts,
each a fully worked solution to an exercise from an earlier book chapter
(`chap16_chap<N>_exercise<k>.m`): 2 from Chapter 2 (ESG Scoring), 1 from
Chapter 3 (ESG Investing), 4 from Chapter 5 (Impact Investing /
biodiversity), 2 from Chapter 10 (Transition Risk, near-duplicates), 1
from Chapter 11 (Portfolio Optimization). No `test_*`/`init_*` scaffolding
files in this directory — all 10 are genuine user-facing exercises.

No data files anywhere in this chapter (confirmed by grepping every
script for `load(`/`readtable`/`xlsread`/`readmatrix`/`importdata` — zero
hits) — every script works entirely from small inline literal arrays
(price/return/covariance vectors, asset universes of 5-8 names, a handful
of survey-style data points).

Several custom functions this chapter calls are **local functions**
defined at the end of the script itself (MATLAB local-function syntax) —
these need no external lookup, just a direct line-by-line port:
`cdf_score1`/`pdf_score1`/`pdf_score2`/`gamma_cdf`/`compute_m_plus`
(`chap2_exercise1`), `esg_transition_matrix` (`chap2_exercise4`),
`fn_lambda_t`/`fn_mu_long_t`/`fn_mu_short_t`/`fn_delta_t`
(`chap5_exercise2`).

## Custom (non-builtin) functions and their status

| Function | Used in | Status |
|---|---|---|
| `compute_te_portfolio` | `chap3_exercise1`, `chap11_exercise1` | Found in `QuantToolbox/rpb/compute_te_portfolio.m`; not itself ported to the `quanttoolbox` package, but this project already built a faithful Python port during Chapter 11 (`min_te_portfolio` in `11a`/`11c`) covering the `gamma=0`/pure-minimize-TE case — `chap11_exercise1` only ever calls it that way (`targets=0, problem=0` everywhere), so it's a direct, already-verified reuse. `chap3_exercise1` additionally needs the **full** API (see below). |
| `compute_mvo_portfolio` | `chap3_exercise1` | Found in `QuantToolbox/rpb/compute_mvo_portfolio.m` (absolute mean-variance sibling of `compute_te_portfolio`, same `H`/`f`/gamma-scan/bisection machinery, just without the benchmark subtraction). **Not ported anywhere** (neither `quanttoolbox` nor an existing project notebook) — genuinely new Python work, though the algebra read directly from the `.m` source (see below) maps cleanly onto `quanttoolbox.optim.quadprog.solve_qp` + `quanttoolbox.optim.bisection.bisection`. |
| `quadratic_form_bond_portfolio2` | `chap11_exercise1` | Not found anywhere in the original archive (confirmed by `find`) — same as Chapter 11's own finding. Already reconstructed once, with a verified sign convention, as a project-local helper in `11c` (`quadratic_form_bond_portfolio2(sector, varphi_AS, varphi_MD, MD, MD_star, varphi_DTS, DTS, DTS_star, gamma_carry, carry, b) -> (Q_b, R_b, c_b, results)`). `chap16_chap11_exercise1.m`'s own Question 3.g independently re-derives and prints `f1_w = 0.5*w'Q_b*w - w'R_b + c_b` — the exact same minus-sign convention 11c settled on — which is a strong independent confirmation that 11c's reconstruction is correct. Directly reusable (call the 11c function for `Q_b,R_b,c_b`, then 11c's plain `quadratic_form(x,Q,R,c)` to evaluate, exactly mirroring what the source script itself does on the next line). |
| `quadprog` (direct call, Q3.g) | `chap11_exercise1` | Standard MATLAB Optimization Toolbox solver, not custom — but worth noting `quanttoolbox.optim.quadprog.solve_qp(q, r, a_eq, b_eq, c_ineq, d_ineq, lb, ub, ...)` uses the *exact same* `0.5x'Qx - R'x` objective convention as `quadratic_form`/MATLAB's `quadprog(H,-R,...)` call here, so it drops in directly with no sign-convention translation needed. |
| `pdfPoissonBinomial` | `chap5_exercise3` | Searched the **entire** archive (`QuantToolbox/` and `HSF/0. Toolbox/`) and `quanttoolbox` — no source anywhere, not a MATLAB Statistics Toolbox builtin either. Genuinely missing with nothing to port from, same situation as Chapter 11's `carbon_budget_compound_reduction`. Not blocked, though: the Poisson-Binomial PMF (distribution of a sum of independent, non-identical Bernoullis) is a standard, well-documented result with a simple DP/convolution recursion — reconstructable from first principles and cross-checkable against the script's own printed invariant `sum(k .* pmf) == sum(p)` (expectation of a sum of Bernoullis). |
| `bisection` | `chap5_exercise2`, `chap3_exercise1` (via `compute_mvo_portfolio`/`compute_te_portfolio`'s internal bisection) | **Already ported**: `quanttoolbox.optim.bisection.bisection(fhandle, a, b, config=None)`, elementwise-capable. Signature matches usage directly. |
| `xpnd` | `chap11_exercise1` | **Already ported**: `quanttoolbox.linalg.special_matrices.xpnd(v, method=1)` — `method=1` is row-wise, matching MATLAB's default and this script's packed-correlation-vector usage exactly. |
| `missex` | `chap2_exercise1` | Found in `QuantToolbox/tools/missex.m` (masks an array to `NaN` wherever a boolean condition holds — used to blank out-of-square segments of a budget-line plot). Not ported; trivial (`np.where(cond, np.nan, x)`). |
| `rows`, `cols`, `sumc`, `sumr`, `meanc`, `lag1`, `seqa`, `cdfn`, `cdfni`, `ftosa`, `text_line`, `skip_line`, `latex_tabular` | throughout | All GAUSS-style/cosmetic utilities living in `QuantToolbox/`/`HSF/0. Toolbox/`, none ported to `quanttoolbox`. Same treatment as every earlier chapter: straightforward numpy/pandas/print equivalents (`cdfn`→`scipy.stats.norm.cdf`, `cdfni`→`norm.ppf`, `rows`→`len`/`.shape[0]`, `latex_tabular`→a plain `pandas.DataFrame`), not real blockers. |
| `gamcdf`, `lognpdf`, `normcdf`, `mvncdf`, `fitdist`, `histogram`, `integral`, `ode45`, `fmincon`, `linprog`, `quadprog` | throughout | All standard MATLAB Statistics/Optimization Toolbox builtins, not custom — map to `scipy.stats.gamma/lognorm/norm/multivariate_normal`, `scipy.integrate.quad`/`solve_ivp`, `scipy.optimize.minimize`/`linprog`, `quanttoolbox.optim.quadprog.solve_qp`. |

### `compute_mvo_portfolio`/`compute_te_portfolio`'s full API (new work for `chap3_exercise1`)

Reading `compute_mvo_portfolio.m` directly: `problem=0` means the
`targets` argument *is* a vector of risk-aversion values `gamma_w`, and
the function just loops `quadprog(H, gamma_w(i)*f, ...)` once per value
to trace an efficient frontier (no bisection needed — this is what
`chap3_exercise1` Q2.c/Q2.e and Q3.f use). `problem=1`/`problem=2` instead
bisect `gamma` (via `bisection`, exactly as already ported) to hit a
target on the linear score `C'x` or on `sigma(x)`, respectively (Q3.g/
Q3.h). The existing `min_te_portfolio` port from `11a`/`11c` only covers
the implicit `gamma=0` pure-minimize case, so `chap3_exercise1` needs a
genuinely new (if straightforward, given the primitives above) Python
helper reproducing this fuller gamma-sweep/bisection-target API — for
both the absolute (`compute_mvo_portfolio`) and benchmark-relative
(`compute_te_portfolio`) forms, which share the same `H`/`f`/loop
structure and can plausibly share one implementation parameterized by
whether a benchmark is subtracted.

### Chapter 11 machinery reuse (verified against the actual `11a`/`11b`/`11c` notebook source)

`chap16_chap11_exercise1.m` turns out to reuse Chapter 11's existing
Python ports almost verbatim:

- **Q2.d-g** (TE-portfolio CI-reduction sweeps): pure `min_te_portfolio`
  calls in a loop — no new code.
- **Q3.g** (L2/quadprog mixed AS/MD/DTS solve): `quadratic_form_bond_portfolio2`
  (from `11c`) to build `Q_b,R_b,c_b`, then `quanttoolbox.optim.quadprog.solve_qp`
  — both already-verified pieces, composed for the first time.
- **Q4.b-c** (L1 mixed-norm reformulation, direct nonsmooth vs. epigraph
  LP): `11b`'s `solve_mixed_norm_te(b, CI, MD, DTS, Sector, Reduction,
  varphi_AS, varphi_MD, varphi_DTS, lb, ub)` builds an **identical** LP
  block structure (`[I_n -I_n Z1 Z1; -I_n -I_n Z1 Z1; C_MD Z2 -I_nS Z3;
  ...]`) to this script's own hand-rolled `linprog` call — confirmed by a
  direct line-by-line comparison of the two `A`/`b` constructions, not
  just structural similarity. Reusable close to verbatim (the only
  difference is `chap16`'s `fmincon` warm-starts from the Q3.g L2
  solution rather than from `b`).
- **Q3.c-e** (three separate `fmincon` solves on `R_AS`/`R_Mix_MD`/
  `R_Mix` under different equality-constraint sets): the objective
  closures themselves (`R_AS`, `R_MD`, `R_DTS`, `R_Mix`) are already
  written out in `11b`'s `solve_mixed_norm_te` (as their L2, not L1,
  counterparts need re-deriving directly from the source — straightforward,
  same shape) and match `min_te_portfolio`'s own SLSQP-with-linear-
  constraints pattern, so no new solver machinery is needed, just new
  glue code assembling the three different constraint sets per question.

## Per-script summary

**`chap2_exercise1`** (ESG weighted-score distributions) — derives the
closed-form CDF/PDF of a two-factor weighted ESG score `S=ω·X1+(1-ω)·X2`
(both `X~U[0,1]`, piecewise triangular/trapezoidal density), the density
of a 3-factor average score, and a Gamma-approximation argument for how
large a portfolio (`m` holdings) needs to be before a diversification
ratio concentrates within `±ε` of 1 with probability `p` (grid search
over `m` for several `(p,ε)` combinations). Inline literals only; no
data. ~212 substantive lines (of 496 total, rest is plot formatting).
Not blocked — only local functions plus `missex`/`gamcdf` (trivial).

**`chap2_exercise4`** (ESG factor aggregation, power-law tilts, ESG
turnover) — aggregates E/S/G sub-scores into one ESG score; simulates
power-law-tilted portfolio weights (`Dirichlet`-like via `u^(1/α)`
normalization) and their correlation with returns under a Gaussian
copula (Monte Carlo, up to 50,000 draws × 4 α-values × up to 12 ρ-values
in a doubly-nested loop); builds an ESG-score-breakpoint transition
matrix and computes portfolio turnover as ESG-score volatility `σ`
varies. ~184 substantive lines. Not blocked, but the nested MC loops
(`50000 × 4` then `12 × 10000 × ...`) are the one real *performance* risk
in this chapter — will need vectorizing over the Monte Carlo draws in
Python rather than translating the MATLAB `for` loops literally.

**`chap3_exercise1`** (CAPM/ESG-tilted portfolio theory) — derives
CAPM expected returns/covariances from a single-factor market model,
tangency/market portfolios and their betas; then builds ESG-constrained
mean-variance frontiers (`compute_mvo_portfolio`) and ESG-vs-tracking-
error frontiers (`compute_te_portfolio`) under integration/selection/
exclusion-style constraints, plus attribution (beta/alpha) analysis of
active portfolios against a stated benchmark. ~349 substantive lines (of
561) — the second-largest script in the chapter. Not blocked, but is the
one script requiring genuinely new machinery (the full gamma-sweep/
bisection-target MVO/TE API described above) rather than pure reuse.

**`chap5_exercise1`** (food security / undernutrition) — log-normal
models of average dietary energy supply (`X`) and requirement (`R`),
closed-form and simulated Prevalence-of-Undernourishment (`PoU`)
curves vs. correlation `ρ` and minimum dietary threshold `r_L`; a
national food-balance-sheet worked example (BMI/height/basal-metabolic-
rate/MDER calculation); a numerical-vs-analytical integral cross-check
of expected food-deficit. ~101 substantive lines. Small, self-contained,
closed-form — no solvers, lowest complexity of the chapter's Chapter-5
scripts. Not blocked (only cosmetic utilities).

**`chap5_exercise2`** (species-richness birth-death dynamics) — models
species colonization (`λ(t)`) and extinction (`μ_long(t)`, `μ_short(t)`)
hazard rates as functions of species richness `S`, finds equilibria
`S*` via bisection (single- and multi-equilibrium cases), integrates the
resulting ODE `dS/dt=λ(t)-μ(t)` forward from 5 initial conditions via
`ode45` to show convergence to equilibrium, sweeps parameters (`β2`,
`μs`) to trace how `S*` shifts, and fits 3 competing species-area-
relationship models (power/exponential/Kobayashi) to the equilibrium
curve via `fmincon` least-squares. ~322 substantive lines (of 747 — the
rest is plot formatting, all fully live/active code, no commented-out
sections). **Largest and most complex of the 4 Chapter-5 scripts** —
ODE integration (`scipy.integrate.solve_ivp` vs. MATLAB's `ode45`,
worth a numerical sanity-check since it's a different adaptive-step
algorithm, same due-diligence standard as other integrator swaps in
this project) plus dozens of repeated bisection root-finds plus 3-model
curve fitting. Not blocked (`bisection` already ported; local functions
straightforward).

**`chap5_exercise3`** (Poisson-Binomial aggregate risk) — computes the
exact PMF of a sum of independent, non-identically-distributed Bernoulli
indicators (an insurance-claims-style aggregation exercise: `k` policies
each independently defaulting with its own probability `p_i`), for two
toy `p` vectors, and verifies `E[sum]=Σp_i` two ways. 41 lines total,
~26 substantive — tiny. The one blocking-adjacent item in the chapter:
`pdfPoissonBinomial` has no source anywhere to port from (see table
above), but is mathematically well-defined and easy to reconstruct.

**`chap5_exercise4`** (survival analysis / life expectancy / VSL) —
**mostly commented out in the source**: Questions 6.a-c and 7.c (Weibull-
vs-exponential survival curves, discounted life expectancy `LE(t;ϱ)`,
quality-adjusted life expectancy `QALE`) are entirely commented-out
dead code in the `.m` file itself (should be disclosed, not built, per
this project's established convention). Only Question 8.e is live: a
Value-of-Statistical-Life (`VSL`) worked example converting between
`VSL`, `VSLY` (value per life-year) and `VQALY` (value per quality-
adjusted life-year) at 3 ages × 2 discount rates via numerical
integration of the discounted (QA)LE integrals. 246 lines total, only
~55 substantive and of those maybe 25 outside the commented block —
smallest genuinely active script in the chapter. Not blocked (`integral`
is a standard builtin; `latex_tabular` cosmetic-only).

**`chap10_exercise1a`/`chap10_exercise1b`** (Cobb-Douglas consumer
welfare under a price shock) — confirmed via `diff` to be identical
except `alpha` (0.6 vs 0.5), `p1` at time `t1` (0.75 vs 1.75), and the
output figure filename tag (`_Q6` vs `_Q7`). Derives Marshallian demand,
indirect utility, and both analytical and numerically-cross-checked
Compensating Variation (CV) and Equivalent Variation (EV) welfare
measures for a 2-good Cobb-Douglas consumer facing a price change,
plus the classic CV/EV/budget-line diagram. ~122 substantive lines each
(of 186-187). Pure closed-form algebra — no solvers, no data, only
`text_line` as a custom function. Lowest-risk pair in the chapter; a
clean case for the collapse-into-one-parametrized-notebook treatment
this project already uses elsewhere (matches `15a`'s `copula4/5/6` and
`11e`'s shared-curve-family pattern).

**`chap11_exercise1`** (carbon-intensity-constrained TE portfolio
optimization + bond MD/DTS quadratic-form + L1/L2 mixed-norm
reformulation) — an 8-asset/2-sector equity+bond toy universe: computes
Scope 1/2/3 carbon intensity, cumulative CI, WACI, ownership ratios and
benchmark-implied CE (Q1); builds the asset covariance matrix from a
packed correlation vector via `xpnd` and runs CI-reduction-constrained
TE-minimizing portfolios (`compute_te_portfolio`/`min_te_portfolio`)
across single targets, a grid of targets, and a 91-point reduction-rate
sweep for both Scope 1+2 and Scope 1+2+3 definitions (Q2); computes
benchmark MD/DTS and builds 3 increasingly-constrained bond
tracking-error solves (AS-only via `fmincon`; AS+MD mixed via `fmincon`
with an extra duration-neutrality constraint; full AS+MD+DTS mixed via
`fmincon`, cross-checked against the exact same objective expressed as
a quadratic form via `quadratic_form_bond_portfolio2` and solved with
`quadprog`) (Q3); and finally reformulates the L1-norm version of the
same mixed AS/MD/DTS objective both as a direct nonsmooth `fmincon`
solve and as an 8-variable-block epigraph `linprog`, cross-checking all
4 resulting portfolios (`b`, L2/quadprog, L1/linprog, L1/fmincon) side
by side (Q4). ~438 substantive lines (of 619) — **by far the largest and
most structurally complex script in the chapter**, though (per the
table/reuse notes above) it draws on Chapter 11's already-verified
Python ports (`min_te_portfolio`, `quadratic_form_bond_portfolio2`,
`solve_mixed_norm_te`, `quanttoolbox.optim.quadprog.solve_qp`, `xpnd`)
for nearly every piece of its machinery — this significantly lowers
its actual build risk relative to its line count; the genuine new work
is composing these pieces together for the first time in one script and
writing the CI/WACI arithmetic (trivial) and Q3's three `fmincon` glue
calls (straightforward, same SLSQP pattern as elsewhere in Chapter 11).

## Proposed notebook split

| Notebook | Scripts | Content | Notes | Status |
|---|---|---|---|---|
| `16a_chap2_esg_scoring` | `chap2_exercise1`, `chap2_exercise4` (2) | Closed-form weighted/averaged ESG-score distributions and portfolio-size diversification thresholds (`exercise1`); ESG factor aggregation, power-law-tilted weight simulations, Gaussian-copula return correlation Monte Carlo, and ESG-breakpoint turnover matrices (`exercise4`). | `missex`/local `cdf_score1`/`pdf_score1`/`pdf_score2`/`gamma_cdf`/`compute_m_plus`/`esg_transition_matrix` all straightforward direct ports; `exercise4`'s nested Monte Carlo loops (up to 50,000 × 4 × up to 12) need vectorizing, not literal-looping, for reasonable runtime. | ✅ |
| `16b_chap3_esg_investing` | `chap3_exercise1` (1) | CAPM betas/expected returns from a single-factor model; ESG-constrained mean-variance efficient frontiers (`compute_mvo_portfolio`) and ESG-vs-tracking-error frontiers under integration/selection/exclusion constraints (`compute_te_portfolio`), plus attribution analysis. | Requires building the **full** `compute_mvo_portfolio`/`compute_te_portfolio` API (gamma-sweep efficient frontier + bisection-to-target on `σ` or on the ESG score) as new Python helpers — the existing `min_te_portfolio` from Chapter 11 only covers the gamma=0 special case. Algebra fully legible from the original `.m` source; primitives (`quanttoolbox.optim.quadprog.solve_qp`, `quanttoolbox.optim.bisection.bisection`) already exist. | ✅ |
| `16c_chap5_biodiversity_dynamics` | `chap5_exercise2` (1) | Species colonization/extinction hazard-rate model, bisection-found equilibria, `ode45`-style forward integration from multiple initial richness levels, parameter sweeps, and 3-model species-area-relationship curve fitting via `fmincon`. | Standalone notebook given its size/complexity (largest of the 4 Chapter-5 scripts): ODE integration (`scipy.integrate.solve_ivp`, worth a numerical cross-check against `ode45`'s different adaptive algorithm), repeated `bisection` calls (already ported), curve fitting via `scipy.optimize.minimize`. Local hazard-rate functions port directly. | ✅ |
| `16d_chap5_risk_and_health_economics` | `chap5_exercise1`, `chap5_exercise3`, `chap5_exercise4` (3) | Log-normal food-security/undernutrition prevalence model with a national food-balance-sheet worked example (`exercise1`); exact Poisson-Binomial aggregate-risk PMF (`exercise3`); Weibull survival / discounted (quality-adjusted) life expectancy / Value-of-Statistical-Life worked example (`exercise4`, only Question 8.e is live — the rest of the source is commented-out dead code). | Grouped by shared theme (closed-form probabilistic/actuarial risk quantification) rather than script number, since `exercise2`'s ODE-based dynamics are a distinct sub-topic (see `16c`). `pdfPoissonBinomial` has no source anywhere in the archive — reconstruct from the standard DP/convolution recursion for the Poisson-Binomial distribution, cross-checked against the script's own `E[sum]=Σp_i` invariant. `exercise4`'s commented-out Q6/Q7 sections should be disclosed as dead code, not built. | ✅ |
| `16e_chap10_transition_risk_welfare` | `chap10_exercise1a`, `chap10_exercise1b` (2, collapsed to 1 parametrized notebook) | Cobb-Douglas consumer welfare under a relative-price shock: Marshallian demand, indirect utility, and analytical + numerically-cross-checked Compensating/Equivalent Variation, run once at `(α,p1)=(0.6,0.75)` and once at `(0.5,1.75)`. | Confirmed near-identical by direct `diff` (only `alpha`, `p1`, and the output figure tag differ) — collapsed into one parametrized notebook per this project's standing convention (mirrors `15a`'s `copula4/5/6`, `11e`'s shared spline-curve helper). Pure closed-form algebra, no data, no solvers — lowest-risk notebook in the chapter. | ✅ |
| `16f_chap11_carbon_portfolio_optimization` | `chap11_exercise1` (1) | Scope 1/2/3 carbon-intensity/WACI/ownership-ratio arithmetic; CI-reduction-constrained tracking-error-minimizing equity portfolios across single targets, grids, and a 91-point sweep; bond MD/DTS/AS mixed tracking-error objective solved via `fmincon` and cross-checked against the equivalent quadratic form via `quadprog`; L1-vs-L2-norm reformulation of the same mixed objective (direct nonsmooth `fmincon` vs. epigraph `linprog`), with all resulting portfolios compared side by side. | Own notebook given its size (largest script in the chapter, ~438 substantive lines) and because it's the natural "capstone" exercise drawing on nearly every piece of Chapter 11's machinery at once. Build risk is lower than the line count suggests: `min_te_portfolio`, `quadratic_form_bond_portfolio2`, `solve_mixed_norm_te`, and `quanttoolbox.optim.quadprog.solve_qp` are all already-verified reuse from `11a`/`11b`/`11c` (confirmed by direct comparison of this script's `linprog`/`quadprog` calls against those notebooks' existing helper code) — the genuine new work is composing them together and writing 3 new `fmincon` glue calls for Question 3.c-e. | ✅ |

Total: 2+1+1+3+2+1 = 10 scripts, 6 notebooks, 0 blocked.

## Working conventions (same as the rest of the series)

Same house conventions as every other chapter: `build_XXn.py` throwaway
build scripts (deleted after successful execution), 0 errors/0 stderr
warnings plus actual-output sanity-checking, transparent disclosure of
data quirks/discrepancies/dead code, near-duplicate scripts collapsed
into shared helpers, delivery + sync to the Mac via `SendUserFile` +
`device_commit_files`, and scoping-doc updates saved to the claude.ai
Project.

## Progress notes

**`16e_chap10_transition_risk_welfare`** (`chap10_exercise1a/1b`, 2
scripts collapsed to 1 notebook) — built and verified 0 errors / 0 stderr
warnings, no data dependencies. Confirmed exactly reproducing the source
`.m` algebra for Marshallian demand, indirect utility, and both the
closed-form and numerically-cross-checked Compensating Variation (CV) and
Equivalent Variation (EV) welfare measures — every printed intermediate
value (points A/B/C/D, `cv`/`cv_numerical`, `ev`/`ev_numerical`) matches
its independent numerical re-derivation to machine precision (`≤6.7e-16`)
in both scenarios. One genuine floating-point boundary singularity
disclosed, not fixed (same established pattern as Chapter 13's Vasicek
density and Chapter 15's Gaussian-copula grid): the plotting grid's
`x1=0.0` point makes the Cobb-Douglas indifference curve
`x2=(u/x1^α)^(1/β)` divide by zero, which is the correct mathematical
behavior (the curve has the `x1=0` axis as a genuine vertical asymptote,
never touching it) rather than a translation bug — suppressed via
`np.errstate(divide="ignore")`.

A real finding surfaced and resolved by direct source comparison, not
assumption: an initial self-authored sanity-check cell asserted `CV<0`/
`EV<0` for the price cut (`1a`) and the reverse for the price hike
(`1b`), based on a "compensation still needed" sign intuition — but the
actual computed values came out the opposite sign in both cases
(`1a`: `CV=+0.4756`, `EV=+0.5652`; `1b`: `CV=-0.9686`, `EV=-0.7322`).
Investigated by re-reading `chap16_chap10_exercise1a.m` line-by-line
(`cv = y_t0.*(1.0-(p1_t1/p1_t0).^(alpha/alpha_beta))`, `cv_numerical =
y_t0 - y_cv`) and confirming the notebook's helper reproduces that exact
formula verbatim — so the computed signs are correct and the *check's own
expectation* was the bug, not the computation. Under the source's own
convention (`CV`/`EV` = income that could be taken away from / must be
given to the consumer to hold them at a reference utility, evaluated at
the *original* utility for CV and the *post-shock* utility for EV), both
measures are positive for a welfare-improving price cut and negative for
a welfare-reducing price hike — fixed the check (not the computation) to
assert the correct sign convention. Also corrected the same cell's Willig-
bounds-ordering assertion, which had hard-coded `|EV|<|CV|` universally:
the correct classical result (verified against both scenarios) is
`|CV|≤|EV|` for a price **decrease** and `|EV|≤|CV|` for a price
**increase** — both scenarios' computed magnitudes confirm the
scenario-appropriate ordering exactly (`1a`: `0.4756≤0.5652` ✓; `1b`:
`0.7322≤0.9686` ✓). Both welfare diagrams (indifference curves, budget
lines, and CV/EV brackets for points A/B/C/D) visually inspected and
confirmed to match the expected Cobb-Douglas geometry, including the
CV/EV bracket sizes matching the computed magnitudes.

**`16a_chap2_esg_scoring`** (`chap2_exercise1/4`, 2 scripts) — built and
verified 0 errors / 0 stderr warnings, no data dependencies (8-name
inline E/S/G literals only). All local functions (`cdf_score1`,
`pdf_score1`, `pdf_score2`, `gamma_cdf`, `compute_m_plus`,
`esg_transition_matrix`) ported directly and cross-checked: `cdf_score1`
numerically differentiates to `pdf_score1` to within grid resolution,
both `pdf_score1`/`pdf_score2` integrate to 1 on `[0,1]`, and the
power-law tilt density `f(t)=αt^(α-1)` integrates to 1 for every `α`
tested (including `α=0.5`'s integrable singularity at `t=0`, handled with
`np.errstate` since it's a genuine density feature, not a bug).
`exercise4`'s doubly/triply-nested Monte Carlo loops (`50,000` draws ×
4 `α` values for Q2.e/2.g; `12` `ρ` values × `10,000` draws × 4 `α` for
Q2.h) were vectorized over the draw axis rather than translated as
literal `for` loops — an exact reformulation (each MATLAB iteration
independently redraws all its randomness, so batching the draws changes
nothing about what's computed), not an approximation; this keeps runtime
to a few seconds. Two real items resolved during the build: (1) a
dead-code note disclosed rather than reproduced literally — Q2.g's
source computes `u2=cdfn(g2)` inside its loop but never uses it (`s=g2`
is used directly), so the Python port simply never computes it; (2) a
transient `LinAlgError` in `esg_transition_matrix`'s bivariate-normal
rectangle-probability helper at very small `σ` (its covariance matrix
`[[1,1],[1,1+σ²]]` becomes numerically near-singular as `σ→0`, since
`det=σ²`), fixed by passing `allow_singular=True` to
`scipy.stats.multivariate_normal` and using `σ=1e-3` rather than `1e-6`
in the "turnover→0 as σ→0" sanity check to stay well clear of
float-precision territory — a numerical-implementation wrinkle on my
own side, not a source-script quirk, since MATLAB's `mvncdf` has no
equivalent singularity guard to disclose. `esg_transition_matrix`'s
bucket-transition-probability rectangle integral was implemented via
inclusion-exclusion on `scipy`'s joint CDF (`F(b,d)-F(a,d)-F(b,c)+F(a,c)`),
reproducing MATLAB's two-sided `mvncdf(xl,xu,...)` call exactly, and
verified every row of every transition matrix sums to 100%, every bucket
`cdf` sums to 100%, and turnover correctly vanishes as `σ→0` (perfect
remeasurement means no bucket ever changes) and rises with both `σ` and
the bucket count `K` (including the `K=1` edge case, where turnover is
trivially and correctly 0 since there's nothing to transition out of).
Also confirmed Q2.g's ESG-factor-correlated mean score exceeds Q2.e's
uncorrelated (≈0) mean for every `α`, as the induced correlation between
weight tilts and realized scores implies. All 24 sanity checks passed;
all 12 figures visually inspected and confirmed structurally correct
(iso-score-line corner geometry, symmetric trapezoidal/triangular score
densities, concentration/dispersion patterns across `α`, and monotonic
turnover-vs-`σ`/`K` curves).

**`16d_chap5_risk_and_health_economics`** (`chap5_exercise1/3/4`, 3
scripts) — built and verified 0 errors / 0 stderr warnings, no data
dependencies (all inline literals). `exercise1`'s log-normal
Prevalence-of-Undernourishment machinery reproduced faithfully, including
one deliberate source-script variable-overwrite pattern disclosed rather
than silently followed: `mu_x`/`sigma_x` are redefined partway through
the script (Question 2.e) from the initial `(7.50, 0.20)` values used in
Questions 1.b-e to log-normal parameters implied by a food-balance-sheet
calculation, and this redefined pair — not the Question-1 values — is
what Question 4.d's expected-food-deficit formula actually consumes;
verified the numerical-vs-analytical `FD` cross-check matches to
`3.7e-13` and, as a bonus identity the source itself demonstrates,
confirmed Question 1.c's and 1.e's two independently-derived PoU formulas
agree to `3.9e-16` at the reconciling threshold `r_L*(ρ)`. `exercise3`'s
`pdfPoissonBinomial` (no source anywhere in the archive) reconstructed as
two independent exact algorithms matching the source's own two-call
pattern — a direct DP/convolution recursion and a discrete-Fourier-
transform-of-characteristic-function method (the standard `poibin`-style
"RF" and "DFT-CF" approaches) — further cross-checked against brute-force
enumeration over all `2⁵` outcomes (feasible at this `n`) and against the
known reduction to a plain `Binomial(n,p)` when all `p_i` are equal. One
real implementation bug caught and fixed during the build (not a source
quirk, since there is no source to compare against): the DFT-CF method
initially used `np.fft.ifft`, which applies the opposite sign convention
in its exponent and silently returned the *reversed* PMF — caught
immediately by the brute-force cross-check (which the DP method passed
but the DFT method failed by a large margin) and fixed to
`np.fft.fft(χ)/L`, after which all three methods agree to floating-point
precision. `exercise4`'s Questions 6.a-c and 7.c are entirely
commented-out dead code in the source (Weibull-vs-exponential survival
comparisons and discounted-life-expectancy curves) — disclosed, not
built; only the live Weibull setup and Question 8.e's
Value-of-Statistical-Life worked example were built, cross-checked on
economic-sensibility grounds (`VSL=v/ΔL=$10` million from the stated
inputs, in line with real-world regulatory VSL figures; `LE` at `t=0`
comes out to exactly `70.00` years, implicitly confirming the Weibull
parameterization's mean-preserving construction `a=m/Γ(1+1/b)`; `VSLY`/
`VQALY` both rise steeply with age as remaining life-years shrink; `QALE
≤ LE` and both discount-adjusted quantities fall under a positive
discount rate, all holding at every one of the 6 `(t,ρ)` combinations
tested). All 22 sanity checks passed; all 4 figures visually inspected
and confirmed structurally correct.

**`16c_chap5_biodiversity_dynamics`** (`chap5_exercise2`, 1 script) —
built and verified 0 errors / 0 stderr warnings, no data dependencies.
The species colonization (`λ`), long/short-term extinction (`μ^long`,
`μ^short`) hazard functions and their bisection-found equilibria
(`fn_delta_t(S*)=0`) all reproduced faithfully and verified: `λ(0)=λ_0`,
`λ(S_s)=0`, `μ^long(0)=0`, `μ^long(S_s)=μ_s` exactly, both monotonic in
`S` as designed; every found equilibrium confirmed to be a genuine sign-
changing root of `δ(S)`, not just a near-zero value. `scipy.integrate.
solve_ivp` (`RK45`) used for the forward ODE integration in place of
MATLAB's `ode45`, cross-checked against `DOP853` (a different, higher-
order embedded Runge-Kutta method) landing on the same converged
trajectory to `<0.1` — confirms the results aren't an artifact of the
integrator choice. One real translation bug caught and fixed during the
build: Question 2.a's Python loop reused the generic variable names
`S_star`/`lambda_star`/`delta_star` inside a `for` loop over 3 scenarios,
which silently clobbered Question 1.f's already-computed global `S_star`
— caught because a later sanity check found `δ(S*)≈0` (bisection had
re-solved correctly) yet `δ(S*±1)` were nowhere near zero (evaluated
under the *wrong*, still-Q1.f, parameter set against the *new*, Q2.a-
overwritten `S_star`); fixed by renaming the loop-local variables.

Three genuine, non-bug findings investigated and disclosed rather than
silently patched: (1) Question 1.h's Case #2 (bistable parameters)
declares `S_0^\star=0` as a "boundary equilibrium" by fiat rather than
solving for it — checking directly, `δ(0)<0` under these parameters, so
`0` is not an actual root, and since `fn_delta_t`'s `S=max(0,S)` clip
only guards a single function evaluation (not the ODE state itself),
`solve_ivp` — like MATLAB's `ode45` would on the identical right-hand
side — drives the two trajectories starting below the unstable
equilibrium `S_1^\star` unboundedly negative rather than idling at `0`;
reproduced faithfully (both environments would show the same behavior)
and simply cropped out of view by the source's own `y∈[0,120]` axis
range, with the finding printed explicitly before the plot. (2) Question
2.d's `S*(μ_s)` curve is **not** monotonically decreasing as a first
glance at the model suggests — it forms a genuine U-shape, falling to a
minimum around `μ_s≈0.85` and then *rising* back up for larger `μ_s`,
because `μ_s` appears twice in `μ^long`'s formula (once as the
extinction ceiling, once sharpening the exponent `β_2·μ_s` that controls
how suddenly that ceiling bites) — confirmed both by direct calculation
and by the source's own `[70,160]` y-axis range being exactly sized to
show this U-shape's minimum rather than a plain decreasing curve. (3)
Trajectories starting near an unstable equilibrium (`S_0=30` in Case #2,
close to `S_1^\star=27.65`) linger there for a long time before being
pushed toward the far equilibrium — the classic slow-escape-from-a-
saddle-point dynamical feature — requiring looser convergence-by-`t=1000`
tolerances in the sanity checks than a naive "should have converged"
assumption, not a translation issue (confirmed by checking that
trajectories starting further from equilibria converge correspondingly
faster). All 26 sanity checks passed; all 12 figures visually inspected
and confirmed structurally correct, including the two disclosed findings
being visibly present in their plots.

**`16f_chap11_carbon_portfolio_optimization`** (`chap11_exercise1`, 1
script, the chapter's largest and final capstone) — built and verified 0
errors / 0 stderr warnings, no data dependencies (8-asset inline literals
only). Reused, in self-contained form, four pieces of already-verified
Chapter 11 machinery: `xpnd` and `quadratic_form_bond_portfolio2` (from
`11a`/`11c`, unchanged), `solve_mixed_norm_te` (from `11b`, unchanged), and
a QP-structured re-implementation of `min_te_portfolio` that calls
`quanttoolbox.optim.quadprog.solve_qp` — an exact convex QP solver (via
`cvxpy`) — directly rather than re-deriving `11a`'s original SLSQP
approximation; `solve_qp`'s own `0.5*x'Qx - R'x` objective convention
matches `quadratic_form_bond_portfolio2`'s output exactly, so its `(Q,R,c)`
triples plug straight into `solve_qp` with no sign conversion, confirmed
directly against the source script's own Question 3.g (which performs the
identical `quadprog(Q_b,-R_b,...)` cross-check). Question 1.d surfaced one
genuine, disclosed model property, not a bug: because this exercise defines
market capitalization as directly proportional to benchmark weight
(`MC_i = b_i * MC_Index`), every issuer's ownership ratio collapses to the
exact same constant (0.01%) regardless of issuer size — confirmed
numerically (all 8 values identical to machine precision) — which makes
the portfolio's owned-emissions-based carbon intensity an *unweighted*
mean of per-issuer intensities, genuinely different from the
benchmark-weighted WACI (verified: `WACI=76.94` vs. `CI=95.61`, a `-19.5%`
relative difference), reproducing the well-known WACI-vs-portfolio-carbon-
footprint divergence from the ESG literature rather than indicating an
error. Question 3.g's cross-check (rebuilding the same mixed AS/MD/DTS
objective under a permuted asset ordering via `quadratic_form_bond_
portfolio2` and re-solving) reproduced Question 3.e's directly-computed
solution to `<1e-8` — a genuine numerical identity confirming both
formulations are the same convex QP, not merely similar. One own-bug was
caught and fixed during verification: a first-draft Question 4 sanity check
compared `R_Mix(w_L2)` against `R_Mix(b)=0` — but `R_Mix(b)` is trivially
zero at the unconstrained benchmark and `b` itself violates the 50%
carbon-reduction budget, so it is not a feasible comparison point;
replaced with a meaningful cross-objective-optimality check verifying
`w_L2` (the R_Mix-minimizer) has the lowest R_Mix and the L1 solutions
(the D_Mix-minimizers) have the lowest D_Mix among the 4 feasible
portfolios compared, both confirmed true. The two independent L1 solvers
(direct nonsmooth SLSQP vs. epigraph LP) agreed to `<1e-6`. All 31 sanity
checks (12 + 10 + 9 across Questions 2/3/4) passed; both Question 2.g
figures (the σ-vs-reduction-rate curve and the 8-panel per-asset weight
grid) visually inspected and confirmed structurally correct (monotonically
rising tracking error as the carbon budget tightens, weights smoothly
reallocating away from high-carbon-intensity issuers).

**`16b_chap3_esg_investing`** (`chap3_exercise1`, 1 script, the chapter's
final and one genuinely-new-machinery notebook) — built and verified 0
errors / 0 stderr warnings, no data dependencies (6-asset inline literals
only). Required building the one piece of Python machinery this chapter's
scoping identified as new (not reusable from earlier chapters): a full port
of `compute_mvo_portfolio`/`compute_te_portfolio`'s 3-mode API (`problem=0`
direct gamma-sweep; `problem=1`/`2` bisect `γ∈[0,10]`, matching the
source's own hard-coded bracket and `BISECTION_Tol=1e-7`, to hit a target
return/score or volatility/tracking-error), unified into one
`compute_portfolio_frontier(score, Sigma, ..., benchmark=None)` helper —
derived algebraically from MATLAB's `quadprog(H,γ·f1+f2,...)` calling
convention by expanding into `solve_qp`'s own `0.5x'Qx-R'x` form
(`Q=Σ`, `R=γ·score` absolute or `R=γ·score+Σb` benchmark-relative),
confirmed at `γ=0` to collapse to exactly the same pure minimum-tracking-
error QP already verified in `16f` (Question 3.f's `γ=0` point reproduces
the benchmark exactly, `σ=0`, `w=b`). Two genuine, disclosed source
features reproduced faithfully rather than "corrected": Question 2.c's
third plotted curve literally pairs `w3`'s return with `w2`'s risk (an
apparent copy-paste artifact in the original `.m` plotting code, not the
underlying portfolio computation) and Question 2.d's comparison table
includes two identical columns by construction (`w1_ast`/`w_ast` are
literally the same MATLAB variable). One further genuine, disclosed model
feature surfaced while designing Question 3.i's sanity checks: the
Selection universe's own pure minimum-tracking-error point (`γ=0`) already
carries a materially positive ESG score (`≈2.09`, vs. `0` for the
unrestricted Integration universe), since assets #4-6 — nearly half of the
benchmark's own weight — are structurally excluded, so "same `γ`" is not
an apples-to-apples comparison of ESG-tilt strength between the Selection
and Integration frontiers; an initial sanity check assuming Selection's
score would stay below Integration's at every `γ` was wrong for this
reason and was replaced with two directly meaningful checks instead. No
translation bugs were found in this notebook (the API derivation, read
directly from `compute_mvo_portfolio.m`/`compute_te_portfolio.m`, matched
the source's algebra on the first attempt). All 29 sanity checks (8 + 10 +
11 across Questions 1/2/3) passed; all 5 figures visually inspected and
confirmed structurally correct (efficient-frontier curves shifting up-left
as the ESG floor tightens, Sharpe ratio falling and ESG score rising
monotonically as `S*` sweeps from -2.5 to 2.5, and the Integration/
Selection/Exclusion tracking-error-vs-ESG-score frontiers ordered as
expected).

**Chapter 16 (Exercise Solution) is now complete: `16a`-`16f`, all 10
exercise scripts accounted for, 0 blocked.**
