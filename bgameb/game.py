"""Main engine to create games
"""
from typing import Optional
from dataclasses import dataclass, field
from bgameb.base import Base, log_enable
from bgameb.types import COMPONENTS, component_type
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
    #     component: component_type,
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

    def add_to(
        self,
        to: str,
        name: str,
        **kwargs
            ) -> None:
        """Add object to game

        Args:
            component (component_type): type of added component.
            name (str): name of added component.
            **kwargs (Dict[str,Any]): dict of named args
        """
        if name in self.keys() and to in self.keys():
            self[to]._increase(name=name, game=self, **kwargs)
            self.logger.info(f'{name} is added to {to}.')
        else:
            raise ComponentClassError(name, self.logger)

    def new(
        self,
        name: str,
        ctype: component_type,
        target: Optional[str] = None,
        **kwargs
            ) -> None:
        """Add new component to game object or any game-hosted object

        Args:
            name (str): name of new component (must be unic)
            ctype (component_type): type of new component
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
        """Copy component from game object to any game-hosted object

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
    game.add_to('cards_deck', 'one_card', count=3)
    game.add_to('game_rules', 'this_rule')
    game.add_to('turn_order', 'this_rule')
    game.cards_deck.deal()
    game.turn_order.deal()

    print(game)
    print('='*20)
    print(game.to_dict())
