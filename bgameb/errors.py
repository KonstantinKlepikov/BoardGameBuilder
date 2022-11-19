"""Custom error classes
"""
from __future__ import annotations
import loguru


class CustomRuntimeError(RuntimeError):
    """Base class for other runtime exceptions
    """


class ComponentIdError(CustomRuntimeError):
    """Component with given name has not wrong name or name isnt unique.
    """
    def __init__(self, id: str) -> None:
        self.message = f'{id=} is not a string.'
        super().__init__(self.message)


class ComponentNameError(CustomRuntimeError):
    """Component with given name has not wrong name or name isnt unique.
    """
    def __init__(self, name: str) -> None:
        self.message = f'Component with {name=} is exist in ' + \
                        'Component class instance or wrong name'
        super().__init__(self.message)


class ComponentClassError(CustomRuntimeError):
    """Given class isn't component.
    """
    def __init__(self, obj_, logger: loguru.Logger) -> None:
        self.message = f'Given: {obj_} not a component or you are trying ' +\
                        'to place a component in a non-designated component.'
        logger.exception(self.message)
        super().__init__(self.message)


class StuffDefineError(AttributeError):
    """Badd definition of item.
    """
    def __init__(self, message: str, logger: loguru.Logger) -> None:
        self.message = message
        logger.exception(self.message)
        super().__init__(self.message)


class ArrangeIndexError(IndexError):
    """Index error for arrange tool.
    """
    def __init__(self, message: str, logger: loguru.Logger) -> None:
        self.message = message
        logger.exception(self.message)
        super().__init__(self.message)
