"""Base constructs for build package objects
"""
from typing import (
    Dict, List, Optional, Any, Iterable
    )
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from bgameb.errors import ComponentNameError, StuffDefineError
from bgameb.utils import log_me, get_random_name


class Components(Mapping):
    """Components mapping.

    This class inherit from dict and not implemets
    __setattr__ and __setitems__. Class represents
    additional dot-acces for attributes of dict
    """
    def __init__(
        self,
        *args,
        **kwargs
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

    def __iter__(self) -> Iterable:
        return iter(self.__dict__)

    def __getattr__(self, attr: str):
        try:
            return self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr: str, value) -> None:
        raise NotImplementedError('This method not implementd for Components')

    def __delattr__(self, attr: str) -> None:
        try:
            del self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setitem__(self, key: str, value) -> None:
        raise NotImplementedError('This method not implementd for Components')

    def __getitem__(self, key: str):
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
        component,
        kwargs: Dict[str, Any]
            ) -> None:
        """Update components dict

        Args:
            component: component class
            kwargs (Dict[str, Any]): aditional args
        """
        # print(f'{kwargs=}')
        comp = component(**kwargs)

        if kwargs['name'] is None:
            kwargs['name'] = comp.name

        self.__dict__.update({kwargs['name']: comp})

    def add(self, component, **kwargs) -> None:
        """Add component to Components dict. Components with
        same names as existed cant be added.

        Raises:
            ComponentNameError: name id not unique

        Args:
            component (Component): component class
            kwargs: aditional args
        """
        # print(f'Add {kwargs=}')
        if kwargs.get('name'):
            self._chek_in(kwargs['name'])
        else:
            self._chek_in(component.name)
            kwargs['name'] = component.name

        self._update(component, kwargs)

    def add_replace(self, component, **kwargs) -> None:
        """Add or replace component in Components dict.

        Args:
            component (Component): component class
            kwargs: aditional args
        """
        if not kwargs.get('name'):
            kwargs['name'] = component.name
        self._update(component, kwargs)

    def get_names(self) -> List[str]:
        """Get names of all components of class

        Returns:
            List[str]: lisct of names of conatined components
        """
        return list(self.__dict__)


class CardTexts(dict):
    """Cards texts collection
    """
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def __getattr__(self, attr: str) -> str:
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr: str, value: str) -> None:
        self[attr] = value

    def __delattr__(self, attr: str) -> None:
        del self[attr]

    def __repr__(self):
        items = (f"{k}={v!r}" for k, v in self.items())
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other: Any) -> bool:
        if isinstance(self, dict) and isinstance(other, dict):
            return self.__dict__ == other.__dict__
        return NotImplemented


@dataclass
class Base(DataClassJsonMixin, ABC):
    """Base class for game, stuff and tools

    Inherited classes needs attr name implementation
    """

    def __post_init__(self) -> None:
        # set random name
        if self.name is None:
            self.name = get_random_name()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(
            f'{self.__class__.__name__} created with {self.name=}.'
            )

@dataclass
class BaseGame(Base, ABC):
    """Base class for game

    Inherited classes needs attr name implementation
    """

    @abstractmethod
    def add(self, component: str, name: Optional[str] = None) -> None:
        """Add stuff or tools to game

        Args:
            component (str): stuff or tool type
            name (str, optional): name of added component.
                                  Defaults to None.
        """


@dataclass
class BaseStuff(Base):
    """Base class for game stuff (like dices or cards)

    Inherited classes needs attr name implementation
    """


@dataclass
class BaseTool(Base):
    """Base class for game tools (like decks or shakers)

    Inherited classes needs attr name implementation
    """
    _stuff_to_add: BaseStuff = field(
        metadata=config(exclude=lambda x: True),
        repr=False,
        init=False
        )
    stuff: Components = field(default_factory=Components, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

    def add(self, name: str, game: BaseGame, count: int = 1) -> None:
        """Add stuff to the tool stuff collection

        Args:
            name (str): name of stuff
            count (int, optional): count of stuff copy Defaults to 1.

        Raises:
            StuffDefineError: count of stuff nonpositive
                              or stuff not exist
        """
        if name not in game.stuff.keys():
            raise StuffDefineError(
                message=f"Stuff with {name=} not exist in a game.",
                logger=self.logger
                )

        if count < 1:
            raise StuffDefineError(
                message=f"Can't add {count} stuff.",
                logger=self.logger
                )

        # add stuff and set a count
        if name not in self.stuff.get_names():
            self.stuff.add(
                self._stuff_to_add,
                **game.stuff[name].to_dict()
                )
            self.stuff[name].count = count
            self.logger.debug(
                f'Added stuff with "{name=}" and {count=}.'
                )

        # if exist increase a count
        else:
            self.stuff[name].count += count
            self.logger.debug(
                f'Number of stuff with "{name=}" increased by {count}. ' +
                f'Result count is {self.stuff[name].count}'
                )

    def _decrease(self, name: str, count: int) -> None:
        """Decrease number of stuff by count

        Args:
            name (str): name of stuff
            count (int): count
        """
        self.stuff[name].count -= count
        self.logger.debug(
            f'Removed {count} stuff with {name=}. ' +
            f'Result count is {self.stuff.get(name, 0)}'
            )
        if self.stuff[name].count <= 0:
            del self.stuff[name]

    def remove(
        self,
        name: Optional[str] = None,
        count: Optional[int] = None
            ) -> None:
        """Remove any kind of stuff copy from tool by its name and count

        Args:
            name (str, optional): name of stuff. Defaults to None.
            count (int, optional): count of stuff. Defaults to None.

        You can use any combination for names and counts to remove all
        stuff, all or any by name or by count.


        Raises:
            StuffDefineError: nonpositive integer for count
        """
        if count is not None and count <= 0:
            raise StuffDefineError(
                f"Count must be a integer greater than 0.",
                logger=self.logger
                )

        if name is None:

            if count is None:
                self.stuff = Components()
                self.logger.debug('Removed all stuff')
            else:
                for stuff in list(self.stuff.keys()):
                    self._decrease(stuff, count)

        elif self.stuff.get(name):
            if count is None:
                del self.stuff[name]
                self.logger.debug(
                    f'Removed all stuff with {name=}.'
                    )
            else:
                self._decrease(name, count)

        else:
            raise StuffDefineError(
                message=f"Stuff with {name=} not exist in tool.",
                logger=self.logger
                )


@dataclass
class BasePlayer(Base):
    """Base class for game players and bots

    Inherited classes needs attr name implementation

    Attrs

        - is_active (bool): Default to True.
        - has_priority (bool): Default to False
        - team (str, optioanl): team name for this player
        - owner_of (List[str]): list of objects owned by player Default to []
        - user_of (List[str]): list of objects used by player Default to []

    """
    is_active: bool = True
    has_priority: bool = False
    team: Optional[str] = None
    owner_of: List[str] = field(default_factory=list, init=False)
    user_of: List[str] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
