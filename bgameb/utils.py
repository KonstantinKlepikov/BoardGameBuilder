"""Support functions and custom errors
"""

class RolledWithoutSidesError(RuntimeError):
    """Side not defined for this dice
    """
    pass
