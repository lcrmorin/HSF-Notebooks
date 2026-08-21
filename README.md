# hsf-notebooks

Jupyter notebook companion to Thierry Roncalli's *Handbook of Sustainable
Finance* (the `HSF/` material in
[`hfs-archive`](https://github.com/lcrmorin/hfs-archive)), rebuilt on top of
[`quanttoolbox`](https://github.com/lcrmorin/QuantToolBox) — the Python port
of the companion MATLAB `QuantToolbox` library.

The original `HSF/` folder is well over a thousand MATLAB scripts (including
per-chapter data-prep scripts) across 18 book chapters (1. Introduction,
2. ESG Scoring, ... 17. Data), plus a sustainable-finance-specific function
library (copulas, credit risk models, Genz quadrature, carbon-budget/ESG
measures) that's being ported directly into `quanttoolbox` rather than
duplicated here — its MATLAB source lives in `QuantToolBox` at
`reference/hsf_toolbox_matlab/`, tracked as a planned port in that repo's
`docs/migration_map.md`. This repo only holds notebooks, plus whatever
small sample data they need to run.

## Structure

```
notebooks/
  hsf/          one notebook per HSF chapter -- 00 = tutorial, 01-17 = book chapters
  examples/     general quanttoolbox walkthroughs, numbered from 0
                (00_building_blocks, 01_risk_budgeting, 02_black_litterman,
                03_mean_variance, 04_whittle, 05_regression, 06_svm) --
                the notebook equivalent of quanttoolbox's own docs/examples
data/           small sample datasets a notebook reads directly (xlsx/csv);
                large or licensed source data stays out of git — see each
                chapter notebook's own data-provenance note
```

## Status

See [`CHAPTERS.md`](CHAPTERS.md) for the chapter-by-chapter tracker.

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
