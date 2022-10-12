"""Custom error classes
"""
from __future__ import annotations
import loguru


class CustomRuntimeError(RuntimeError):
    """Base class for other runtime exceptions
    """


class ComponentNameError(CustomRuntimeError):
    """Component with given name is in Components
    class instance.
    """
    def __init__(self, name: str) -> None:
        self.message = f'Component with {name=} is exist in ' + \
                        'Components class instance or wrong name'
        super().__init__(self.message)


class ComponentClassError(CustomRuntimeError):
    """Given class isnt component
    """
    def __init__(self, obj_, logger: loguru.Logger) -> None:
        self.message = f'Given: {obj_} not a component.'
        logger.exception(self.message)
        super().__init__(self.message)


class StuffDefineError(AttributeError):
    """Defining stuff error
    """
    def __init__(self, message: str, logger: loguru.Logger) -> None:
        self.message = message
        logger.exception(self.message)
        super().__init__(self.message)


class ArrangeIndexError(IndexError):
    """Index error for arrange tool
    """
    def __init__(self, message: str, logger: loguru.Logger) -> None:
        self.message = message
        logger.exception(self.message)
        super().__init__(self.message)
