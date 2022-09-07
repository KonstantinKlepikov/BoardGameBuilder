"""Main engine to create game object
"""
from typing import (
    Union, NamedTuple, TypeVar, Dict, List, Optional, Type
    )
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.rollers import BaseRoller
from bgameb.shakers import Shaker
from bgameb.errors import ComponentNameError
from bgameb.utils import log_me


comp_bounds = Union[Shaker, BaseRoller]
Component = TypeVar('Component', bound=comp_bounds)


class GameShakers(NamedTuple):
    """Game shakers collection
    """


class Components(dict):
    """Components mapping.

    This class inherit from dict and not implemets
    __setattr__ and __setitems__. Class represents
    additional dot-acces for attributes of dict
    """
    def __init__(
        self,
        *args: List[Dict[str, Component]],
        **kwargs: Dict[str, Component]
        ) -> None:
        """Args must be a dicts
        """
        super().__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                self.__dict__.update(arg)
            else:
                raise AttributeError('Args must be a dicts')
        if kwargs:
            self.__dict__.update(kwargs)

    def __getattr__(self, attr: str) -> Component:
        try:
            return self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr: str, value: Component) -> None:
        raise NotImplementedError('This method not implementd for Components')

    def __delattr__(self, attr: str) -> None:
        try:
            del self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setitem__(self, key: str, value: Component) -> None:
        raise NotImplementedError('This method not implementd for Components')

    def __getitem__(self, key: str) -> Component:
        return self.__dict__[key]

    def __delitem__(self, key: str) -> None:
        del self.__dict__[key]

    def __repr__(self):
        items = (f"{k}={v!r}" for k, v in self.__dict__.items())
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __len__(self) -> int:
        return len(self.__dict__)

    def _chek_in(self, name: str) -> Optional[bool]:
        """Chek is name of component is unique

        Args:
            name (str): name for component

        Raises:
            ComponentNameError: name id not unique

        Returns:
            Optional[bool]: if it is in
        """
        if name in self.__dict__.keys():
            raise ComponentNameError(name=name)
        return True

    def add(
        self,
        component: Type[comp_bounds],
        name: Optional[str] = None,
        **kwargs
        ) -> None:
        """Add component to Components dict

        Args:
            component (Component): component class
            name (Optional[str]): Name for component instance.
                                  If None - used default for class.
                                  Defaults to None.
        """
        if name:
            self._chek_in(name)
            self.__dict__.update({name: component(name=name, **kwargs)})
        else:
            self._chek_in(component.name)
            self.__dict__.update({component.name: component(**kwargs)})


@dataclass
class Game(DataClassJsonMixin):
    """Create the game object
    """

    name: str = 'game'
    shakers: NamedTuple = field(default_factory=tuple, init=False)

    def __post_init__(self) -> None:
        self.shakers = GameShakers()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(f'Game created.')

    def add(self, component: Component) -> None:
        """Add game component to game

        Args:
            component (Component): any class instance of components
        """
        # TODO: separate by type without if's, remove tuple
        if isinstance(component, Shaker):

            sh_dict = self.shakers._asdict()
            sh_dict[component.name] = component
            sh_types = self.shakers.__annotations__
            sh_types[component.name] = type(component)

            gsh = NamedTuple('GameShakers', sh_types.items())
            self.shakers = gsh(**sh_dict)

            self.logger.info(f'Added {self.shakers}.')
