"""Main engine to create game
"""
from typing import Union, Type
from dataclasses import dataclass
from dataclasses_json import dataclass_json
import bgameb
from bgameb.base import Base, log_enable
from bgameb.constraints import COMPONENTS


TypeComp = Type[Union[
    'bgameb.Card', 'bgameb.Dice', 'bgameb.Step',
    'bgameb.Player', 'bgameb.Game', 'bgameb.Steps',
    'bgameb.Bag', 'bgameb.Shaker', 'bgameb.Deck',
    'bgameb.Steps',
        ]]


@dataclass_json
@dataclass(repr=False)
class Game(Base):
    """The main game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        self._types_to_add = COMPONENTS


    def __getattr__(self, attr: str) -> TypeComp:
        try:
            return self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)


if __name__ == '__main__':
    import bgameb
    from pprint import pprint
    log_enable()

    game = bgameb.Game('one board game')
    game.add(bgameb.Steps('Steps'))
    game.steps.add(bgameb.Step('step 0'))
    game.steps.add(bgameb.Step('step 1', priority=1))
    game.steps.deal()
    game.add(bgameb.Deck('Deck'))
    game.deck.add(
        bgameb.Card('First', description='story', count=3)  # type: ignore
            )
    game.deck.add(bgameb.Card('Second', count=1))

    print(f'Other: {game.deck.first.other}')
    game.deck.first.counter['yellow'] = 12
    game.deck.second.counter['banana'] = 0

    steps = game.steps.deal()
    game.deck.deal().shuffle()
    deck = game.deck.current

    game.IS_ACTIVE = True  # type: ignore

    game.add(bgameb.Shaker('blue shaker'))
    game.blue_shaker.add(
        bgameb.Dice('dice#8', sides=8, count=10)
            )

    result = game.blue_shaker.dice_8.roll()

    print(f'Result of shake: {result}')
    print('='*20 + '\n')
    print(f'Repr: {repr(game)}')
    print('='*20 + '\n')
    print(f'Print: {game}')
    print('='*20 + '\n')
    pprint(game.to_dict())
    print('='*20 + '\n')
    pprint(deck)
    print('='*20 + '\n')
    print(f'Current deck ids: {game.deck.current_ids()}')
    print('='*20 + '\n')
    print(f'Names in game: {game.get_names()}')
    print('='*20 + '\n')
    print(
        'Get by id "Game Steps" in game: '
        f'{game.by_id("Game Steps")}'
            )
    print('='*20 + '\n')
    print(f'Dir: {dir(game)}')
