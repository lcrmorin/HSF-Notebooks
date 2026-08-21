# Chapter tracker

Status legend: ⬜ not started · 🟨 in progress · ✅ notebook done

| # | Chapter | `.m` scripts | Status | Notes |
|---|---|---|---|---|
| 0 | Tutorial | 11 | ✅ | `notebooks/hsf/00_tutorial.ipynb` -- a single notebook translating the original MATLAB `tutorial/` lessons (arrays, strings, plotting, structs, N-D arrays, regression, user functions). NumPy/Matplotlib only, no other dependency. |
| 1 | Introduction | 12 (9 chapter scripts) | ✅ | `notebooks/hsf/01_introduction.ipynb`. Needs only pandas/numpy/matplotlib — no toolbox dependency. Two near-duplicate script pairs (`chap1_pri1.m`/`pri1a.m`, and the `pri2`/`pri2a`/`pri2b.m` trio across data vintages) consolidated into one section each, using the most recent (2024) PRI data vintage. Reads `pri_regulation_2024.xlsx`/`pri_signatory_2024.xlsx` directly via `pandas.read_excel` instead of the original's `xlsread` → `.mat` round trip. |
| 2 | ESG Scoring | 56 | ⬜ | Ratings, scoring methodologies (Gini/KS backtests), Markov rating-transition models. |
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
