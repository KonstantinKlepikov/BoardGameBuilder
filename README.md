# BoardGameBuilder

!!! Project now is in very early stage. Dont use it in any apps :)

[![Release and upload to pypi](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml)
[![Deploy static content to Pages](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml)

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
from typing import Optional
from dataclasses import dataclass
from bgameb import (
    Game, Player, Steps, Step, Deck, Card, Shaker, Dice,
    Bag, log_enable
        )


if __name__ == '__main__':
    log_enable()

    # create the game
    G = Game('one board game')

    # add player
    G.add(Player('Player'))

    # The stuff objects are saved in attribute c.
    # Names are converted to snake case
    player = G.c.player

    # add game tuns order
    G.add(Steps('Steps'))
    G.c.steps.add(Step('step0'))
    G.c.steps.add(Step('step1', priority=1))

    # start new turn
    current_steps = G.c.steps.deal()

    # Game_steps is a priority queue, linked with priority attribute
    last = G.c.steps.pop()

    # add deck object and cards
    G.add(Deck('Deck'))
    G.c.deck.add(
        Card('First', description='story', count=3)
            )
    G.c.deck.add(Card('Second', count=1))

    # Specific arguments is stored to dict attribute `other`
    description = G.c.deck.c.first.other['description']

    # If you need more clear schema, inherite from any class.
    # Additional, we can define _to_relocate mapping -this
    # help move values from some attrs to another or convert some
    # values to related with Game outsade-hosted schema
    @dataclass
    class MyCard(Card):
        description: Optional[str] = None
        some_text: Optional[str] = 'some texts'
        is_open: Optional[bool] = None

        def __post_init__(self) -> None:
            super().__post_init__()
            self._to_relocate = {
                'is_open': 'opened'
                    }

    G.c.deck.add(
        MyCard('Thierd', description='story', count=12)
            )

    # Use default counters of cards
    G.c.deck.c.first.counter['yellow'] = 12
    G.c.deck.c.second.counter['banana'] = 0

    # relocate values
    G.c.deck.c.thierd.relocate()

    # Deal and shuffle deck
    G.c.deck.deal().shuffle()

    # You can add additional attributes directly, but
    # this attributes can not added to the schema
    G.IS_ACTIVE = True

    # Add shaker and dices
    G.add(Shaker('blue shaker'))
    G.c.blue_shaker.add(
        Dice('dice#8', info='some important', sides=8, count=10)
            )

    # and roll dices
    result = G.c.blue_shaker.c.dice_8.roll()

    # Use bag as collection of any items
    G.add(Bag('Bag'))
    G.c.bag.add(Dice('dice'))
    G.c.bag.add(Card('card'))

    # components and technical attrs not added to shcema.
    # You can reconstruct full schema fit build_json() method
    schema = G.relocate_all().to_json()
```

## Documentation

- [docs](https://konstantinklepikov.github.io/BoardGameBuilder/)
- [pypi](https://pypi.org/project/bgameb/)

## Development

[how install project for development](https://konstantinklepikov.github.io/BoardGameBuilder/usage.html).

Typicaly: `pip install -e .[dev]`

### Available cli

`make proj-doc`

`make test`

to check simple scenario use `python tests/check.py`

`make test-pypi` to test deploy to testpypi

`make log` - insert fragmet name to store new about project

`make ipython` run interactive terminal

`make check` check flake8 and mypy

Available fragmet naming:

- .feature: Signifying a new feature.
- .bugfix: Signifying a bug fix.
- .doc: Signifying a documentation improvement.
- .removal: Signifying a deprecation or removal of public API.
- .misc: A ticket has been closed, but it is not of interest to users.

`make draft` - to check changelog output before release.

`make release` - to bump version, build changelog, commit, push tags and changes.

\* for version management are used [incremental](https://github.com/twisted/incremental) and [towncrier](https://pypi.org/project/towncrier/) for changelog
\* project based on [dataclasses-json](https://github.com/lidatong/dataclasses-json)
