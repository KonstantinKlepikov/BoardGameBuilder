"""Base constructs for build package objects
"""
import re
import string
import json
from typing import (
    Optional, Iterator, TypeVar, Generic, Any, Union, AbstractSet,
    Iterable
        )
from collections.abc import Mapping, KeysView, ValuesView, ItemsView
from collections import Counter
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from bgameb.errors import ComponentNameError
from loguru._logger import Logger
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


IntStr = Union[int, str]
AbstractSetIntStr = AbstractSet[IntStr]
MappingIntStrAny = Mapping[IntStr, Any]


# TODO: test me
class PropertyBaseModel(BaseModel):
    """
    Serializing properties with pydantic
    https://github.com/samuelcolvin/pydantic/issues/935
    https://github.com/pydantic/pydantic/issues/935#issuecomment-554378904
    https://github.com/pydantic/pydantic/issues/935#issuecomment-1152457432
    """
    @classmethod
    def get_properties(cls):
        return [
            prop for prop
            in dir(cls)
            if isinstance(getattr(cls, prop), property)
            and prop not in ("__values__", "fields")
                ]

    def dict(
        self,
        *,
        include: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        exclude: Union[AbstractSetIntStr, MappingIntStrAny] = None,
        by_alias: bool = False,
        skip_defaults: bool = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        attribs = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )
        props = self.get_properties()
        # Include and exclude properties
        if include:
            props = [prop for prop in props if prop in include]
        if exclude:
            props = [prop for prop in props if prop not in exclude]

        # Update the attribute dict with the properties
        if props:
            attribs.update({prop: getattr(self, prop) for prop in props})

        return attribs


class Base(PropertyBaseModel):
    """Base class for game, stuff, tools players and other stuff

    ..
        Attr:

            id (str): id of stuff

            _counter (Counter): Counter object.
                                Isn't represented in final json or dict.
                                Is initialized automaticaly by __init__.
                                Counter is a collection.Counter.

            _logger (Logger): loguru logger

        Counter is a `collection.Counter
        <https://docs.python.org/3/library/collections.html#collections.Counter>`_
    """
    id: str
    _counter: Counter[Any] = Field(default_factory=Counter)
    _logger: Logger = Field(...)

    def __init__(self, **data):
        super().__init__(**data)

        self._counter = Counter()
        self._logger = logger.bind(
            classname=self.__class__.__name__,
            name=self.id)

    class Config:
        underscore_attrs_are_private = True


class BaseGame(Base):

    def __init__(self, **data):
        super().__init__(**data)

        self._logger.info('===========NEW GAME============')
        self._logger.info(
            f'{self.__class__.__name__} created with id="{self.id}".'
                )


class BasePlayer(Base):
    """Base class for players
    """


class BaseItem(Base):
    """Base class for game items (like dices or cards)
    """


K = TypeVar('K', bound=str)
V = TypeVar('V', bound=BaseItem)


class Component(GenericModel, Generic[K, V], Mapping[K, V]):
    """Components mapping - this represents a collection of items or
    tools, used for create instance of game objects, like dices or decks
    """

    def __init__(
        self,
        *args: tuple[dict[K, V]],
        **kwargs: dict[K, V]
            ) -> None:
        for arg in args:
            if isinstance(arg, dict):
                for k, v, in arg.items():
                    self.__dict__[k] = v
            else:
                raise AttributeError('Args must be a dict of dicts')
        if kwargs:
            for k, v, in kwargs.items():
                self.__dict__[k] = v

    def __iter__(self) -> Iterator:  # type: ignore
        return iter(self.__dict__)

    def __setattr__(self, attr: K, value: V) -> None:  # type: ignore
        self.__setitem__(attr, value)

    def __getattr__(self, attr: K) -> V:  # type: ignore
        try:
            return self.__getitem__(attr)
        except KeyError:
            raise AttributeError(attr)

    def __delattr__(self, attr: K) -> None:  # type: ignore
        try:
            self.__delitem__(attr)
        except KeyError:
            raise AttributeError(attr)

    def __setitem__(self, attr: K, value: V) -> None:
        self.__dict__[attr] = value

    def __getitem__(self, attr: K) -> V:
        return self.__dict__[attr]  # type: ignore

    def __delitem__(self, attr: K) -> None:
        del self.__dict__[attr]

    def __repr__(self) -> str:
        items = list(
            {f"{k}: {v!r}" for k, v in self.items()}
                )
        return f"{{{', '.join(items)}}}"

    def __len__(self) -> int:
        return len(self.__dict__)

    def keys(self) -> KeysView[K]:
        return self.__dict__.keys()  # type: ignore

    def values(self) -> ValuesView[V]:
        return self.__dict__.values()

    def items(self) -> ItemsView[K, V]:
        return self.__dict__.items()  # type: ignore

    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=lambda c: c.dict())

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
        if name is None:
            name = self._make_name(stuff.id)
        else:
            name = self._make_name(name)

        comp = stuff.__class__(**stuff.dict())
        self.__dict__[name] = comp

    @property
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


class BaseTool(Base, GenericModel, Generic[K, V]):
    """Base class for game tools
    """
    c: Component[K, V] = Field(
        default_factory=Component[K, V], exclude=True, repr=False
            )
    current: list[V] = []
    last: Optional[V] = None

    class Config(Base.Config):
        json_encoders = {
            Component: lambda c: c.to_json()
                }

    @property
    def current_ids(self) -> list[str]:
        """Get ids of current objects

        Returns:
            List[str]: list ids of current
        """
        return [item.id for item in self.current]

    @property
    def last_id(self) -> Optional[str]:
        """Get id of last

        Returns:
            Optional[str]: id
        """
        if self.last is not None:
            return self.last.id
        return None

    def get_items(self) -> dict[str, V]:
        """Get items from Component

        Returns:
            dict[str, Item]: items mapping
        """
        return {item.id: item for item in self.c.values()}

    def _item_replace(self, item: V) -> V:
        """Get item replaced copy

        Returns:
            Item (Item): an item object
        """
        return item.__class__(**item.dict())

    def by_id(self, id: str) -> list[V]:
        """Get item from current by its id

        Args:
            id (str): item id

        Returns:
            list[Item]: items
        """
        return [item for item in self.current if item.id == id]

    def clear(self) -> None:
        """Clear the current and last
        """
        self.current.clear()
        self.last = None
        self._logger.debug('Current and last clear!')

    def append(self, item: V) -> None:
        """Append item to current

        Args:
            item (Item): appended items
        """
        item = self._item_replace(item)
        self.current.append(item)
        self._logger.debug(f'To current is appended item: {item.id}')

    def count(self, item_id: str) -> int:
        """Count the number of current items with given id.

        Args:
            item_id (str: an item id

        Returns:
            int: count of items
        """
        count = self.current_ids.count(item_id)
        self._logger.debug(f'Count of {item_id} in current is {count}')
        return count

    def extend(self, items: Iterable[V]) -> None:
        """Extend the current by appending items
        started from the left side of iterable.

        Args:
            items (Iterable[Item]): iterable with items
        """
        items = [self._item_replace(item) for item in items]
        self.current.extend(items)
        self._logger.debug(
            f'Current are extended by {[item.id for item in items]} from right'
                )

    def index(
        self,
        item_id: str,
        start: int = 0,
        end: Optional[int] = None
            ) -> int:
        """Return the position of item in the current
        (after index start and before index stop).
        Returns the first match or raises ValueError if not found.

        Args:
            item_id (str): an item id
            start (int): start index. Default to 0.
            end (int, optional): stop index. Default to None.

        Returns:
            int: index of the the first match
        """
        names = self.current_ids
        ind = names.index(item_id, start) if end is None \
            else names.index(item_id, start, end)
        self._logger.debug(f'Index of {item_id} in current is {ind}')
        return ind

    def insert(self, item: V, pos: int) -> None:
        """Insert item into the current at given position.

        Args:
            item (Item): an item object
            pos (int): position
        """
        item = self._item_replace(item)
        self.current.insert(pos, item)
        self._logger.debug(f'To current is inserted {item.id} on {pos=}')

    def pop(self) -> V:
        """Remove and return an item from the current.
        If no items are present, raises an IndexError.

        Returns:
            Item: an item object
        """
        self.last = self.current.pop()
        self._logger.debug(f'{self.last.id} is poped from current')
        return self.last

    def remove(self, item_id: str) -> None:
        """Remove the first occurrence of item from current.
        If not found, raises a ValueError.
        Args:
            item_id (str): an item id
        """
        ind = self.index(item_id)
        item = self.current[ind]
        self.current.remove(item)
        self._logger.debug(f'Is removed from current {item_id}')

    def reverse(self) -> None:
        """Reverse the items in the current.
        """
        self.current.reverse()
        self._logger.debug('Current is reversed')
