"""Base constructs for build package objects
"""
import re
import string
from typing import List, Optional, Iterator
from collections.abc import Mapping
from collections import Counter
from dataclasses import dataclass, field, make_dataclass
from dataclasses_json import dataclass_json, config
from bgameb.errors import (
    ComponentNameError, ComponentClassError, ComponentIdError
        )
from loguru import logger


logger.disable('bgameb')


def log_enable(
    log_path: str = './logs/game.log',
    log_level: str = 'DEBUG'
        ) -> None:
    """Enable logging

    Args:
        log_path (str, optional): path to log file.
                                  Defaults to './logs/game.log'.
        log_level (str, optional): logging level. Defaults to 'DEBUG'.
    """
    logger.remove()
    logger.add(
        sink=log_path,
        level=log_level,
        format='{extra[classname]}: "{extra[name]}" -> func {function} | ' +
        '{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
    )
    logger.enable('bgameb')


@dataclass_json
@dataclass(repr=False)
class Component(Mapping):
    """Component mapping
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

    def __iter__(self) -> Iterator:
        return iter(self.__dict__)

    def __getattr__(self, attr: str):
        try:
            return self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __delattr__(self, attr: str) -> None:
        try:
            del self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setitem__(self, attr: str, value):
        attr = self._make_name(attr)
        self.__dict__.update({attr: value})

    def __getitem__(self, attr: str):
        return self.__dict__[attr]

    def __delitem__(self, attr: str) -> None:
        del self.__dict__[attr]

    def __repr__(self):
        items = (
            f"{k}={v!r}" for k, v
            in self.__dict__.items()
            if not k.startswith('_')
            and not k.startswith('current')
                )
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __len__(self) -> int:
        return len(self.__dict__)

    def _is_unique(self, name: str) -> Optional[bool]:
        """Chek is name of nested component is unique
        for based component __dict__

        Args:
            name (str): name of component

        Raises:
            ComponentNameError: name not unique

        Returns:
            True: is unique
        """
        if name not in self.__dict__.keys():
            return True
        raise ComponentNameError(name)

    def _is_valid(self, name: str) -> bool:
        """Chek is name of component contains correct symbols
        match [a-zA-Z_][a-zA-Z0-9_]*$ expression:

            * a-z, A-Z, 0-9 symbols
            * first letter not a number amd not a _
            * can be used _ symbol in subsequent symbols

        Args:
            name (str): name of component

        Raises:
            ComponentNameError: name is not valid

        Returns:
            bool: is valid
        """
        if re.match("[a-z][a-z0-9_]*$", str(name)):
            return True
        return False

    def _make_name(self, name: str) -> str:
        """
        Replace spaces and other specific characters
        in the name with _

        Args:
            name (str): name of component

        Returns:
            name (str): safe name of component
        """
        name = str(name).lower()
        available = set(string.ascii_letters.lower() + string.digits + '_')

        if " " in name:
            name = name.replace(' ', '_')

        diff = set(name).difference(available)
        if diff:
            for char in diff:
                name = name.replace(char, '_')

        if not self._is_valid(name):
            raise ComponentNameError(name)

        return name

    def _update(
        self,
        component,
            ) -> None:
        """Update Component dict with safe name

        Args:
            component: component instance
        """
        name = self._make_name(component.id)

        if self._is_unique(name):
            comp = component.__class__(**component.to_dict())

        if name not in self.__dataclass_fields__.keys():
            self.__class__ = make_dataclass(
                self.__class__.__name__,
                fields=[(name, type(comp), field(default=comp))],
                bases=(self.__class__, ),
                repr=False
                )

        self.__dict__.update({name: comp})

    def get_names(self) -> List[str]:
        """Get names of all components in Component

        Returns:
            List[str]: list of components names
        """
        return [
            name for name
            in self.__dict__.keys()
            if not name.startswith('_')
                ]


@dataclass_json
@dataclass(repr=False)
class Base(Component):
    """Base class for game, stuff, tools players and other components

    Attr:
        - id (str): id of component
        - counter (Counter): counter object
        - _type (Optional[str]): type for check when this component
          can be added
        - _types_to_add (List[str]): types of components, that can
          be added

    Counter is a 'collection.Counter
    <https://docs.python.org/3/library/collections.html#collections.Counter>'
    object
    """
    id: str
    counter: Counter = field(default_factory=dict)  # type: ignore
    _type: Optional[str] = field(
        default=None,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )
    _types_to_add: List[str] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )

    def __post_init__(self) -> None:
        # check id
        if not isinstance(self.id, str):
            raise ComponentIdError(self.id)

        # int counter
        self.counter = Counter()

        # set self_type
        self._type = self.__class__.__name__.lower()

        # set logger
        self._logger = logger.bind(
            classname=self.__class__.__name__,
            name=self.id)
        if self._type == 'game':
            self._logger.info('===========NEW GAME============')
        self._logger.info(
            f'{self.__class__.__name__} created with id="{self.id}".'
            )

    def add(self, component) -> None:
        """Add another component to this component

        Args:
            component (Component): component instance
        """
        if component._type in self._types_to_add:
            self._update(component)
            self._logger.info(f'"{component.id}" is added to "{self.id}".')
        else:
            raise ComponentClassError(component, self._logger)
