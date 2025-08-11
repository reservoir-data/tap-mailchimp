"""Nox configuration."""

from __future__ import annotations

import os

import nox

nox.needs_version = ">=2025.2.9"
nox.options.default_venv_backend = "uv"

PYPROJECT = nox.project.load_toml()
PYTHON_VERSIONS = nox.project.python_versions(PYPROJECT)

package = "tap-mailchimp"
src_dir = "tap_mailchimp"
tests_dir = "tests"
locations = src_dir, tests_dir, "noxfile.py"


@nox.session(python=PYTHON_VERSIONS)
def tests(session: nox.Session) -> None:
    """Execute pytest tests and compute coverage."""
    groups = ["testing"]
    if "GITHUB_ACTIONS" in os.environ:
        groups.append("ci")

    session.run_install(
        "uv",
        "sync",
        "--locked",
        "--no-dev",
        *(f"--group={g}" for g in groups),
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
            "UV_PYTHON": session.python,
        },
    )

    session.run("pytest", *session.posargs)
