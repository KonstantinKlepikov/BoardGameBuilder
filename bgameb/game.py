"""Main engine to create games
"""
from typing import Optional
from dataclasses import dataclass, field
from bgameb.base import Base, log_enable
from bgameb.types import (
    COMPONENTS, NONSTUFF, COMPONENTS_TYPES, NONSTUFF_TYPES,
    STUFF_TYPES, STUFF
)
from bgameb.tools import Rules, Turn
from bgameb.errors import ComponentClassError


@dataclass
class BaseGame(Base):
    """Base class for game
    """
    game_rules: Rules = field(init=False)
    turn_order: Turn = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.game_rules = Rules('game_rules')
        self.turn_order = Turn('turn_order')


@dataclass
class Game(BaseGame):
    """Create the game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()

    # def add(
    #     self,
    #     component: COMPONENTS_TYPES,
    #     name: str,
    #     **kwargs
    #         ) -> None:
    #     """Add stuff to game tool

    #     Args:
    #         name (str): name of added stuff.
    #         to (str): name of tool, where added
    #         **kwargs (Dict[str,Any]): dict of named args
    #     """
    #     if component in COMPONENTS.keys():
    #         self._add(COMPONENTS[component], name=name, **kwargs)
    #         self.logger.info(f'{name} is added to game.')
    #     else:
    #         raise ComponentClassError(component, self.logger)

    # def add_to(
    #     self,
    #     to: str,
    #     name: str,
    #     **kwargs
    #         ) -> None:
    #     """Add object to game

    #     Args:
    #         component (COMPONENTS_TYPES): type of added component.
    #         name (str): name of added component.
    #         **kwargs (Dict[str,Any]): dict of named args
    #     """
    #     if name in self.keys() and to in self.keys():
    #         self[to]._increase(name=name, game=self, **kwargs)
    #         self.logger.info(f'{name} is added to {to}.')
    #     else:
    #         raise ComponentClassError(name, self.logger)

    def new(
        self,
        name: str,
        ctype: COMPONENTS_TYPES,
        target: Optional[str] = None,
        **kwargs
            ) -> None:
        """Add new component to game object or any game-hosted object

        Args:
            name (str): name of new component (must be unic)
            ctype (COMPONENTS_TYPES): type of new component
            target (Optional[str], optional): name of class, where placed copy.
                                              Defaults to None.

        Raises:
            ComponentClassError: target or type of component not exist
        """
        if ctype in COMPONENTS.keys():
            if not target:
                self._add(COMPONENTS[ctype], name=name, **kwargs)
                self.logger.info(f'{name} is added to game.')
            elif target in self.keys():
                self[target]._add(COMPONENTS[ctype], name=name, **kwargs)
                self.logger.info(f'{name} is added to {target}.')
            else:
                raise ComponentClassError(target, self.logger)

        else:
            raise ComponentClassError(ctype, self.logger)

    def copy(
        self,
        source: str,
        target: str,
        **kwargs
            ) -> None:
        """Copy stuff from game object to any game-hosted tool or player

        Args:
            source (str): name of copied class
            target (str): name of class, where placed copy

        Raises:
            ComponentClassError: target or source not exist

        As result this operation we need two classes inside Game object:
        - target Component-like class
        - source Component-like class

        When method was called, is created new Component with all
        attributes of source class and it placed in target class
        """
        if source in self.keys() and target in self.keys():
            self[target]._increase(name=source, game=self, **kwargs)
            self.logger.info(f'{source} is added to {target}.')
        else:
            raise ComponentClassError((source, target), self.logger)



if __name__ == '__main__':
    log_enable()
    game = Game('one_board_game')
    game.new(
        'this_rule',
        ctype='rule',
        text="The text is short, but the rule is important"
        )
    game.new('one_card', ctype='card')
    game.new('cards_deck', ctype='deck')
    game.copy('one_card', 'cards_deck', count=3)
    game.copy('this_rule', 'game_rules')
    game.copy('this_rule', 'turn_order')
    game.cards_deck.deal()
    game.turn_order.deal()

    print(game)
    print('='*20)
    print(game.to_dict())
