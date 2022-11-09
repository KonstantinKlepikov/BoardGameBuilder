"""Main engine to create game
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from bgameb.base import Base, log_enable
from bgameb.types import COMPONENTS


@dataclass_json
@dataclass(repr=False)
class Game(Base):
    """The main game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        self._types_to_add = COMPONENTS


if __name__ == '__main__':
    import bgameb
    from pprint import pprint
    log_enable()
    game = bgameb.Game('one_board_game')
    game.add(bgameb.Steps('game_steps'))
    game.game_steps.add(bgameb.Step('step0'))
    game.game_steps.add(bgameb.Step('step1', priority=1))

    game.add(bgameb.Deck('cards_deck'))
    card = bgameb.Card('one_card')
    card.add(bgameb.Counter('yellow'))

    game.cards_deck.add(card)
    game.cards_deck.one_card.count = 3

    game.game_steps.deal()
    game.cards_deck.deal()

    game.is_active = True  # type: ignore

    game.add(bgameb.Shaker('blue_shaker'))
    game.blue_shaker.add(bgameb.Dice('eight', sides=8, count=10))

    result = game.blue_shaker.eight.roll()

    print(result)
    print('='*20 + '\n')
    print(repr(game))
    print('='*20 + '\n')
    print(game)
    print('='*20 + '\n')
    pprint(game.to_dict())
    print('='*20 + '\n')
    print(dir(game))
