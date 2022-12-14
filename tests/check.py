from pprint import pprint
from typing import Optional
from dataclasses import dataclass
import bgameb


if __name__ == '__main__':
    bgameb.log_enable()

    # create the game
    G = bgameb.Game('one board game')

    # add player
    G.add(bgameb.Player('Player'))

    # The players object is in attribute p, items -> i, tools -> t.
    # Names are converted to snake case
    player = G.p.player

    # add game tuns order
    G.add(bgameb.Steps('Steps'))
    G.t.steps.add(bgameb.Step('step0'))
    G.t.steps.add(bgameb.Step('step1', priority=1))

    # start new turn
    current_steps = G.t.steps.deal()

    # Game_steps is a priority queue, linked with priority attribute
    last = G.t.steps.pull()

    # add deck object and cards
    G.add(bgameb.Deck('Deck'))
    G.t.deck.add(
        bgameb.Card('First', description='story', count=3)
            )
    G.t.deck.add(bgameb.Card('Second', count=1))

    # Specific arguments is stored to dict attribute `other`
    description = G.t.deck.i.first.other['description']

    # If you need more clear schema, inherite from any class
    @dataclass(repr=False)
    class MyCard(bgameb.Card):
        description: Optional[str] = None

        def __post_init__(self) -> None:
            super().__post_init__()

    G.t.deck.add(
        MyCard('Thierd', description='story', count=12)
            )

    # Use default counters of cards
    G.t.deck.i.first.counter['yellow'] = 12
    G.t.deck.i.second.counter['banana'] = 0

    # Deal and shuffle deck
    G.t.deck.deal().shuffle()

    # You can add additional attributes directly, but
    # this attributes can not added to the schema
    G.IS_ACTIVE = True

    # Add shaker and dices
    G.add(bgameb.Shaker('blue shaker'))
    G.t.blue_shaker.add(
        bgameb.Dice('dice#8', info='some important', sides=8, count=10)
            )

    # and roll dices
    result = G.t.blue_shaker.i.dice_8.roll()

    # Use bag as collection of any items
    G.add(bgameb.Bag('Bag'))
    G.t.bag.add(bgameb.Dice('dice'))
    G.t.bag.add(bgameb.Card('card'))

    # get the schema
    schema = G.to_json()

    print('='*20 + '\n')
    print(f'Repr: {G}')
    print('='*20 + '\n')
    pprint(G.to_dict())
    print('='*20 + '\n')
    print(f'Result of shake: {result}')
    print('='*20 + '\n')
    print(f'Dir: {dir(G)}')
