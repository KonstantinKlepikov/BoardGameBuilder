"""Base constructs for build package objects
"""
import re
import string
from typing import Optional, Iterator, TypeVar, Any
from collections.abc import Mapping, KeysView, ValuesView, ItemsView
from collections import Counter
from dataclasses import dataclass, field
from dataclasses_json import (
    dataclass_json, DataClassJsonMixin, Undefined, CatchAll,
    config
        )
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


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Base(DataClassJsonMixin):
    """Base class for game, stuff, tools players and other stuff

    Attr:
        - id (str): id of stuff
        - other (Dict[str, Any]): all other data, added to instance
                                  at declaration
        - counter (Counter): counter object
        - _to_relocate (dict[str, str): mapping for relocation any data
                                         to attributes inside dataclass. You
                                         can use names of attributes or methods
                                         of class for this mapping.

    Counter is a `collection.Counter
    <https://docs.python.org/3/library/collections.html#collections.Counter>`_
    """
    id: str
    other: CatchAll = field(
        default_factory=dict,
        metadata=config(exclude=lambda x: True),  # type: ignore
            )
    counter: Counter = field(
        default_factory=Counter,
        metadata=config(exclude=lambda x: True),  # type: ignore
            )
    _to_relocate: dict[str, str] = field(
        default_factory=dict,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        init=False,
    )

    def __post_init__(self) -> None:
        # check id
        if not isinstance(self.id, str):
            raise ComponentIdError(self.id)

        # int counter
        self.counter = Counter()

        # set logger
        self._logger = logger.bind(
            classname=self.__class__.__name__,
            name=self.id)

    @property
    def _inclusion(self) -> dict[str, Any]:
        return {
            k: v for k, v
            in self.__dict__.items()
            if not k.startswith('_')
            and k not in ['current', 'last', 'other']
                }

    def __repr__(self) -> str:
        items = {f"{k}={v!r}" for k, v in self._inclusion.items()}
        return f"{type(self).__name__}({', '.join(items)})"

    def relocate(self) -> 'Base':
        """Relocate data. For this is used mapping from
        _to_relocate attribute

        Returns:
            Base
        """
        for key, val in self._to_relocate.items():
            if key in self._inclusion.keys() and val in dir(self):

                if callable(getattr(self, val)):
                    self.__dict__[key] = getattr(self, val)()
                    self._logger.info(f'Is used "{val}" to fill "{key}".')
                else:
                    self.__dict__[key] = self.__dict__.get(val)
                    self._logger.info(f'"{val}" is relocated to "{key}".')

        return self


V = TypeVar('V', bound=Base)


class Component(Mapping[str, V]):
    """Component mapping
    """
    __inclusion__: dict[str, V]

    def __init__(
        self,
        *args,
        **kwargs
            ) -> None:
        """Args must be a dicts
        """
        self.__dict__.update(__inclusion__={})

        for arg in args:
            if isinstance(arg, dict):
                for k, v, in arg.items():
                    self.update(stuff=v, name=k)
            else:
                raise AttributeError('Args must be a dict of dicts')
        if kwargs:
            for k, v, in kwargs.items():
                self.update(stuff=v, name=k)

        # set logger
        self.__dict__.update({'_logger': logger.bind(
            classname=self.__class__.__name__,
            name='component'
                )})

    def __iter__(self) -> Iterator:
        return iter(self.__inclusion__)

    def __setattr__(self, attr: str, value: V) -> None:
        raise NotImplementedError

    def __getattr__(self, attr: str) -> V:
        try:
            return self.__getitem__(attr)
        except KeyError:
            raise AttributeError(attr)

    def __delattr__(self, attr: str) -> None:
        try:
            self.__delitem__(attr)
        except KeyError:
            raise AttributeError(attr)

    def __setitem__(self, attr: str, value: V) -> None:
        raise NotImplementedError

    def __getitem__(self, attr: str) -> V:
        return self.__inclusion__[attr]

    def __delitem__(self, attr: str) -> None:
        del self.__inclusion__[attr]

    def __repr__(self) -> str:
        items = list({f"{k}={v!r}" for k, v in self.items()})
        return f"{{{', '.join(items)}}}"

    def __len__(self) -> int:
        return len(self.__inclusion__)

    def keys(self) -> KeysView[str]:
        return self.__inclusion__.keys()

    def values(self) -> ValuesView[V]:
        return self.__inclusion__.values()

    def items(self) -> ItemsView[str, V]:
        return self.__inclusion__.items()

    def _is_unique(self, name: str) -> bool:
        """Chek is name of nested stuff is unique

        Args:
            name (str): name of stuff

        Raises:
            ComponentNameError: name not unique

        Returns:
            True: is unique
        """
        if name in self.keys():
            raise ComponentNameError(name)
        return True

    def _is_valid(self, name: str) -> bool:
        """Chek is name of stuff contains correct symbols
        match [a-zA-Z_][a-zA-Z0-9_]*$ expression:

            * a-z, A-Z, 0-9 symbols
            * first letter not a number amd not a _
            * can be used _ symbol in subsequent symbols

        Args:
            name (str): name of stuff

        Raises:
            ComponentNameError: name is not valid

        Returns:
            Trye: is valid
        """
        if not re.match("[a-z][a-z0-9_]*$", str(name)):
            raise ComponentNameError(name)
        return True

    def _make_name(self, name: str) -> str:
        """
        Replace spaces and other specific characters
        in the name with _

        Args:
            name (str): name of stuff

        Returns:
            name (str): safe name of stuff
        """
        name = str(name).lower()
        available = set(string.ascii_letters.lower() + string.digits + '_')

        if " " in name:
            name = name.replace(' ', '_')

        diff = set(name).difference(available)
        if diff:
            for char in diff:
                name = name.replace(char, '_')

        self._is_valid(name)
        self._is_unique(name)

        return name

    def update(
        self,
        stuff: V,
        name: Optional[str] = None,
            ) -> None:
        """Update Component dict with safe name

        Args:
            stuff (Type[Base]): Base subclass instance
            name (Optional[str]). key to update dict. Defult to None.
        """
        if not issubclass(stuff.__class__,  Base):
            raise ComponentClassError(stuff, self._logger)

        if name is None:
            name = self._make_name(stuff.id)
        else:
            name = self._make_name(name)

        comp = stuff.__class__(**stuff.to_dict())  # type: ignore
        self.__inclusion__.update({name: comp})

    def ids(self) -> list[str]:
        """Get ids of all added stuff in Component

        Returns:
            List[str]: list of stuff ids
        """
        return [stuff.id for stuff in self.values()]

    def by_id(self, id: str) -> Optional[V]:
        """Get stuff object by its id

        Args:
            id (str): stuff id

        Returns:
            V, optional: stuff object
        """
        for comp in self.values():
            if comp.id == id:
                return comp
        return None
