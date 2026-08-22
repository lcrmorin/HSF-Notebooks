# Chapter 12 (Physical Risk) — scoping & roadmap

Chapter 12 ships 50 `chap12_*.m` exercise scripts (confirmed by direct
`ls`/`find` against `HSF/12. Physical Risk/`, not filename-pattern
estimation; the directory's 51st `.m` file, `compute_horizontal_
resolution.m`, is a shared 3-line helper function, not an exercise
script). There is no `Results/` folder for this chapter. Every one of
the 50 scripts was read directly in full (not inferred from filenames)
by a scoping agent, with the same rigor established in Chapter 11: no
script gets flagged blocked without independently testing its actual
data dependency for readability, and every ambiguous column/sheet
mapping was resolved by reading the shipped `Data/chap12_*.m` loader
script rather than guessed at. They fall into 10 natural families:
crop/climate-index tables (3), geodesy & map projections + wind-
direction convention (7), IPCC/CMIP climate-model grid-resolution
mechanics (6), IPCC assessment-report grid/vertical-level statistics
(6), ND-GAIN country vulnerability index (5), Climate Risk Index (CRI)
and IPCC AR6 hazard-impact tables (3), financial-loss/catastrophe
actuarial metrics (8), sector & corporate physical-risk exposure (6),
extreme-value statistical distributions for hazard modeling (3), and
physical vulnerability (damage) curves (3).

## The central finding: MATLAB `table`/`string` objects, not an isolated datetime column

Chapter 11's data-readability gotcha was narrow: a couple of `.mat`
files had one unreadable MCOS `datetime` axis inside an otherwise
perfectly readable numeric struct. **Chapter 12's version of this
gotcha is much broader**: nearly every dataset in this chapter is
shipped as a MATLAB `table` object (`T`, `T1`, `T2`, `T_RS`, `T_Loss`,
`T_vulnerability`, …) — and `table` itself is an MCOS class, so
`scipy.io.loadmat` cannot parse it at all. Directly testing every one
of the 14 distinct `.mat` files referenced by this chapter's scripts
confirms this: **13 of 14 load as a single opaque `MatlabOpaque`
blob keyed `'None'`, with zero readable content** (`scipy.io.loadmat`
prints the same "Duplicate variable name None" warning pattern seen in
Chapter 11, but here it swallows the whole file, not just one column).
The **sole exception** is `chap12_ext_ipcc_hazard_impact.mat`, which
happens to also store one plain numeric array (`data`, a 50×21
`float64` matrix, confirmed readable) alongside its opaque `region`
string-array/table content — a partial case, not a full escape.

**None of this actually blocks anything, though.** Every single one of
the 14 `.mat` files has a matching `.xlsx` sibling in `Data/`, and
**all 14 were confirmed independently readable via `pandas.read_excel`**
with the expected sheets and columns present. Better still, each
dataset's own `Data/chap12_*.m` *loader* script (the small script that
originally built the `.mat` from the `.xlsx` — e.g.
`Data/chap12_ext_mandel.m`, `Data/chap12_ext_ecb_physical_risk.m`,
`Data/chap12_2025_Paredes.m`) is itself shipped in the archive and was
read directly. These loader scripts are extremely valuable: they show
**exactly** which sheet became which table variable and any
transformation applied (renames, joins, unit scaling, sentinel-value
handling) — turning what would otherwise be column-index guesswork
into a fully-specified reconstruction recipe for every dataset in this
chapter. Full per-dataset detail is in the "Data dependency
verification" section below. **Bottom line: 0 of the 50 scripts are
truly blocked** by missing/unreadable data — this chapter has no
`chap11_MSCI_World`-style hole. The complications here are of a
different, tamer kind (documented below): a Mapping-Toolbox map
projection dependency, some column-index/multi-row-header parsing
care, and a handful of genuinely-missing custom statistical helper
functions that need faithful from-formula reimplementation.

## Script-by-script summary, grouped by family

### A. Crop/climate index tables (`cid1-3`, 3 scripts)
| Script | Summary |
|---|---|
| `cid1` | Growing-degree-day (GDD) calculation from a hardcoded 7-day min/max temperature series; weekly and seasonal (×12) GDD totals. No data file. |
| `cid2` | LaTeX table of crop growing-season definitions (initial/develop/mid/harvest-stage day counts) from the Paredes (2025) FAO-style crop calendar dataset, sorted alphabetically by crop name with season-label abbreviation. |
| `cid3` | LaTeX table of the Zhang (2011) climate-index definitions (ID/Name/Definition/Units), with LaTeX-symbol substitution (`≥`→`$\ge$`, `C`→`$^{\circ}\mathrm{C}$`). |

### B. Geodesy, coordinate systems, wind-direction convention, map projections (`coordinate1-6`, `data1`, 7 scripts)
| Script | Summary |
|---|---|
| `coordinate1` | Degrees-minutes-seconds → decimal-degrees conversion, one worked example. No data. |
| `coordinate2` | WGS84 ellipsoid flattening/eccentricity computed two ways (from semi-axes, and from inverse flattening), cross-checked against MATLAB's `wgs84Ellipsoid` builtin. No data. |
| `coordinate3` | Full geodetic (lat/lon/height, Paris coords) → ECEF (x,y,z) conversion worked by hand from the WGS84 formulas, then cross-checked against MATLAB's `geodetic2ecef`. No data. |
| `coordinate4` | World map in a Mollweide projection with a land-area overlay (Mapping Toolbox `axesm`/`geoshow`/`shaperead('landareas.shp')`). |
| `coordinate5` | Same, Lambert (azimuthal equal-area) projection. |
| `coordinate6` | Same, Wiechel (polar pseudo-azimuthal) projection. |
| `data1` | Wind-direction/-speed vector diagram: compass-rose figure showing the meteorological "wind FROM φ" convention decomposed into u (east-west) / v (north-south) Cartesian components, with an explicit worked numeric example (φ=240°, speed=1.0). No data. |

### C. IPCC/CMIP climate-model grid-resolution mechanics (`grid1`, `grid2a-e`, 6 scripts)
| Script | Summary |
|---|---|
| `grid1` | Back-of-envelope "how many climate-model grid boxes exist" calculation: Earth surface area ÷ box area, scaled by variable count, time steps/day, and years. No data. |
| `grid2a` | Horizontal-resolution-in-km formula (`R = length(1°) × √(Δφ·Δλ·cos φ)`) evaluated at several latitudes and two `R`-values (real ellipsoid semi-axes vs. spherical mean radius). No data. |
| `grid2b` | Plots that same resolution formula continuously from equator to pole (10°×10° grid) — the "grid boxes shrink toward the poles" figure. No data. |
| `grid2c` | Numerically integrates the resolution formula over latitude (`integral`, i.e. `scipy.integrate.quad`) for several parameterizations, to get an average effective resolution. No data. |
| `grid2d` | Same resolution formula evaluated at a table of historical model resolutions (5.6°→0.375°) at two latitudes, plus a closed-form latitude-averaged approximation (`0.7628×…`). No data. |
| `grid2e` | Same as `grid2d` but calls the shared `compute_horizontal_resolution` helper (0°, 45°, and averaged) instead of inlining the formula — confirms the helper reproduces the 0.7628 constant. No data. |

### D. IPCC assessment-report grid/vertical-level statistics (`grid3a-f`, 6 scripts)
| Script | Summary |
|---|---|
| `grid3a` | `compute_horizontal_resolution` + summary stats (n/median/min/max/mean, via a local `compute_stats` helper) of atmosphere/ocean grid resolution and vertical-level counts for the IPCC **FAR** report's models. |
| `grid3b` | Same, for **SAR**, computed separately for atmosphere-grid and ocean-grid spacing (FAR's table doesn't split atm/ocean angle; SAR's does). |
| `grid3c` | Same, for **TAR**. Byte-for-byte identical structure to `grid3b` except the table name (`T_TAR` vs `T_SAR`). |
| `grid3d` | Same, for **AR4**. Byte-for-byte identical structure to `grid3b`/`grid3c` except table name (`T_AR4`). |
| `grid3e` | Hardcoded, per-report (AR1 through AR6) lists of individual climate models' atmosphere/ocean **vertical level counts** (not horizontal resolution), summarized via a local `grid_analyze` helper using MATLAB `global`s; ends with AR7. |
| `grid3f` | Same pattern as `grid3e`, restricted to AR6 and AR7, but with a **different literal dataset** under the same global variable names (values ~10x larger — almost certainly a different metric, e.g. resolution in meters rather than a level count; reproduce literally either way, the exact semantic label doesn't change the port). |

### E. ND-GAIN country vulnerability/readiness index (`ext_ndgain_country1-5`, 5 scripts)
| Script | Summary |
|---|---|
| `ext_ndgain_country1` | Correlation matrix (LaTeX table) between the aggregate ND-GAIN vulnerability score and its 6 sector sub-scores (ecosystems/food/habitat/health/infrastructure/water), most recent year. |
| `ext_ndgain_country2` | Scatter plot of the 6 sector vulnerability scores vs. the aggregate score, most recent year, one marker style per sector. |
| `ext_ndgain_country3` | Vulnerability-vs-readiness correlation and scatter, comparing 1995 vs. 2023, plus a filtered-subsample (vulnerability > 0.45) correlation. |
| `ext_ndgain_country4` | Top-10 / bottom-10 country rankings by aggregate vulnerability score (most recent year). |
| `ext_ndgain_country5` | Top-10 / bottom-10 country rankings by aggregate **ND-GAIN (readiness-adjusted "gain")** score. |

### F. Climate Risk Index (CRI) and IPCC AR6 hazard-impact tables (`ext_cri_country1`, `ext_ipcc_hazard_impact1-2`, 3 scripts)
| Script | Summary |
|---|---|
| `ext_cri_country1` | 3-panel pie chart (fatalities / people affected / economic loss shares by hazard type) from the Germanwatch-style Climate Risk Index (CRI) 2026 dataset. |
| `ext_ipcc_hazard_impact1` | LaTeX table of IPCC AR6 regional hazard-impact metrics (7 hazard indicators × 3 global-warming levels: 1.5°C/2°C/4°C) across ~50 IPCC reference regions, reordered so the world/continent aggregates sit at the end. |
| `ext_ipcc_hazard_impact2` | Top-5 most/least-affected-region rankings per hazard indicator (ascending sort for the 2 indicators where "lower is worse", descending for the rest), formatted as a two-block LaTeX table. |

### G. Financial-loss / catastrophe-actuarial metrics (`financial_loss2-5b`, 8 scripts)
| Script | Summary |
|---|---|
| `financial_loss2` | Converts a table of return periods `T` and per-event expected losses `E` into non-exceedance probabilities, then compounds them across `T` and over `n`-year holding horizons (1/2/5/10/15/25y) into cumulative probability-of-loss and expected cumulative loss. No data. |
| `financial_loss3` | Antofie-et-al.-style expected-loss-vs-time curves (river flood / coastal flood / landslide, EL in km²) fit with a smoothing spline (`csaps`) through discrete `n`-year data points, endpoints weighted heavily. |
| `financial_loss4a` | ECB physical-risk-score distribution (share of portfolio in each of 4 risk tiers) by country and economic activity, for one specific hazard scenario (`ipcc_eu_CDD_v_hist_a`, historical drought-days). |
| `financial_loss4b` | Same as `4a`, different scenario (`ipcc_eu_CDD_v_2060_r85_a`, 2060 RCP8.5 drought-days) — near-identical script, different hazard-scenario filter string. |
| `financial_loss4c` | ECB expected-loss-at-maturity and expected-annual-loss (% of portfolio) by country/activity, historical coastal-flood scenario (`ud_cf_1971_2000_hist`). |
| `financial_loss4d` | Same as `4c`, 2071-2100 RCP8.5 scenario (`ud_cf_2071_2100_RCP85`) — near-identical script, different scenario filter. |
| `financial_loss5a` | Mandel-et-al.-style capital-at-risk table (median/95%-VaR by bond/equity/capital) across 3 climate scenarios, plus VaR/EL "tail multiplier" ratios. |
| `financial_loss5b` | Mandel-et-al. regional table: value share, impact share, impact ratio, largest contributing peril, plus (after a join with a second sheet) direct/equity impact ratios by world region. |

### H. Sector & corporate physical-risk exposure (`corporate1`, `sector3`, `sector4`, `sector6a`, `sector6b`, `sector7a`, 6 scripts)
| Script | Summary |
|---|---|
| `corporate1` | S&P-sector physical-risk exposure/sensitivity scores (developed-market vs. emerging-market) under Medium-2030, Medium-2050 and High-2050 climate scenarios, one combined LaTeX table. |
| `sector3` | Cline (2007) agricultural GDP-impact-by-region table (with vs. without carbon-fertilization effect), plus min/max/mean summary diagnostics. |
| `sector4` | Tiny 4-row hardcoded before/after-style difference table (no context/labels beyond the numbers themselves — appears to be a companion illustrative table, possibly continuing the carbon-fertilization theme of `sector3` with a different, smaller dataset). No data file. |
| `sector6a` | Munich Re NatCat stacked bar chart (insured vs. uninsured losses per year, 1980-2025) with a 10-year trailing moving average overlay. |
| `sector6b` | Munich Re NatCat losses aggregated over a set of custom historical sub-periods (by-decade plus a few notable multi-year windows), with insured-loss share, as a LaTeX table. |
| `sector7a` | EIOPA insurance-risk-dashboard historical-vs-current physical-risk scores by country × peril (2025 vintage), missing-value sentinel handling, printed and LaTeX table forms. |

### I. Extreme-value statistical distributions for hazard modeling (`statistical_modeling1a-c`, 3 scripts)
| Script | Summary |
|---|---|
| `statistical_modeling1a` | Mean/std. dev. of 3 fitted hazard-intensity distributions (Gaussian, Weibull, Generalized Extreme Value) via MATLAB's `makedist`. No data. |
| `statistical_modeling1b` | PDFs of the same 3 distributions plotted together (wind-speed axis), with the "custom" Weibull/GEV pdf implementations cross-checked numerically against MATLAB's builtin `wblpdf`/`gevpdf`; also prints the Weibull distribution's skewness coefficient. No data. |
| `statistical_modeling1c` | Return-period / quantile table: for 3 wind speeds, computes exceedance probability and implied return period under each of the 3 distributions, and the inverse (quantile at 3 confidence levels), cross-checking forward/inverse consistency. No data. |

### J. Physical vulnerability (damage) curves (`vulnerability1-3`, 3 scripts)
| Script | Summary |
|---|---|
| `vulnerability1` | Huizinga flood depth-damage curves by infrastructure type (residential/commercial/industrial/etc.), one curve per type, smoothing-spline-fit and sorted by damage severity at 5m depth. |
| `vulnerability2` | Same Huizinga dataset, but curves split by world region instead of infrastructure type (fixed to one infrastructure type). |
| `vulnerability3` | Parametric cubic wind-damage curve `D(w) = υ³/(1+υ³)`, `υ = max(w−w₋,0)/(w½−w₋)` (the classic Emanuel-style tropical-cyclone wind vulnerability function), plotted for 3 different `(w₋, w½)` parameter sets and 4 unit-convention variants (m/s, knots, mph) selectable via an `if/elseif` block (only `units==1` is actually exercised by the script as written). |

**Total: 3+7+6+6+5+3+8+6+3+3 = 50**, matching the archive's confirmed script count exactly.

## Data dependency verification (per dataset)

All 14 distinct `.mat` files referenced by this chapter's 50 scripts
were tested directly with `scipy.io.loadmat`, and all 14 matching
`.xlsx` siblings were tested with `pandas.read_excel`. Each dataset's
own `Data/chap12_*.m` loader script (where present) was also read to
resolve the exact sheet→table-variable mapping and any transform
applied. Findings:

| Dataset (`Data/chap12_*`) | `.mat` readable via scipy? | `.xlsx` readable? | Used by | Notes |
|---|---|---|---|---|
| `2025_Paredes` | No — whole file is one opaque `MatlabOpaque` blob (the `table` `T`) | Yes, sheet `Table 5` (53 rows) | `cid2` | The loader script (`Data/chap12_2025_Paredes.m`) shows `T.Name = extractBefore(T.Crop," (")` — i.e. the `.mat`'s "Name" field is *derived* from the xlsx's "Crop" column by stripping the parenthetical species name (e.g. `"Carrots (Daucus carota)"` → `"Carrots"`). Trivial to replicate (`str.split(" (")[0]`). Filename case note: `cid2.m` requests `'Data\chap12_2025_paredes.mat'` (lowercase p) but the shipped file is `chap12_2025_Paredes.mat` (capital P) — matches on case-insensitive Windows, needs an exact-case match on Linux build. |
| `2011_Zhang` | No (opaque) | Yes, sheet `Table` (33 rows: ID/Name/Definition/Units) | `cid3` | Direct 1:1 mapping, loader script confirms `T = readtable(...,'sheet','Table')` with no transform. Same lowercase/uppercase filename-casing note (`cid3.m` requests `chap12_2011_zhang.mat`, shipped file is `chap12_2011_Zhang.mat`). |
| `ext_cri_2026` | No (opaque) | Yes, sheets `Table 1`, `Table 2`, `Annex` | `ext_cri_country1` | Loader confirms `T1`→Table 1, `T2`→Table 2, `T3`→Annex, no transform. `ext_cri_country1.m` uses `T2` directly; columns (Hazard/Fatalities/Affected/Economic_loss_USD) match exactly, no ambiguity. |
| `ext_ipcc_hazard_impact` | **Partially** — the `data` variable (50×21 `float64`) loads directly and correctly; `region` (a string array) is opaque/unreadable | Yes, 7 sheets `SM2`-`SM8` | `ext_ipcc_hazard_impact1`, `ext_ipcc_hazard_impact2` | The `Data/chap12_ext_ipcc_hazard_impact.m` loader fully specifies the recipe: loop `iter=1..7` over sheets `SM2..SM8` (one sheet per hazard indicator, ordered `TXx, TNn, Rx1day, Rx5day, Moisture, Moisture10, CDD`), horizontally concatenate each sheet's `GWL_15/GWL_20/GWL_40` columns into `data`, **×100 only for the `Rx1day` (SM4) and `Rx5day` (SM5) sheets**, replace sentinel `-99` with NaN (`miss(data,-99)`), and take `region` from any one sheet's first column (verified identical across all 7 sheets). Since `data` already loads directly from the `.mat`, only `region` actually needs the `.xlsx` fallback — confirmed present and consistent. |
| `ext_ndgain_country_index` | No (opaque) | Yes, 13 sheets: `gain, vulnerability, capacity, exposure, sensitivity, readiness, ecosystems, food, habitat, health, infrastructure, water, Datawrapper` | `ext_ndgain_country1-5` | Sheet names map 1:1 onto the scripts' `T_vulnerability`/`T_readiness`/`T_gain`/`T_ecosystems`/etc. variable names — no ambiguity. Each sheet is `ISO3, Name, <year columns 1995…latest>`; `pos = cols(T0)` in the scripts just means "use the most recent year column", i.e. the rightmost column. |
| `ext_antofie` | No (opaque) | Yes, sheet `Data` (6 rows: n/EL_river/p_river/EL_coastal/p_coastal/EL_landslide/p_landslide) | `financial_loss3` | Direct match, no ambiguity. |
| `ext_ecb_physical_risk` | No (opaque) | Yes, 5 sheets: `physical_risk_hazards, description_risk_scores, risk_scores, description_loss, loss` | `financial_loss4a-4d` | Loader confirms `T_RS = readtable(...,'sheet',3)` (→ `risk_scores`) and `T_Loss = readtable(...,'sheet',5)` (→ `loss`). Both sheets carry one **extra unnamed leading column** in the raw xlsx (visible as a blank header in `pandas`) which corresponds to a real MATLAB table variable (not a pandas artifact) — so column indices are offset by +1 from the visible-named-column position. With that +1 accounted for, `T_RS{:,17:20}` = the 4 `physcl_rsk_scr0..3_prcntg_ptfl` risk-tier-share columns used by `4a`/`4b` (confirmed exact match), and `T_Loss{:,[11 13]}` = `physcl_rsk_near_mtrty_expctd_lss_prcntg_ptfl` + `physcl_rsk_near_annl_expctd_lss_prcntg_ptfl` used by `4c`/`4d` (confirmed exact match). This offset is worth flagging clearly for the build phase so it isn't rediscovered by trial and error. |
| `ext_mandel` | No (opaque) | Yes, sheets `Table 1`, `Table 2`, `Table 4` | `financial_loss5a`, `financial_loss5b` | `financial_loss5a` uses `T1` → `Table 1` directly, columns match (`Statistic, Scenario, Capital, Bond, Equity`), no ambiguity. **`financial_loss5b` uses `T2`, which the loader script reveals is `T2 = join(T2,T4)`** — i.e. the `.mat`'s `T2` is *not* simply `Table 2`, it's `Table 2` **joined with `Table 4`** on their shared `Region` key. Reconstructing this join (`pandas.merge(table2_df, table4_df, on="Region")`) gives 11 columns in the natural join order (`Region, Value_share, Impact_share, Impact_ratio, Largest_contributor, Impact, Direct_impact, Equity_impact, Equity_value, Ratio1, Ratio2`), against which the script's `T{:,indx}` with `indx=[6 4 10 11]` resolves unambiguously to `[Impact, Impact_ratio, Ratio1, Ratio2]`. This was initially confusing (Table 2 alone only exports 6 columns, not enough for index 10/11) until the loader script's `join` call was found — a good example of "read the actual loader/source before flagging as blocked," per this series' standing convention. |
| `ipcc_grid` | No (opaque) | Yes, sheets `FAR, SAR, TAR, AR4, AR5, AR6` (AR5/AR6 sheets are empty — not used by any of the 4 `grid3a-d` scripts, which only reference `T_FAR/T_SAR/T_TAR/T_AR4`) | `grid3a-3d` | Direct 1:1 sheet-name mapping, columns (`Number, Model, A_Resolution, A_Level, O_Resolution, O_Level`) match the scripts' field accesses (`.A_angle`, `.A_Level`, `.O_angle`, `.O_Level`) once the `_Resolution`→`_angle` naming is accounted for (the loader likely parses each `"5.0° × 5.0°"`-style resolution string into a 2-column `[Δφ,Δλ]` numeric array named `A_angle`/`O_angle` — reconstructable directly from the `A_Resolution`/`O_Resolution` text column via a regex split, not independently verified byte-for-byte but low risk given the numbers involved are simple, round grid spacings). |
| `ext_cline_2007` | No (opaque) | Yes, sheets `TableValues, Regions, Data, TableValues (2)` | `sector3` | `sector3.m` accesses `T.Regions`/`T.Without_CF`/`T.With_CF`, which map directly onto the `Data` sheet (`Regions, Without_CF, With_CF`, 76 data rows — even, so the script's `reshape(country,n,2)` with `n=38` works cleanly). The `Regions` sheet (74 rows, country/subzone abbreviation legend) and the two `TableValues` sheets (raw pre-restructured source tables) are metadata/scratch, not used by `sector3.m`. |
| `ext_munich_re` | No (opaque) | Yes, sheet `Feuil1` (`year, total_loss, insured_loss`, 45 rows) | `sector6a`, `sector6b` | Direct match, no ambiguity. |
| `ext_eiopa_dashboard` | No (opaque) | Yes, sheets `Sheet1` (620 rows: `DB_version, Country, ISO_code, Peril, Historical_score, Risk_estimation, Insurance_penetration, Estimated_score`) and `Feuil1` (30-row summary, unused by `sector7a.m`) | `sector7a` | Direct match against `Sheet1`, no ambiguity. This `.xlsx` is the largest data file in the chapter (5.6 MB) but reads fine with `pandas`. |
| `ext_huizinga_flood` | No (opaque) | Yes, sheet `Damage function` (`Infrastructure, Depth, Europe, North_America, Latam, Asia, Africa, Oceania, Global`, 54 rows = 9 depths × 6 infrastructure types) | `vulnerability1`, `vulnerability2` | Direct match, no ambiguity — 54 rows reshapes cleanly to the scripts' `reshape(x,9,6)` calls. |
| `snp_physical_risk` | No (opaque) | Yes, sheets `Medium 2030, Medium 2050, High 2030, High 2050` | `corporate1` | Direct 1:1 sheet mapping; `corporate1.m` uses `T_Medium_2030, T_Medium_2050, T_High_2050` (3 of the 4 sheets — `High 2030` is loaded by the `Data/` loader script but never referenced by `corporate1.m` itself, not a bug, just unused). Each sheet has a **2-row merged header** (`Weights`/`Physical Risk` group labels on row 1, `Exposure Risk`/`Sensitivity Risk` sub-group labels on row 2, `Sector/DM/EM/DM/EM/DM/EM` column labels on row 3) that pandas' default single-row header parsing won't reproduce — needs an explicit `header=[0,1,2]` (MultiIndex) or manual `skiprows=2` + hardcoded column names when building. `T{:,4:7}` (the columns `corporate1.m` actually uses) = `Exposure Risk (DM, EM)` + `Sensitivity Risk (DM, EM)`, confirmed by column position. |

**Also present in `Data/` but referenced by none of the 50 scripts**
(orphan datasets, not a blocker for anything — just noting they exist
in case a future chapter extension wants them): `chap12_2021_Baatz.
xlsx`, `chap12_ext_data_Oxford_2024.xlsx`, `chap12_ext_data_exposure.*`,
`chap12_ext_data_ngfs.xlsx`, `chap12_ext_data_vulnerability.*`,
`chap12_ext_ipcc_atlas.*`, `chap12_reanalysis_data.*`,
`chap12_ext_swiss_re.xlsx`, `chap12_ext_van_leeuwen.xlsx`,
`chap_cmip6_mip_tables.xlsx`. None of these are `.nc` NetCDF files —
there is **no NetCDF dependency anywhere in this chapter's 50 scripts**
despite the chapter's climate-science subject matter (grid-resolution
scripts work from small hardcoded/tabular data, not gridded climate
fields).

**Conclusion: 0 of 50 scripts are blocked by missing or unreadable
data.** Every dataset referenced is either self-contained (20 of 50
scripts use no external data file at all) or has a fully-verified,
readable `.xlsx` fallback (30 of 50 scripts), with the exact
sheet/column mapping for every single one confirmed either directly
(by comparing column headers to script field-name accesses) or via the
shipped `Data/chap12_*.m` loader script (which fully resolves the two
initially-ambiguous cases: `financial_loss5b`'s joined `T2`, and
`ext_ipcc_hazard_impact`'s per-sheet ×100 scaling/concatenation
recipe).

## Custom/non-standard function inventory

Unlike Chapter 11 (which needed `QuantToolbox/rpb/` for its
tracking-error solver), Chapter 12's scripts lean almost entirely on
**generic `QuantToolbox` utility functions** (string/table/formatting
helpers reused across every chapter) plus a **chapter-local helper**.
All were checked against `QuantToolbox/` (the shared archive-wide
toolbox, sibling to `HSF/0. Toolbox/`) and `HSF/0. Toolbox/`.

**Found and straightforward to port** (all in `QuantToolbox/`, not
`HSF/0. Toolbox/` — this chapter barely touches the latter, which
holds only `latex_tabular.m`/`save_graphic2.m`/`hatchfill.m`/
`latex_sa.m` plus the `spider_plot`/tutorial folders unused this
chapter):
- `init_color` / `init_global` — global color-palette / global-variable
  initializers. **Note, unlike Chapter 11's `init_colour`(British)/
  `init_color`(American) split**: Chapter 12 consistently calls the
  American-spelled `init_color`, which **is** present — no
  spelling-mismatch workaround needed here.
- `ftosa(x, width, decimals)` — formats a numeric array as a
  fixed-width/fixed-decimal string matrix for `disp`. Trivial
  `numpy`/Python f-string port.
- `strcat2(varargin)` — horizontally concatenates strings/string
  columns with automatic row-broadcasting and blank padding. Found and
  read in full (`QuantToolbox/tools/strcat2.m`).
- `packr(x)` — drops rows containing missing values (returns
  `[cleaned, index]`). Found (`QuantToolbox/tools/packr.m`), read in
  full — a thin wrapper around `selif`/`countmiss`.
- `rows(x)`, `cols(x)` — row/column counts (GAUSS-style helpers).
  Trivial `.shape[0]`/`.shape[1]`.
- `text_line(width, char)`, `skip_line(n)` — cosmetic print separators.
- `selif(x, condition)` — boolean row-filter (GAUSS-style `select if`).
- `miss(x, sentinel)` — replaces a sentinel value (e.g. `-99`, `-9`)
  with `NaN`.
- `pdfn(x,mu,sigma)`, `cdfn(x,mu,sigma)`, `cdfni(p)` — Gaussian
  pdf/cdf/quantile. Found and read in full — standard closed forms
  (`pdfn` via the standard-normal density scaled by `1/sigma`; `cdfn`
  via `erf`; `cdfni` via `erfinv`). Used in `statistical_modeling1c`.
- `latex_tabular(data, width, fmt, ...)`, `save_graphic2(name)` — found
  in `HSF/0. Toolbox/tools/` (the one place this chapter does touch the
  chapter-agnostic toolbox), formatting/export helpers, mechanical port.
- `indnv`, `xpnd`, `missex` — found in `QuantToolbox/tools`/`matrix`,
  **not actually called by any of the 50 Chapter 12 scripts** (found
  during the broad function-name sweep but unused here; listed for
  completeness since they were relevant in Chapter 11).
- `compute_horizontal_resolution(delta_phi, delta_lambda)` — the
  chapter's one shared local helper (shipped as its own `.m` file
  alongside the exercise scripts, not in a toolbox folder). **Read in
  full** — trivial 8-line closed-form: `R_0 = 111.2·√(Δφ·Δλ)` at the
  equator, `R_45` at 45° latitude (`×cos(π/4)`), `R_avg = 0.7628·R_0`.
  Used by `grid2e` and all of `grid3a-3d`.
- `compute_stats(x)` (in `grid3a-3d`) and `grid_analyze(ar)` (in
  `grid3e-3f`) — both are **local nested functions defined inside their
  own `.m` files** (standard MATLAB local-function syntax at the bottom
  of the script), not external toolbox calls. No lookup needed, just
  port the ~5-line body directly. `grid3b`, `grid3c`, `grid3d` are
  **byte-for-byte identical** except for which table variable
  (`T_SAR`/`T_TAR`/`T_AR4`) they load — a strong candidate for one
  shared, parametrized Python helper called 3 times rather than 3
  copies (mirrors Chapter 11's `net_zero_barahhou3-6`-style collapse).
  `grid3e`/`grid3f` similarly share one `grid_analyze` body and should
  become one shared helper too.

**Genuinely not found anywhere in the archive** (checked across
`QuantToolbox/`, `HSF/0. Toolbox/`, and a full-archive `find`):
- **`strcat3`** — called in `ext_ipcc_hazard_impact1`,
  `ext_ipcc_hazard_impact2`, `ext_ndgain_country1`, `corporate1`, and
  `sector7a`, always with a call signature (variadic string args,
  including cases with 5+ args) identical to the *found* `strcat2`.
  No `strcat3.m` exists anywhere in the archive (confirmed by exact
  and case-insensitive filename search, and by searching for any
  `function ... strcat3` definition). Best read: a near-duplicate/
  variant of `strcat2` (possibly differing only in inter-column
  padding width) that a few scripts happen to call instead — since its
  observed call signature is a strict superset-compatible match for
  `strcat2`'s, the safe, disclosed reconstruction is to reuse the same
  `strcat2` port for both, flagged in the notebook markdown as
  "`strcat3`'s definition is not in the archive; treated as
  functionally identical to `strcat2` based on identical call-site
  usage — not independently verified."
- **`pdfweibull`, `pdfgev`, `cdfweibull`, `cdfweibulli`, `cdfgev`,
  `cdfgevi`, `skewness_weibull`** — called only in
  `statistical_modeling1b`/`1c`, following the same `pdf<dist>`/
  `cdf<dist>`/`cdf<dist>i` naming convention as the *found*
  `pdfn`/`cdfn`/`cdfni`, but none of the Weibull/GEV variants exist
  anywhere in the archive. **This is the chapter's one real "nontrivial
  statistical model" family** — but the risk is low and
  self-verifying: `statistical_modeling1b`/`1c` themselves cross-check
  the "custom" Weibull/GEV pdf/cdf against MATLAB's *built-in*
  `wblpdf`/`gevpdf` (`disp(max(abs(pdf2-pdf2b)))` etc.), meaning these
  are provably standard closed-form Weibull/GEV functions, not some
  idiosyncratic house convention. Faithful ports:
  - MATLAB `makedist("Weibull",A,B)` uses (scale=A, shape=B) →
    `scipy.stats.weibull_min(c=B, scale=A)`.
  - MATLAB `makedist("GeneralizedExtremeValue",xi,sigma,mu)`
    / `gevpdf(x,k,sigma,mu)` uses (shape k=ξ, scale σ, location μ) →
    `scipy.stats.genextreme(c=-xi, loc=mu, scale=sigma)` (note scipy's
    GEV shape parameter is negated relative to MATLAB's ξ convention —
    a common, well-documented gotcha worth a code comment).
  - `skewness_weibull(alpha,beta)` has a standard closed form in terms
    of the Gamma function (`scipy.special.gamma`); reconstructible and
    directly checkable against `scipy.stats.weibull_min(...).stats
    ('s')` as an extra cross-check beyond what the source script itself
    does.
  - Build-phase recommendation: implement the "custom" pdf/cdf/quantile
    trio directly from the textbook Weibull/GEV formulas (not just by
    calling `scipy.stats` under a different name), then run the exact
    same `max(abs(custom - scipy))` cross-check the source script runs
    against MATLAB's builtins — preserves the pedagogical intent
    (showing the closed form) while getting the same faithfulness
    guarantee Chapter 11's `quadratic_form` sign-convention check gave.

No other custom/unfamiliar function names were found in any of the 50
scripts beyond MATLAB/Statistics-and-Curve-Fitting-Toolbox/Mapping-
Toolbox builtins (`csaps`, `wblpdf`, `gevpdf`, `makedist`, `movmean`,
`integral`, `wgs84Ellipsoid`, `geodetic2ecef`, `shaperead`, `axesm`,
`geoshow`, `quiver`) — all of which have standard, well-known Python
equivalents (`csaps` package for smoothing splines, `scipy.stats` for
the distributions, `pandas.rolling` for the moving average,
`scipy.integrate.quad`, `pyproj`/manual formulas for geodesy,
`cartopy` for the map-projection scripts, `matplotlib.pyplot.quiver`).

## Proposed notebook split

| Notebook | Scripts | Description | Blockers | Status |
|---|---|---|---|---|
| `12a_crop_climate_indices` | `cid1-3` (3) | GDD calculation; Paredes (2025) crop-calendar table; Zhang (2011) climate-index-definition table. | None (self-contained + 2 fully-readable `.xlsx` fallbacks) | ✅ |
| `12b_geodesy_wind_and_map_projections` | `coordinate1-6`, `data1` (7) | DD/DMS conversion; WGS84 ellipsoid parameters; geodetic→ECEF worked example; 3 world-map projections (Mollweide/Lambert/Wiechel) with land overlay; wind-direction u/v vector-decomposition diagram. | None — resolved via `basemap`/`basemap-data` (offline GSHHS land data) instead of the originally-planned `cartopy` (blocked: this sandbox's network egress refuses cartopy's live Natural Earth download), plus a hand-derived closed-form for Wiechel (confirmed absent from PROJ entirely, not just missing a named `cartopy.crs` wrapper). | ✅ |
| `12c_ipcc_grid_resolution_formulas` | `grid1`, `grid2a-e` (6) | Global grid-box-count estimate; the `R=length(1°)·√(Δφ·Δλ·cosφ)` horizontal-resolution formula evaluated pointwise, plotted continuously, integrated over latitude, and via the shared `compute_horizontal_resolution` helper. | None | ✅ |
| `12d_ipcc_assessment_report_grids` | `grid3a-f` (6) | Per-IPCC-report (FAR through AR7) summary statistics of model grid resolution and vertical-level counts, from the shipped `chap12_ipcc_grid.xlsx`/hardcoded literal arrays. | None (data fully readable via `.xlsx`; `grid3e`/`3f` are pure hardcoded literals) | ✅ |
| `12e_ndgain_country_vulnerability` | `ext_ndgain_country1-5` (5) | ND-GAIN aggregate-vs-sector vulnerability correlation/scatter; vulnerability-vs-readiness scatter (1995 vs 2023); top/bottom-10 country rankings by vulnerability and by overall "gain" score. | None | ✅ |
| `12f_cri_and_ipcc_hazard_impact` | `ext_cri_country1`, `ext_ipcc_hazard_impact1-2` (3) | CRI 2026 fatalities/affected/economic-loss pie charts by hazard; IPCC AR6 regional hazard-impact table (7 indicators × 3 warming levels); top-5 most/least-affected-region rankings per indicator. | None (`ext_ipcc_hazard_impact*`'s numeric `data` loads directly from the `.mat`; only the region-label axis needs the `.xlsx` fallback, confirmed) | ✅ |
| `12g_financial_loss_and_catastrophe_metrics` | `financial_loss2-5b` (8) | Return-period-to-probability conversion and cumulative-loss compounding; Antofie flood/landslide expected-loss curves; ECB physical-risk-score and expected-loss tables (2 scenario pairs each); Mandel capital-at-risk and regional-impact tables. | None. `financial_loss4a`/`4b` and `4c`/`4d` are each near-identical parametrized pairs (only the hazard-scenario filter string differs) — collapse each pair into one helper called twice. `financial_loss5b`'s `T2` needs the `Table 2`⋈`Table 4` join reconstruction documented above. | ✅ |
| `12h_sector_and_corporate_exposure` | `corporate1`, `sector3`, `sector4`, `sector6a`, `sector6b`, `sector7a` (6) | S&P sector physical-risk exposure/sensitivity by scenario; Cline (2007) agricultural GDP impact with/without carbon fertilization; a small hardcoded companion diff table; Munich Re NatCat stacked-loss bar chart + trailing average; Munich Re losses by custom historical sub-period; EIOPA insurance risk-dashboard scores by country/peril. | None. `corporate1`'s `snp_physical_risk.xlsx` needs explicit multi-row-header handling (documented above). | ✅ |
| `12i_extreme_value_distributions` | `statistical_modeling1a-c` (3) | Gaussian/Weibull/GEV hazard-intensity distribution moments; PDF comparison plot with a from-formula-vs-MATLAB-builtin cross-check; return-period/quantile table with forward/inverse consistency check. | Needs the `pdfweibull`/`pdfgev`/`cdfweibull*`/`cdfgev*`/`skewness_weibull` reimplementation-from-formula described above (self-verifying via the source script's own built-in cross-check, low risk). | ✅ |
| `12j_vulnerability_curves` | `vulnerability1-3` (3) | Huizinga flood depth-damage curves by infrastructure type and by region (smoothing-spline fit); Emanuel-style cubic wind-speed damage curve for 3 parameter sets. | None | ✅ |

**Total: 3+7+6+6+5+3+8+6+3+3 = 50**, matching the archive's confirmed
script count exactly. **0 scripts are fully blocked** — every notebook
is buildable end-to-end from data that is either self-contained or has
a confirmed-readable `.xlsx` fallback with a fully-resolved column
mapping.

## Special-case blockers and complications

1. **Map-projection / geospatial dependency (`12b`, `coordinate4-6`,
   3 scripts) — RESOLVED during the `12b` build; noted here for the
   record since the original plan (below) didn't survive contact with
   this sandbox.** MATLAB's Mapping Toolbox (`axesm`/`geoshow`/
   `shaperead`) is used to draw a world map with a land-area overlay in
   three different projections (Mollweide, Lambert conformal conic, and
   the more exotic "Wiechel" polar pseudoazimuthal projection).
   - `landareas.shp` (the land-boundary shapefile the scripts read) is
     a MATLAB Mapping-Toolbox example-data file, not shipped in this
     archive. The originally-planned substitute, `cartopy.feature.LAND`
     (Natural Earth data), **was confirmed blocked**: this sandbox's
     network egress refuses the live Natural Earth shapefile download
     cartopy needs (`403 Forbidden`), even after installing `cartopy`
     itself successfully via pip. The `basemap`/`basemap-data` PyPI
     packages were used instead — `basemap-data`'s wheel bundles GSHHS
     coastline data directly (no runtime download), and `Basemap`
     draws `'moll'` (Mollweide) and `'lcc'` (Lambert conformal conic —
     substituted for the scoping-phase guess of "Lambert azimuthal
     equal-area"; the source script just calls `axesm('lambert',...)`,
     which is MATLAB's conformal-conic Lambert) directly.
   - The scoping-phase assumption that Wiechel is "a real PROJ
     operation (`+proj=wiechel`)" was **wrong** — checked directly
     against pyproj's full `get_proj_operations_map()` (184 entries)
     and it's genuinely absent, not just missing a named
     `cartopy.crs` convenience wrapper. Wiechel also isn't a `Basemap`
     projection. It was implemented by hand from its closed-form
     polar-aspect equations (sourced via web search against a HandWiki
     mirror of the Wikipedia article, since the primary Wikipedia page
     renders its formulas as un-scraped images/MathML — the result was
     verified independently by confirming $x^2+y^2=2R^2(1-\sin\varphi)$
     algebraically, the same radial equal-area function as the polar
     Lambert azimuthal projection Wiechel is derived from). Land
     polygons for the Wiechel plot come from the same `basemap-data`
     GSHHS data, extracted as raw (lon, lat) vertices via a
     plate-carree (`'cyl'`) `Basemap` instance (whose projected x/y
     equal unprojected lon/lat, a convenient extraction trick) and then
     transformed through the hand-derived formula.
   - `coordinate2`/`coordinate3` also touch the Mapping Toolbox
     (`wgs84Ellipsoid`, `geodetic2ecef`) but only as a **cross-check**
     against formulas the scripts already derive by hand — `pyproj`
     (`Transformer.from_crs("EPSG:4979","EPSG:4978")`) reproduces
     `geodetic2ecef` exactly (verified to the mm level against the
     hand-derived formula for the Paris worked example).

2. **Filename case-sensitivity** (cosmetic, not a blocker):
   `cid2.m`/`cid3.m` request `chap12_2025_paredes.mat`/
   `chap12_2011_zhang.mat` (lowercase), but the shipped files are
   `chap12_2025_Paredes.mat`/`chap12_2011_Zhang.mat` (capitalized).
   Silently case-insensitive on the original Windows/MATLAB
   environment; needs an exact-case path on a Linux build.

3. **`ext_ecb_physical_risk`'s +1 column-index offset** (documented in
   the data-verification table above) — a real trap for anyone building
   `financial_loss4a-4d` from the `.xlsx` without reading the loader
   script first: the visually "first" named column in the exported
   sheet (`hzrd_typ`) is actually MATLAB table column **2**, not column
   1, because of a leading blank-header column that survives the
   export. Get this wrong and `T{:,17:20}` silently points at the wrong
   4 columns without erroring.

4. **`financial_loss5b`'s `T2 = join(Table2, Table4)`** (documented
   above) — without reading `Data/chap12_ext_mandel.m`, this script
   looks like it needs an 11-column table that doesn't exist anywhere
   in the shipped `.xlsx` (`Table 2` alone only has 6 columns) and
   could easily be mis-flagged as blocked. It isn't — it's a
   reconstructable join on the shared `Region` key.

5. **No licensed/paid-data dependency and no NetCDF dependency found**
   anywhere in this chapter's 50 scripts, despite the subject matter
   (IPCC/CMIP climate grids, reanalysis-adjacent framing) — everything
   is small tabular/scalar data or hardcoded literals. The one large
   file (`chap12_ext_eiopa_dashboard.xlsx`, 5.6 MB) is a public EIOPA
   dashboard export and reads fine with `pandas`.

6. **`grid3e`/`grid3f`'s use of MATLAB `global` variables** plus
   `eval(strcat("L_AR",num2str(ar),"_AGCM"))` to dynamically look up a
   variable by constructed name — a MATLAB idiom with no direct Python
   analog; the natural port is a plain Python `dict` keyed by
   assessment-report number (`{1: {"AGCM": [...], "OGCM": [...]}, ...}`)
   passed into `grid_analyze(ar)` instead of relying on globals+`eval`.
   Purely a translation-style note, not a blocker.

7. **`sector4`'s hardcoded 4×4 table has no labels or surrounding
   context in the source `.m` file** (no `disp` header, no variable
   names beyond `data`/`diff`) — the notebook build will need to infer
   reasonable axis/column labels from the chapter text (Cline 2007
   carbon-fertilization theme, given its position right after
   `sector3`) rather than from the script itself, since the script
   genuinely doesn't say what the 4 columns represent.

## Progress notes

**`12a_crop_climate_indices`** (`cid1-3`, 3 scripts) — built and verified
0 errors / 0 stderr warnings. All three scripts are LaTeX reference-table
builders (`ftosa`/`strcat2`/`latex_tabular` + `disp()`); per this series'
established convention (`08g`, `05d`, `10d`) they're rendered as pandas
`DataFrame`s rather than reproducing raw LaTeX markup. `cid1` is a
self-contained 7-day growing-degree-days arithmetic exercise (no data
file). `cid2` and `cid3` are the first confirmation of the chapter-wide
MATLAB-`table`-MCOS-opacity finding in practice: both `.mat` files load as
opaque blobs via `scipy.io.loadmat`, and both loader scripts
(`Data/chap12_2025_Paredes.m`, `Data/chap12_2011_Zhang.m`) were followed
exactly against the verified-readable `.xlsx` siblings, which are now
copied into the repo's `data/` folder. `cid2`'s `Name`/`Species` split
(from the loader's `extractBefore`/`extractBetween` on `"Name (Species)"`)
was ported with a single regex; `cid2`'s `Season`-label abbreviation
dictionary and `cid3`'s `"C"` &#8594; `°C` units substitution (kept as a
plain Unicode degree symbol rather than the source's LaTeX `$^{\circ}
\mathrm{C}$`, since the notebook displays directly) both matched the
source scripts' `replace()` calls one-for-one on manual inspection of the
raw `.xlsx` values. No bugs found; no functions flagged as newly reusable
beyond those already in the custom-function inventory above.

**`12b_geodesy_wind_and_map_projections`** (`coordinate1-6`, `data1`,
7 scripts) — built and verified 0 errors / 0 stderr warnings. The chapter's
one real "needs a substitute library" complication, and it needed more
improvisation than scoped: `cartopy`'s live Natural Earth download is
blocked by this sandbox's network egress (`403 Forbidden`, confirmed after
`cartopy` itself installed fine via pip), so `coordinate4`/`coordinate5`
(Mollweide, Lambert conformal conic) were rebuilt on `basemap`+
`basemap-data` instead — the latter bundles GSHHS coastline data directly
in its wheel, so no network access is needed at all. `coordinate6`
(Wiechel) turned out to need a genuine from-scratch implementation: the
scoping report's assumption that `+proj=wiechel` is a real PROJ operation
was wrong (confirmed against pyproj's full 184-entry
`get_proj_operations_map()` — it just isn't there, and it isn't a
`Basemap` projection either), so it's built from the closed-form
polar-aspect equations
$x=R(\sin\lambda\cos\varphi-(1-\sin\varphi)\cos\lambda)$,
$y=-R(\cos\lambda\cos\varphi+(1-\sin\varphi)\sin\lambda)$, sourced via web
search (the primary Wikipedia article's formulas render as un-scraped
images, so a HandWiki mirror was used instead) and independently verified
by confirming algebraically that $x^2+y^2=2R^2(1-\sin\varphi)$ — the same
radial equal-area function as the polar Lambert azimuthal projection
Wiechel is derived from, which is exactly the "area-preserving polar
transform" relationship the Wikipedia article describes in prose. Land
polygons for the Wiechel plot reuse the same `basemap-data` GSHHS
geometry, extracted as raw unprojected (lon, lat) vertices via a neat
trick: a plate-carree (`'cyl'`) `Basemap` instance's projected x/y
coordinates equal raw lon/lat, so `.landpolygons[i].boundary` recovers the
underlying vertex data without needing any of Basemap's own projection
machinery. `coordinate2`/`coordinate3`'s WGS84-ellipsoid and
geodetic-to-ECEF hand formulas were cross-checked against `pyproj`
(`Transformer.from_crs("EPSG:4979","EPSG:4978")`) and matched to the mm
level on the Paris worked example. One cosmetic bug caught on visual
review: the wind-compass diagram's title initially overlapped the
"North ($v_+$)" axis label — fixed with `pad=28` on `ax.set_title`. Two
new dependencies added to `requirements.txt`: `pyproj`, `basemap`/
`basemap-data` (superseding the scoping doc's `cartopy` assumption).

**`12c_ipcc_grid_resolution_formulas`** (`grid1`, `grid2a-e`, 6 scripts) —
built and verified 0 errors / 0 stderr warnings, no data dependencies. A
clean confirmation exercise: `grid2c`'s integral of $\sqrt{\Delta\varphi
\cdot\Delta\lambda\cdot\cos\varphi}$ at $\Delta\varphi=1°$ over
$[0,\pi/2]$, averaged, evaluates to exactly `0.7628` — the same constant
`grid2d`/`grid2e` use as the hardcoded `R_avg = 0.7628 * ...` shortcut,
confirming that constant *is* this integral rather than an unrelated
empirical fudge factor. One authentic (not a bug) discrepancy noted for
the record: `grid2d`'s $R_{avg}$ column and `grid2e`'s $R_{avg}$ column
disagree by 1 km at $\Delta\varphi=2.8°$ (237 vs. 238) — `grid2d` computes
`length_phi = pi*R/180` at full precision while the shared
`compute_horizontal_resolution` helper hardcodes `length_phi = 111.2`, so
the two scripts' underlying constant differs in the 3rd decimal place and
occasionally flips a rounding boundary; this is a faithful reproduction
of an inconsistency that exists in the source `.m` files themselves, not
a porting bug, and is noted here rather than silently "fixed." Introduced
`compute_horizontal_resolution` as a shared helper (matches the archive's
own `compute_horizontal_resolution.m`, used again by `grid3*` in `12d`).

**`12d_ipcc_assessment_report_grids`** (`grid3a-f`, 6 scripts) — built and
verified 0 errors / 0 stderr warnings, no data blockers. `grid3a-d` (one
assessment report each: FAR/SAR/TAR/AR4) collapsed into a single
parametrized `analyze_ar_sheet(sheet, has_ocean)` loop, since all four are
the same computation over a different sheet of `chap12_ipcc_grid.xlsx` —
FAR skips the ocean-resolution block via `has_ocean=False` since its
`O_Resolution` column is entirely missing (ocean components weren't
consistently gridded/reported for FAR-era models). Ported the archive's
own `Resolution_to_Angular`/`Rhomboidal_to_Angular`/`Triangular_to_Angular`
/`Format_Angular` (`Data/chap12_ipcc_grid.m`) as one `resolution_to_angular`
function handling all three grid-resolution notations (`"R21"` rhomboidal,
`"T63"` triangular, `"2.5°x3.75°"` plain angular) that appear across the
`A_Resolution`/`O_Resolution` columns. `grid3e`/`grid3f`'s MATLAB
`global`+`eval(strcat("L_AR",num2str(ar),"_AGCM"))` variable-name-building
idiom (selecting one of several hardcoded literal arrays by assessment-report
number) ported directly as a Python dict keyed by AR number — no `eval`
needed. **Genuine source data inconsistency found and disclosed** (not a
porting bug): `grid3e`'s hardcoded AR4 atmosphere-level literal has `32`
for the 4th model (`CGCM3.1`, `T47` variant), while the same model's level
count in `chap12_ipcc_grid.xlsx`'s `AR4` sheet (used by `grid3d`) reads
`31` — everything else in both AR4 datasets matches exactly. This is an
inconsistency between two independently-maintained copies of the same
figure in the source archive itself (the hardcoded script literal vs. the
spreadsheet), not introduced by this port; both values are reproduced
faithfully as-is (`grid3d`'s stats use the spreadsheet's `31`, `grid3e`'s
stats use the literal's `32`), matching what each MATLAB script would
itself produce.

**`12e_ndgain_country_vulnerability`** (`ext_ndgain_country1-5`, 5
scripts) — built and verified 0 errors / 0 stderr warnings, no data
blockers (all 12 ND-GAIN sheets load cleanly via `pandas.read_excel`, no
MCOS opacity issue here since we read straight from the `.xlsx` rather
than the `.mat`). **Data-indexing quirk caught and disclosed, not
silently fixed:** every one of the 5 scripts indexes country rows via
MATLAB's `T{2:end,pos}`, which — since `T`'s row 1 is Afghanistan
(alphabetically first, confirmed via `openpyxl` raw-cell inspection, no
hidden header/aggregate row involved) — deliberately or accidentally
excludes Afghanistan from every correlation, scatter, and ranking in this
notebook. Reproduced faithfully (`.iloc[1:]`) rather than corrected, so
the tables/figures match what the source `.m` scripts themselves
produce; flagged prominently in the notebook's intro markdown rather than
buried. All rankings sanity-checked against real-world knowledge of the
published ND-GAIN Country Index: the `ext_ndgain_country5` "highest Gain
score" top 10 (Norway, Finland, Switzerland, Denmark, Sweden, Singapore,
New Zealand, UK, Germany, Australia) and "most vulnerable" top 10 from
`ext_ndgain_country4` (Chad, Niger, Solomon Islands, Micronesia,
Guinea-Bissau, Sudan, Somalia, Tonga, Sierra Leone, Eritrea) both match
published ND-GAIN rankings closely, and the vulnerability-readiness
correlation (`ext_ndgain_country3`, roughly $-0.6$ in both 1995 and 2023,
collapsing to near-zero when restricted to already-highly-vulnerable
countries) is a substantively plausible finding, not just
internally-consistent numbers. One cosmetic matplotlib warning caught and
fixed on first run: passing both `facecolors` and `edgecolors` to
`scatter` for `'x'`/`'*'` marker styles (which have no separate fill)
triggered a `UserWarning` — fixed by using plain `color=` for those two
marker styles instead.

**`12f_cri_and_ipcc_hazard_impact`** (`ext_cri_country1`,
`ext_ipcc_hazard_impact1-2`, 3 scripts) — built and verified 0 errors /
0 stderr warnings, no data blockers. Ported the archive's own
`Data/chap12_ext_ipcc_hazard_impact.m` loader faithfully: 7 indicators
(`TXx`, `TNn`, `Rx1day`, `Rx5day`, `Moisture`, `Moisture10`, `CDD`) each
from their own sheet (`SM2`-`SM8`) at 3 global-warming levels, with
`Rx1day`/`Rx5day` rescaled ×100 (stored as fractions) and a `-99`
missing-data sentinel replaced with `NaN`; added an explicit
region-consistency assertion across all 7 sheets matching the source's
own `all(region == row2)` check (passed on the real data). **One real bug
caught and fixed during the build:** the first pass at
`ext_cri_country1`'s share table constructed the `pandas.DataFrame` with
`index=labels` while its input `Series` still carried their original
`0..5` integer index from the source table — pandas silently reindexed
every column to all-`NaN` (string labels don't match an integer index),
which only surfaced downstream as a cryptic matplotlib
`ValueError: cannot convert float NaN to integer` deep in the pie-chart
tight-bbox layout code, not as a visible NaN in the printed table (which
was checked and looked fine before the mistake was made — the bug was
introduced fixing something else and only caught by the plot actually
failing to render). Fixed by building the `DataFrame` first, then
assigning `.index = labels.values` afterward. `ext_ipcc_hazard_impact1`'s
row reordering (moving Greenland/Iceland to sit beside the two Antarctica
rows at the end) and `ext_ipcc_hazard_impact2`'s top-5 rankings were
cross-checked against real-world IPCC AR6 Interactive Atlas knowledge:
`TNn` (coldest-night warming) top regions are all high-latitude
(NE/NW North America, Russian Arctic, Russian Far East) — matches the
well-known Arctic-amplification finding; `Moisture`/`Moisture10` (drying)
top regions are Mediterranean/Central-and-South-America — matches known
IPCC drying hotspots; `Rx1day` (extreme 1-day precipitation) top regions
are all African/Arabian — matches known monsoon-intensification findings.
Substantively plausible, not just internally consistent.

**`12g_financial_loss_and_catastrophe_metrics`** (`financial_loss2-5b`,
8 scripts) — built and verified 0 errors / 0 stderr warnings, no data
blockers. This notebook exercises two of the trickiest data-mapping
issues flagged in the scoping report, both handled by **referencing
columns by name rather than by MATLAB's 1-based position**, sidestepping
the risk entirely rather than trying to get the position arithmetic
exactly right: `ext_ecb_physical_risk`'s leading unnamed index column
(confirmed to shift `T{:,17:20}`/`T{:,[11 13]}` by exactly one position
relative to the visible column headers — position 17 does land on
`physcl_rsk_scr0_prcntg_ptfl` as predicted, confirming the offset's
source), and `ext_mandel`'s `Table 2`/`Table 4` join (reproduced with
`pandas.merge(..., on="Region", how="inner")`, confirmed to produce the
same 13x11 shape the source's `join()` does). `financial_loss4a/4b` and
`4c/4d` collapsed into one parametrized helper each
(`ecb_risk_score_table(hzrd_typ)`, `ecb_loss_table(hzrd_typ)`), called
twice with the historical vs. projected-scenario filter string. Results
sanity-checked against real-world knowledge: the Netherlands shows by far
the highest coastal-flood expected loss (5.2-5.7% of portfolio, both at
maturity and projected to worsen under RCP8.5) of any country in
`financial_loss4c/4d` — a strong, substantively correct signal given the
Netherlands' below-sea-level coastal geography, not just an
internally-consistent number. `financial_loss5a`'s `sortrows(T,2)` (sort
by the `Statistic` column) reproduced via
`sort_values("Statistic", kind="stable")`, confirmed to correctly group
all 3 "Mean" rows before all 3 "Q99" rows while preserving each group's
original scenario order (relied on for the script's subsequent
`T{1:3,:}`/`T{4:6,:}` slicing into `EL`/`VaR`).

**`12h_sector_and_corporate_exposure`** (`corporate1`, `sector3`, `sector4`,
`sector6a`, `sector6b`, `sector7a`, 6 scripts) — built and verified 0
errors / 0 stderr warnings, no data blockers. `corporate1`'s scoped-out
3-row merged-header complication was resolved as anticipated:
`chap12_snp_physical_risk.xlsx`'s scenario sheets (`Medium 2030`,
`Medium 2050`, `High 2050`) each have a scenario-group label row, a
Weights/Exposure-Risk/Sensitivity-Risk sub-group row, then the real
`Sector`/`DM`/`EM` header row — read directly with `header=2` (0-indexed)
on `pandas.read_excel` rather than the previously-scoped
`skiprows`/MultiIndex approach, which turned out simpler and matched
`T{:,4:7}`'s columns exactly (`Exposure_DM/EM`, `Sensitivity_DM/EM`). A
sheet-name case mismatch was found and fixed the same way as the earlier
`chap12_2025_Paredes`/`chap12_2011_Zhang` filename-casing issue: the
source `sector3.m` script requests sheet
`'data'` (lowercase) but the shipped `chap12_ext_cline_2007.xlsx` sheet is
actually named `Data` (capital D) — matched case-insensitively on the
original Windows/MATLAB environment, so the Python port uses the correct
`"Data"` case directly. `sector4`'s hardcoded 4x4 table (flagged in the
scoping doc as having no labels or context in the source `.m`) was
reproduced exactly as computed, with generic `Col 1-4` labels rather than
invented ones, and the lack of provenance disclosed in the notebook
markdown per the chapter's stated convention. `sector7a`'s EIOPA
country x peril nested-loop construction (31 countries x 5 perils, taking
`max` of `Historical_score` across all `DB_version` vintages 2022-2025 for
the historical column and `Estimated_score` at `DB_version==2025` for the
current column, with `-9` "not applicable" sentinels replaced by `NaN`)
matched the source script's logic exactly and produced substantively
plausible output on inspection: Austria (landlocked) correctly shows `NaN`
for Coastal Flood, and the `Total (2025)` column ranges roughly 4-12,
consistent with EIOPA's published 0-10-ish risk-score scale. The Munich Re
stacked bar chart (`sector6a`) was visually verified: green (insured) and
blue (uninsured, stacked on top so the bar's full height reads as total
"overall" losses) bars plus a red 10-year trailing moving average
(`.rolling(window=11, min_periods=1).mean()`, matching MATLAB's
`movmean(x,[10 0])`) show clear loss spikes at 2005 (Katrina), 2011
(Japan earthquake/tsunami), 2017 (Harvey/Irma/Maria), and 2022 (Ian) —
all well-known major catastrophe years — with a genuine upward trend in
the moving average, consistent with the well-documented rise in global
catastrophe losses over the period rather than an artifact of the port.
`sector6b`'s uninsured-share aggregates (55-83% across the various
decade/custom-window periods) are also in a plausible range for the
historically well-known natural-catastrophe "protection gap."

**`12i_extreme_value_distributions`** (`statistical_modeling1a-c`, 3
scripts) — built and verified 0 errors / 0 stderr warnings, no data
dependencies. This notebook exercises the chapter's one genuinely
"reimplement a nontrivial statistical model from formula" case, exactly
as scoped: `pdfweibull`/`cdfweibull`/`cdfweibulli` and
`pdfgev`/`cdfgev`/`cdfgevi`/`skewness_weibull` don't exist anywhere in
the archive, so they were written directly from the textbook Weibull/GEV
pdf/cdf/quantile/skewness closed forms (MATLAB `(scale, shape)` Weibull
convention; MATLAB `(shape ξ, scale σ, location μ)` GEV convention, with
scipy's GEV shape sign negated relative to MATLAB's ξ). The build
reproduced the source scripts' own verification logic and got the same
result: `max|pdfweibull - scipy.stats.weibull_min.pdf|` and
`max|pdfgev - scipy.stats.genextreme.pdf|` both landed at ~1e-17
(machine precision), and the `1c` return-period table's forward
(`cdf`) → inverse (`cdfi`) round trip (`p_check` vs. the original
`alpha`) matched to ~1e-16 — as close to a formal proof of correctness
as this series gets without a citation to a textbook table. Skewness
cross-check: the hand-derived `skewness_weibull(280,14) = -0.7651`
matches `scipy.stats.weibull_min(...).stats('s')` exactly. Substantive
sanity check beyond the numerical cross-checks: the GEV's return periods
at wind speeds 300/310/320 km/h (20-42 years) are dramatically shorter
than the Gaussian's at the same speeds (161-4299 years) — a real,
expected consequence of the GEV's heavier right tail (`xi_gev=0.15>0`,
Fréchet-type) vs. the Gaussian's thin tail, visually confirmed in the
PDF plot (GEV's long right tail past 300 km/h vs. the Gaussian's near-zero
density there) rather than just an artifact of the port. The Weibull's
negative skewness is also visually consistent with the plotted curve's
long left tail / sharp right cutoff.

**`12j_vulnerability_curves`** (`vulnerability1-3`, 3 scripts) — built and
verified 0 errors / 0 stderr warnings. This is the final Chapter 12
notebook: with `12j` complete, all 50 `chap12_*.m` exercise scripts
across `12a`-`12j` are accounted for, 0 blocked by missing or unreadable
data. `vulnerability1`/`vulnerability2` reuse the same weighted-endpoint
`csaps` smoothing-spline pattern established in `12g`'s
`financial_loss3`. **One real indexing bug caught before it shipped**:
the source `.m` sorts the 6 infrastructure-type/region columns by
`damage(5,:)` (MATLAB 1-indexed row 5), which is the **2m**-depth row
(`depth = [0, 0.5, 1, 1.5, 2, 3, 4, 5, 6]`, so row 5 = the 5th value =
2.0), *not* the 5m-depth row the initial scoping-doc description implied
— caught by cross-checking the actual `Depth` column values against the
row index during the build (not caught by nbconvert, since either index
choice executes without error — a good example of why output-plausibility
review matters beyond exception-absence) and fixed to the correct
0-indexed row 4. `vulnerability1` fixes the region at "Europe" (the
source script's `region(indx=1)`, with `indx` never varied despite the
variable's name suggesting a loop) while comparing across the 6
infrastructure types; `vulnerability2` fixes the infrastructure type at
"Residential buildings" (the first group in the table, and the one whose
`Global` column happens to be entirely `NaN` — irrelevant here since
`T{:,3:end-1}` excludes `Global` from this script's column range anyway)
while comparing across the 6 regions. Both figures are substantively
plausible: Transport/Agriculture accumulate flood damage fastest across
infrastructure types (consistent with lighter, more damage-prone
structures), Industrial buildings are the most resilient (consistent
with heavier-duty construction), and all 6 region-split residential
curves are smooth and monotonic 0-100%. `vulnerability3`'s parametric
Emanuel-style cubic wind-damage curve was cross-checked visually: for
all 3 `(w_-, w_{1/2})` parameter sets, the plotted curve passes exactly
through its own `(w_-, 0)` circle and `(w_{1/2}, 50)` diamond markers,
confirming the closed-form `D(w) = upsilon^3/(1+upsilon^3)` was ported
correctly (only the source's `units==1`, km/h, branch is exercised, per
the scoping doc's note that the other 3 unit-convention branches are
unreachable as the script is written). One missing house-palette color
(`color_orange`, used by all 3 scripts' 6-color palette) was added as a
literal hex (`#ffa500`, matching `init_color.m`'s `[255 165 0]/255`
RGB) rather than approximated.

**Chapter 12 (Physical Risk) is now complete: `12a`-`12j`, all 50
scripts accounted for, 0 blocked.**

## Working conventions (same as the rest of the series)

- Faithful `.m`-to-Python translation via the `build_XXn.py` throwaway-
  script pattern; execute with `nbclient`, confirm 0 errors/0 stderr
  warnings, visually spot-check every figure before finalizing.
- Missing custom toolbox functions get reimplemented transparently with
  an explicit derivation/provenance caveat in the notebook markdown —
  and where a script's behavior depends on ambiguous data-file column
  mapping, the exact source `.m` (and, for this chapter, the `Data/
  chap12_*.m` loader script) is read directly before building rather
  than inferred from a survey summary alone.
- Near-duplicate/parametrized-variant scripts get collapsed into one
  shared Python helper function called multiple times, rather than
  duplicated — flagged per-notebook above (`financial_loss4a/4b`,
  `financial_loss4c/4d`, `grid3b/3c/3d`, `grid3e/3f`).
- 0 errors, 0 stderr warnings, AND actual-output-sanity (not just
  exception-absence) is the verification standard for every notebook —
  two real bugs in Chapter 11 (`11a`'s rank-deficient constraints,
  `11c`'s sign convention) were caught only by scrutinizing printed
  numeric output for plausibility, not by the absence of exceptions.
- Every genuinely blocked script gets flagged explicitly rather than
  silently skipped or faked — though this chapter, unusually, has none.
- Never run git directly — hand the user exact commands to run
  themselves.
- Deliver + sync every artifact to the user's Mac via `SendUserFile` +
  `mcp__remote-devices__device_commit_files`, and save scoping-doc
  updates to the attached claude.ai Project via `Projects.project_write`.
