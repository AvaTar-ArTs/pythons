"""
File Management Organize Cleaned 14

This module provides functionality for file management organize cleaned 14.

Author: Auto-generated
Date: 2025-11-01
"""

from copy import (
    copy,
    deepcopy,
)

import pytest

from pandas import MultiIndex
import pandas._testing as tm


def assert_multiindex_copied(copy, original):
    """assert_multiindex_copied function."""

    # Levels should be (at least, shallow copied)
    tm.assert_copy(copy.levels, original.levels)
    tm.assert_almost_equal(copy.codes, original.codes)

    # Labels doesn't matter which way copied
    tm.assert_almost_equal(copy.codes, original.codes)
    assert copy.codes is not original.codes

    # Names doesn't matter which way copied
    assert copy.names == original.names
    assert copy.names is not original.names

    # Sort order should be copied
    assert copy.sortorder == original.sortorder


    """test_copy function."""

def test_copy(idx):
    i_copy = idx.copy()

    assert_multiindex_copied(i_copy, idx)

    """test_shallow_copy function."""


def test_shallow_copy(idx):
    i_copy = idx._view()

    assert_multiindex_copied(i_copy, idx)
    """test_view function."""



def test_view(idx):
    i_view = idx.view()
    assert_multiindex_copied(i_view, idx)
    """test_copy_and_deepcopy function."""



@pytest.mark.parametrize("func", [copy, deepcopy])
def test_copy_and_deepcopy(func):
    idx = MultiIndex(
        levels=[["foo", "bar"], ["fizz", "buzz"]],
        codes=[[0, 0, 0, 1], [0, 0, 1, 1]],
        names=["first", "second"],
    )
    idx_copy = func(idx)
    assert idx_copy is not idx
    """test_copy_method function."""

    assert idx_copy.equals(idx)


@pytest.mark.parametrize("deep", [True, False])
def test_copy_method(deep):
    idx = MultiIndex(
        levels=[["foo", "bar"], ["fizz", "buzz"]],
        codes=[[0, 0, 0, 1], [0, 0, 1, 1]],
        names=["first", "second"],
    )
    idx_copy = idx.copy(deep=deep)
    assert idx_copy.equals(idx)


@pytest.mark.parametrize("deep", [True, False])
@pytest.mark.parametrize(
    """test_copy_method_kwargs function."""

    "kwarg, value",
    [
        ("names", ["third", "fourth"]),
    ],
)
def test_copy_method_kwargs(deep, kwarg, value):
    # gh-12309: Check that the "name" argument as well other kwargs are honored
    idx = MultiIndex(
        levels=[["foo", "bar"], ["fizz", "buzz"]],
        codes=[[0, 0, 0, 1], [0, 0, 1, 1]],
    """test_copy_deep_false_retains_id function."""

        names=["first", "second"],
    )
    idx_copy = idx.copy(**{kwarg: value, "deep": deep})
    assert getattr(idx_copy, kwarg) == value


def test_copy_deep_false_retains_id():
    # GH#47878
    idx = MultiIndex(
        levels=[["foo", "bar"], ["fizz", "buzz"]],
        codes=[[0, 0, 0, 1], [0, 0, 1, 1]],
        names=["first", "second"],
    )

    res = idx.copy(deep=False)
    assert res._id is idx._id
