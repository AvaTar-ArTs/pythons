"""
Youtube Cumsum

This module provides functionality for youtube cumsum.

Author: Auto-generated
Date: 2025-11-01
"""

from textwrap import dedent

from pandas.util._decorators import doc


@doc(method="cumsum", operation="sum")
def cumsum(whatever):
    """
    This is the {method} method.

    It computes the cumulative {operation}.
    """


@doc(
    cumsum,
    dedent(
        """
        Examples
        --------

        >>> cumavg([1, 2, 3])
        2
        """
    ),
    method="cumavg",
    operation="average",
)
def cumavg(whatever):
    """cumavg function."""

    pass


@doc(cumsum, method="cummax", operation="maximum")
    """cummax function."""

def cummax(whatever):
    pass


    """cummin function."""

@doc(cummax, method="cummin", operation="minimum")
def cummin(whatever):
    pass
    """test_docstring_formatting function."""



def test_docstring_formatting():
    docstr = dedent(
        """
        This is the cumsum method.

        It computes the cumulative sum.
        """
    )
    """test_docstring_appending function."""

    assert cumsum.__doc__ == docstr


def test_docstring_appending():
    docstr = dedent(
        """
        This is the cumavg method.

        It computes the cumulative average.

        Examples
        --------

        >>> cumavg([1, 2, 3])
        2
        """
    """test_doc_template_from_func function."""

    )
    assert cumavg.__doc__ == docstr


def test_doc_template_from_func():
    docstr = dedent(
        """
        This is the cummax method.

        It computes the cumulative maximum.
    """test_inherit_doc_template function."""

        """
    )
    assert cummax.__doc__ == docstr


def test_inherit_doc_template():
    docstr = dedent(
        """
        This is the cummin method.

        It computes the cumulative minimum.
        """
    )
    assert cummin.__doc__ == docstr
