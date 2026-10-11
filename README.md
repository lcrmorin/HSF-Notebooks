# hsf-notebooks

A Jupyter notebook series covering the material in Thierry Roncalli's
*Handbook of Sustainable Finance*, built on top of
[`quanttoolbox`](https://github.com/lcrmorin/QuantToolBox) for the
underlying quantitative-finance and risk-modeling functions (portfolio
optimization, credit risk, copulas, carbon-budget/ESG measures, and so
on).

The notebooks follow the book's own chapter structure (1. Introduction,
2. ESG Scoring, ... 16. Exercise Solutions). This repo holds the
notebooks themselves, plus whatever small sample data each one needs to
run.

## Navigation

The collection contains **83 notebooks**. Start with the [notebook index](INDEX.md),
which lists each lesson and the original section codes combined within merged lessons.
Merged notebooks have a contents list and retain local exercise numbers within each part.

## Structure

```
notebooks/
  hsf/          lessons grouped by HSF chapter; 00 = tutorial.
                Letters identify topics; combined letters identify merged
                lessons (for example, 13ef combines baseline and stressed transitions).
data/           small sample datasets a notebook reads directly (xlsx/csv);
                large or licensed source data stays out of git — see each
                chapter notebook's own data-provenance note
```

`quanttoolbox`'s own worked examples (bond pricing, portfolio construction,
risk budgeting, ...) live in `QuantToolBox`'s own `docs/examples/` and
aren't duplicated here.

## Status

All 16 chapters are complete — see [`CHAPTERS.md`](CHAPTERS.md) for the
chapter-by-chapter tracker.

Notebook helpers that turned out to be generic enough have since been
promoted into `quanttoolbox` directly, and the notebooks delegate to
them. A handful stay notebook-local on purpose — either tied to one
chapter's specific model, or (as with `16d`'s Poisson-binomial PMF
functions) because the notebook's own point is cross-checking
independent implementations against each other, which delegating to a
single shared implementation would defeat.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Execution audit

On 2026-10-11, all **83 notebooks** ran successfully from fresh kernels
against the sibling `QuantToolBox/src` checkout: **940 code cells** and
**424 PNG figures**, with no error outputs or emitted notebook warnings
on the final runs. Outputs were refreshed and notebook formats validated.
Representative figures were visually checked; this is an execution audit,
not an independent verification of every model or dataset.

The audit added the missing `xlrd` dependency for the palaeoclimate `.xls`
file and improved crowded date labels in the greenium charts. Existing
notebook warning filters remain in place. See the
[execution report](reports/notebook-execution.json) for individual timings,
dependency versions, source hashes, and rechecks.

To repeat the audit from this directory after the setup above:

```bash
python -m ipykernel install --sys-prefix --name hsf-notebooks
PYTHONPATH="../QuantToolBox/src" python scripts/execute_notebooks.py --kernel hsf-notebooks
```

The runner starts a fresh kernel for each lesson and refreshes successful
notebook outputs, so back up any outputs you want to retain. Failed runs
leave the original notebook intact and save a partial copy in
`reports/failed/`. Use `--pattern '04c*'` to rerun a lesson, `--jobs 1` to
reduce memory use, or `--timeout 1200` to allow longer individual cells on
slower machines. A subset run replaces the report unless `--report` names
a separate file.

## Data provenance

Chapter notebooks read directly from each topic's original source data
(e.g. PRI signatory/regulation databases, GSIR reports). Where a dataset
is small and freely redistributable it's committed under `data/`; where
it isn't, the notebook documents where to obtain it and reads it from a
path you provide. Where a notebook is missing a section because the
underlying data isn't available, that's noted in the notebook itself
rather than silently skipped.
