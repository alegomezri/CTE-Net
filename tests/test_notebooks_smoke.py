"""Smoke test: every Models/ and Ablation/ notebook runs end-to-end without error.

Requires the real dataset in data/raw/ (see README "Prepare the data"). Runs with
CTE_NET_SMOKE_TEST=1, which each notebook honors by shrinking epochs/seeds/Optuna
trials so this finishes in minutes instead of hours. Results are methodology-correct
but not the published numbers -- this test checks the pipeline runs, not accuracy.
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = REPO_ROOT / "data" / "raw"

NOTEBOOKS = sorted((REPO_ROOT / "Models").glob("*.ipynb")) + sorted(
    (REPO_ROOT / "Ablation").glob("*.ipynb")
)

pytestmark = pytest.mark.skipif(
    not DATA_ROOT.exists(),
    reason=f"dataset not found at {DATA_ROOT} -- see README 'Prepare the data'",
)


@pytest.mark.parametrize("notebook", NOTEBOOKS, ids=lambda p: p.stem)
def test_notebook_runs(notebook, tmp_path):
    env = dict(os.environ, CTE_NET_SMOKE_TEST="1", CUBLAS_WORKSPACE_CONFIG=":4096:8")
    output = tmp_path / f"{notebook.stem}.executed.ipynb"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=1800",
            "--output",
            str(output),
            str(notebook),
        ],
        cwd=notebook.parent,
        env=env,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr[-4000:]
