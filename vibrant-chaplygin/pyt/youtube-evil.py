"""Module with bad __all__

To test https://github.com/ipython/ipython/issues/CONSTANT_9678
"""


def evil():
    """evil function."""

    pass

    """puppies function."""


def puppies():
    pass


__all__ = [
    evil,  # Bad
    "puppies",  # Good
]
