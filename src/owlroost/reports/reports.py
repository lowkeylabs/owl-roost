# src/owlroost/reports/reports.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
TODO: Document module.

Notes
-----
Describe responsibilities, ownership,
and architectural role.
"""

from __future__ import annotations

from os.path import relpath
from pathlib import Path

import yaml

from owlroost.display.discovery import (
    find_first_trial,
    find_runs,
    find_sessions,
)

REQUIRED_LEVELS = [
    "results",
    "case",
    "session",
    "run",
    "trial",
]


def write_metadata(
    path: Path,
    *,
    level: str,
    template_dir: Path,
):
    data = {
        "level": level,
        "paths": {
            "template_dir": str(
                template_dir.resolve(),
            ),
        },
    }

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as fh:
        yaml.safe_dump(
            data,
            fh,
            sort_keys=False,
        )


def materialize_index_qmd(
    *,
    template_file: Path,
    target_file: Path,
    payload_dir: Path,
):
    text = template_file.read_text(
        encoding="utf-8",
    )

    relative_payload_dir = relpath(
        payload_dir,
        start=target_file.parent,
    )

    text = text.replace(
        "__PAYLOAD_DIR__",
        relative_payload_dir,
    )

    target_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    target_file.write_text(
        text,
        encoding="utf-8",
    )


def ensure_report_artifacts(
    *,
    target_dir: Path,
    level: str,
    results_template_dir: Path,
):
    template_dir = (results_template_dir / level).resolve()

    write_metadata(
        target_dir / "_metadata.yml",
        level=level,
        template_dir=template_dir,
    )

    materialize_index_qmd(
        template_file=(template_dir / "_index.qmd"),
        target_file=(target_dir / "index.qmd"),
        payload_dir=template_dir,
    )


def check_report_artifacts(
    target_dir: Path,
):
    issues = []

    if not (target_dir / "_metadata.yml").exists():
        issues.append("missing _metadata.yml")

    if not (target_dir / "index.qmd").exists():
        issues.append("missing index.qmd")

    return issues


def validate_template_tree(
    results_template_dir: Path,
):
    missing = []

    for level in REQUIRED_LEVELS:
        template_file = results_template_dir / level / "_index.qmd"

        if not template_file.exists():
            missing.append(str(template_file))

    if missing:
        raise RuntimeError("Missing report templates:\n" + "\n".join(missing))


def sync_reports(
    results_dir: Path,
    results_template_dir: Path,
):
    results_dir = Path(results_dir).resolve()

    results_template_dir = Path(results_template_dir).resolve()

    validate_template_tree(
        results_template_dir,
    )

    # ------------------------------------
    # Results root
    # ------------------------------------
    ensure_report_artifacts(
        target_dir=results_dir,
        level="results",
        results_template_dir=(results_template_dir),
    )

    case_seen = set()

    for session_dir in find_sessions(
        results_dir,
    ):
        session_dir = Path(session_dir).resolve()

        case_dir = session_dir.parent.parent

        if case_dir not in case_seen:
            ensure_report_artifacts(
                target_dir=case_dir,
                level="case",
                results_template_dir=(results_template_dir),
            )

            case_seen.add(case_dir)

        ensure_report_artifacts(
            target_dir=session_dir,
            level="session",
            results_template_dir=(results_template_dir),
        )

        for run_dir in find_runs(
            session_dir,
        ):
            ensure_report_artifacts(
                target_dir=run_dir,
                level="run",
                results_template_dir=(results_template_dir),
            )

            trial_dir = find_first_trial(
                run_dir,
            )

            if trial_dir:
                ensure_report_artifacts(
                    target_dir=trial_dir,
                    level="trial",
                    results_template_dir=(results_template_dir),
                )
