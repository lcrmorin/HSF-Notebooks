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

## Structure

```
notebooks/
  hsf/          one notebook per HSF chapter -- 00 = tutorial, 01-17 = book
                chapters; a chapter big enough to split into clearly
                separate topics gets a lettered pair instead (02a, 02b, ...)
data/           small sample datasets a notebook reads directly (xlsx/csv);
                large or licensed source data stays out of git — see each
                chapter notebook's own data-provenance note
```

`quanttoolbox`'s own worked examples (bond pricing, portfolio construction,
risk budgeting, ...) live in `QuantToolBox`'s own `docs/examples/` and
aren't duplicated here.

## Status

See [`CHAPTERS.md`](CHAPTERS.md) for the chapter-by-chapter tracker.

Some notebooks define their own numeric helpers rather than reaching for
`quanttoolbox`, when a function is specific to one chapter or it isn't
yet clear whether it's reused elsewhere. Helpers that look generic enough
to promote later are tracked in
[`PACKAGING_CANDIDATES.md`](PACKAGING_CANDIDATES.md).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

## Data provenance

Chapter notebooks read directly from each topic's original source data
(e.g. PRI signatory/regulation databases, GSIR reports). Where a dataset
is small and freely redistributable it's committed under `data/`; where
it isn't, the notebook documents where to obtain it and reads it from a
path you provide. Where a notebook is missing a section because the
underlying data isn't available, that's noted in the notebook itself
rather than silently skipped.
