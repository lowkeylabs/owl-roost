# src/owlroost/core/settings.py
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

import os
from pathlib import Path

from owlroost.version import __version__


def get_roost_root():
    return Path(__file__).resolve().parents[1]


def get_mosek_info():
    report = {
        "mosek_package_installed": False,
        "mosek_package_version": "Unknown",
        "mosek_license_path": "Not Set",
        "mosek_status_message": "Disabled - requires license",
        "mosek_available": False,
    }

    # Check Package Installation & Version
    # This is indepedent of whether a license exists.
    try:
        import mosek

        report["mosek_package_installed"] = True

        # Pull Version Info directly via the native API component
        with mosek.Env() as env:
            # Formats major, minor, revision versions
            report["mosek_package_version"] = f"{env.getversion()}"
    except ImportError:
        report["mosek_status_message"] = "Python package is not installed in this environment."
        pass

    # Check System License Path Variable
    # If no license, then exit.
    env_lic_path = os.environ.get("MOSEKLM_LICENSE_FILE")
    if env_lic_path:
        env_lic_path = os.path.expanduser(env_lic_path)
    else:
        # Fallback default location if environment variable isn't specified
        env_lic_path = os.path.expanduser("~/mosek/mosek.lic")

    if not Path(env_lic_path).exists():
        report["mosek_license_path"] = f"License not found (MOSEKLM_LICENSE_FILE={env_lic_path})"
        if report["mosek_package_installed"]:
            report["mosek_status_message"] = (
                "Python package installed - but disabled.  Require license"
            )
        return report
    report["mosek_license_path"] = f"Found: {env_lic_path}"

    # 3. Test Active License Checkout & Global Env Initialization
    if report["mosek_package_installed"]:
        try:
            with mosek.Env() as env:
                # Explicitly attempts an environment checkout initialization
                with env.Task():
                    report["mosek_available"] = True
                    report["mosek_status_message"] = (
                        "MOSEK available.  License is verified and active."
                    )
        except mosek.Error as e:
            # Captures distinct error code constraints (e.g., code 1008 for expired, 1001 for missing)
            report["mosek_status_message"] = (
                f"MOSEK init() failed - MOSEK API Error {e.errno}: {e.msg}"
            )
        except Exception as general_error:
            report["mosek_status_message"] = (
                f"MOSEK init() failed - System Error: {str(general_error)}"
            )

    # Display clean overview results
    return report


def get_owl_version():
    from owlplanner.version import __version__ as owl_version

    return owl_version


def get_conf_dir():
    return get_roost_root() / "conf"


def get_workspace_dir():
    return get_roost_root() / "workspace"


def get_workspace_template_dir():
    return get_roost_root() / "templates"


def get_roost_makefile():
    return get_workspace_template_dir() / "roost.mk"


def get_settings():
    """
    Return all known installation
    metadata.

    Returns
    -------
    dict
    """

    info = {
        "roost_version": __version__,
        "owl_version": get_owl_version(),
        "root": get_roost_root(),
        "conf": get_conf_dir(),
        "workspace": get_workspace_dir(),
        "templates": get_workspace_template_dir(),
        "makefile": get_roost_makefile(),
    }

    info.update(get_mosek_info())

    return info


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

    if name in get_settings().keys():
        return get_settings()[name]

    print(f"name not found: {name}")
