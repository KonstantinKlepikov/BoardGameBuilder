"""Base constructs for build package objects
"""
from typing import (
    Dict, List, Optional, Any, Iterable
    )
from abc import ABC
from collections.abc import Mapping
from dataclasses import dataclass, field, make_dataclass
from dataclasses_json import DataClassJsonMixin
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


@dataclass(init=False)
class Components(Mapping, DataClassJsonMixin):
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

    def __iter__(self) -> Iterable:
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
        comp = component(**kwargs)

        if kwargs['name'] not in self.__dataclass_fields__.keys():
            self.__class__ = make_dataclass(
                self.__class__.__name__,
                fields=[(kwargs['name'], type(comp), field(default=comp))],
                bases=(self.__class__, ),
                )

        self.__dict__.update({kwargs['name']: comp})

    def _add(self, component, **kwargs) -> None:
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

    def _add_replace(self, component, **kwargs) -> None:
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


@dataclass
class Base(Components, DataClassJsonMixin, ABC):
    """Base class for game, stuff and tools
    """
    name: str
    is_active: bool = True

    def __post_init__(self) -> None:
        # check name
        if not isinstance(self.name, str):
            raise ComponentNameError(
                name=self.name
            )

        # set logger
        self.logger = logger.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(
            f'{self.__class__.__name__} created with {self.name=}.'
            )
