"""Base constructs for build package objects
"""
from typing import (
    Dict, List, Optional, Any, Iterable, Sequence
    )
from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config
from bgameb.errors import ComponentNameError
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
        self.__dict__.update(
            {kwargs['name']: component(**kwargs)}
            )

    def add(self, component, **kwargs) -> None:
        """Add component to Components dict. Components with
        same names as existed cant be added.

        Raises:
            ComponentNameError: name id not unique

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
        if not self.name:
            self.name = get_random_name()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(
            f'{self.__class__.__name__} created with {self.name=}.'
            )

    @staticmethod
    def _chek_name(name: str, chek: Sequence[str]) -> bool:
        """Chek exist name string in seequence
        # TODO: test me

        Args:
            name (str): name sting
            check (Sequence[str]): cheked collection

        Returns:
            bool: name is exist or not in collection
        """
        if name in chek:
            return True
        return False


@dataclass
class BaseStuff(Base, ABC):
    """Base class for game stuff (like dices and cards)

    Inherited classes needs attr name implementation
    """


@dataclass
class BaseTool(Base, ABC):
    """Base class for game tools (like decs and shakers)

    Inherited classes needs attr name implementation
    """

    @abstractmethod
    def add(self, name: str, count: int = 1) -> None:
        """Add stuff to tool
        Args:
            name (str): name of added stuff
            count (int, optional): count added stuf. Defaults to 1.
        """

    @abstractmethod
    def remove(
        self,
        name: Optional[str] = None,
        count: Optional[int] = None
            ) -> None:
        """Remove stuff from tool

        Args:
            name (str, optional): name of removed stuff. Defaults to None.
            count (int, optional): count removed stuf. Defaults to None.
        """


@dataclass
class BasePlayer(Base, ABC):
    """Base class for game players and bots

    Inherited classes needs attr name implementation
    """
