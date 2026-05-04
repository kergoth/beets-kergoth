"""Nox sessions."""

import os
import shutil
from pathlib import Path

import nox


python_versions = ["3.10", "3.11", "3.12", "3.13", "3.14"]
nox.needs_version = ">= 2026.4.10"
nox.options.sessions = ("pip-audit", "tests", "docs-build")
nox.options.default_venv_backend = "uv"


@nox.session(name="pip-audit", python=python_versions[0])
def pip_audit(session: nox.Session) -> None:
    """Audit dependencies for known vulnerabilities."""
    session.install(".")
    session.install("pip-audit")
    session.run("pip-audit", "--local")


@nox.session(python=python_versions)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    existing_path = session.env.get("PYTHONPATH", "")
    session.env["PYTHONPATH"] = (
        f"tests{os.pathsep}{existing_path}" if existing_path else "tests"
    )
    args = session.posargs or ["tests"]
    session.install(".")
    session.install("pytest<8", "pytest-cov", "pytest-cram", "cram")
    session.run("pytest", *args)


@nox.session(name="docs-build", python=python_versions[0])
def docs_build(session: nox.Session) -> None:
    """Build the documentation."""
    args = session.posargs or ["docs", "docs/_build"]
    session.install(".")
    session.install("sphinx")

    build_dir = Path("docs", "_build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

    session.run("sphinx-build", *args)
