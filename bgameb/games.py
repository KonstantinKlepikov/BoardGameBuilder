"""Main engine to create game object
"""
from typing import Union, NamedTuple, TypeVar
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.rollers import BaseRoller
from bgameb.shakers import Shaker
from bgameb.utils import log_me


Component = TypeVar('Component', bound=Union[Shaker, BaseRoller])


class GameShakers(NamedTuple):
    """Game shakers collection
    """


@dataclass
class Game(DataClassJsonMixin):
    """Create the game object
    """

    name: str = 'game'
    shakers: NamedTuple = field(default_factory=tuple, init=False)

    def __post_init__(self) -> None:
        self.shakers = GameShakers()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(f'Game created.')

    def add(self, component: Component) -> None:
        """Add game component to game

        Args:
            component (Component): any class instance of components
        """
        # TODO: separate by type without if's, remove tuple
        if isinstance(component, Shaker):

            sh_dict = self.shakers._asdict()
            sh_dict[component.name] = component
            sh_types = self.shakers.__annotations__
            sh_types[component.name] = type(component)

            gsh = NamedTuple('GameShakers', sh_types.items())
            self.shakers = gsh(**sh_dict)

            self.logger.info(f'Added {self.shakers}.')
