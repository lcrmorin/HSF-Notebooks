# Session handoff — HSF MATLAB → Python translation project

Read this first in any new session before doing anything else. It's the
continuity note for a long-running project translating Thierry Roncalli's
`hfs-archive` MATLAB/GAUSS toolbox (companion to *Handbook of Sustainable
Finance*) into Python — both the core toolbox and a companion set of
Jupyter notebooks walking through the book chapter by chapter.

## The three repos

- **`QuantToolBox`** — Python port of the core MATLAB toolbox. Cloud
  mirror lives at `/root/work/qtb/QuantToolBox` and has **no `.git`** —
  any git operation on this repo must be handed to the user as exact
  commands to run themselves, never executed directly by Claude.
- **`hsf-matlab`** — read-only reference clone of the original MATLAB
  source. Only ever read from, never written to. On the user's Mac at
  `~/Desktop/hsf_project/hsf-matlab`; staged copies used for reading
  land under `/mnt/user-data/uploads/hsf_project/hsf-matlab/HSF/`.
- **`hsf-notebooks`** — the Jupyter-notebook companion. Cloud working
  copy at `/root/work/hsf-notebooks`, pulled from the user's Mac at
  `~/Desktop/hsf_project/hsf-notebooks`. This one **does** have a real
  local `.git`, but git commands are *still* always handed to the user
  as exact commands to run themselves — never run directly by Claude,
  even though the repo exists locally.

The user's Mac is reached through the device bridge
(`mcp__remote-devices__*` tools) — it's only reachable while the Claude
desktop app is open and connected; if a tool call fails with "device not
connected," retry once, and if it still fails just tell the user and
wait, don't hammer it.

## Standing conventions (do not deviate without being told)

- **Never run git commands directly** in either repo. Always give the
  user the exact `git add` / `git commit` / `git push` commands as a
  code block and let them run it themselves.
- **Never use `git add -A`** — always add specific files by name.
- **`device_bash` cannot delete files** — only `mv` into a `_to_delete/`
  subfolder, then tell the user what was moved there.
- **Notebook build pattern**: write a throwaway `build_XXn.py` script in
  `/root/work/hsf-notebooks/` using `nbformat`/`nbclient`
  (`new_notebook()`/`new_code_cell()`/`new_markdown_cell()`), execute it
  end-to-end with `NotebookClient(nb, timeout=180,
  kernel_name="python3").execute(cwd="notebooks/hsf")`, check for 0
  errors and 0 warnings, spot-check a few rendered figures visually
  (extract PNG output, `Read` the file), validate with
  `nbformat.validate(nb)`, **delete the build script** once the
  notebook is written, then deliver.
- **House style inside notebooks**: `plt.rcParams["figure.facecolor"] =
  "white"`, `axes.spines.top`/`right = False`, `DATA_DIR =
  "../../data"`, markdown section headers `## N. Title` /
  `### N.M Subtitle` with "From `chapN_xxx.m`" provenance notes tying
  every section back to its source script(s).
- **Gotchas already hit and fixed**: triple-double-quote docstrings
  inside a `code(r"""...""")` build-script cell break the outer raw
  string — use `#` comments instead, never docstrings, inside notebook
  cell source. `numpy` 2.4.4 removed `np.trapz` — use
  `scipy.integrate.trapezoid`. `\%` outside LaTeX mathtext renders with
  a visible backslash in matplotlib — use plain `%`. Matplotlib's inline
  backend auto-displays-and-closes the current figure at the end of
  every cell — build any multi-panel figure entirely within ONE code
  cell, never split across cells. Calling `ax.set_xticks(...)` with tick
  values outside a just-set `ax.set_xlim(...)` can silently expand the
  view to include them (a matplotlib autoscale quirk) — call
  `set_xlim` *after* `set_xticks` when reproducing a source figure whose
  own tick range extends past its axis limits.
- **`quanttoolbox` is not preinstalled in a fresh cloud container** —
  each new session needs `pip install quanttoolbox --break-system-packages`
  before any notebook that imports it (most of Chapters 2-4, and
  `09e_emission_trend_forecasting`) will execute. Discovered the hard
  way in the Chapter 9 session: a `python3 -c "import quanttoolbox"`
  check failed with `ModuleNotFoundError` even though earlier notebooks
  in the same conversation clearly used it successfully — that earlier
  "success" was a false read (a markdown-only first cell, not an actual
  import test), not evidence the package was really available. Always
  verify with a real import check before trusting that a notebook using
  `quanttoolbox` will build cleanly in a new container.
- **Data-provenance philosophy**: read real source data directly via
  `pandas.read_excel` rather than fabricating or hardcoding it, inferring
  column semantics from the *consuming* script's own variable/legend
  names, not guesswork. When a `.m` script's data dependency genuinely
  isn't present anywhere in the repo (proprietary panel data, etc.), the
  section is skipped entirely and the omission is documented in both the
  notebook's intro markdown and in `CHAPTERS.md` — never fabricate a
  substitute. When a source spreadsheet itself has a data-quality
  artifact (e.g. a garbled row), leave it as-is and note it rather than
  guess-fixing.
- **Near-duplicate vintage scripts** (e.g. `..._2022.m` vs `..._2023.m`
  reproducing the same figure from an updated data cut): consolidate to
  the most recent vintage only, and say so in `CHAPTERS.md`. Only build
  multiple vintages side by side when they genuinely carry different
  content that no single vintage covers alone (documented per-case in
  `CHAPTERS.md` when this happens — see the 4c row for an example).
- **Packaging-candidates policy**: notebook-local helper functions stay
  inline (not ported into `quanttoolbox` immediately) and get tracked in
  `PACKAGING_CANDIDATES.md` with status 🔵 (candidate, used once so far)
  / 🟡 (confirmed reusable, used in ≥2 notebooks) / ✅ (packaged). A
  function is only promoted to 🟡 once a *second* notebook actually
  reuses it — not on the first plausible-looking use. **No decision
  about porting anything into `quanttoolbox` should be made yet** — this
  is deferred to the end of the whole project, and requires "looking
  elsewhere" (e.g. scikit-learn, scipy) first before assuming a bespoke
  implementation is needed.
- **Delivery pattern for every completed notebook**: `SendUserFile` on
  the notebook + updated `CHAPTERS.md` + `PACKAGING_CANDIDATES.md` (+ any
  new `data/*.xlsx` files used), then
  `mcp__remote-devices__device_commit_files` to write them into
  `~/Desktop/hsf_project/hsf-notebooks/...` on the user's Mac (mirroring
  the same relative paths), then give the user the exact git commands.
  If a batch has many files, split `device_commit_files` calls into
  groups of ~5-6 — a single call with too many files can time out.

## Progress so far

Tracked authoritatively in `hsf-notebooks/CHAPTERS.md` — always read
that file fresh at the start of a new session rather than trusting this
summary's snapshot, since it's updated after every notebook. As of this
handoff:

| # | Chapter | Status |
|---|---|---|
| 0 | Tutorial | ✅ |
| 1 | Introduction | ✅ |
| 2a | ESG Scoring — Ratings & transitions | ✅ |
| 2b | ESG Scoring — Scoring methodology | ✅ |
| 3a | ESG Investing — Risk premia & factor models | ✅ |
| 3b | ESG Investing — Pastor-Stambaugh, Pedersen & tracking error | ✅ |
| 3c | ESG Investing — Performance measurement | ✅ |
| 4a | ESG Products — Market overview, labels & regulation | ✅ |
| 4b | ESG Products — The GSS bond market | ✅ |
| 4c | ESG Products — The greenium | ✅ |
| 4d | ESG Products — Real assets & impact investing | ✅ |
| 5 | Impact Investing | ⬜ — 163 scripts, **largest chapter by far** |
| 6 | Engagement | ⬜ — 32 scripts |
| 7 | Accounting | ⬜ — 0 `.m` scripts, likely a discussion-only chapter, confirm before deciding whether it needs a notebook at all |
| 8 | Economic Modeling | ⬜ — 264 scripts, largest overall; likely needs `quanttoolbox.sustainable_finance.climate` (DICE model etc.) |
| 9 | Risk Measures | ⬜ — 52 scripts, carbon budget/intensity/offsetting — likely needs `quanttoolbox.sustainable_finance.carbon` |
| 10 | Transition Risk | ⬜ — 43 scripts |
| 11 | Portfolio Optimization | ⬜ — 80 scripts, decarbonization-constrained construction, builds on `quanttoolbox.portfolio` |
| 12 | Physical Risk | ⬜ — 70 scripts |
| 13 | Stress Testing | ⬜ — 37 scripts |
| 14 | Conclusion | ⬜ — empty folder, confirm whether it has any content |
| 15 | Technical Appendix | ⬜ — 17 scripts |
| 16 | Exercise Solution | ⬜ — 10 scripts |
| 17 | Data | ⬜ — empty folder, likely just a dataset pointer, not a real chapter |

Given Chapter 5's size (163 scripts — by far the largest chapter tackled
so far, more than 4x chapter 4's total), it will almost certainly need
splitting into several sub-notebooks (5a, 5b, 5c, ...) the same way
chapters 2, 3, and 4 were. Scope it the same way those were scoped:
stage and read every `.m` script plus its `Data/*.m` prep scripts first,
identify which have real backing data vs. which are illustrative/
hardcoded, identify vintage duplicates to consolidate, *then* decide the
notebook split — don't guess the split before reading the source.

## Outstanding git commits (as of this handoff)

Two batches may still be uncommitted on the user's Mac — check
`git status` / `git log` there first rather than assuming:

1. **3b**: `notebooks/hsf/03b_pastor_pedersen_te.ipynb`, `CHAPTERS.md`,
   `PACKAGING_CANDIDATES.md`
2. **Chapter 4 (4a-4d)**: 4 notebooks, `CHAPTERS.md`,
   `PACKAGING_CANDIDATES.md`, and 11 `data/chap4_*.xlsx` files (esg_market
   1/3/4, CBI_data 1/2/4_2023, greenium 1_2023/1_2024/2, real_asset 1/2)

All of these files were already written to
`~/Desktop/hsf_project/hsf-notebooks/` via the device bridge — they just
may not be committed yet. The exact commands were given to the user in
chat; if lost, reconstruct from `git status` in that repo.

## First steps in a new session

1. Read `hsf-notebooks/CHAPTERS.md` and `PACKAGING_CANDIDATES.md` fresh
   (either from the Mac via the device bridge, or re-pull the cloud
   working copy) to confirm current status hasn't drifted from this
   snapshot.
2. Check `git status` / `git log` in `~/Desktop/hsf_project/hsf-notebooks`
   (hand the user the command, don't run it) to see if the two batches
   above are actually still pending.
3. Ask the user whether to continue with Chapter 5, or whatever they'd
   like next — don't assume without checking, since a lot can happen
   between sessions.
