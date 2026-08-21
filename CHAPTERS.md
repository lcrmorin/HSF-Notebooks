# Chapter tracker

Status legend: ⬜ not started · 🟨 in progress · ✅ notebook done

| # | Chapter | `.m` scripts | Status | Notes |
|---|---|---|---|---|
| 0 | Toolbox | 163 (163 vendored for reference; `tools/`+`external/` excluded) | ⬜ | Not a chapter notebook — this is the bond/copula/credit/genz/hsf/maths/stats function library. A reference copy of the MATLAB source now lives at `QuantToolBox/reference/hsf_toolbox_matlab/`, and the planned Python module mapping is in that repo's `docs/migration_map.md` ("HSF toolbox port (planned)"). A `00_toolbox.ipynb` primer notebook can follow once enough of it lands there. |
| 1 | Introduction | 12 (9 chapter scripts) | ✅ | `notebooks/hsf/01_introduction.ipynb`. Needs only pandas/numpy/matplotlib — no toolbox dependency. Two near-duplicate script pairs (`chap1_pri1.m`/`pri1a.m`, and the `pri2`/`pri2a`/`pri2b.m` trio across data vintages) consolidated into one section each, using the most recent (2024) PRI data vintage. Reads `pri_regulation_2024.xlsx`/`pri_signatory_2024.xlsx` directly via `pandas.read_excel` instead of the original's `xlsread` → `.mat` round trip. |
| 2 | ESG Scoring | 56 | ⬜ | Ratings, scoring methodologies (Gini/KS backtests), Markov rating-transition models. |
| 3 | ESG Investing | 69 | ⬜ | |
| 4 | ESG Products | 55 | ⬜ | |
| 5 | Impact Investing | 163 | ⬜ | Largest chapter by script count. |
| 6 | Engagement | 32 | ⬜ | |
| 7 | Accounting | 0 | ⬜ | No `.m` scripts (2 `.xlsx`, 1 `.png`) — likely a discussion chapter with no code exercises; confirm before deciding whether it needs a notebook at all. |
| 8 | Economic Modeling | 264 | ⬜ | Largest chapter overall. Likely depends heavily on the DICE temperature model and other `0. Toolbox/hsf/` functions. |
| 9 | Risk Measures | 52 | ⬜ | Carbon budget/intensity/offsetting measures — depends on `0. Toolbox/hsf/carbon_*` functions. |
| 10 | Transition Risk | 43 | ⬜ | |
| 11 | Portfolio Optimization | 80 | ⬜ | Decarbonization-constrained portfolio construction — likely builds directly on `quanttoolbox.portfolio`. |
| 12 | Physical Risk | 70 | ⬜ | |
| 13 | Stress Testing | 37 | ⬜ | |
| 14 | Conclusion | 0 | ⬜ | Empty folder — confirm whether this chapter has any content at all. |
| 15 | Technical Appendix | 17 | ⬜ | |
| 16 | Exercise Solution | 10 | ⬜ | |
| 17 | Data | 0 | ⬜ | Empty folder — likely just a pointer to where chapter datasets live, not a chapter itself. |

## Tutorials (not chapter-specific)

Separate from the HSF chapters: `notebooks/tutorials/` holds general
`quanttoolbox` walkthroughs — the notebook equivalent of the package's own
`docs/examples/` deep dives, numbered from 0 the same way `notebooks/hsf/`
is. This replaces `quanttoolbox`'s own `Examples/tutorial/` folder (11
generic MATLAB-101 lessons, unrelated to any quanttoolbox function), which
has been dropped from that repo's `docs/migration_map.md` tracker in favor
of these — quanttoolbox-specific rather than MATLAB-generic. None started
yet.

| # | Notebook | Based on | Status |
|---|---|---|---|
| 0 | `00_building_blocks.ipynb` | `docs/examples/building_blocks.md` (bisection, numerical gradient/Hessian, proximal operators, vec/vech) | ⬜ |
| 1 | `01_risk_budgeting.ipynb` | `docs/examples/risk_budgeting.md` | ⬜ |
| 2 | `02_black_litterman.ipynb` | `docs/examples/black_litterman.md` | ⬜ |
| 3 | `03_mean_variance.ipynb` | `docs/examples/mean_variance.md` | ⬜ |
| 4 | `04_whittle.ipynb` | `docs/examples/whittle.md` | ⬜ |
| 5 | `05_regression.ipynb` | `docs/examples/regression.md` | ⬜ |
| 6 | `06_svm.ipynb` | `docs/examples/svm.md` | ⬜ |
