"""Execute lessons in fresh kernels and record errors, stderr, and timings.

Example (with notebook dependencies and a Python kernel installed)::

    PYTHONPATH=../QuantToolBox/src python scripts/execute_notebooks.py --jobs 2

Successful runs replace notebook outputs; failed runs preserve the original
notebook and save the partially executed copy alongside the JSON report.
Use --pattern to rerun a subset. Back up notebooks before a full refresh.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def run_notebook(path, kernel, timeout, report_dir):
    start = time.monotonic()
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None
    result = {"notebook": path.name, "status": "passed", "error": None}
    try:
        NotebookClient(
            notebook,
            timeout=timeout,
            kernel_name=kernel,
            resources={"metadata": {"path": str(path.parent)}},
            record_timing=True,
        ).execute()
        nbformat.validate(notebook)
        nbformat.write(notebook, path)
    except Exception as exc:  # noqa: BLE001 - record failures and continue the batch
        result["status"] = "failed"
        result["error"] = f"{type(exc).__name__}: {exc}"
        failed_dir = report_dir / "failed"
        failed_dir.mkdir(exist_ok=True)
        nbformat.write(notebook, failed_dir / path.name)
    result["seconds"] = round(time.monotonic() - start, 2)
    result["code_cells"] = sum(c.cell_type == "code" for c in notebook.cells)
    result["executed_cells"] = sum(
        c.cell_type == "code" and c.execution_count is not None for c in notebook.cells
    )
    result["stderr"] = [
        {"cell": i, "text": output.text}
        for i, cell in enumerate(notebook.cells)
        for output in cell.get("outputs", [])
        if output.output_type == "stream" and output.name == "stderr"
    ]
    result["figures"] = sum(
        "image/png" in output.get("data", {})
        for cell in notebook.cells
        for output in cell.get("outputs", [])
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", nargs="+", default=["*.ipynb"])
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=600, help="Seconds per cell")
    parser.add_argument("--kernel", default="python3")
    parser.add_argument(
        "--report", type=Path, default=ROOT / "reports" / "notebook-execution.json"
    )
    args = parser.parse_args()
    paths = sorted(
        {
            path
            for pattern in args.pattern
            for path in (ROOT / "notebooks" / "hsf").glob(pattern)
        }
    )
    if not paths:
        parser.error("No matching notebooks")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    import quanttoolbox

    packages = {}
    for name in (
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "nbformat",
        "nbclient",
        "ipykernel",
        "openpyxl",
        "xlrd",
        "csaps",
        "scikit-learn",
        "pyproj",
        "basemap",
        "cvxpy",
        "qpsolvers",
        "statsmodels",
    ):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = None
    report = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "executable": sys.executable,
        "quanttoolbox_source": quanttoolbox.__file__,
        "packages": packages,
        "kernel": args.kernel,
        "timeout_seconds_per_cell": args.timeout,
        "results": [],
    }
    print(
        f"Running {len(paths)} notebooks; toolbox: {quanttoolbox.__file__}", flush=True
    )
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {
            pool.submit(
                run_notebook, path, args.kernel, args.timeout, args.report.parent
            ): path
            for path in paths
        }
        for future in as_completed(futures):
            result = future.result()
            report["results"].append(result)
            report["results"].sort(key=lambda item: item["notebook"])
            args.report.write_text(json.dumps(report, indent=2) + "\n")
            print(
                f"{len(report['results'])}/{len(paths)} {result['status']} "
                f"{result['notebook']} ({result['seconds']}s, "
                f"{len(result['stderr'])} stderr outputs)",
                flush=True,
            )
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    return int(any(item["status"] == "failed" for item in report["results"]))


if __name__ == "__main__":
    sys.exit(main())
