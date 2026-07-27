# tests/household/test_round_trip.py
#
# Copyright (c) 2026 John Leonard
# SPDX-License-Identifier: GPL-3.0-or-later
# See LICENSE file in repository root.

"""
Round-trip tests for Household import/export.

Notes
-----
Verifies that importing an OWL case into
a Household Library and exporting it
again preserves the canonical household
representation.
"""

from __future__ import annotations

from pathlib import Path

from owlplanner.config.plan_bridge import (
    plan_to_config,
)

from owlroost.household.loaders import (
    load_household_manifest,
)
from owlroost.household.operations import (
    export_case,
    import_case,
)
from owlroost.household.specs import (
    HouseholdLibrarySpec,
)
from owlroost.workspace.owl_utils import (
    resolve_household,
)


def test_import_export_round_trip(
    tmp_path,
):
    """
    Importing a case into a Household
    Library and exporting it again
    preserves the canonical household.
    """

    #
    # Arrange
    #

    fixture_dir = Path(__file__).parent / "fixtures" / "jack+jill"

    source_case = fixture_dir / "case_jack+jill.toml"

    source_hfp = fixture_dir / "HFP_jack+jill.xlsx"

    assert source_case.is_file()
    assert source_hfp.is_file()

    library = HouseholdLibrarySpec(
        name="test",
        root=tmp_path / "library",
    )

    library.root.mkdir()

    #
    # Import
    #

    imported = import_case(
        source_case,
        library,
    )

    #
    # Verify library contents.
    #

    imported = load_household_manifest(
        imported.root,
        library,
    )

    assert imported.manifest_file.is_file()
    assert imported.case_file.is_file()
    assert imported.hfp_file.is_file()

    #
    # Export
    #

    export_dir = tmp_path / "export"

    export_dir.mkdir()

    exported_case, exported_hfp = export_case(
        imported,
        export_dir,
    )

    assert exported_case.is_file()
    assert exported_hfp.is_file()

    #
    # Compare canonical plans.
    #

    original_plan = resolve_household(
        source_case,
    )

    exported_plan = resolve_household(
        exported_case,
    )

    # Import and export case are not symmetrical - the
    # HFP file name is changed as necessary.

    original_plan.hfpFileName = imported.hfp_file.name
    #    exported_plan.hfpFileName = exported_hfp.name
    exported_plan.hfpFileName = imported.hfp_file.name

    assert plan_to_config(
        original_plan,
    ) == plan_to_config(
        exported_plan,
    )
