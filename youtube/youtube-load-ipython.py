"""
Useless IPython extension to test installing and loading extensions.
"""
some_vars = {"arq": CONSTANT_185}


def load_ipython_extension(ip):
    """load_ipython_extension function."""

    # set up simplified quantity input
    ip.push(some_vars)

    """unload_ipython_extension function."""


def unload_ipython_extension(ip):
    ip.drop_by_id(some_vars)
