"""Main engine to create games
"""
from typing import Optional, Type
from dataclasses import dataclass, field
from bgameb.tools import Shaker
from bgameb.stuff import BaseRoller, BaseCard
from bgameb.errors import ComponentClassError
from bgameb.constructs import Components, Base, BaseStuff


@dataclass
class Game(Base):
    """Create the game object
    """
    name: Optional[str] = None
    shakers: Components = field(default_factory=Components, init=False)
    decks: Components = field(default_factory=Components, init=False)
    game_rollers: Components = field(default_factory=Components, init=False)
    game_cards: Components = field(default_factory=Components, init=False)

    def __post_init__(self) -> None:
        self.shakers = Components()
        self.decks = Components()
        self.game_rollers = Components()
        self.game_cards = Components()
        super().__post_init__()

    def add_stuff(self, stuff: Type[BaseStuff], **kwargs) -> None:
        """Add component to game

        Args:
            stuff (Type[game_stuff_type]): any class instance of game stuffs
            like rollers, cards etc
            kwargs: additional arguments of component
        """
        if issubclass(stuff, BaseRoller):
            self.game_rollers.add(stuff, **kwargs)
            self.logger.info(f'Roller added: {self.game_rollers=}.')
        elif issubclass(stuff, BaseCard):
            self.game_cards.add(stuff, **kwargs)
            self.logger.info(f'Card added: {self.game_cards=}.')
        else:
            raise ComponentClassError(class_=stuff)

    def add_shaker(self, name: Optional[str] = None) -> None:
        """Add shaker to game shakers

        Args:
            name (str): name for added shaker
        """
        if name:
            self.shakers.add(
                Shaker, name=name, _game_rollers=self.game_rollers
                )
        else:
            self.shakers.add(
                Shaker, name=Shaker.name, _game_rollers=self.game_rollers
                )
