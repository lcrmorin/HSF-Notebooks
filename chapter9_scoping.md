# Chapter 9 (Risk Measures) — scoping & roadmap

Despite the book's chapter title, Chapter 9 is entirely carbon-accounting
and climate-transition-metric content — not financial VaR/ES-style risk
measures. It ships 52 scripts, all under a `chap9_*` prefix, plus 2
`Data/*.m` prep scripts. It's being built as a lettered sequence of
notebooks (`09a`-`09g`), the same pattern as Chapter 5's biodiversity
case study and Chapter 8 Part 1.

Scoped by reading `chap9_carbon_budget1.m`-`carbon_budget7.m` directly and
using a dedicated Explore subagent to survey the remaining ~45 scripts by
group, to preserve context budget without sacrificing fidelity on the
functions actually being reimplemented.

## Planned notebook split

| Notebook | Scripts | Topic | Status |
|---|---|---|---|
| `09a_carbon_budget_accounting` | `carbon_budget1-7` (7) | First-principles carbon-budget accounting: past/expected/net-positive/net-negative budgets, three closed-form emission-reduction models (linear/compound/exponential decline) cross-checked against numerical integration, piecewise-linear multi-period budgets with sub-period additivity, probability-weighted warming-threshold budgets, and sector/global emissions-scenario milestone-year budget tables. No data dependency. | ✅ |
| `09b_ghg_protocol_worked_examples` | `scope1-5`, `scope10-11` (7, `scope7` skipped as a byte-identical duplicate of `scope5`) | GHG Protocol Scope 1/2/3 worked-example accounting: disclosure-share ratios, location-based Scope 2 calculation, spend-based Scope 3 activity estimation, real EU grid emission-factor time series (`chap9_EF_scope2_LB1.xlsx`, only `scope4` produces a figure), country-level allocation-based emissions, a real CDP panel comparing location- vs market-based Scope 2 reporting (`chap9_CDP2.xlsx`), and a PCAF-style financed-emissions/EVIC worked example. **Correction from the original subagent scope:** the archive contains only `scope1-5`, `scope7`, `scope10`, `scope11` (8 scripts, not 11) — `scope6`, `8`, `9`, `12` do not exist in the shipped archive. | ✅ |
| `09c_sector_carbon_intensity_trucost_msci` | `ci1` buildable (1); `ci2`, `ci4`, `ce1`, `ce1a`, `ce1b`, `ce1c`, `ce2`, `ce3` blocked (8) | Sector/portfolio carbon-intensity metrics. **Correction from the original subagent scope:** the archive contains `ci1`, `ci2`, `ci4` (3, not `ci1-9`) plus a previously-missed `carbon_ce*` group (`ce1`, `ce1a`, `ce1b`, `ce1c`, `ce2`, `ce3` — 6 more scripts, GICS-sector-level Scope 1/2/3 carbon-emissions breakdowns) discovered only once the archive's full file list was checked directly rather than inferred from filename patterns. All of `ci2`, `ci4`, and every `ce*` script depend on the same missing proprietary `Trucost_Data1_2019` dataset — flagged explicitly, not built. `ci1` (self-contained: portfolio carbon intensity via dollar-weighted WACI-style blending vs. a naive weighted-average of company-level intensities) is built as a thin single-section notebook. | ✅ (partial — 1 of 9 scripts, 8 blocked) |
| `09d_gwp_radiative_forcing` | `gwp1`, `gwp2a-f` (7, `gwp2f` folded into `gwp2a`'s section as a second panel) | Global Warming Potential and radiative-forcing physics, all self-contained (no data dependency): mass-based GWP-weighted emissions aggregation, the Bern-model CO2/CH4 atmospheric decay curves (100-year and 5000-year horizons), decay-rate densities, AGWP(t) cumulative-forcing integrals, and the GWP(t) horizon curve — reproduces the standard GWP-100(CH4)=28.39 (AR5) value exactly as a numerical check. **Correction:** the archive has only one `gwp1` script (not `gwp1a-c`) plus `gwp2a-f` (6, not `gwp2a-e`). | ✅ |
| `09e_emission_trend_forecasting` | `trend1-6` (6) | Emission-trend forecasting: linear/log-linear OLS trend extrapolation (4 sections), a compound-growth reference table, and a state-space local-linear-trend model estimated by Whittle likelihood and Kalman-filtered. **Correction:** the archive has no `chap9_ects*` scripts at all — the actual script family is `chap9_carbon_trend1-6.m` (matches the original count of 6 by coincidence). The needed Kalman/state-space toolkit turned out to already exist in the real `quanttoolbox` PyPI package (`quanttoolbox.econometrics.kalman`, `quanttoolbox.econometrics.whittle`) — it just wasn't installed in this session's fresh container (`pip install quanttoolbox --break-system-packages`); see `SESSION_HANDOFF.md`. The Whittle optimization doesn't fully converge on this series' 14 observations (flagged transparently in the notebook, not hidden) but the point estimates and resulting Kalman-filtered slope are still usable. | ✅ |
| `09f_transition_pathways_pac_scoring` | `pac1-5` (5) + 3 orphaned self-contained scripts (`carbon_offsetting2`, `consolidation1`, `greenness_grs1`) folded in as addenda | Climate Action Tracker / PAC-style national transition-pathway scoring: sector emission-reduction since a 2020 baseline, trend-vs-target-vs-NZE-scenario comparison, carbon budgets under each pathway (reuses `09a`'s `carbon_budget_piecewise`, now 🟡), and simplified participation/ambition/credibility score trajectories plus archetype radar profiles (disclosed simplification — the source's `pac4`/`pac5` are highly idiosyncratic hand-tuned spline/polar diagrams not worth porting pixel-for-pixel; see the notebook's top-of-file note). Plus 3 small addenda scripts with no natural home elsewhere: annual carbon-offset market volumes, GHG consolidation-approach worked example (equity share/financial control/operational control), and a Green Revenue Share worked example. **Correction:** `pac1-5` (5 scripts) matched the original estimate, but the 3 addenda scripts were missed entirely by the original subagent scope. | ✅ |
| `09g_cdp_netzero_tracking` | `tale1-3` buildable (3); `tale4-5` blocked (2) | CDP-style corporate net-zero-commitment tracking: three illustrative issuers' "track record vs. 2020-trend vs. targets vs. NZE scenario" comparison charts. `tale4`/`tale5` depend on a missing `cdp_filter` helper function; the archive does ship `chap9_CDP1.xlsx`, but inspection confirms it's a different, single-year 6-company snapshot with no multi-year/sector/target/NZE panel data — not what `cdp_filter` needs. Confirmed blocked, not just assumed. | ✅ (partial — 3 of 5 scripts, 2 blocked) |

**Final, verified total** (confirmed by listing every `chap9_*.m` file in
the archive directly, after building all of `09a`-`09f`): 7 + 8 + 9 + 7
+ 6 + 8 + 5 = **50 exercise scripts**, exactly matching a direct
`ls`-based count of the archive's `chap9_*.m` files. This accounts for
the full chapter (the archive also ships 2 `Data/*.m` prep scripts,
`chap9_EF_Scope2_LB1.m` and `chap9_CDP2.m`, not counted as exercise
scripts). The original subagent-based scope undercounted by missing an
entire script family (`carbon_ce1/1a/1b/1c/2/3`, folded into `09c`'s
blocked-scripts list) and 3 orphaned scripts with no filename-pattern
home (`carbon_offsetting2`, `consolidation1`, `greenness_grs1`, folded
into `09f` as addenda) — both found only once every file was actually
read rather than pattern-matched by name. Lesson for `09g` and for
Chapter 10's scoping: confirm the full file list directly (`ls`) before
finalizing a script-count table, rather than trusting a subagent's
filename-pattern survey alone.

## Data-blocked scripts (confirmed: 10 of 50)

Two datasets referenced by Chapter 9 scripts are absent from the shipped
`hfs-archive` archive entirely:

- **`Trucost_Data1_2019`** and **`NZE_MSCI_World`** — block 8 scripts in
  `09c`: `ci2`, `ci4`, and all 6 `carbon_ce*` scripts (`ce1`, `ce1a`,
  `ce1b`, `ce1c`, `ce2`, `ce3` — a script family missed by the original
  subagent-based scope entirely, found only once `09c` was actually
  built and the archive's full file list checked directly).
- **CDP issuer-level panel data**, combined with a missing custom
  function **`cdp_filter`** (not present anywhere in the shipped
  toolbox) — blocks `tale4`/`tale5` in the planned `09g` notebook (not
  yet built; expected based on the script names, to be confirmed the
  same way `09c`'s count was).

By coincidence this 8+2=10 total lands close to the original "10 of 52"
estimate, but for different reasons: not because 8 of 9 `ci*` scripts
were blocked (there are only 3 `ci*` scripts, and only 2 are blocked),
but because 6 previously-unknown `ce*` scripts turned out to share the
same missing-data problem. Per this project's standing convention,
these are flagged explicitly rather than silently skipped or faked with
synthetic data.

**Chapter 9 is now complete (2026-08-22)**: all 7 notebooks (`09a`-`09g`)
built, verified (0 errors/0 stderr warnings, every figure visually
checked), delivered, and tracked. 40 of the chapter's 50 exercise
scripts are built faithfully; the other 10 are explicitly flagged as
data-blocked (8 in `09c` on missing Trucost/MSCI data, 2 in `09g` on a
missing `cdp_filter` function plus its required panel data) rather than
skipped silently or faked. Two disclosed simplifications: `09f`'s
`pac4`/`pac5` sections reproduce the underlying scoring data with
standard chart types rather than the source's idiosyncratic hand-tuned
spline/polar layouts.

## Custom/missing-function inventory

- **`carbon_budget_Reduction(t0, t, CE_t0, R, mtd)`** and
  **`carbon_budget_piecewise(t0, t, t_k, CE_k)`** — both referenced by
  `chap9_carbon_budget*.m` but not present anywhere in the shipped
  `hfs-archive` toolbox. Reimplemented in `09a` from the closed-form
  emission-decline formulas (`Reduction`) and from `carbon_budget7.m`'s
  own inline equivalent computation (`piecewise`, whose 3-output split
  is inferred, not verified against an original function body — flagged
  in the notebook). See `PACKAGING_CANDIDATES.md`'s "Chapter 9a" section.
- **`cdp_filter`** — referenced by `chap9_tale4.m`/`tale5.m`, not present
  in the shipped toolbox, and its required CDP panel data is also
  missing — this pairing is unbuildable faithfully (see Data-blocked
  section above), not just a reimplementation task.
- **State-space/Kalman toolkit for `09e`** — turned out not to need any
  new reimplementation: `quanttoolbox.econometrics.kalman` and
  `quanttoolbox.econometrics.whittle` already exist in the real
  `quanttoolbox` PyPI package (the archive has no `chap9_ects*` scripts
  at all — that guess was wrong; the actual scripts are `chap9_carbon_
  trend1-6.m`). The only issue was that `quanttoolbox` wasn't installed
  in this session's fresh container — see `SESSION_HANDOFF.md`'s new
  gotcha note.

## Working conventions (same as the rest of the series)

- Faithful `.m`-to-Python translation via the `build_XXn.py` throwaway-
  script pattern; execute with `nbclient`, confirm 0 errors/0 stderr
  warnings, visually spot-check every figure before finalizing.
- Missing custom toolbox functions get reimplemented transparently with
  an explicit data-provenance caveat in the notebook markdown.
- Near-duplicate/superseded scripts get noted and skipped rather than
  rebuilt, same policy as earlier chapters.
- Missing/blocked data dependencies get explicitly flagged rather than
  faked with synthetic data.
- Never run git directly — hand exact `git add`/`commit`/`push` commands
  to the user.
