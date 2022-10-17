"""Main engine to create games
"""
from typing import Optional
from dataclasses import dataclass, field
from dataclasses_json import config
from bgameb.base import Base, log_enable
from bgameb.types import COMPONENTS, NONSTUFF, COMPONENTS_TYPES, STUFF
from bgameb.tools import Rules, Turns
from bgameb.errors import ComponentClassError


@dataclass
class BaseGame(Base):
    """Base class for game
    """
    game_rules: Rules = field(init=False)
    turn_order: Turns = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.game_rules = Rules('game_rules')
        self.turn_order = Turns('turn_order')


@dataclass
class Game(BaseGame):
    """Create the game object
    """
    type_: str = field(
        default='game',
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def new(
        self,
        name: str,
        ctype: COMPONENTS_TYPES,
        target: Optional[str] = None,
        **kwargs
            ) -> None:
        """Add new component to game or any stuff to game-hosted tool or player

        Args:
            name (str): name of new component (must be unic)
            ctype (COMPONENTS_TYPES): type of new component
            target (str, optional): name of class, where placed component.
                                              Defaults to None.

        Raises:
            ComponentClassError: target or type of component not exist
        """
        if ctype in COMPONENTS.keys():
            if not target:
                self._add(COMPONENTS[ctype], name=name, **kwargs)
                self.logger.info(f'{name} is added to game.')
            elif target in self.keys() \
                    and self[target].type_ in NONSTUFF.keys() \
                    and ctype in STUFF.keys():
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
            source (str): name of copied stuff
            target (str): name of tool or player, where placed copy

        Raises:
            ComponentClassError: target or source not exist

        As result this operation we need two classes inside Game object:
        - target Component-like stuff
        - source Component-like tool

        When method was called, is created new Component with all
        attributes of source class and it placed in target class
        """
        if source in self.keys() \
                and self[source].type_ in STUFF.keys() \
                and target in self.keys() \
                and self[target].type_ in NONSTUFF.keys():
            self[target].update(name=source, game=self, **kwargs)
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
    game.new('blue_shaker', ctype='shaker')
    game.new('eight', ctype='dice', target='blue_shaker', sides=8, count=10)
    result = game.blue_shaker.eight.roll()

    print(game)
    print('='*20)
    print(game.to_dict())
