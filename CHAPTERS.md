# Chapter tracker

Status legend: ⬜ not started · 🟨 in progress · ✅ notebook done

A chapter large enough to split into two clearly separate topics gets a
lettered pair of notebooks (`2a`, `2b`, ...) instead of one long one — the
book chapter number stays the row's identity either way.

| # | Chapter | `.m` scripts | Status | Notes |
|---|---|---|---|---|
| 0 | Tutorial | 11 | ✅ | `notebooks/hsf/00_tutorial.ipynb` -- a single notebook translating the original MATLAB `tutorial/` lessons (arrays, strings, plotting, structs, N-D arrays, regression, user functions). NumPy/Matplotlib only, no other dependency. |
| 1 | Introduction | 12 (9 chapter scripts) | ✅ | `notebooks/hsf/01_introduction.ipynb`. Needs only pandas/numpy/matplotlib — no toolbox dependency. Two near-duplicate script pairs (`chap1_pri1.m`/`pri1a.m`, and the `pri2`/`pri2a`/`pri2b.m` trio across data vintages) consolidated into one section each, using the most recent (2024) PRI data vintage. Reads `pri_regulation_2024.xlsx`/`pri_signatory_2024.xlsx` directly via `pandas.read_excel` instead of the original's `xlsread` → `.mat` round trip. |
| 2a | ESG Scoring — Ratings & transitions | 19 | ✅ | `notebooks/hsf/02a_ratings_and_transitions.ipynb`. Rating-scale construction (normal- and beta-based) plus discrete- and continuous-time Markov rating-transition analysis: n-step transitions, stationary distribution (3 methods), monthly↔annual conversion, expected hitting time, generator matrices, and rating stability compared against a real credit-transition matrix. Uses `quanttoolbox.sustainable_finance.entropy.estimate_markov_generator`; everything else is numpy/scipy, no other toolbox dependency. The ESG 1-year transition matrix (`P1`) is read directly from `esg_transition_matrix.xlsx` instead of hard-coded, matching the original's own hard-coded values to 2 decimal places. |
| 2b | ESG Scoring — Scoring methodology | 25 (+ 12 data-prep) | ✅ | `notebooks/hsf/02b_scoring_methodology.ipynb`. Weight aggregation/variance propagation, Bates-distribution and Beta-distribution score transforms, basket variance/confidence bands under constant correlation (`quanttoolbox.stats.distributions.constant_correlation_matrix`), the q/z/qz/zq/bz scoring-and-aggregation framework (applied to real SEC CEO pay-ratio data), Shannon-entropy scoring (`quanttoolbox.sustainable_finance.entropy.shannon_entropy`), and the LPI/RLI case studies. The `Data/*.m` scripts for the Gini/selection/precision/ROC/performance/discriminant/KS curves turned out to be thin `xlsread→.mat` converters with no computation anywhere in the MATLAB source — those curves are read directly from their `.xlsx` source data instead of derived from an unstated formula (`gini1` excepted: a pure textbook illustration, reproduced from first principles). The backtesting scripts (`scoring_backtesting1-5.m`) do have real computation — a MATLAB `csaps` smoothing-spline pass — translated with the `csaps` Python package. |
| 3 | ESG Investing | 69 | ⬜ | |
| 4 | ESG Products | 55 | ⬜ | |
| 5 | Impact Investing | 163 | ⬜ | Largest chapter by script count. |
| 6 | Engagement | 32 | ⬜ | |
| 7 | Accounting | 0 | ⬜ | No `.m` scripts (2 `.xlsx`, 1 `.png`) — likely a discussion chapter with no code exercises; confirm before deciding whether it needs a notebook at all. |
| 8 | Economic Modeling | 264 | ⬜ | Largest chapter overall. Likely depends heavily on the DICE temperature model and other functions planned for `quanttoolbox`'s `sustainable_finance/climate.py`. |
| 9 | Risk Measures | 52 | ⬜ | Carbon budget/intensity/offsetting measures — depends on functions planned for `quanttoolbox`'s `sustainable_finance/carbon.py`. |
| 10 | Transition Risk | 43 | ⬜ | |
| 11 | Portfolio Optimization | 80 | ⬜ | Decarbonization-constrained portfolio construction — likely builds directly on `quanttoolbox.portfolio`. |
| 12 | Physical Risk | 70 | ⬜ | |
| 13 | Stress Testing | 37 | ⬜ | |
| 14 | Conclusion | 0 | ⬜ | Empty folder — confirm whether this chapter has any content at all. |
| 15 | Technical Appendix | 17 | ⬜ | |
| 16 | Exercise Solution | 10 | ⬜ | |
| 17 | Data | 0 | ⬜ | Empty folder — likely just a pointer to where chapter datasets live, not a chapter itself. |
