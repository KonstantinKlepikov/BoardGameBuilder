"""Custom error classes
"""
from loguru._logger import Logger


class CustomRuntimeError(RuntimeError):
    """Base class for other runtime exceptions
    """


class ComponentNameError(CustomRuntimeError):
    """Given name of component is wrong or name isn't unique.
    """
    def __init__(self, name: str) -> None:
        self.message = f'Stuff with {name=} is exist in ' + \
                        'Component class instance or wrong name of stuff.'
        super().__init__(self.message)


class ComponentClassError(CustomRuntimeError):
    """Given class can't be a part of component.
    """
    def __init__(self, obj_, logger: Logger) -> None:
        self.message = f'Given: {obj_} cant be used as part of Component.'
        logger.exception(self.message)
        super().__init__(self.message)


class StuffDefineError(AttributeError):
    """Bad definition of item.
    """
    def __init__(self, message: str, logger: Logger) -> None:
        self.message = message
        logger.exception(self.message)
        super().__init__(self.message)


class ArrangeIndexError(IndexError):
    """Index error for arrange tool.
    """
    def __init__(self, message: str, logger: Logger) -> None:
        self.message = message
        logger.exception(self.message)
        super().__init__(self.message)
