"""Main engine to create game object
"""
from typing import (
    Union, TypeVar, Dict, List, Optional, Type, Any
    )
from dataclasses import dataclass, field
from collections.abc import Mapping
from dataclasses_json import DataClassJsonMixin
from bgameb.rollers import BaseRoller
from bgameb.shakers import Shaker
from bgameb.cards import Card
from bgameb.errors import ComponentNameError, ComponentClassError
from bgameb.utils import log_me


comp_bounds = Union[Shaker, BaseRoller, Card]
Component = TypeVar('Component', bound=comp_bounds)


class Components(Mapping):
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

    def __iter__(self):
        return iter(self.__dict__)

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

    def _update(
        self,
        component: Type[comp_bounds],
        kwargs: Dict[str, Any]
            ) -> None:
        """Update components dict

        Args:
            component (Type[comp_bounds]): component class
            kwargs (Dict[str, Any]): aditional args
        """
        self.__dict__.update(
            {kwargs['name']: component(**kwargs)}
            )

    def add(
        self,
        component: Type[comp_bounds],
        **kwargs
        ) -> None:
        """Add component to Components dict

        Args:
            component (Component): component class
            kwargs: aditional args
        """
        if kwargs.get('name'):
            self._chek_in(kwargs['name'])
        else:
            self._chek_in(component.name)
            kwargs['name'] = component.name
        self._update(component, kwargs)

@dataclass
class Game(DataClassJsonMixin):
    """Create the game object
    """

    name: str = 'game'
    shakers: Components = field(default_factory=dict, init=False)
    rollers: Components = field(default_factory=dict, init=False)
    cards: Components = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.shakers = Components()
        self.rollers = Components()
        self.cards = Components()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(f'Game created.')

    def add(self, component: Component, **kwargs) -> None:
        """Add component to game

        Args:
            component (Component): any class instance of components
            kwargs: additional arguments of component
        """
        if issubclass(component, BaseRoller):
            self.rollers.add(component, **kwargs)
            self.logger.info(f'Roller added: {self.rollers=}.')
        elif component in Shaker.__mro__:
            self.shakers.add(component, **kwargs)
            self.logger.info(f'Shaker added: {self.shakers=}.')
        elif component in Card.__mro__:
            self.cards.add(component, **kwargs)
            self.logger.info(f'Card added: {self.cards=}.')
        else:
            raise ComponentClassError(class_=component)
