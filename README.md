# hsf-notebooks

Jupyter notebook companion to Thierry Roncalli's *Handbook of Sustainable
Finance* (the `HSF/` material in
[`hfs-archive`](https://github.com/lcrmorin/hfs-archive)), rebuilt on top of
[`quanttoolbox`](https://github.com/lcrmorin/QuantToolBox) — the Python port
of the companion MATLAB `QuantToolbox` library.

The original `HSF/` folder is well over a thousand MATLAB scripts (including
per-chapter data-prep scripts) across 18 chapters (0.
Toolbox, 1. Introduction, 2. ESG Scoring, ... 17. Data), plus a chapter-0
toolbox of sustainable-finance-specific functions (copulas, credit risk
models, Genz quadrature, carbon-budget/ESG measures) that doesn't exist in
`quanttoolbox` yet. That toolbox is being ported directly into
`quanttoolbox` itself rather than duplicated here — this repo only holds
notebooks, plus whatever small sample data they need to run. The original
MATLAB toolbox source has been moved (not copied) out of `hfs-archive` to
`QuantToolBox/reference/hsf_toolbox_matlab/`, as source material for that
port; `hfs-archive`'s old `Examples/tutorial/` MATLAB-101 lessons moved
the other way, into `hfs-archive`'s `HSF/0. Toolbox/tutorial/`.

## Structure

```
notebooks/
  hsf/          one notebook per HSF chapter (00 = toolbox primer, 01-17 = chapters)
  tutorials/    general quanttoolbox tutorials, numbered from 0
                (00_building_blocks, 01_risk_budgeting, 02_black_litterman,
                03_mean_variance, 04_whittle, 05_regression, 06_svm) —
                the notebook equivalent of quanttoolbox's own docs/examples,
                and the direct replacement for quanttoolbox's old
                Examples/tutorial/ MATLAB-101 lessons (dropped from that
                repo's migration_map.md tracker in favor of these)
data/           small sample datasets a notebook reads directly (xlsx/csv);
                large or licensed source data stays out of git — see each
                chapter notebook's own data-provenance note
```

## Status

See [`CHAPTERS.md`](CHAPTERS.md) for the chapter-by-chapter tracker (mirrors
the tracker style used in `quanttoolbox`'s `docs/migration_map.md`).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Data provenance

Chapter notebooks read directly from the original chapter's source
spreadsheets (e.g. PRI signatory/regulation databases, GSIR reports) rather
than round-tripping through the original MATLAB `.mat` intermediate files.
Where a dataset is small and freely redistributable it's committed under
`data/`; where it isn't, the notebook documents where to obtain it and reads
it from a path you provide.
