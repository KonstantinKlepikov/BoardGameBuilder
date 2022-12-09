"""Main engine to create game
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from bgameb.base import Base, log_enable
from bgameb.constraints import COMPONENTS


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

    game = bgameb.Game('one board game')
    game.add(bgameb.Steps('Game Steps'))
    game.game_steps.add(bgameb.Step('step 0'))
    game.game_steps.add(bgameb.Step('step 1', priority=1))

    game.add(bgameb.Deck('Cards Deck'))
    card = bgameb.Card('One card', description='story')  # type: ignore
    game.cards_deck.add(card)
    game.cards_deck.one_card.count = 3

    print(f'Other: {game.cards_deck.one_card.other}')
    game.cards_deck.one_card.counter['yellow'] = 12
    game.cards_deck.one_card.counter['banana'] = 0

    steps = game.game_steps.deal()
    game.cards_deck.deal()
    deck = game.cards_deck.shuffle()

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
    print(f'Current deck ids: {game.cards_deck.get_current_ids()}')
    print('='*20 + '\n')
    print(f'Names in game: {game.get_names()}')
    print('='*20 + '\n')
    print(
        'Get by id "Game Steps" in game: '
        f'{game.get_component_by_id("Game Steps")}'
            )
    print('='*20 + '\n')
    print(f'Dir: {dir(game)}')
