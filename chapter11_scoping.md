# Chapter 11 (Portfolio Optimization) — scoping & roadmap

Chapter 11 ships 77 `chap11_*.m` exercise scripts (confirmed by direct
`find`, not filename-pattern estimation), organized into 4 families:
`basic`/`lp`/`qf` (12, foundational tracking-error-optimization
machinery), `decarbonization`/`decarbonization_bond`/
`decarbonization_equity` (34, carbon-intensity-constrained portfolio
construction), `net_zero`/`net_zero_barahhou` (31, net-zero-alignment
pathways and TE-decomposition robustness checks). Scoped via two
parallel research agents (one per major family group) that read every
script's actual content plus checked the shared `QuantToolbox`/
`HSF/0. Toolbox` locations for custom-function definitions, followed by
direct verification (by me) of every script whose behavior depended on
ambiguous data-file column/sheet mapping — a lesson carried forward
from Chapters 9-10's "confirm directly, don't infer" convention.

## The central blocker: `data/chap11_MSCI_World`

The single biggest blocker in this chapter: **`data/chap11_MSCI_World`
(a stock-level MSCI World holdings/emissions/covariance dataset) does
not exist anywhere in the shipped archive.** It is required by the
*compute* step of roughly 20 of the 34 decarbonization-family scripts
and `net_zero10a` (which also needs a second missing file,
`data/MSCI_WORD_2015_2023`, and `Results/Decarbonization1`). Unlike
Chapter 9/10's blockers, several of these compute scripts *do* have a
plotting sibling that reads a **precomputed results workbook**
(`Results/chap11_decarbonization_equity.xlsx`, `Results/chap11_
decarbonization_bond.xlsx`, `Results/chap11_net_zero10a.mat`, `Results/
chap11_net_zero10c.mat`) which **is** shipped and readable — so the
*chart* can still be built faithfully from real archived results even
though the *optimization that produced them* cannot be re-run from
scratch. Every such case is called out explicitly per notebook below;
scripts with no such fallback (no precomputed artifact anywhere in the
repo) are flagged fully blocked.

## Other missing custom functions (need reimplementation)

- **`init_colours`** (British spelling) — called in nearly every script
  in the decarbonization/net_zero families for `colour_blue/red/green/
  violet/black` constants. **Not defined anywhere in the repo** (only
  the American-spelling `init_color`/`color_*` exists, in a handful of
  scripts). Trivial to work around: just define a matplotlib palette
  once and use it everywhere; not a real blocker.
- **`quadratic_form(x,Q,R,c)`** — evaluates `0.5*x'Qx + x'R + c`.
  Trivial, reimplement directly.
- **`quadratic_form_risk`**, **`quadratic_form_bond_portfolio1`**,
  **`quadratic_form_bond_portfolio2`**, **`bond_portfolio_metrics`** —
  build the `(Q,R,c)` matrices behind the AS/MD/DTS bond
  tracking-error objective (absolute-target and benchmark-relative
  versions) and compute per-sector MD/DTS aggregates. **Not found
  anywhere in the repo.** The algebra is legible from usage (sums of
  squared per-sector tracking deviations, weighted by `varphi_*`
  coefficients, expressed as a quadratic form) — reimplemented once as
  shared Python helpers in `11a`/`11c`, with an explicit caveat that
  the exact internal derivation is inferred from call-site usage, not
  verified against an original function body (same honesty standard as
  Chapter 9's `carbon_budget_piecewise`).
- **`carbon_budget_compound_reduction(t0,t,Delta_R,R_minus,CE_t0[,g_Y])`**
  — used in `net_zero1e`, `net_zero2`, `net_zero3` (all print-only, no
  figures). **Not found anywhere in the repo.** A plausible compounding
  emissions-reduction-to-cumulative-budget formula will be reconstructed
  from usage and clearly caveated as inferred, not verified — these 3
  scripts are pedagogically thin (print-only diagnostics) so the risk
  of a faithfulness gap is contained and disclosed rather than silently
  built as if certain.
- **`compute_te_portfolio`** (and siblings `compute_te_portfolio_return`/
  `_volatility`) — **found**, in `QuantToolbox/rpb/`. The core
  quadprog-based tracking-error-minimizing solver used throughout this
  chapter: minimizes `(w-b)'Sigma(w-b)` subject to linear equality/
  inequality constraints and box bounds, with optional gamma/return/
  vol-targeting modes (bisection search). Ported once as a shared
  Python helper (`cvxpy` or `scipy.optimize` QP) used across `11a` and
  the net-zero notebooks.
- All other referenced helpers (`rows`, `sumc`, `cols`, `ftosa`, `seqa`,
  `xpnd`, `packr`, `missex`, `text_line`, `skip_line`, `strcat2`,
  `latex_tabular`, `bisection`, `indnv`, `lag1`, `stdc`,
  `save_graphic`/`save_graphic2`, `spider_plot`) were all located in
  `QuantToolbox/` or `HSF/0. Toolbox/` — cosmetic/utility, straightforward
  numpy/pandas/matplotlib equivalents.

## Planned notebook split

| Notebook | Scripts | Topic | Data | Status |
|---|---|---|---|---|
| `11a_tracking_error_optimization_basics` | `basic1-4` (4) | CI/ESG-constrained tracking-error-minimizing equity and bond portfolios via `compute_te_portfolio` (QP) and `quadratic_form_bond_portfolio2` (bond mixed AS/MD/DTS objective, reimplemented). | None (hardcoded 8-asset/9-asset universes) | ✅ |
| `11b_l1_l2_norm_reformulation` | `lp1-4` (4) | ℓ1- vs ℓ2-norm Monte Carlo illustration, then the mixed-norm bond tracking-error objective reformulated as a linear program (`linprog`/epigraph slack variables) vs. direct nonsmooth `fmincon`, cross-checked. | None | ✅ |
| `11c_quadratic_form_verification` | `qf1-4` (4) | Pedagogical identity-checks of the `quadratic_form`/`quadratic_form_risk`/`quadratic_form_bond_portfolio1/2`/`bond_portfolio_metrics` machinery (reimplemented in 11a/11c) against hand-derived formulas. | None | ✅ |
| `11d_decarbonization_toy_examples` | `decarbonization1-4` (4) | Self-contained 8-asset/12-sector illustrations: threshold vs. order-statistic vs. naive CI-reduction approaches, a bond mixed-objective CI-constrained solve, and a static GICS-sector CI-reduction table. | None | ✅ |
| `11e_decarbonization_results` | `decarbonization_bond1a/1b`, `decarbonization_equity2b/3e/4e/5b` buildable (6); `decarbonization5`, `equity1a-1c`, `equity2a/2c`, `equity3a-3d`, `equity4a-4d`, `equity5a`, `equity6a-6e`, `equity7a-7d` blocked (28, all need the missing `MSCI_World` dataset, and `equity2c`/`7c`/`7d` additionally need missing `.mat` checkpoints with no `.xlsx` fallback) | Risk-vs-CI-reduction curves under progressively tighter box/sector constraints (C0 unconstrained through C3 sector+name-bounded), built from the real precomputed `Results/*.xlsx` workbooks — faithful charts of real archived results, even though the underlying optimizations can't be re-run from scratch. | `Results/chap11_decarbonization_bond.xlsx`, `Results/chap11_decarbonization_equity.xlsx` (both exist; exact sheet/column mapping per script confirmed by direct source read, not inferred) | ✅ |
| `11f_net_zero_pathway_benchmarks` | `net_zero1a-1d`, `net_zero8` (5) | Global/sector emissions-scenario decomposition, and 4 normalized decarbonization-pathway benchmarks (IEA/NZAOA/CTB/PAB) vs. advanced/developing-economy CE/CI trajectories — all self-contained hardcoded IEA-style data. | None | ✅ |
| `11g_net_zero_carbon_budget` | `net_zero1e`, `net_zero2`, `net_zero3` (3) | Compounding emissions-reduction-rate-to-cumulative-carbon-budget worked examples (print-only). Requires reconstructing `carbon_budget_compound_reduction` from usage — disclosed as inferred, not verified. | None | ✅ |
| `11h_net_zero_te_optimization` | `net_zero4-7` (4) | 8-asset toy portfolios hitting a CI-reduction glide path via QP (`compute_te_portfolio`) and via LP+`fmincon`, with/without green-intensity-floor and carbon-momentum-ceiling constraints — two base-vs-extended optimizer pairs. | None | ✅ |
| `11i_net_zero_stock_level_results` | `net_zero10b`, `net_zero10c` buildable (2); `net_zero10a` blocked (1, needs missing `MSCI_WORD_2015_2023` + `Results/Decarbonization1`) | Tracking-error and active-share trajectories 2020-2035 under 4 pathway benchmarks × 4 emission scopes, from the real precomputed `Results/chap11_net_zero10a.mat`/`10c.mat` (both confirmed readable — ordinary numeric/struct arrays, no MCOS blocker). | `Results/chap11_net_zero10a.mat`, `Results/chap11_net_zero10c.mat` (both exist and readable) | ✅ |
| `11j_net_zero_taxonomy_and_thematic` | `net_zero12`, `net_zero14`, `net_zero15` (3) | GICS 4-level sector taxonomy tree diagram (custom patch-based chart, "satellite" sub-industries highlighted), green-bond-index tracking error, thematic-equity-fund rolling tracking error. | `Data/chap11_gics_classification_2023.mat`, `Data/chap11_green_bonds.mat`, `Data/chap11_thematic_equity_funds.mat` (all exist and readable — the two latter have one unreadable MCOS "None" variable each, which turned out to be the `datetime` date axis; recovered from the shipped `.xlsx` siblings instead, values checked to match the `.mat` numeric arrays exactly) | ✅ |
| `11k_net_zero_core_satellite` | `net_zero16-18` (3) | Core-satellite bond/equity allocation algebra: single case → 4-asset TE-vol formula → full grid sweep across allocation/correlation assumptions. | None | ✅ |
| `11l_net_zero_barahhou_te_decomposition` | `net_zero_barahhou1-10` (10) | Post-processing/robustness plots from a Barahhou-et-al.-style TE decomposition: CTB-vs-PAB and Decarbonization-vs-Transition tracking-error trajectories by scope (10 scripts collapse to ~4 reusable plotting patterns per the scoping survey), sector-allocation spider/radar charts, and DTS/Active-Share-vs-reduction-rate curves. | `Data/chap11_net_zero_Barahhou1-6.mat`, `chap11_net_zero_barahhou7/9/10.xlsx` (all exist and confirmed readable) | ✅ |

Total: 4+4+4+4+6+5+3+4+2+3+3+10 = 52 buildable scripts (of which 6 in
`11e` and 2 in `11i` are plot-only ports of precomputed results, not
independently-reproducible optimizations) + 25 fully blocked
(`decarbonization5`, `equity1a-1c`, `equity2a/2c`, `equity3a-3d`,
`equity4a-4d`, `equity5a`, `equity6a-6e`, `equity7a-7d`, `net_zero10a`)
= 77, matching the archive's confirmed file count exactly.

## Progress notes

- **`11a`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  10 cells, 1 figure (`basic4`'s 2x3 AS/MD/DTS-vs-reduction-target grid,
  visually confirmed against the source's axis limits/ticks/colors).
  `min_te_portfolio` (the `compute_te_portfolio` gamma=0 port) and
  `quadratic_form_bond_portfolio2`'s algebra both checked out against a
  direct 1.5e-8-level cross-check between the nonlinear (`fmincon`-
  equivalent) and quadratic-form (`quadprog`-equivalent) solves of
  `basic3`'s `R_Mix` objective. Caught and fixed a real solver bug during
  the build: `basic1`'s "CI + ESG + Sector-neutral" scenario and both of
  `basic2`'s scenarios pass an equality-constraint matrix `A = [A0; A1;
  A2]` (budget row plus both sector-membership rows) — since every asset
  belongs to exactly one of the two sectors, `A1 + A2 = A0` row-wise, so
  this 3-row system is rank-deficient. `scipy.optimize.minimize`'s SLSQP
  hits a singular Jacobian in its LSQ subproblem on a rank-deficient
  equality system and silently returns the initial guess (`w = b`,
  `sigma = 0`) unchanged, rather than erroring — a first draft's printed
  tables showed the "CI + ESG + Sector-neutral" and both `basic2`
  scenarios landing exactly on the benchmark with zero tracking error,
  which is what caught it (all three scenarios' inequality-constraint
  targets, e.g. 30% CI reduction, clearly weren't binding). MATLAB's
  `quadprog` (interior-point-convex) handles rank-deficient equality
  constraints without issue, so this was a scipy-specific gap, not a
  translation error in the constraint algebra itself. Fixed generally
  inside `min_te_portfolio` with a `_prune_redundant_rows` helper that
  incrementally drops any equality row that doesn't increase the
  constraint matrix's rank before handing it to SLSQP — verified the
  post-fix solutions bind exactly on every active inequality target
  (e.g. `basic1`'s CI(w)=183.204=0.70×261.72 and Score(w)=0.669 both
  bind to the letter) and satisfy the (now-reduced) equality system
  exactly. This bug will recur in later Chapter 11 notebooks (`11f`-`11l`
  reuse `min_te_portfolio` and several also pass full sector/scope
  partitions as equality constraints alongside a budget row) — the fix
  lives in the shared helper so it's already covered, and
  `_prune_redundant_rows` is a strong `PACKAGING_CANDIDATES.md` entry in
  its own right, independent of `min_te_portfolio`.

- **`11b`** built and verified 2026-08-22: 0 errors/0 stderr warnings,
  10 cells, 1 figure (`lp1`'s 2x2 L1-vs-L2-norm Monte Carlo scatter,
  visually confirmed against the source's exact per-panel axis limits).
  `lp1` uses `rng(10)` in MATLAB for exact scatter reproducibility;
  MATLAB's Mersenne Twister stream isn't reproducible from Python, so a
  NumPy `default_rng` seed is used instead and the notebook discloses
  that the individual points will differ from the source figure even
  though the statistical shape (scale, spread, regression fit) is
  faithful. `lp2`-`lp4` share one new helper, `solve_mixed_norm_te`
  (packaging candidate, see `PACKAGING_CANDIDATES.md`), that solves the
  L1 mixed AS/MD/DTS bond tracking-error objective both as a direct
  nonsmooth minimization (`fmincon`-equivalent) and as an epigraph LP
  reformulation (`linprog`-equivalent) and cross-checks them. Both
  solvers agree exactly on `CI(w)` (the binding constraint) and closely
  on `R_Mix(w)` in every case; `max|w_fmincon - w_linprog|` is sometimes
  a few percentage points rather than ~0 because the L1 objective's
  sector-aggregated terms are piecewise-linear, so the optimum can sit
  on a flat face of the feasible region with more than one minimizing
  `w` — disclosed in the notebook as expected non-uniqueness, not a
  translation gap (confirmed by `R_Mix`/`CI` agreeing where `w` itself
  doesn't exactly).

- **`11c`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 10
  cells, all identity checks (14 in Section 1, plus 3 more sections
  cross-checking `quadratic_form_risk`/`quadratic_form_bond_portfolio1`/
  `quadratic_form_bond_portfolio2`/`bond_portfolio_metrics` against manual
  formulas) verified to exactly 0 diff. **Caught and fixed a real sign
  error before it could propagate further**: a first draft assumed
  `quadratic_form(x,Q,R,c) = 0.5x'Qx + x'R + c` (plus sign on the linear
  term) — this is the natural-looking convention and is what the earlier
  session summary going into this notebook had asserted as "confirmed."
  It is wrong. Testing both sign conventions numerically against `qf1.m`'s
  own `qf5a`/`qf5b` shift identity (`quadratic_form(x-y,Q,R,c) ==
  quadratic_form(x,Q,R+Qy,0.5y'Qy+y'R+c)`) shows only the MINUS
  convention (`0.5x'Qx - x'R + c`) makes it hold for arbitrary x,y,Q,R,c;
  six of `qf1.m`'s 14 identities (`qf5`,`qf6`,`qf8`,`qf10`,`qf12`,`qf14`
  — every one involving the linear `R` term and a nonzero shift) failed
  with the plus convention and passed exactly with the minus convention.
  This flows through to every downstream reconstruction: `R` in
  `_sector_risk_matrices` flips from `-M'X_star` to `+M'X_star`, and the
  carry term's sign in `quadratic_form_bond_portfolio1`/`_2` flips from
  `-gamma_carry*carry` to `+gamma_carry*carry` (plus a `+gamma_carry*(b@
  carry)` constant term in `_2`'s `c_b` that a first draft omitted
  entirely). None of this affects `11a`/`11b`, which never call a
  `quadratic_form`-shaped Python function directly (11a's `min_te_
  portfolio` builds `(w-b)'Sigma(w-b)` directly; 11b's L1 objective is
  built directly too) — this convention only matters wherever a notebook
  actually calls a `quadratic_form(x,Q,R,c)`-shaped helper, which starts
  here. **Any later Chapter 11 notebook reusing `quadratic_form`/
  `quadratic_form_risk`/`quadratic_form_bond_portfolio1/2` must copy
  `11c`'s minus-sign versions, not re-derive from the "obvious" plus
  convention.** Section 4 also replaced an initial hand-guessed "expected
  value" comment (which was itself wrong — computed without actually
  working through the algebra) with a proper manual-formula cross-check
  matching Sections 2-3's style; the corrected result confirms
  $R_{\\mathrm{Mix}}(b)=0$ exactly (holding the benchmark means zero
  deviation *and* zero carry adjustment, since carry is linear in
  $w-b$), not the non-zero value the first guess claimed.

- **`11d`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 11
  cells, 2 figures both visually confirmed correct (threshold/order-
  statistic/naive CI-reduction frontier, `decarbonization1`'s 0-70% range
  and `decarbonization2`'s wider 0-90% range with the interpolated naive
  curve) — in both, the threshold curve sits at or below the discrete
  order-statistic/naive points, as expected since it's the TE-minimizing
  frontier. First direct reuse of both `11a`'s `min_te_portfolio` and
  `11c`'s `quadratic_form_bond_portfolio2` in the same notebook — no
  changes needed to either, promoting `quadratic_form_bond_portfolio2`
  to 🟡 (confirmed reusable) in `PACKAGING_CANDIDATES.md`. Two disclosed
  source quirks, not translation choices: (1) `decarbonization2`'s figure
  scales $\\sigma(w|b)$ by `1e2` while `decarbonization1`'s otherwise-
  identical figure uses `1e4`, both labeled "(in bps)" — reproduced
  literally since the y-limits (`[0,16]`) only make sense with `1e2`;
  (2) `decarbonization3` computes an `fmincon` solution and immediately
  overwrites it with a `quadprog` solution on the next line before either
  is used, so only the `quadprog`-equivalent path (`solve_min_quadratic_
  form`, a new thin wrapper minimizing `quadratic_form` directly, reusing
  `_prune_redundant_rows`) was ported.

- **`11e`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 15
  cells, 6 figures all visually confirmed correct (bond AS/DTS
  tracking-error frontiers; equity unconstrained-CI frontier; two 2x2
  grids of equity threshold-shape frontiers; equity `C3(0,10,2)`
  frontier) — every curve shows the expected monotone-increasing,
  correctly-ordered shape (looser box constraints produce lower tracking
  error at every reduction target). Copied `Results/chap11_
  decarbonization_bond.xlsx` and `Results/chap11_decarbonization_equity.xlsx`
  into this repo's `data/` folder (both shipped and readable — only the
  underlying stock-level `MSCI_World` dataset that would let these be
  *recomputed* is missing). Built a shared `spline_curve` helper (natural
  cubic spline through the archived discrete points, matching every
  script's `SmoothingParam` being within `1e-13` to `1e-3` of 1, i.e.
  effectively full interpolation, disclosed in the notebook) and a
  `plot_four_curves` helper for the repeated SC1/SC1-2/SC1-3up/SC1-3
  4-curve layout, reused across all 6 sections. One initially-surprising
  but confirmed-correct observation: `equity3e`'s `C1(0,1.5)` and
  `C1(0,1.25)` panels look nearly identical — checked directly against
  the workbook's raw numbers (e.g. row 40: 7.669094 vs. 7.670971) and
  confirmed this is genuine in the archived data, not a column-mapping
  bug. The other 28 scripts in this family remain fully blocked (no
  `.xlsx`/`.mat` fallback at all, or a missing `.mat` checkpoint) and are
  documented in the notebook's closing markdown rather than silently
  dropped.

- **`11f`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 12
  cells, 4 figures + 1 table, all visually/numerically confirmed correct
  (sector and global emissions-scenario decomposition; the IEA/NZAOA/CTB/
  PAB normalized-pathway comparison and its reduction-percentage table,
  cross-checked against each other — e.g. CTB starts at exactly 30%
  reduction and PAB at exactly 50% by construction, NZAOA reaches exactly
  100% by 2050; sector-level pathway benchmarks; advanced-vs-developing
  CE/CI trajectories). All smoothing-spline fits (`csaps(x,y,p,xi)` in
  the source, MATLAB's Spline Toolbox) are ported with the `csaps`
  Python package rather than a `scipy` smoothing spline, since it's a
  parameter-compatible port of the same algorithm (same `p` in `[0,1]`
  with the same interpolation-vs-least-squares-line endpoints) —
  `net_zero1d`'s `save('results/sector_iea',...)` call is reproduced as
  in-memory arrays (`sector_iea_t`/`sector_iea_y`) rather than a file,
  since nothing in this notebook needs it persisted; a later notebook
  needing that data (`net_zero12`, per this doc's table) will recompute
  it the same way rather than depend on a save/load round-trip across
  notebooks.

- **`11g`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 9
  cells, no figures (print-only diagnostics, matching the source). The
  chapter's lowest-confidence reconstruction — `carbon_budget_compound_
  reduction` isn't defined anywhere in the archive — but it checks out
  unusually well: the reconstructed model ($CE(s)=CE_{t_0}(1-R_-)[(1-
  \\Delta R)(1+g_Y)]^{s-t_0}$, cumulative budget = sum over the horizon)
  is the same compounding-decline shape already independently confirmed
  for `11f`'s CTB/PAB benchmark curves, and `net_zero3`'s own bisection
  precondition (`CB(theta_min)<0 and CB(theta_max)>0`) is satisfied
  exactly by the reconstructed formula's values (1100 at `Delta_R=0`,
  199.9 at `Delta_R=0.50`, target 750 in between). Strongest check:
  `net_zero3`'s growth-adjustment identity `theta'=1-(1-theta)/(1+g_Y)`
  and a direct re-solve of the bisection at `g_Y=3%` both land on
  **exactly** `theta=0.1069`, confirming the compound-reduction formula
  and the growth-adjustment identity are mutually consistent. One
  disclosed ambiguity that couldn't be resolved from usage alone: the
  source function returns two values (`CB1`,`CB2`) and no call site
  distinguishes what they differ by (each call only ever consumes one),
  so both are reconstructed as the same cumulative-sum quantity here
  rather than guessed apart further.

- **`11h`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 10
  cells, no figures (print-only glide-path tables, matching the source).
  Covers `net_zero4-7`: the same 8-asset equity/bond toy universes from
  `11a`/`11d`, re-solved at 7-8 points along a CTB-style compounding
  CI-reduction glide path ($R_-=30\\%$, $\\Delta R=7\\%$/yr) rather than an
  arbitrary grid. `net_zero4` (`min_te_portfolio` QP) tracks its target
  exactly at every point. `net_zero6` adds a green-intensity floor and
  carbon-momentum ceiling on top; the two highest glide-path targets
  ($R=51.3\\%$, $66.1\\%$) turn out to be infeasible jointly with those
  overlay constraints in this toy universe (confirmed independently via
  a standalone feasibility LP: max achievable reduction ≈51%) — SLSQP
  settles at the closest feasible point rather than erroring, so
  `Reduction %` plateaus instead of continuing to track the target,
  matching what the source's own unchecked `compute_te_portfolio` call
  would do. **Real bug caught and fixed while building `net_zero5`**: a
  first draft assumed it reused `11b`'s 4-asset bond toy universe (by
  analogy with `net_zero4`'s equity/`11a` relationship) — re-reading
  `chap11_net_zero5.m` directly showed it actually declares its own
  **8-asset** `b`/`CI`/`MD`/`DTS`/`Sector` (same `b`/`CI` as `net_zero4`/
  `net_zero6`, with new bond fields). Caught because every R-target row
  past `R=0` came back all-`NaN` (LP infeasible) — a duration-neutrality
  equality constraint on only 4 assets pins `CI(w)` to a narrow feasible
  band (≈[198,261] here) that a 30%+ reduction target can never reach,
  confirmed via a standalone LP min/max-`CI(w)` feasibility check. After
  switching to the correct 8-asset universe, `MD(w_lp)` binds to `MD(b)`
  exactly at every point and `max|w_lp - w_fmincon|` stays ≤0.0001
  (consistent with `11b`'s L1 non-uniqueness note). `net_zero7` reuses
  the same 8-asset bond universe plus `net_zero6`'s GI/CM overlay
  (confirmed correct on the first draft this time, having already been
  corrected once in an earlier pass) and correctly returns `NaN` rows at
  the same two infeasible glide-path points as `net_zero6` — matching
  the source's own `if retcode2 == 1` guard around a `NaN`-initialized
  results array on an infeasible `linprog` call.

- **`11i`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 7
  cells, 2 figures (both 2x2 scope grids, verified visually — monotone
  smooth curves, correctly ordered PAB > CTB > NZAOA > IEA by stringency
  at every scope, matching the intuition that the strictest pathway
  should carry the highest tracking error). Covers `net_zero10b`/`10c`,
  both pure plotting scripts reading real precomputed
  `Results/chap11_net_zero10a.mat`/`chap11_net_zero10c.mat` (copied into
  `data/`) — the same "compute blocked, plot buildable from shipped
  results" situation as several `11e` scripts. `net_zero10a`'s actual
  compute step stays blocked (missing `MSCI_WORD_2015_2023` stock-level
  panel and `Results/Decarbonization1`); `net_zero10c`'s compute step
  has no `.m` source anywhere in the archive at all, only its shipped
  `.mat` output and the plotting consumer — reproduced literally (fixed
  `all_results(6)` index, `y/2` scaling) with no attempt to reverse-
  engineer what the other 6 struct entries or the halving represent.
  Introduced `smoothing_spline_curve` (genuine `csaps` smoothing at
  `p=0.9`, not `11e`'s near-interpolating natural-cubic approximation —
  the first Chapter 11 script where `SmoothingParam` isn't within
  `1e-3` of 1) and `packr`/`plot_scope_grid` helpers.

- **`11j`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 8
  cells, 3 figures. **Data note, not actually a blocker**: `chap11_green_
  bonds.mat` and `chap11_thematic_equity_funds.mat` each store their
  date axis as a MATLAB `datetime` (an MCOS object `scipy.io.loadmat`
  can't parse — it silently drops the variable and warns "Duplicate
  variable name None"). Recovered from each file's shipped `.xlsx`
  sibling instead; the reconstructed numeric arrays were checked to
  match the `.mat` files' `index`/`duration`/`equity_data` values
  exactly (to `0.0` max absolute difference) once restricted to the same
  date range and forward-filled for the handful of non-trading-day gaps
  the `.mat` version already had baked in — so this is a full-fidelity
  recovery, not a lower-confidence fallback. `net_zero12`'s GICS-tree
  diagram (11 sectors → 25 industry groups → 74 industries → 163
  sub-industries, 29 flagged "satellite") is a faithful direct port of
  the source's nested-subdivision geometry, reusing `11f`'s established
  `sector_iea`-style "read the source line by line, don't guess the
  layout" approach — verified correct only after zooming into the
  rendered figure (thumbnail-scale it wrongly looked like the Industry
  Group column had no internal gridlines; a 2x crop confirmed the
  subdivisions were there, just fine relative to sectors with only 1-2
  industry groups). **Real bug caught and fixed**: `net_zero14`'s
  duration bar chart initially rendered as a completely blank panel —
  `matplotlib`'s `bar()` on a raw `datetime64` x-axis interprets a plain
  numeric `width` in the array's native time unit (nanoseconds here),
  not days, so `width=20` silently became a ~2e-10-day-wide (invisible)
  bar; fixed by passing `width=np.timedelta64(20, "D")` explicitly.
  Caught by noticing the "Duration" subplot was empty even though its
  y-axis had auto-scaled to the correct 5-9 range (proof the data was
  there, just not rendered) — a reminder that "the axis limits look
  right" isn't the same check as "the plotted marks are visible."

- **`11k`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 8
  cells, no figures (closed-form algebra + print/table output only, no
  data files, no optimizer). Covers `net_zero16-18`: core-satellite
  bond/equity allocation algebra, a 4-factor blended tracking-error-
  volatility formula, and a full grid sweep across satellite weight,
  equity split, and two correlation scenarios. Reused `corr_from_lower_
  triangle` (from `03a`/`03b`, already flagged in `PACKAGING_CANDIDATES.
  md` as the correct replacement for a locally-redefined `xpnd`) rather
  than reimplementing `xpnd` a third time. **Faithfully reproduced
  source bug, not fixed**: `net_zero18`'s `Sigma2` line is
  `Sigma2 = sigma .* sigma'`, which never multiplies by the correlation
  matrix `rho` its own preceding lines build — so `Sigma2` is actually
  an all-pairs-$\rho=1$ covariance matrix, not the $\rho=0.8$
  equity-cross-correlation scenario the surrounding code implies (almost
  certainly a copy-paste bug in the original `.m`, since `Sigma1`'s
  otherwise-identical line does multiply by its own `rho`). Reproduced
  literally with a markdown disclosure rather than silently corrected,
  per this series' standing "faithful port first" convention. **Self-
  caught error**: a first draft of this same markdown cell described
  the correlation structure backwards (attributed the $\rho=0.8$
  equity-cross-correlation to `Sigma1` instead of to what `Sigma2`'s
  dead-code `rho` was supposed to produce) — caught on a second reading
  of the source's `rho` literals before finalizing, not by a numeric
  check, since both scenarios ran without error either way.

- **`11l`** built and verified 2026-08-22: 0 errors/0 stderr warnings, 12
  cells, 10 figures, all verified visually (monotone glide-path curves,
  PAB/Transition consistently above CTB/Decarbonization as expected,
  correct truncation at each fitted series' own data range per `missex`,
  and both radar charts showing the expected "Index" baseline forming
  the complete outer ring under per-axis normalization). Completes the
  planned 12-notebook Chapter 11 split (`11a`-`11l`, all 77 exercise
  scripts accounted for). Collapsed `net_zero_barahhou1-10` into the 4
  reusable patterns the original scoping survey predicted: risk-vs-time
  CTB/PAB (`barahhou1-2`), the same with a shaded scenario gap and a
  printed average-gap diagnostic (`barahhou3-6`, one parametrized helper
  called 4 times), sector-level radar/spider charts (`barahhou7-8`), and
  risk-vs-reduction-level fit against the CTB/PAB glide path rather than
  against time directly (`barahhou9-10`). **`barahhou8` turned out not
  to need its own data file** — a first read of the file listing showed
  no `chap11_net_zero_Barahhou8.*` and nearly got flagged as blocked,
  but the script itself (`xlsFileName = 'data/chap11_net_zero_
  barahhou7.xlsx'`) reuses `barahhou7`'s workbook across its two sheets
  (with vs. without an exclusion filter) — caught by reading the source
  before assuming a missing same-numbered data file meant a missing
  input. The `spider_plot` sector-radar chart (a third-party MATLAB
  toolbox shipped in `0. Toolbox/external/`, not ported line-for-line)
  was reimplemented directly against its documented behavior: each of
  the 11 GICS-sector axes gets its own `AxesLimits`-style normalization
  by that axis's own max value across the plotted series, rendered on
  plain Cartesian unit-circle geometry rather than `matplotlib`'s
  polar projection (which assumes one shared radial scale and can't
  represent per-axis limits directly) — no errors surfaced in this
  reconstruction on the first attempt, but it's the chapter's least
  literally-verified visual element, precisely because there's no
  MATLAB rendering to diff a screenshot against.

## Working conventions (same as the rest of the series)

- Faithful `.m`-to-Python translation via the `build_XXn.py` throwaway-
  script pattern; execute with `nbclient`, confirm 0 errors/0 stderr
  warnings, visually spot-check every figure before finalizing.
- Missing custom toolbox functions get reimplemented transparently with
  an explicit derivation/provenance caveat in the notebook markdown —
  and where a script's behavior depends on ambiguous data-file column
  mapping (as in `11e`/`11i`), the exact source `.m` is read directly
  before building rather than inferred from a survey summary alone.
- Near-duplicate/parametrized-variant scripts get collapsed into one
  shared Python helper function called multiple times, rather than
  rebuilt as independent code blocks — this chapter has an unusually
  high rate of lettered a/b/c/d/e variants that differ in only one or
  two parameters (bounds, ranking statistic, y-axis scaling).
- Missing/unreadable data dependencies get explicitly flagged rather
  than faked with synthetic data — this chapter's blocker list (25
  scripts) is larger than any prior chapter's, entirely traceable to
  one missing stock-level dataset (`chap11_MSCI_World`) plus a handful
  of missing `.mat` checkpoints with no fallback.
- Never run git directly — hand exact `git add`/`commit`/`push`
  commands to the user.
- Confirm the archive's actual file list directly before finalizing a
  script-count table (already done here: 77 confirmed via `find`).
