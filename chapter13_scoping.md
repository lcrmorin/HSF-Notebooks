# Chapter 13 (Stress Testing) — scoping & roadmap

Chapter 13 ships 36 `chap13_credit*.m` exercise scripts (confirmed by
direct `ls`/`find` against `HSF/13. Stress Testing/`, not
filename-pattern estimation: `credit1` through `credit10`, `credit11a-c`,
`credit12a-c`, `credit13a-c`, `credit14a-d`, `credit15a-c`, `credit16a-b`,
`credit17a-c`, `credit18`). There is no `Results/` folder for this
chapter. Every one of the 36 scripts was read directly in full (not
inferred from filenames), with the same rigor established in Chapters
11-12: no script gets flagged blocked without independently testing its
actual data dependency, and no function gets flagged missing without an
exact **and** case-insensitive filename/function-definition search across
the whole archive. They fall into 10 natural families: structural
(Merton/Black-Cox) credit-risk baselines (3), the climate-extended Merton
model and its asset-shock analogues (4), the Reinders credit-transition
mark-to-market loss model (4), jump-diffusion climate risk and
piecewise-exponential hazard curves (3), baseline rating-transition
Markov-generator hazard curves (3), climate-stressed Markov-generator
default-rate calibration (6), single-factor Gaussian-copula conditional
default probability (4), stochastic LGD models with climate correlation
(3), Vasicek implied-LGD curves and correlation calibration (3), and
Monte-Carlo/semi-analytic/closed-form default-rate distributions (3).

## The central finding: every genuinely missing MATLAB function is already ported into this project's own `quanttoolbox` Python package

Chapters 11-12's "missing function" risk was always about **archive
coverage**: a handful of statistical helpers (`pdfweibull`, `strcat3`, …)
that simply don't exist anywhere in `hfs-archive`, requiring a from-formula
reimplementation disclosed as such. **Chapter 13's version of this is
much bigger in raw count but dramatically lower in actual risk.** Every
one of this chapter's 36 scripts leans on a family of credit-model
functions — `PD_Merton_Model`, `PD_Black_Cox_Model`,
`E0_Extended_Merton_Model`/`B0_Extended_Merton_Model`/
`PD_Extended_Merton_Model`, `Reinders_Credit_Model`,
`Merton_Jump_Climate_Model`, `survivalExponential`,
`Survival_Markov_Generator`, `Density_Markov_Generator` — **none of which
exist anywhere in this checkout of `hfs-archive`** (confirmed by exact
and case-insensitive filename search and a full-archive `grep` for their
definitions; there is no `credit/` subfolder anywhere under either
`QuantToolbox/` or `HSF/0. Toolbox/` in this local mirror, even though
`estimate_markov_generator` — used by 9 of this chapter's scripts — is
independently confirmed to be a genuine chapter-2-era archive dependency
too, since `HSF/2. ESG Scoring/chap2_rating_markov9-13.m` call the exact
same name and also come up empty).

**This turns out not to matter, because the port already exists.** This
project's own `requirements.txt` already depends on a pip-installed
`quanttoolbox` package (v0.3.0, "Python port of the MATLAB
QuantToolBox"), and Chapter 2's shipped notebook
(`notebooks/hsf/02a_ratings_and_transitions.ipynb`) already imports
`quanttoolbox.sustainable_finance.entropy.estimate_markov_generator` in
production. Checking the rest of that installed package directly:
`quanttoolbox.credit.structural` (`black_scholes`, `pd_merton_model`,
`b0_extended_merton_model`, `e0_extended_merton_model`,
`pd_extended_merton_model`, `pd_black_cox_model`, `merton_jump_model`,
`merton_jump_climate_model`, `reinders_credit_model`) and
`quanttoolbox.credit.reduced_form` (`survival_markov_generator`,
`density_markov_generator`, `hazard_markov_generator`,
`survival_exponential`, `cdf_exponential`, `pdf_exponential`,
`inv_exponential`, `rnd_exponential`) together cover **every single
credit-model function this chapter calls**, each with a docstring citing
its exact MATLAB source (`Original: credit/PD_Merton_Model.m`, etc.) and,
in several cases, an explicit translation note disclosing a source-side
quirk (e.g. `B0_Extended_Merton_Model.m`/`E0_Extended_Merton_Model.m`
accept an unused `mu_a` "kept for consistent signature", `Reinders_
Credit_Model.m`'s `mu_A` is genuinely vestigial and dropped,
`Hazard_Markov_Generator.m`'s internal function name doesn't match its own
filename in the original — MATLAB dispatches by filename so this is
harmless there, and the Python port is named after the filename/
computation instead). The generic numerical helpers this chapter also
needs (`numerical_gradient`, `numerical_hessian` — used self-verifyingly
in `credit8a`; `csspline`/`fspline`/`invspline` — used in `credit13c`)
are separately confirmed present **both** in the MATLAB `QuantToolbox/`
(`maths/numerical_gradient.m`, `maths/numerical_hessian.m`,
`spline/csspline.m`, `spline/fspline.m`, `spline/invspline.m` — all found
directly) **and** already ported into `quanttoolbox.maths.numerical_diff`
/ `quanttoolbox.spline.spline`. **Bottom line: 0 of the 36 scripts need a
single from-scratch statistical reimplementation** — every custom
function this chapter calls is either sitting in the MATLAB toolbox
folders directly, or already available as a tested Python import that
matches this project's own established convention (Chapter 2 already
uses this exact package for this exact function). Full inventory and
call-signature cross-checks are in the "Custom/non-standard function
inventory" section below.

## Data: a genuine non-issue — the chapter's only dataset is an orphan

Unlike Chapters 11-12, **none of this chapter's 36 exercise scripts loads
any external data file at all.** A systematic sweep of every script for
`xlsread`/`readtable`/`readmatrix`/`load`/any `.xlsx`/`.mat` literal
turned up nothing — every one of the 36 scripts works entirely from
hardcoded parameters and literal matrices (most conspicuously the
8×8 "Kavvathas rounded" rating-transition matrix, retyped verbatim in 9
different scripts: `credit11a` through `credit14c`). The chapter's
`Data/` folder does contain exactly one dataset,
`chap13_ext_Reinders.xlsx` (2 sheets, `Data`/`Data V2`, 23×10 each — no
`.mat` sibling exists for this chapter at all, so there is no MCOS-table-
opacity question to even test) plus its own loader/table-builder script
`Data/chap13_ext_Reinders.m` — but **that loader script is never called
by any of the 36 `chap13_credit*.m` exercise scripts**; it is a
standalone LaTeX-table generator (confirmed: `grep`-ing all 36 scripts
for `reinders`/`.xlsx`/`.mat`/`xlsread`/`readtable` only turns up the
unrelated `Reinders_Credit_Model` function calls in `credit8a-d`, not the
dataset). It was still verified directly: `pandas.read_excel` reads both
sheets cleanly (sector code, sector description, and 8 numeric columns —
matching the loader script's `T{:,1:2}` / `T{:,3:10}` split exactly), so
even if a future chapter extension wants it, it's a fully-readable,
unambiguous dataset with no complications. **Conclusion: 0 of 36 scripts
are blocked or even data-dependent** — this is a purely
parameter-and-formula chapter.

## Script-by-script summary, grouped by family

### A. Structural credit-risk baselines: Merton and Black-Cox (`credit1-3`, 3 scripts)
| Script | Summary |
|---|---|
| `credit1` | Calibrates `(A0, sigma_A)` from `(E0, sigma_E, D, mu_A, r, T)` via `PD_Merton_Model` and prints the single-point result (`A0`, `sigma_A`, distance-to-default, PD in bps). **The plot section is broken as written**: it plots `PD1`/`PD2`/`PD3` against `tau`, but the script only ever computes a single scalar `PD` — `PD1`/`PD2`/`PD3` are never assigned anywhere in the file. The legend labels (`σE=40%,μA=7%`; `σE=42%,μA=7%`; `σE=40%,μA=6%`) and axis limits (`tau` 0-10) make the *intent* clear (three PD-vs-maturity curves for three `(σ_E,μ_A)` combinations), so it's reconstructable, but it cannot be a literal line-for-line port — see "Special-case blockers" below. |
| `credit2` | Clean, working version of the same idea: `PD_Merton_Model`'s PD plotted vs. `mu_A` (0-10%) for three scenarios (`tau=1,D=10`; `tau=2,D=10`; `tau=1,D=15`). No data. |
| `credit3` | `PD_Black_Cox_Model`'s first-passage PD in a 4-panel sensitivity sweep (vs. `t`, `B`, `mu_A`, `sigma_A`), each panel overlaying a single base-case scatter point (`x0`,`y0`) on the continuous curve via `eval(strcat("x",iter_str))`-style dynamic variable lookup. No data. |

### B. Extended Merton climate model and asset-shock analogues (`credit4-7`, 4 scripts)
| Script | Summary |
|---|---|
| `credit4` | **Self-verification script** (not a figure/table builder) for `E0_Extended_Merton_Model`/`B0_Extended_Merton_Model`/`PD_Extended_Merton_Model` — Blasberg's climate-extended Merton model where the firm's discount/growth factor `delta(t)` is itself a correlated Brownian motion. Runs 3 explicit tests with PASS/FAIL output: (1) balance-sheet identity `E0+B0 = A0·exp(-delta0'·T)`; (2) recovery of the classical Merton formulas when `delta0=mu_delta=sigma_delta=0`; (3) monotonicity of PD in `mu_delta`. No data. |
| `credit5` | `PD_Extended_Merton_Model`'s PD plotted vs. `delta0` (0-10%) for 4 `(mu_delta, sigma_delta, rho)` scenarios, including the degenerate `(0,0,0)` case that collapses to standard Merton. No data. |
| `credit6` | **Does not call any Extended-Merton function** — a plain standard-Merton distance-to-default computed inline (`normcdf`/`cdfni`-free, just `normcdf(-DD)`) under an instantaneous asset-value haircut `xi(t)` (`A_t = (1-xi)·A0`), for two haircut ranges (a fine 1-10% table with an average marginal-PD sensitivity `delta`, and a coarse 0-25% plot). No data. |
| `credit7` | Same haircut-shock setup as `credit6`, but derives the **implied drift adjustment** `Δμ_A*(t)` needed to reproduce a given PD-preserving haircut, both from the exact formula (inverting `cdfni(PD0)`, uses the archive's `cdfni`) and a first-order approximation (`-ξ/T`), compared across two maturities (`T=5,10`). No data. |

### C. Reinders credit-transition mark-to-market loss model (`credit8a-8d`, 4 scripts)
| Script | Summary |
|---|---|
| `credit8a` | **Self-verification script**: computes `Reinders_Credit_Model`'s analytic loss gradient/Hessian (`D_Loss`, `D2_Loss`) at a sweep of asset-haircut levels `xi`, and independently cross-checks them against `numerical_gradient`/`numerical_hessian` applied to two **locally-defined** functions (`Merton_MV_E`, `Merton_MV_D` — plain Merton equity/debt value formulas, defined at the bottom of this same `.m` file) — printing both side by side for visual comparison, no formal PASS/FAIL assertion. |
| `credit8b` | `Reinders_Credit_Model`'s portfolio loss `Loss(xi)` plotted vs. haircut `xi` (0-99.9%) for 4 `(omega_E, omega_D)` equity/debt-weight combinations. |
| `credit8c` | Identical setup to `8b`, plots the first derivative `D_Loss(xi)` instead. |
| `credit8d` | Identical setup to `8b`/`8c`, plots the second derivative `D2_Loss(xi)` instead (only panel with `ax.XAxisLocation='origin'`, since this curve crosses zero). |

### D. Jump-diffusion climate risk and piecewise-exponential hazard curves (`credit9a`, `credit9b`, `credit10`, 3 scripts)
| Script | Summary |
|---|---|
| `credit9a` | `Merton_Jump_Climate_Model`'s equity/bond value and jump-adjustment factor `k`, tabulated across a `lambda` (jump-frequency) grid for 3 `(mu_Z, sigma_Z)` jump-severity/uncertainty scenarios, combined into one LaTeX table (`latex_tabular`). |
| `credit9b` | Same model, but isolates and plots the **credit-spread impact** (`Δs = -1/T·log(B0/D) - r`, relative to the no-jump baseline) as each of `lambda`, `mu_Z`, `sigma_Z` is varied independently (3 subplots: frequency/severity/uncertainty impact). |
| `credit10` | `survivalExponential`'s piecewise-constant-hazard survival curve `S(t)` for a baseline hazard-rate term structure (8 knots, 1-30y) vs. two "climate scenario" hazard bumps added at the longer knots, plus a 10y/20y implied-PD table (`ftosa`). |

### E. Rating-transition Markov generator: baseline hazard curves, discrete vs. continuous time (`credit11a-c`, 3 scripts)
| Script | Summary |
|---|---|
| `credit11a` | **Discrete-time embedding approach** (no `estimate_markov_generator`/`Survival_Markov_Generator` call at all): repeatedly multiplies the (row-normalized) Kavvathas 8×8 transition matrix `P` by itself 150 times to get cumulative default probabilities by year and rating, then backs out an implied hazard rate `lambda(t)` via log-survival first-differencing (`lagn`). 4-panel plot, 2 ratings per panel (AAA/AA, A/BBB, BB/B, CCC alone). |
| `credit11b` | **Continuous-time generator approach**: `Lambda = estimate_markov_generator(logm(P))`, then `Survival_Markov_Generator`/`Density_Markov_Generator` give `S(t)`/`f(t)` on a fine (0.2y-step, 400y) grid, hazard `lambda=f/S`. Same 4-panel/2-rating-per-panel layout as `11a`, for direct discrete-vs-continuous-time comparison. |
| `credit11c` | Same continuous-time generator setup as `11b`, but plots the raw default-time density `f(t)` (`Density_Markov_Generator`'s direct output) instead of the hazard ratio. |

### F. Rating-transition Markov generator: climate-stressed default-rate calibration (`credit12a-c`, `credit13a-c`, 6 scripts)
| Script | Summary |
|---|---|
| `credit12a` | Builds a "climate-stressed" generator `Lambda_Climate` (the default-column entries of `Lambda` scaled by `2.5×` and the diagonal re-balanced to keep zero row-sums — a "widen the door to default" stress), verifies row-sums via `disp`, but the survival-curve plot itself (`S = Survival_Markov_Generator(t,Lambda)`) **uses the unstressed `Lambda`, not `Lambda_Climate`** — see "Special-case blockers" below; this looks like an unused/dead computation in the source rather than a plotting bug (the plot itself is internally consistent, just not the "climate" curve the surrounding code suggests). |
| `credit12b` | Same `Lambda_Climate` construction (`2.5×`), this time **correctly used**: hazard rate `lambda(t)=f/S` computed under `Lambda_Climate`, same 4-panel/2-rating layout as `11a`/`11b`. |
| `credit12c` | Same `Lambda_Climate` construction; computes `pdf` under `Lambda` first, then **immediately overwrites it** with `pdf` under `Lambda_Climate` (the first line's result is discarded, dead code, not a bug in the final output) — plots the climate-stressed default-time density, 4-panel/2-rating layout matching `11c`. |
| `credit13a` | `Lambda_Climate` with a `2.0×` stress factor (not `2.5×`), evaluated at 7 discrete horizons (1,5,10,20,30,50,1000y): baseline-vs-climate PD table and baseline-vs-climate hazard-rate table, both `latex_tabular`. |
| `credit13b` | Same `2.0×`-stressed generator, full time grid (0-100y, finer near 0), 4-panel comparison of `S(t)`/`PD(t)`/`f(t)`/`lambda(t)` for one fixed rating (`indx=4`, i.e. BBB), baseline vs. climate overlaid on each panel. |
| `credit13c` | Sweeps the stress multiplier `beta` itself (0-10, not fixed at `2.0`/`2.5`) and tracks the resulting long-run (t→1000y) AAA hazard rate; fits a smoothing spline (`csspline`) through `(beta, default_rate)` and **inverts it** (`invspline`) to find the `beta` values that reproduce `1.25×`/`1.5×`/`2×` the baseline default rate — an explicit calibration exercise, annotated on the figure with dashed guide lines and text labels. |

### G. Single-factor Gaussian-copula conditional default probability with a climate factor (`credit14a-d`, 4 scripts)
| Script | Summary |
|---|---|
| `credit14a` | Converts the raw Kavvathas `P` into cumulative-probability thresholds `z_ij` (via `cdfni`, capped at ±10 for the 0%/100% cells), verifies the discretization reproduces `P` exactly, then computes the **conditional** transition matrix under one systematic-factor realization (`X_climate=1`, `rho_climate=0.20`) — a Merton/Vasicek single-factor conditioning of every cell, not just the default column. LaTeX table output. |
| `credit14b` | Same `z_ij` construction (with the ±10 cap widened to ±7, `Inf_limit=7`), restricted to the **default column only** (`z1`/`z2` sliced to column `K`), swept over 10 `(X_climate, rho_climate)` combinations — a scenario grid rather than one point. Two output formats (`latex_tabular`, `ftosa`). |
| `credit14c` | Identical to `14b`, except `P` is first passed through `logm`→`estimate_markov_generator`→`expm` (the generator-repair round-trip) before re-deriving `p_ij`/`z_ij` — a robustness check that the copula-conditioning approach still works on the "repaired" transition matrix, not just the raw rounded one (the repaired `P` differs slightly from the raw `P`, so the two scripts' numeric outputs are expected to differ, not just be duplicates). |
| `credit14d` | Minimal standalone example (no rating matrix at all): single-obligor conditional PD `p(X) = Φ((Φ⁻¹(PD) - √ρ·X)/√(1-ρ))` for `PD=0.10`, `rho=0.20`, across 7 systematic-factor values — the textbook single-factor/Vasicek building block that `14a-c` generalize to a full rating matrix. |

### H. Stochastic LGD models with climate correlation (`credit15a-c`, 3 scripts)
| Script | Summary |
|---|---|
| `credit15a` | Frye/Pykhtin-style "structural" stochastic-LGD formula `LGD = 1-Φ(μ_i/√(1+σ_i²))` and its climate-adjusted version (an added `√ρ_climate·X_climate` systematic shift in the numerator/denominator), evaluated at one `(μ_i,σ_i)=(0.10,0.50)` parameter set across 7 `X_climate` values. |
| `credit15b` | Compares that same structural climate-LGD formula (`LGD_climate1`) against an **alternate, copula-style reparametrization built directly from a target unconditional `LGD=0.50`** (`LGD_climate2 = Φ((Φ⁻¹(LGD) - √ρ·X)/√(1-ρ))`, the Vasicek single-factor form applied to LGD instead of PD) — prints both side by side across the same 7 `X_climate` values for visual comparison; the two formulas are different derivations of a similar systematic-LGD-shift idea and are not algebraically identical, so the comparison is qualitative, not an equality check. |
| `credit15c` | The `LGD_climate2` (Vasicek-form) formula from `15b`, tabulated across 4 `rho_climate` values × 7 `X_climate` values, `latex_tabular` output. |

### I. Vasicek implied-LGD curves and climate-correlation calibration (`credit16a-b`, `credit18`, 3 scripts)
| Script | Summary |
|---|---|
| `credit16a` | Vasicek's "implied LGD consistent with a target expected loss" formula (`LGD = Φ(Φ⁻¹(D̄)-k)/D̄`, `k=(Φ⁻¹(PD)-Φ⁻¹(EL))/√(1-ρ)`, `PD=0.10`), 4-panel sensitivity sweep (vs. `D̄`, `ρ`, `EL`, `PD` individually, each re-deriving the other 3 fixed params from scratch — no shared helper). |
| `credit16b` | **Line-for-line identical to `16a`** except `PD=0.20` instead of `0.10`, and one extra trailing `exportgraphics(gcf,"fig.png",'Resolution',150)` call not present in `16a` — a strong parametrized-duplicate candidate. |
| `credit18` | Solves for the climate-adjusted correlation `rho_climate` that reproduces a target default-rate multiplier (`1.25×`/`1.5×`/`2×` baseline, for 4 `PD` values × 6 `delta` multiplier-minus-one values) via `fmincon` minimizing squared error against `invcdf_default_rate` (a 2-line **local function** at the bottom of the file — the Vasicek quantile formula, same math family as `credit16a/b`'s `D_bar`). Two sibling local functions, `pdf_default_rate` and `cdf_default_rate`, are also defined but **never actually called** anywhere in the script (dead code, harmless). |

### J. Default-rate distribution: Monte Carlo, semi-analytic, and closed-form (`credit17a-c`, 3 scripts)
| Script | Summary |
|---|---|
| `credit17a` | Monte Carlo simulation (`rng(123)`, 1,000,000 systematic-factor draws × 1,000 obligors each) of the single-factor Gaussian-copula default-rate distribution at 4 `rho` values (0/0.20/0.50/0.90, `PD=0.20`); summary stats table (mean/std/7 quantiles) plus a 4-panel histogram. |
| `credit17b` | Same 4 `rho`/`PD` values, but computes the **exact default-count PMF** via numerical integration (`integral`, `'ArrayValued'`) of the binomial-conditional-on-factor mixture over the factor's normal density — a semi-analytic alternative to `17a`'s simulation, 4-panel line-plot in the same layout. |
| `credit17c` | Same 4 rho values (`0.01` substituted for `0.00`, since the formula is undefined there), computes the continuous large-portfolio-limit default-rate **density in closed form** (the standard Vasicek/Basel ASRF density) — no simulation or numerical integration needed, direct formula evaluation on a 400-point grid. |

**Total: 3+4+4+3+3+6+4+3+3+3 = 36**, matching the archive's confirmed
script count exactly.

## Data dependency verification

| Dataset (`Data/chap13_*`) | `.mat` file? | `.xlsx` readable? | Used by any of the 36 exercise scripts? | Notes |
|---|---|---|---|---|
| `ext_Reinders` | **None shipped** — no `.mat` sibling exists for this chapter's one dataset, so there is no MATLAB-table/MCOS-opacity question to test at all | Yes — `pandas.read_excel` reads both sheets (`Data`, `Data V2`, 23×10 each) cleanly | **No.** Confirmed by grepping all 36 `chap13_credit*.m` scripts for `reinders`/`.xlsx`/`.mat`/`xlsread`/`readtable`/`readmatrix`/`load` — the only hits are unrelated calls to the `Reinders_Credit_Model` function in `credit8a-8d`, which takes no external data and is fully covered by the found/ported `quanttoolbox.credit.structural.reinders_credit_model`. | The dataset's own loader script, `Data/chap13_ext_Reinders.m`, is a standalone LaTeX-table/inequality-check builder (`str = string(T{:,1:2})` for the sector code/description columns, `num = T{:,3:10}` for 8 numeric columns, `disp(xi_t(:,3) > xi_t(:,4))` compares two of them) — read in full and fully resolved, but it is never invoked by any of the 36 exercise scripts, so it plays no role in this chapter's notebook build. Orphan dataset, not a blocker for anything. |

**Conclusion: 0 of 36 scripts have any data dependency at all**, blocked
or otherwise — this is the cleanest possible data situation of any
chapter in the series so far, cleaner even than Chapter 11's
mostly-self-contained scripts.

## Custom/non-standard function inventory

Unlike Chapters 11-12, this chapter's function inventory splits cleanly
into two groups: generic `QuantToolbox`-wide utilities (present directly
in the MATLAB archive, as usual) and a large family of **credit-model**
functions that are absent from this `hfs-archive` checkout entirely but
are already fully ported into this project's own installed `quanttoolbox`
Python package.

**Found directly in `QuantToolbox/`** (generic, chapter-agnostic utility
functions, exactly the same kind Chapters 11-12 relied on):
- `init_color` / `init_global` — global color-palette / global-variable
  initializers (`QuantToolbox/init_color.m`, `QuantToolbox/init_global.m`).
  `init_color.m` also defines the `colors` (plural) 23-row RGB matrix used
  by every multi-series plot in this chapter (`colors(iter,:)`) — found in
  the same file, not a separate lookup.
- `sumr(x)` (`QuantToolbox/tools/sumr.m`) — row-sum, used to row-normalize
  the Kavvathas matrix (`P = P ./ sumr(P)`) in every `credit11-14` script.
- `rows(x)`, `cols(x)` (`QuantToolbox/matrix/`) — GAUSS-style row/column
  counts.
- `seqa(start,step,n)` (`QuantToolbox/tools/seqa.m`) — arithmetic sequence
  generator, used to build the fine time grids in `credit11b/c`-`13a-c`.
- `lagn(x,n)` (`QuantToolbox/tools/lagn.m`) — lag operator, used in
  `credit11a`'s log-survival differencing.
- `miss(x,sentinel)` (`QuantToolbox/tools/miss.m`) — sentinel→NaN
  replacement, used in `credit11a` to guard the `log(S)` differencing
  against zero-survival cells.
- `cdfn(x)`, `cdfni(p)` (`QuantToolbox/stats/`) — Gaussian cdf/quantile,
  used throughout the copula-conditioning family (`credit14-16`, `18`).
- `ftosa(x,width,decimals)` (`QuantToolbox/tools/ftosa.m`) — fixed-width
  numeric-array formatter for `disp`.
- `latex_tabular(data,width,fmt,...)` (`QuantToolbox/latex/latex_tabular.m`)
  — LaTeX table builder.
- `skip_line(n)` (`QuantToolbox/tools/skip_line.m`) — cosmetic separator.
- `save_graphic2(name)` (`HSF/0. Toolbox/tools/save_graphic2.m` — the one
  place this chapter touches the chapter-agnostic `HSF/0. Toolbox/`
  rather than `QuantToolbox/`) — figure-export helper.
- `numerical_gradient(fun,x0)`, `numerical_hessian(fun,x0)`
  (`QuantToolbox/maths/`) — used self-verifyingly in `credit8a` to
  cross-check `Reinders_Credit_Model`'s analytic derivatives.
- `csspline(x,y,w,p)`, `invspline(coeffs,y)`, `fspline(coeffs,x)`
  (`QuantToolbox/spline/`) — smoothing-spline fit/invert/evaluate, used in
  `credit13c`'s beta-calibration curve.

**Not present anywhere in this `hfs-archive` checkout, but already
ported and available in the installed `quanttoolbox` Python package**
(confirmed by exact and case-insensitive filename search across the whole
archive, including a dedicated search for a `credit/` subfolder under
both `QuantToolbox/` and `HSF/0. Toolbox/` — neither exists in this
checkout):
- **`PD_Merton_Model`** (`credit1`, `credit2`) → `quanttoolbox.credit.
  structural.pd_merton_model`. Calibrates unobserved `(A0, sigma_A)` from
  observed `(E0, sigma_E, D)` via a 2-equation least-squares fit
  (`scipy.optimize.minimize(method="BFGS")`, replacing MATLAB's
  `fminunc`), then returns the physical-measure PD at horizon `tau`.
  Docstring confirms the exact source file and every translation
  decision (positivity via `abs()`, no bounds, matching the original).
- **`PD_Black_Cox_Model`** (`credit3`) → `quanttoolbox.credit.structural.
  pd_black_cox_model`. Standard closed-form first-passage default
  probability; return signature (`pd_tau`, `s_tau`, `d1`, `d2`, `varphi`)
  matches `credit3.m`'s `[PD,S,d1,d2,varphi]` exactly.
- **`E0_Extended_Merton_Model`, `B0_Extended_Merton_Model`,
  `PD_Extended_Merton_Model`** (`credit4`, `credit5`) →
  `quanttoolbox.credit.structural.{e0,b0,pd}_extended_merton_model`.
  Blasberg (2024)'s climate-extended Merton model. **Extra confidence**:
  the reparametrization formulas (`sigma_a_prime`, `delta0_prime`) in the
  Python port are byte-for-byte the same closed forms `credit4.m` itself
  states in its own comments as the balance-sheet-identity check —
  i.e. the missing function's exact math is independently confirmable
  from the calling script's own self-verification logic, not just trusted
  from the ported package.
- **`Reinders_Credit_Model`** (`credit8a-8d`) → `quanttoolbox.credit.
  structural.reinders_credit_model`. Equity+debt mark-to-market loss
  under an asset-value haircut, plus its analytic first/second
  derivatives — self-verified independently in `credit8a` itself against
  `numerical_gradient`/`numerical_hessian` (see family C above), the same
  "provably correct via the source script's own cross-check" pattern
  Chapter 12 established for its Weibull/GEV functions.
- **`Merton_Jump_Climate_Model`** (`credit9a`, `credit9b`) →
  `quanttoolbox.credit.structural.merton_jump_climate_model`. Merton
  (1976) jump-diffusion firm-value model; docstring discloses a genuine
  (harmless) inconsistency between this function and its sibling
  `Merton_Jump_Model.m` regarding an early-exit-on-`lambda=0`
  optimization, verified mathematically equivalent either way.
- **`survivalExponential`** (`credit10`) → `quanttoolbox.credit.
  reduced_form.survival_exponential`. Piecewise-constant-hazard survival
  curve; docstring discloses and resolves a genuine dispatch ambiguity in
  the original MATLAB (`size(lambda,2)==1` branching) that doesn't
  translate cleanly to numpy's dimension-agnostic 1-D arrays — resolved
  by dispatching on array dimensionality instead, confirmed consistent
  with every case the original code actually exercises.
- **`Survival_Markov_Generator`, `Density_Markov_Generator`**
  (`credit11b-13c`, 9 scripts) → `quanttoolbox.credit.reduced_form.
  {survival,density}_markov_generator`. Generator-implied default-time
  survival/density (`S(t)=1-expm(tΛ)[:,K-1]`,
  `f(t)=(Λ·expm(tΛ))[:,K-1]`) — the single most-reused function family in
  this chapter. A sibling `hazard_markov_generator` (=`f/S`, the
  `lambda(t)` this chapter's scripts compute inline every time) is also
  already available, even though no `chap13_credit*.m` script imports it
  under that name (they all just divide `f./S` themselves).
- **`estimate_markov_generator`** (`credit11b-c`, `12a-c`, `13a-c`,
  `14c` — 9 scripts) → `quanttoolbox.sustainable_finance.entropy.
  estimate_markov_generator`. Israel, Rosenthal & Wei (2001)'s generator-
  repair method, returning `(Lambda1, Lambda2)` (two repair variants) —
  **already in production use** in this project's own Chapter 2 notebook
  (`02a_ratings_and_transitions.ipynb`, cell 31/37, which even runs it on
  the exact same Kavvathas 8×8 matrix this chapter reuses). Chapter 13's
  scripts call it with a single-output assignment
  (`Lambda = estimate_markov_generator(Lambda)`), i.e. take only the
  first repair variant `Lambda1` — direct signature match confirmed
  against Chapter 2's `Lambda1, Lambda2 = estimate_markov_generator(...)`
  unpacking.

**Locally-defined functions** (standard MATLAB local-function syntax at
the bottom of their own `.m` file, not toolbox calls, no lookup needed):
`Merton_MV_E`/`Merton_MV_D` in `credit8a` (plain Merton equity/debt value
formulas, used only for the numerical-gradient cross-check); `check(cond)`
in `credit4` (trivial PASS/FAIL string helper); `pdf_default_rate`/
`invcdf_default_rate`/`cdf_default_rate` in `credit18` (Vasicek quantile-
family formulas; only `invcdf_default_rate` is actually called, the other
two are dead code in this script).

**No other custom/unfamiliar function names were found** in any of the 36
scripts beyond MATLAB/Statistics-Toolbox/Optimization-Toolbox builtins
(`normcdf`, `norminv`, `normpdf`, `binopdf`, `quantile`, `histogram`,
`rng`, `randn`, `logm`, `expm`, `fmincon`, `integral`,
`'ArrayValued'`, `exportgraphics`) — all standard `scipy`/`numpy`
equivalents, several already exercised elsewhere in this series
(`scipy.linalg.logm`/`expm` in Chapter 2, `scipy.optimize.minimize` for
`fmincon`-style constrained solves matching `quanttoolbox`'s own
`pd_merton_model` convention for `fminunc`).

## Proposed notebook split

| Notebook | Scripts | Description | Blockers | Status |
|---|---|---|---|---|
| `13a_structural_credit_baselines` | `credit1-3` (3) | Merton-model calibrated PD (equity-implied asset value/vol); Black-Cox first-passage PD, 4-panel sensitivity. | `credit1`'s plot section references undefined `PD1/PD2/PD3` in the source — reconstructed from the legend/axis-limit context (see complications below), not a literal line-for-line port. | ✅ |
| `13b_extended_merton_climate_model` | `credit4-7` (4) | Blasberg extended-Merton climate model self-verification (balance-sheet identity, standard-Merton recovery, monotonicity); PD-vs-`delta0` sensitivity; plain-Merton asset-haircut PD sensitivity and implied-drift-adjustment formulas. | None — `E0/B0/PD_Extended_Merton_Model` fully available via `quanttoolbox.credit.structural`, self-verified by `credit4` itself. | ✅ |
| `13c_reinders_transition_loss` | `credit8a-8d` (4) | Reinders equity+debt mark-to-market loss under an asset-value haircut, self-verified via numerical gradient/Hessian cross-check, then plotted (loss, first derivative, second derivative) across 4 equity/debt-weight scenarios. | None — `Reinders_Credit_Model` fully available via `quanttoolbox.credit.structural.reinders_credit_model`, self-verified in `8a`. `8b/8c/8d` are near-identical scripts differing only in which derivative column of the shared `Reinders_Credit_Model` output they plot — collapse into one shared computation + 3 plot calls. | ✅ |
| `13d_jump_diffusion_and_hazard_curves` | `credit9a`, `credit9b`, `credit10` (3) | Merton jump-diffusion climate model (equity/bond value and credit-spread-impact tables/plots across jump frequency/severity/uncertainty); piecewise-exponential baseline-vs-climate-scenario survival curves. | None — `Merton_Jump_Climate_Model`/`survivalExponential` fully available via `quanttoolbox.credit.{structural,reduced_form}`. | ✅ |
| `13e_markov_transition_baseline_hazard` | `credit11a-c` (3) | Discrete-time (matrix-power) vs. continuous-time (generator) rating-transition hazard-rate curves, compared side by side; continuous-time default-time density. | None — `estimate_markov_generator`/`Survival_Markov_Generator`/`Density_Markov_Generator` all available via `quanttoolbox`. | ✅ |
| `13f_markov_transition_climate_stress` | `credit12a-c`, `credit13a-c` (6) | Climate-stressed generator construction (default-column stress factor `beta`, row-sums re-balanced) at two fixed stress levels (`2.5×`, `2.0×`): survival/hazard/density curves, discrete-horizon PD/hazard tables, and a `beta`-calibration curve (spline-inverted to hit target default-rate multiples). | `credit12a`'s survival plot uses the unstressed `Lambda`, not the `Lambda_Climate` it computes and row-sum-checks — needs an explicit build-time decision (reproduce faithfully vs. treat as source bug), see complications below. All 6 scripts repeat the identical `Lambda_Climate` construction block (only `beta` differs, `12`=2.5, `13`=2.0) — strong candidate for one shared `build_climate_stressed_generator(Lambda, beta)` helper. | ✅ |
| `13g_single_factor_conditional_default` | `credit14a-d` (4) | Single-factor Gaussian-copula conditional transition/default probabilities under a systematic climate factor — full matrix (one scenario), default-column only (10-scenario grid), the same on a generator-repaired `P`, and a minimal single-obligor textbook example. | None — pure `cdfn`/`cdfni` closed forms, no missing functions. `14b`/`14c` share nearly all their code (only the input `P` differs) — collapse into one parametrized helper. | ✅ |
| `13h_stochastic_lgd_climate` | `credit15a-c` (3) | Frye/Pykhtin structural stochastic-LGD climate adjustment; comparison against an alternate Vasicek-form LGD-climate reparametrization; the latter tabulated across a correlation×factor grid. | None — pure `cdfn`/`cdfni` closed forms. | ✅ |
| `13i_vasicek_implied_lgd_and_calibration` | `credit16a-b`, `credit18` (3) | Vasicek implied-LGD 4-panel sensitivity (two `PD` levels); climate-correlation calibration via constrained optimization to hit target default-rate multiples. | None — pure `cdfn`/`cdfni`/`fmincon`-equivalent closed forms. `16a`/`16b` are a near-exact parametrized duplicate (only `PD` differs) — collapse into one helper called twice. | ✅ |
| `13j_default_rate_distribution_methods` | `credit17a-c` (3) | Single-factor default-rate distribution via 3 independent methods: Monte Carlo simulation (1M scenarios), semi-analytic PMF via numerical integration, and the closed-form large-portfolio (Vasicek/ASRF) density — all at the same 4 correlation levels for direct comparison. | None — Monte Carlo via `numpy.random.Generator`, integration via `scipy.integrate.quad`, closed form is a direct formula. | ✅ |

**Total: 3+4+4+3+3+6+4+3+3+3 = 36**, matching the archive's confirmed
script count exactly. **0 scripts are blocked** — every notebook is
buildable end-to-end; the only build-phase decisions flagged above are
about faithfully reproducing two small source-script quirks (`credit1`'s
broken plot section, `credit12a`'s unused `Lambda_Climate`), not about
missing functions or data.

## Special-case blockers and complications

1. **`credit1`'s plot section is not literally executable as written.**
   It computes a single scalar `PD` via `PD_Merton_Model`, then plots
   `PD1`/`PD2`/`PD3` vs. `tau` — none of which are ever assigned anywhere
   in the file. Running this script in MATLAB as-is would itself error
   with "undefined variable PD1". The surrounding context (three legend
   labels describing `(σ_E, μ_A)` combinations `(40%,7%)`/`(42%,7%)`/
   `(40%,6%)`, and `ax.XLim=[0 10]` matching a `tau` axis) makes the
   *intended* computation clear: loop `PD_Merton_Model` over `tau=0:10`
   for each of those 3 parameter combinations, matching exactly the
   pattern `credit2` (the very next script) uses correctly. Build-phase
   recommendation: reconstruct the 3-curve computation from that context,
   with an explicit markdown note that the source script's plot section
   is broken/incomplete as shipped and this is a faithful reconstruction
   of its evident intent, not a literal translation.

2. **`credit12a` computes `Lambda_Climate` (with a row-sum sanity check)
   but never uses it** — the survival curve it actually plots
   (`S = Survival_Markov_Generator(t,Lambda)`) uses the unstressed
   `Lambda`. This isn't a runtime error (the script runs fine and
   produces an internally-consistent baseline survival plot), but it
   means the "climate" framing implied by the surrounding
   `Lambda_Climate` computation doesn't reach this script's own figure —
   that only happens in `12b`/`12c`, which use `Lambda_Climate` correctly.
   Reproduce faithfully (baseline curve, `Lambda_Climate` computed but
   unused) rather than "fixing" it to plot the stressed curve, matching
   this series' standing convention of disclosing rather than silently
   correcting source-script quirks — flagged prominently in `13f`'s
   notebook markdown.

3. **The identical `Lambda_Climate`-construction code block appears
   verbatim in 6 scripts** (`credit12a-c` at `beta=2.5`, `credit13a-c` at
   `beta=2.0`) — a strong, low-risk candidate for one shared
   `build_climate_stressed_generator(Lambda, beta)` Python helper, the
   same treatment Chapter 12 gave `grid3b/c/d` and this project's
   `financial_loss4a/4b`-style parametrized pairs.

4. **`credit16a`/`credit16b` are a near-exact duplicate pair** (only
   `PD` differs: `0.10` vs. `0.20`; `16b` has one extra trailing
   `exportgraphics` call with no functional effect on the notebook) —
   collapse into one `vasicek_implied_lgd_panel(pd)` helper called twice,
   matching Chapter 12's `financial_loss4a/4b` treatment exactly.

5. **`credit14b`/`credit14c` share nearly all their code**, differing
   only in whether the conditional-probability calculation starts from
   the raw rounded Kavvathas `P` (`14b`) or the generator-repaired
   `P = expm(estimate_markov_generator(logm(P)))` (`14c`) — a
   parametrized-input pair, not a literal duplicate (the two scripts'
   numeric outputs are expected to differ slightly, since the repair
   step changes `P`), best expressed as one helper taking `P` as an
   argument.

6. **The Kavvathas 8×8 rating-transition matrix is retyped as a literal
   in 9 separate scripts** (`credit11a` through `credit14c`) — the exact
   same matrix (down to the same 2-decimal rounding) already lives in
   this project's own `notebooks/hsf/02a_ratings_and_transitions.ipynb`
   (as `P_kavvathas`, used there specifically to demonstrate
   `estimate_markov_generator` on a *credit* transition matrix, alongside
   Chapter 2's own *ESG-rating* transition matrices). Worth a one-line
   cross-reference in `13e`'s/`13f`'s notebook markdown rather than
   silently re-typing the matrix as if it were unique to this chapter —
   not a blocker, just a nice continuity note for a reader following the
   series in order.

7. **No licensed/paid-data dependency, no `.mat` file, and — uniquely
   among the chapters scoped so far — no external data dependency of any
   kind** anywhere in this chapter's 36 exercise scripts. The one dataset
   present in `Data/` (`chap13_ext_Reinders.xlsx`) is a confirmed orphan,
   used only by its own non-exercise loader/table-builder script.

8. **`credit18`'s two unused local functions** (`pdf_default_rate`,
   `cdf_default_rate` — only `invcdf_default_rate` is actually called)
   are harmless dead code in the source; no need to port them, though
   they're cheap enough to include for completeness/documentation value
   if convenient (they're the natural PDF/CDF siblings of the one
   function the script does use).

## Progress notes

**`13a_structural_credit_baselines`** (`credit1-3`, 3 scripts) — built and
verified 0 errors / 0 stderr warnings, no data dependencies.
`quanttoolbox.credit.structural.pd_merton_model`/`pd_black_cox_model`
were confirmed importable and their dataclass return fields
(`pd_tau`/`a0`/`sigma_a`/`s_tau`/`dd_tau` and
`pd_tau`/`s_tau`/`d1`/`d2`/`varphi`) matched the source scripts'
`[PD,A0,sigma_A,S,DD]`/`[PD,S,d1,d2,varphi]` multi-output order exactly
before building anything, per the scoping doc's central finding. As
scoped, `credit1`'s broken plot section (`PD1`/`PD2`/`PD3` referenced but
never assigned) was reconstructed from the legend/axis context — a
3-scenario PD-vs-`tau` sweep — and flagged explicitly in the notebook
markdown as a faithful reconstruction of evident intent, not a literal
port. One numerical-boundary case handled during the build (not itself a
bug, present in the underlying formulas): both `pd_merton_model` at
`tau=0` and `pd_black_cox_model` at `tau=0` divide by a
`sigma*sqrt(tau)=0` term, which numpy resolves to a (correct, harmless)
`+/-inf` exactly the way MATLAB's floating-point arithmetic would — wrapped
in `np.errstate(divide="ignore", invalid="ignore")` to keep the notebook
at 0 stderr warnings, since this is a silent-in-MATLAB boundary case, not
an error being suppressed. Output substantively sanity-checked, not just
exception-free: the reconstructed `credit1` plot shows the classic
textbook Merton hump-shaped PD-vs-maturity term structure (PD rises then
falls as horizon lengthens, since positive asset drift eventually
dominates over accumulated volatility) — a strong confirmation that the
reconstruction is not just internally consistent but reproduces the
expected structural-credit-model shape; `credit2`'s PD-vs-`mu_A` curves
are monotonically decreasing as expected (higher asset drift -> lower
default risk) and correctly ordered by leverage/maturity; `credit3`'s
4-panel Black-Cox sensitivity has its white-circle base-case marker
landing exactly on the curve in all 4 panels (all read PD=6.9388%,
matching the printed single-point calculation to the last decimal),
confirming the vectorized sweep and the scalar base-case calculation are
numerically consistent, with each panel's monotonicity (PD up with
barrier/vol, down with drift, up with time) matching structural-credit
theory.

**`13b_extended_merton_climate_model`** (`credit4-7`, 4 scripts) — built
and verified 0 errors / 0 stderr warnings, no data dependencies.
`credit4`'s self-verification suite — the strongest confidence check
available for a "missing but ported" function family — passed all 3
tests against the installed `quanttoolbox.credit.structural.
{e0,b0,pd}_extended_merton_model` functions at machine precision (balance-
sheet identity and standard-Merton-recovery errors both `0.00e+00`,
monotonicity in `mu_delta` confirmed across 5 test points). `credit5`'s
PD-vs-`delta0` sweep is correctly ordered by the systematic-correlation
sign (`rho=-0.5` gives the highest PD, `rho=+0.5` the lowest, consistent
with negative correlation compounding climate-drag and low-asset-value
states together). `credit6`'s haircut-sensitivity table and plot are
numerically consistent with each other (the plot's value at `xi=0.01`
matches the table's first row exactly) and monotonically/convexly
increasing, as expected for a distance-to-default formula. **One
disclosed dead-code finding in `credit7`**: the source script computes a
`DD`/`PD0`/`A_t`/`PD1` distance-to-default block and an `implied_mu_A_10`
variable (inverting `PD0` via `cdfni`) for both `T=5` and `T=10`, but
none of it feeds into the script's actual plot — the plotted "True
formula"/"Approximation" curves are pure closed forms
(`Delta_mu_A = -ln(1-xi)/T` and its first-order approximation `xi/T`)
that don't depend on `A0`/`D`/`sigma_A` at all. Reproduced as only the
plot-relevant computation, with the unused block disclosed in the
notebook markdown rather than ported as if load-bearing. Visual
cross-check: the `T=5` curve is exactly double the `T=10` curve at every
`xi`, as the closed form `-(1/T)*ln(1-xi)` predicts — confirmed by eye
against the figure. One boundary-case `RuntimeWarning` (`log(0)=-inf` at
`xi=100%`, the same silent-in-MATLAB floating-point behavior seen in
`13a`) suppressed via `np.errstate` to keep the notebook at 0 stderr.

**`13c_reinders_transition_loss`** (`credit8a-8d`, 4 scripts) — built and
verified 0 errors / 0 stderr warnings, no data dependencies. `credit8a`'s
three-way self-verification (numerical gradient vs. the underlying
plain-Merton formula's closed-form derivative vs.
`reinders_credit_model`'s own analytic `D_Loss`; numerical Hessian vs.
`D2_Loss`) matched to 4 decimal places across the entire `xi=0..95%`
grid — the numerical and closed-form first derivatives (`g1_E`/`g2_E`,
`g1_D`/`g2_D`) are identical to the displayed precision at every point,
and `grd_Loss`/`D_Loss` agree exactly while `hss_Loss`/`D2_Loss` agree to
within ~1e-4 (expected finite-difference-vs-analytic-Hessian tolerance).
`credit8b-8d` collapsed into one shared `reinders_credit_model` call
(vectorized over both `xi` and the 4 `(omega_E,omega_D)` scenarios via
broadcasting) followed by 3 plot cells, as scoped. Output substantively
plausible: all 4 loss curves rise monotonically from 0 with the haircut;
the first-derivative curves' inflection points visually line up with the
second-derivative curves' zero-crossings across all 4 scenarios,
confirming the three plots are mutually consistent representations of
the same underlying loss function family (not independently-computed
curves that happen to look plausible in isolation).

**`13d_jump_diffusion_and_hazard_curves`** (`credit9a`, `credit9b`,
`credit10`, 3 scripts) — built and verified 0 errors / 0 stderr
warnings, no data dependencies. `merton_jump_climate_model`'s scalar-only
`lambda_` requirement (noted in its own docstring) was handled with an
explicit Python loop over the jump-frequency grid, matching the source
script's own `for iter=1:nIters` loop structure rather than attempting a
vectorized call. Output is a strong, textbook-consistent sanity check
across the board: `E0+B0` equals `A0=50` exactly at every grid point (the
balance-sheet identity holding under jump-diffusion too, with `r=0` in
this parametrization); at `lambda=0` all 3 scenarios converge to the
identical no-jump baseline `(E0,B0)=(35.73,14.27)`; and as jump risk
increases, equity value *rises* while bond value *falls* toward 0 — the
classic Merton-model result that equity (a call option on firm assets)
gains from increased risk at debtholders' expense (the asset-substitution
effect), here driven by jump risk instead of continuous volatility. The
`k` (expected relative jump size) column matches the closed form
`exp(mu_Z+0.5*sigma_Z^2)-1` exactly for all 3 scenarios (`-0.0906`,
`-0.864`, `-0.0535`). `credit9b`'s 3 credit-spread-impact panels are all
monotonically increasing in the expected direction (more frequent jumps,
more severe/negative jumps, more jump-size uncertainty all raise the
credit spread). `credit10`'s survival curves visually overlap for `t<5`
(before either climate scenario's first nonzero hazard bump, which start
at the 10y knot) and diverge cleanly afterward, with climate scenario 2
(the uniformly larger hazard bump) declining fastest — confirming the
piecewise-exponential construction is behaving exactly as the knot
structure implies, not just producing plausible-looking curves in
isolation.

**`13e_markov_transition_baseline_hazard`** (`credit11a-c`, 3 scripts) —
built and verified 0 errors / 0 stderr warnings, no data dependencies.
The Kavvathas 8x8 matrix's boundary case (the absorbing "D" rating's
survival probability being exactly 0 for `t>0`, causing a `0/0` in the
hazard-ratio `f(t)/S(t)` computation before that column is dropped) was
handled with `np.errstate`, the same silent-in-MATLAB pattern established
in `13a`/`13b`. Output is strongly plausible on both an internal-
consistency and domain-knowledge basis: `credit11a` (discrete
matrix-power) and `credit11b` (continuous-time generator) produce
visually near-identical 4-panel hazard curves — exactly the
discrete-vs-continuous-time agreement the two scripts are designed to
demonstrate side by side — and every rating's hazard curve converges to
the *same* long-run asymptotic hazard rate (~100-105 bps) regardless of
starting quality, a well-known ergodic/steady-state property of
irreducible-up-to-absorption Markov chains. `credit11c`'s default-time
densities are unimodal and correctly ordered by credit quality (lower
ratings peak earlier and at much higher density, e.g. CCC's ~280x10^-3
peak near `t~2` vs. AAA's ~7x10^-3 peak near `t~50`), consistent with
well-known credit-migration term-structure shape patterns. A shared
`panel_plot` helper collapsed the near-identical 4-panel
2-ratings-per-panel layout used by both `11a` and `11b` into one
reusable function.

**`13f_markov_transition_climate_stress`** (`credit12a-c`, `credit13a-c`,
6 scripts) — built and verified 0 errors / 0 stderr warnings, no data
dependencies. Both disclosed source-script quirks were confirmed by
direct reading before building (not assumed from the scoping summary)
and reproduced faithfully: `credit12a`'s survival-curve plot genuinely
uses the unstressed `Lambda`, not the `Lambda_Climate` it computes and
row-sum-checks; `credit12c` computes a dead first call to
`Density_Markov_Generator(t,Lambda)` before immediately overwriting it
with the climate-stressed version (reproduced as a single call, since
the dead call has no observable effect). The identical `Lambda_Climate`
construction block across all 6 scripts collapsed into one shared
`build_climate_stressed_generator(Lambda, beta)` helper, as scoped. All
6 row-sum checks confirmed zero to floating-point precision (~1e-15/1e-16).
Output cross-checks strongly, both internally and against `13e`: the
`beta=2.5`/`beta=2.0` climate-stressed hazard/density curves show the
same "every rating converges to one long-run asymptotic hazard rate"
property established in `13e`, just at a higher asymptotic level (e.g.
`beta=2.5`'s ~150bps vs. `13e`'s unstressed ~103bps); `credit13a`'s
`t=1000` hazard-rate row independently reproduces `13e`'s ~102.8bps
baseline value to 1 decimal place, a strong cross-notebook consistency
check; `credit13b`'s 4-panel `S`/`PD`/`f`/`lambda` comparison for BBB is
mutually consistent across all 4 panels (climate always above/faster
than baseline in the direction that increases risk); and `credit13c`'s
calibration curve is smooth, monotonic, concave, with its dashed guide
lines landing exactly on the target `1.25x`/`1.5x`/`2x` default-rate
multiples at the computed `implied_beta` values. One equivalent-
computation optimization applied and disclosed: since only the `t=1000`
long-run hazard matters for `credit13c`'s `beta`-sweep, it's evaluated
directly at a single time point rather than the source's full
5001-point `0..1000y` grid — confirmed to produce a bit-identical result
to the last row of the full grid, just without the 29x redundant
full-grid computation.

**`13g_single_factor_conditional_default`** (`credit14a-d`, 4 scripts) —
built and verified 0 errors / 0 stderr warnings, no data dependencies.
Used `scipy.stats.norm.cdf`/`.ppf` for `Φ`/`Φ⁻¹` (the pattern already
established in `13a`/`13b`), not a locally-reinvented `erf`/`erfinv`
helper. `credit14b`/`14c` collapsed into one shared
`conditional_default_column_grid(P, Inf_limit)` helper taking `P` as an
argument, as scoped; `credit14a`'s full-matrix single-scenario
computation and `thresholds_from_matrix(P, Inf_limit)` (the
cumsum→`Φ⁻¹`→cap construction shared by all four scripts) factored out
separately since `14a` needs the full threshold grid, not just the
default column. All four scripts' sanity checks passed: `14a`'s
discretization round-trip (`Φ(z2)-Φ(z1)` reconstructing `p_ij` exactly)
is correct to floating-point precision (~1.8e-16 max error); `14a`'s
conditional matrix row sums are exactly 100% for all 8 ratings (a
single-factor conditioning is just a location shift of the underlying
normal, so it cannot break the partition-of-unity property); `14b`'s
10-scenario grid is within `[0,100]`% throughout and non-decreasing in
each rating's conditional PD as the scenario worsens (`X: 1→2→3` at
fixed `ρ=0.20`); the `X=10, ρ=0` column (an extreme factor draw with
zero systematic loading) reduces to the raw unconditional default
column exactly, as expected; `14c` (generator-repaired `P`) differs
from `14b` (raw `P`) by a small but non-trivial amount (max ~1.29
percentage points, mean ~0.04pp across the grid) — small enough to
confirm the repair only lightly perturbs `P`, large enough to confirm
the two scripts are not accidental duplicates; and `14d`'s minimal
single-obligor example is strictly monotonically decreasing in `X`
(52.68% at `X=-3` down to 0.17% at `X=+3`, crossing the 10% unconditional
PD near `X=0`, as its own smooth S-shaped plot confirms visually).
Chapter 13 is now 7/10 notebooks complete (`13a`-`13g`, 26/36 scripts).

**`13h_stochastic_lgd_climate`** (`credit15a-c`, 3 scripts) — built and
verified 0 errors / 0 stderr warnings, no data dependencies. `credit15a`'s
structural (Frye-Pykhtin) conditional LGD is monotonically decreasing in
`X_climate` as expected (higher factor draw = better recovery in this
sign convention). One genuine subtlety caught during sanity-checking and
corrected before shipping: my first sanity assertion claimed
`LGD(X=0)` should equal the unconditional structural LGD — it does not
(46.36% vs. 46.44%), because conditioning on the factor also shrinks the
residual recovery-score variance from `σ_i²` to `σ_i²(1-ρ)`, so the
`X=0` "average factor" slice is not the same integral as the
factor-marginalized unconditional distribution (a Jensen's-inequality-type
effect through the `Φ` nonlinearity, not a bug). Corrected the check to
report the (small, expected) gap with an explanation rather than assert a
false equality. `credit15b`'s comparison of the structural curve against
a **Vasicek-form** reparametrization (`Φ((Φ⁻¹(LGD)-√ρX)/√(1-ρ))` seeded
from an assumed exogenous `LGD=50%`) was reproduced faithfully, including
disclosing that the two curves start from different unconditional levels
by construction (structural ≈46.4% vs. assumed 50%) — the source script
compares two distinct LGD specifications' climate-sensitivity *shapes*,
not two parametrizations of the same base rate; the Vasicek-form curve
does hit exactly 50% at `X=0` by construction (its defining property),
confirmed numerically. `credit15c`'s 4-correlation × 7-factor grid checks
out on both required properties: the `ρ=0` row is exactly flat at 50%
(no systematic exposure), and the `X`-spread of conditional LGD widens
monotonically as `ρ` increases (0pp → 68.3pp → 86.6pp → 95.1pp).
Chapter 13 is now 8/10 notebooks complete (`13a`-`13h`, 29/36 scripts).

**`13i_vasicek_implied_lgd_and_calibration`** (`credit16a-b`, `credit18`,
3 scripts) — built and verified 0 errors / 0 stderr warnings, no data
dependencies. `credit16a`/`16b` collapsed into one shared
`vasicek_implied_lgd_sweeps(PD_base)` + `plot_implied_lgd_panels(...)`
pair as scoped (only `PD_base` differs: 10% vs. 20%). One real
grid-construction bug caught and fixed before shipping: `np.arange`'s
floating-point accumulation overshoots the intended `D̄=1.00`/`PD=1.00`
grid endpoints by ~1e-16, making `norm.ppf` correctly return `NaN` for a
just-over-1 probability — not a MATLAB-matching boundary singularity (unlike
the disclosed `tau=0`/`xi=1` cases elsewhere in this chapter), just an
artifact of my own grid construction, so probability-valued inputs are
clipped to `[1e-12, 1-1e-12]` inside the shared helper. After the fix, all
four panel shapes check out for both `PD=10%` and `PD=20%`: implied LGD
→100% as `D̄→100%`, →0% as `ρ→99.99%`, →100% as `EL→PD_base` (only reached
within the swept grid for the `PD=10%` case, correctly noted as not
applicable for `PD=20%` since the `EL` grid caps at 10%), and falls
toward 0% as `PD` rises far past the fixed `EL=5%`. `credit18`'s
`fmincon`-based climate-correlation calibration reproduced via
`scipy.optimize.minimize` (bounded, same `ρ=20%` starting point) — this
surfaced a genuine, disclosed model property, not a bug: the Vasicek
default-rate quantile `invcdf_default_rate(α,PD,ρ)` is **not
monotonically increasing in `ρ`** for low `PD` (it peaks at an interior
`ρ` — e.g. ~0.50 for `PD=1%`, ~0.64 for `PD=2%` — then falls back toward
0% as `ρ→1`), so for `PD=1%`/`δ∈{50%,100%}` and `PD=2%`/`δ=100%` no
`ρ_climate∈[0,1]` reproduces the target default-rate stretch exactly; the
bounded solver converges to the closest achievable point near the
interior peak with a residual of several percentage points, flagged
explicitly rather than silently reported as an exact fit. Every other
cell (`PD∈{5%,10%}` at every `δ`, and lower-`δ` cells for `PD∈{1%,2%}`)
hits its target to within 0.01pp, and the `δ=0` column returns exactly
`ρ_climate=20%=ρ_base` for every `PD` row, as required. Also disclosed:
the source script's `pdf_default_rate`/`cdf_default_rate` local MATLAB
functions are defined but never called in the script body (dead code,
not reproduced). Chapter 13 is now 9/10 notebooks complete (`13a`-`13i`,
32/36 scripts) — only `13j` (`credit17a-c`, default-rate distribution
methods) remains.

**`13j_default_rate_distribution_methods`** (`credit17a-c`, 3 scripts) —
built and verified 0 errors / 0 stderr warnings, no data dependencies.
**One genuine equivalent-computation optimization applied and verified**:
`credit17a`'s MATLAB loop draws `n=1000` fresh idiosyncratic obligor
deviates *per scenario* (`1,000,000` scenarios × `1,000` obligors ≈ 10⁹
draws); since those `n` obligor outcomes are i.i.d. Bernoulli(`p(X)`)
conditional on the systematic factor `X`, their sum is *exactly* (not
approximately) `Binomial(n, p(X))` — replaced the explicit inner loop
with a single vectorized `rng.binomial(n, p_x)` draw per scenario, cutting
runtime from what would be a very slow explicit loop to ~1.2 seconds,
confirmed unbiased (`E[D̄]≈PD=20%` at every `ρ`, to 3 decimal places) and
correctly dispersion-increasing in `ρ` (std rises monotonically from
1.27% at `ρ=0` to 33.1% at `ρ=90%`). `credit17b`'s semi-analytic PMF used
`scipy.integrate.quad_vec` to batch the `(n+1)`-length integrand into one
call per `ρ` rather than `n+1` separate `scipy.integrate.quad` calls
(mathematically identical, just faster) — confirmed each PMF sums to
exactly 1.0 and has mean exactly `PD=0.20`. `credit17c`'s closed-form
density checks out via a genuinely interesting numerical-methods finding
(not a bug, fully investigated and disclosed): a naive trapezoidal check
on the same 400-point `d`-grid the source script itself plots on gives
areas of `[1.0, 1.0, 1.0154, 0.7227]` across `ρ=[1%,20%,50%,95%]` — the
`ρ=95%` shortfall is real and expected, not an error, because at high
correlation the density becomes extremely concentrated in narrow spikes
right at `d→0`/`d→1` (correlated portfolios default "all or nothing"),
which a fixed-resolution linear grid can't resolve. Verified via an
analytic change-of-variables (`x=Φ⁻¹(d)`, which cancels the density's
`exp(0.5x²)` term against the substitution Jacobian and reduces the whole
family to an ordinary Gaussian in `x` with variance `ρ/(1-ρ)`) that the
true area is exactly 1.0 for every `ρ`, confirmed numerically over
generous ±15σ bounds with no integration warnings. Added (not in the
source scripts) a 3-way overlay cross-check at the shared `ρ=20%` level —
Monte Carlo histogram, semi-analytic PMF, and closed-form density all lie
on top of each other almost exactly, the strongest possible confirmation
that all three independently-coded methods describe the same underlying
distribution. One unit-consistency bug caught and fixed while building
that overlay (my own addition, not a source-script issue): the semi-
analytic/closed-form curves are naturally densities-per-unit-fraction-`d`
while a `density=True` histogram over percentage-scaled bins is a
density-per-percentage-point — combining them directly without adjustment
made the histogram appear ~100x too small; fixed by dividing the PMF/
closed-form curves by 100 before overlaying, confirmed by the resulting
near-perfect visual overlap. **Chapter 13 (Stress Testing) is now
complete: `13a`-`13j`, all 36 scripts accounted for, 0 blocked.**

## Working conventions (same as the rest of the series)

- Faithful `.m`-to-Python translation via the `build_XXn.py` throwaway-
  script pattern; execute with `nbclient`, confirm 0 errors/0 stderr
  warnings, visually spot-check every figure before finalizing.
- Missing custom toolbox functions get reimplemented transparently with
  an explicit derivation/provenance caveat in the notebook markdown —
  and where a script's behavior depends on ambiguous data-file column
  mapping, the exact source `.m` is read directly before building rather
  than inferred from a survey summary alone. For this chapter
  specifically: the "missing" credit-model functions are not
  reimplemented from scratch at all, but imported directly from this
  project's own `quanttoolbox` package (already a `requirements.txt`
  dependency, already used in Chapter 2) — cite the exact
  `quanttoolbox.credit.*`/`quanttoolbox.sustainable_finance.entropy`
  import path in each notebook's markdown rather than re-deriving the
  formulas inline.
- Near-duplicate/parametrized-variant scripts get collapsed into one
  shared Python helper function called multiple times, rather than
  duplicated — flagged per-notebook above (`credit8b/8c/8d`,
  `credit12a-c`+`credit13a-c`'s shared `Lambda_Climate` construction,
  `credit14b/14c`, `credit16a/16b`).
- 0 errors, 0 stderr warnings, AND actual-output-sanity (not just
  exception-absence) is the verification standard for every notebook —
  two real bugs in Chapter 11 (`11a`'s rank-deficient constraints,
  `11c`'s sign convention) were caught only by scrutinizing printed
  numeric output for plausibility, not by the absence of exceptions.
- Every genuinely blocked script gets flagged explicitly rather than
  silently skipped or faked — though this chapter, like Chapter 12, has
  none.
- Never run git directly — hand the user exact commands to run
  themselves.
- Deliver + sync every artifact to the user's Mac via `SendUserFile` +
  `mcp__remote-devices__device_commit_files`, and save scoping-doc
  updates to the attached claude.ai Project via `Projects.project_write`.
