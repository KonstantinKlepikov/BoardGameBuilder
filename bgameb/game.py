"""Main engine to create game
"""
from typing import Optional
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from bgameb.base import Base, log_enable
from bgameb.types import (
    COMPONENTS, COMPONENTS_TYPES, MARKERS_MORE,
    ITEMS_MORE, TOOLS_MORE, MARKERS, ITEMS, TOOLS,
    PLAYERS
    )
from bgameb.tools import Steps
from bgameb.errors import ComponentClassError


@dataclass_json
@dataclass(repr=False)
class Game(Base):
    """The main game object

    Args:
        game_steps (Steps): game turn steps order
    """
    game_steps: Steps = field(init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.game_steps = Steps('game_steps')

    def new(
        self,
        name: str,
        type_: COMPONENTS_TYPES,
        target: Optional[str] = None,
        **kwargs
            ) -> None:
        """Add new component to game or any subcomponent in game

        Args:
            name (str): name of new component (must be unic)
            type_ (COMPONENTS_TYPES): type of new component
            target (str, optional): name of class, where placed component.
                                    Defaults to None.

        Raises:
            ComponentClassError: target or type of component not exist
        """
        if target:
            try:
                target_type = self[target].__class__.__name__.lower()
            except KeyError:
                raise ComponentClassError((target), self._logger)

        if type_ in COMPONENTS.keys():

            if not target:
                self._add(COMPONENTS[type_], name=name, **kwargs)
                self._logger.info(f'{name} is added to game.')

            elif (type_ in MARKERS.keys() and target_type in MARKERS_MORE) \
                    or (type_ in ITEMS.keys() and target_type in ITEMS_MORE) \
                    or (type_ in TOOLS.keys() and target_type in TOOLS_MORE) \
                    or (type_ in PLAYERS.keys()
                        and target_type not in COMPONENTS):
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
        """Copy component from game object to any game-hosted component

        Args:
            source (str): name of copied stuff
            target (str): name of stuff, where placed copy

        Raises:
            ComponentClassError: target or source not exist

        As result this operation we need two classes inside Game object:
        - target component
        - source component

        All this classes must be a Components instances.

        When method was execute, it create new component with all
        attributes of source stuff and place it in target component.

        You can make copy in order: markers -> items -> tools -> players

        For example markers can be copied to tools,
        but players can't be copied.
        """
        try:
            source_type = self[source].__class__.__name__.lower()
            target_type = self[target].__class__.__name__.lower()
        except KeyError:
            raise ComponentClassError((source, target), self._logger)

        if source in self.keys() and target in self.keys() \
                and (
                    (source_type in MARKERS.keys()
                        and target_type in MARKERS_MORE)
                    or (source_type in ITEMS.keys()
                        and target_type in ITEMS_MORE)
                    or (source_type in TOOLS.keys()
                        and target_type in TOOLS_MORE)
                    ):

            to_copy: dict = self[source].to_dict()
            to_copy.update(kwargs)
            to_copy = self[source].__class__(**to_copy)
            self[target]._update(to_copy)
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
    game.new('yellow', type_='counter', target='one_card')
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
