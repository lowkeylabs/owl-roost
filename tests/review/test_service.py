# tests/review/test_service.py

from __future__ import annotations

from owlroost.review.service import (
    ReviewService,
    review,
)


def test_review_returns_observations(
    tmp_path,
):
    """
    Review returns the canonical
    observations dictionary.
    """

    observations = review(
        tmp_path,
    )

    assert observations["root"] == tmp_path.resolve()

    assert "has_workspace" in observations
    assert "has_household" in observations
    assert "has_valid_household" in observations
    assert "next_step" in observations


def test_review_resolves_root(
    tmp_path,
):
    """
    Root path is normalized to an
    absolute Path.
    """

    service = ReviewService()

    observations = service.review(
        tmp_path,
    )

    assert observations["root"] == tmp_path.resolve()


def test_determine_next_step_missing_household():
    """
    Missing household is the first
    prerequisite.
    """

    service = ReviewService()

    observations = {
        "has_household": False,
        "has_valid_household": False,
        "has_workspace": False,
    }

    assert (
        service.determine_next_step(
            observations,
        )
        == "Locate a household."
    )


def test_determine_next_step_invalid_household():
    """
    Invalid households are
    corrected before continuing.
    """

    service = ReviewService()

    observations = {
        "has_household": True,
        "has_valid_household": False,
        "has_workspace": False,
    }

    assert (
        service.determine_next_step(
            observations,
        )
        == "Correct the household."
    )


def test_determine_next_step_missing_workspace():
    """
    A valid household precedes
    workspace initialization.
    """

    service = ReviewService()

    observations = {
        "has_household": True,
        "has_valid_household": True,
        "has_workspace": False,
    }

    assert (
        service.determine_next_step(
            observations,
        )
        == "Initialize a workspace."
    )


def test_determine_next_step_complete():
    """
    Completed prerequisites produce
    a completed review.
    """

    service = ReviewService()

    observations = {
        "has_household": True,
        "has_valid_household": True,
        "has_workspace": True,
    }

    assert (
        service.determine_next_step(
            observations,
        )
        == "Review complete."
    )
