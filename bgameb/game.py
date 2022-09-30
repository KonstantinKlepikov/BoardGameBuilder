"""Main engine to create games
"""
from typing import Literal, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bgameb.base import Base
from bgameb.rules import RulesMixin
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
        self,
        component: component,
        name: str,
        **kwargs: Dict[str, Any]
            ) -> None:
        """Add object to game

        Args:
            component (component): type of added component.
            name (str): name of added component.
            **kwargs (Dict[str,Any]): dict of named args
        """

    @abstractmethod
    def add_to(
        self,
        name: str,
        to: str,
        **kwargs: Dict[str, Any]
            ) -> None:
        """Add stuff to game tool

        Args:
            name (str): name of added stuff.
            to (str): name of tool, where added
            **kwargs (Dict[str,Any]): dict of named args
        """


@dataclass
class Game(RulesMixin, BaseGame):
    """Create the game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()

    def add(
        self,
        component: component,
        name: str,
        **kwargs
            ) -> None:
        for source in [STUFF, TOOLS, PLAYERS]:
            if component in source.keys():
                self._add(source[component], name=name, **kwargs)
                self.logger.info(f'{name} is added to game.')
                break
        else:
            raise ComponentClassError(component, self.logger)

    def add_to(
        self,
        to: str,
        name: str,
        **kwargs
            ) -> None:
        if name in self.keys() and to in self.keys():
            self[to]._increase(name=name, game=self, **kwargs)
            self.logger.info(f'{name} is added to {to}.')
        else:
            raise ComponentClassError(name, self.logger)


if __name__ == '__main__':
    game = Game('one_board_game')
    game.add('card', name='one_card')
    game.add('deck', name='cards_deck')
    game.add_to('cards_deck', 'one_card', count=3)
    game.add_rule('this_rule', "The text is short, but the rule is important")
    game.cards_deck.deal()
    print(game)
    print('='*20)
    print(game.to_dict())
