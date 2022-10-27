"""Base constructs for build package objects
"""
from typing import Dict, List, Optional, Any, Iterator, Tuple
from collections.abc import Mapping
from dataclasses import dataclass, field, make_dataclass
from heapq import heappop, heappush
from dataclasses_json import config, dataclass_json
from bgameb.errors import ComponentNameError
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
class Components(Mapping):
    """Components mapping
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

    def __setitem__(self, attr: str, value) -> None:
        self.__dict__.update({attr: value})

    def __getitem__(self, attr: str):
        return self.__dict__[attr]

    def __delitem__(self, attr: str) -> None:
        del self.__dict__[attr]

    def __repr__(self):
        items = (
            f"{k}={v!r}" for k, v
            in self.__dict__.items()
            if not k.startswith('_') and not k.startswith('current')
            )
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __len__(self) -> int:
        return len(self.__dict__)

    def _chek_in(self, name: str) -> Optional[bool]:
        """Chek is name of component is unique

        Args:
            name (str): name of component

        Raises:
            ComponentNameError: name id not unique

        Returns:
            Optional[bool]: if it is in Components and unique
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
            kwargs (Dict[str, Any]): additional args for component
        """
        comp = component(**kwargs)

        if kwargs['name'] not in self.__dataclass_fields__.keys():
            self.__class__ = make_dataclass(
                self.__class__.__name__,
                fields=[(kwargs['name'], type(comp), field(default=comp))],
                bases=(self.__class__, ),
                repr=False
                )

        self.__dict__.update({kwargs['name']: comp})

    def _add(self, component, **kwargs) -> None:
        """Add component to Components dict. Components with
        same names as existed in Components cant be added.

        Raises:
            ComponentNameError: name not unique

        Args:
            component: component class
            kwargs: additional args for component
        """
        if kwargs.get('name'):
            self._chek_in(kwargs['name'])
        else:
            self._chek_in(component.name)
            kwargs['name'] = component.name

        self._update(component, kwargs)

    def _add_replace(self, component, **kwargs) -> None:
        """Add or replace component in Components dict.

        Args:
            component: component class
            kwargs: additional args for component
        """
        if not kwargs.get('name'):
            kwargs['name'] = component.name
        self._update(component, kwargs)

    def get_names(self) -> List[str]:
        """Get names of all components in Components

        Returns:
            List[str]: list of components names
        """
        return list(self.__dict__)


@dataclass_json
@dataclass
class Order:
    """Order of steps priority queue. Isnt tradesafe.
    Can be used for define geme steps order.

    Args:

        - current List[Tuple[int, Components]]: priority queue list
    """
    current: List[Tuple[int, Components]] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )

    def __len__(self) -> int:
        """Len of queue

        Returns:
            int: len of current queue
        """
        return len(self.current)

    def clear(self) -> None:
        """Clear the current queue
        """
        self.current = []

    def put(self, item) -> None:
        """Put Step object to queue

        Args:
            item (Step): Step class instance
        """
        heappush(self.current, (item.priority, item))

    def get(self) -> Components:
        """Get Syep object from queue with lowest priority

        Returns:
            Step: Step instance object
        """
        return heappop(self.current)[1]


@dataclass_json
@dataclass(repr=False)
class Base(Components):
    """Base class for game, stuff, tools players and other components

    Args:

        - name (str): name of component
    """
    name: str

    def __post_init__(self) -> None:
        # check name
        if not isinstance(self.name, str):
            raise ComponentNameError(
                name=self.name
            )

        # set logger
        self._logger = logger.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self._logger.info(
            f'{self.__class__.__name__} created with {self.name=}.'
            )
