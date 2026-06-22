# src/owlroost/core/info.py
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

from pathlib import Path

from owlroost.version import __version__


def get_roost_root():
    return Path(__file__).resolve().parents[1]


def get_conf_dir():
    return get_roost_root() / "conf"


def get_workspace_dir():
    return get_roost_root() / "workspace"


def get_workspace_template_dir():
    return get_roost_root() / "templates"


def get_roost_makefile():
    return get_workspace_template_dir() / "roost.mk"


def get_installation_info():
    """
    Return all known installation
    metadata.

    Returns
    -------
    dict
    """

    return {
        "version": __version__,
        "root": get_roost_root(),
        "conf": get_conf_dir(),
        "workspace": get_workspace_dir(),
        "templates": get_workspace_template_dir(),
        "makefile": get_roost_makefile(),
    }


def get_installation_value(
    name,
):
    """
    Return a single installation
    metadata value.

    Raises
    ------
    KeyError
        Unknown name.
    """

    return get_installation_info()[name]
