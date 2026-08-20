"""
Summary of __init__.py

This module is part of the AVATARARTS ecosystem.
For more information about the AVATARARTS project, see the main documentation.
"""

import functools
import warnings


def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            "%r is deprecated" % (func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)
        return func(*args, **kwargs)

    return wrapper
