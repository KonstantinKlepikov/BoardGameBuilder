class CustomRuntimeError(RuntimeError):
    """Base class for other runtime exceptions
    """
    pass


class ComponentNameError(CustomRuntimeError):
    """Component with given name is in Components
    class instance.
    """
    def __init__(self, name) -> None:
        self.message = f'Component with {name=} is in Components class instance'
        super().__init__(self.message)


class ComponentClassError(RuntimeError):
    """Given class isnt component
    """
    def __init__(self, class_) -> None:
        self.message = f'Given class: {class_} not a component.'
        super().__init__(self.message)


class RollerSidesError(RuntimeError):
    """Count of sides not defined for this rolled object
    """
    pass


class RollerDefineError(AttributeError):
    """Count of rollers not defined
    """
