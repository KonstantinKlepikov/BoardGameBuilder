"""Main engine to create game object
"""
from typing import Union, NamedTuple, TypeVar
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.rollers import BaseRoller
from bgameb.shakers import Shaker
from bgameb.utils import logger


Component = TypeVar('Component', bound=Union[Shaker, BaseRoller])


class GameShakers(NamedTuple):
    name: str = 'game_shakers'


@dataclass
class Game(DataClassJsonMixin):
    """Create the game object
    """

    name: str = 'game'
    shakers: NamedTuple = field(default_factory=tuple, init=False)
    # logging: bool = False
    # log_level: str = 'INFO'

    def __post_init__(self):
        self.shakers = GameShakers()

        # set logger
        # if self.logging:
        #     logger.enable('bgameb')
        #     my_filter.level = self.log_level
            # self.logger = logger.bind(
            #     game_name=self.name,
            #     classname=self.__class__.__name__,
            #     name=self.name)
            # self.logger.info(f'Game created. Logging level="{self.log_level}"')
        self.logger = logger.bind(
            game_name=self.name,
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(f'Game created.')

    def add_component(self, component: Component) -> None:
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

            GameShakers = NamedTuple('GameShakers', sh_types.items())
            self.shakers = GameShakers(**sh_dict)
