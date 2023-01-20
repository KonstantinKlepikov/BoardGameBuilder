"""Base constructs for build package objects
"""
import re
import string
import json
from typing import (
    Optional, Iterator, TypeVar, Generic, Any, Union, AbstractSet
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
    Workaround for serializing properties with pydantic
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

    Attr:
        - id (str): id of stuff
        - counter (Counter): counter object
        - _logger (Logger): loguru logger

    Counter is a `collection.Counter
    <https://docs.python.org/3/library/collections.html#collections.Counter>`_
    """
    id: str
    counter: Counter = Field(default_factory=Counter, exclude=True, repr=False)
    _logger: Logger = Field(...)

    def __init__(self, **data):
        super().__init__(**data)

        # init counter
        self.counter = Counter()

        # set logger
        self._logger = logger.bind(
            classname=self.__class__.__name__,
            name=self.id)

    class Config:
        underscore_attrs_are_private = True


K = TypeVar('K', bound=str)
V = TypeVar('V', bound=Base)


class Component(GenericModel, Generic[K, V], Mapping[K, V]):
    """Component mapping
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
