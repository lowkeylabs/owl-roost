# src/owlroost/study/studies/market_uncertainty.py
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

from owlroost.study.specs import (
    StudySpec,
)


def register_studies(
    reg,
):
    reg.register_study(
        StudySpec(
            name="market_uncertainty",
            title="Market Uncertainty",
            description=(
                "Explores how retirement outcomes "
                "change under different market "
                "return assumptions, historical "
                "periods, and stochastic return "
                "sequences."
            ),
            experiment_names=[
                "bootstrap_quick",
                "fixed_return_models",
                "historical_models",
            ],
        )
    )
