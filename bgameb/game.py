"""Main engine to create games
"""
from typing import Optional
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from bgameb.base import Base, log_enable
from bgameb.types import COMPONENTS, NONSTUFF, COMPONENTS_TYPES, STUFF
from bgameb.tools import Steps
from bgameb.errors import ComponentClassError


@dataclass_json
@dataclass(repr=False)
class BaseGame(Base):
    """Base class for game

    Args:
        game_steps (Steps): game turn steps order
    """
    game_steps: Steps = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.game_steps = Steps('game_steps')


@dataclass_json
@dataclass(repr=False)
class Game(BaseGame):
    """The main game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()

    def new(
        self,
        name: str,
        type_: COMPONENTS_TYPES,
        target: Optional[str] = None,
        **kwargs
            ) -> None:
        """Add new component to game or any stuff to game-hosted tool or player

        Args:
            name (str): name of new component (must be unic)
            type_ (COMPONENTS_TYPES): type of new component
            target (str, optional): name of class, where placed component.
                                    Defaults to None.

        Raises:
            ComponentClassError: target or type of component not exist
        """
        if type_ in COMPONENTS.keys():
            if not target:
                self._add(COMPONENTS[type_], name=name, **kwargs)
                self._logger.info(f'{name} is added to game.')
            elif target in self.keys() \
                    and self[target]._type in NONSTUFF.keys() \
                    and type_ in STUFF.keys():
                self[target]._add(COMPONENTS[type_], name=name, **kwargs)
                self._logger.info(f'{name} is added to {target}.')
            else:
                raise ComponentClassError(target, self._logger)

        else:
            raise ComponentClassError(type_, self._logger)

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
        - target tool component
        - source stuff component

        All this classes must be a Components instances.

        When method was execute, it create new stuff component with all
        attributes of source stuff and place it in target tool component
        """
        if source in self.keys() \
                and self[source]._type in STUFF.keys() \
                and target in self.keys() \
                and self[target]._type in NONSTUFF.keys():
            self[target].update(name=source, game=self, **kwargs)
            self._logger.info(f'{source} is added to {target}.')
        else:
            raise ComponentClassError((source, target), self._logger)


if __name__ == '__main__':
    from pprint import pprint
    log_enable()
    game = Game('one_board_game')
    game.new(
        'step0',
        type_='step',
        target='game_steps'
            )
    game.new(
        'step1',
        type_='step',
        target='game_steps',
        priority=1
            )
    game.new('one_card', type_='card')
    game.new('cards_deck', type_='deck')
    game.copy('one_card', 'cards_deck', count=3)
    game.game_steps.deal()
    game.cards_deck.deal()
    game.is_active = True  # type: ignore
    game.new('blue_shaker', type_='shaker')
    game.new('eight', type_='dice', target='blue_shaker', sides=8, count=10)
    result = game.blue_shaker.eight.roll()

    print(repr(game))
    print('='*20 + '\n')
    print(game)
    print('='*20 + '\n')
    pprint(game.to_dict())
    print('='*20 + '\n')
    print(dir(game))
