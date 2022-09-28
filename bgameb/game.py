"""Main engine to create games
"""
from typing import Optional, Literal
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bgameb.base import Base
from bgameb.tools import TOOLS, TOOLS_TYPES
from bgameb.stuff import STUFF, STUFF_TYPES
from bgameb.players import PLAYERS, PLAERS_TYPES
from bgameb.errors import ComponentClassError


component = Literal[STUFF_TYPES, TOOLS_TYPES, PLAERS_TYPES]


@dataclass
class BaseGame(Base, ABC):
    """Base class for game
    """

    @abstractmethod
    def add(
        self, component: component, name: Optional[str] = None, **kwargs
            ) -> None:
        """Add stuff or tools to game

        Args:
            component (component): type of added component.
            name (str, optional): name of added component.
                                  Defaults to None.
            **kwargs (any): dict of named args
        """


@dataclass
class Game(BaseGame):
    """Create the game object

    Attrs

        - name (str): game name
    """

    def __post_init__(self) -> None:
        super().__post_init__()

    def add(
        self,
        component: component,
        name: Optional[str] = None,
        **kwargs
            ) -> None:
        for source in [STUFF, TOOLS, PLAYERS]:
            if component in source.keys():
                self._add(source[component], name=name, **kwargs)
                self.logger.info(f'{component} is added: {self.get_names()}.')
                break
        else:
            raise ComponentClassError(component, self.logger)
