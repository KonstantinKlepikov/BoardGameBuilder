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

    def add(
        self,
        component: component_type,
        name: str,
        **kwargs
            ) -> None:
        """Add stuff to game tool

        Args:
            name (str): name of added stuff.
            to (str): name of tool, where added
            **kwargs (Dict[str,Any]): dict of named args
        """
        if component in COMPONENTS.keys():
            self._add(COMPONENTS[component], name=name, **kwargs)
            self.logger.info(f'{name} is added to game.')
        else:
            raise ComponentClassError(component, self.logger)

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
        obj_type: component_type,
        to_obj: Optional[str] = None,
        **kwargs
            ) -> None:
        if obj_type in COMPONENTS.keys():
            if not to_obj:
                self._add(COMPONENTS[obj_type], name=name, **kwargs)
                self.logger.info(f'{name} is added to game.')
            else:
                self['to_obj']._add(COMPONENTS[obj_type], name=name, **kwargs)
                self.logger.info(f'{name} is added to {to_obj}.')

        else:
            raise ComponentClassError(obj_type, self.logger)

    def copy(
        self,
        copied: str,
        to_obj: str,
        **kwargs
            ) -> None:
        if copied in self.keys() and to_obj in self.keys():
            self[to_obj]._increase(name=copied, game=self, **kwargs)
            self.logger.info(f'{copied} is added to {to_obj}.')
        else:
            raise ComponentClassError((copied, to_obj), self.logger)



if __name__ == '__main__':
    log_enable()
    game = Game('one_board_game')
    game.add(
        'rule',
        name='this_rule',
        text="The text is short, but the rule is important"
        )
    game.add('card', name='one_card')
    game.add('deck', name='cards_deck')
    game.add_to('cards_deck', 'one_card', count=3)
    game.add_to('game_rules', 'this_rule')
    game.add_to('turn_order', 'this_rule')
    game.cards_deck.deal()
    game.turn_order.deal()

    print(game)
    print('='*20)
    print(game.to_dict())
