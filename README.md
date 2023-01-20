# BoardGameBuilder

!!! Project now is in very early stage. Dont use it in any apps :)

[![Release and upload to pypi](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml)
[![Deploy static content to Pages](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml)

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
from typing import Optional
from pydantic import Field
from bgameb import (
    Game, Player, Steps, Step_, Deck, Card, Shaker, Dice,
    Bag, log_enable
        )


if __name__ == '__main__':
    log_enable()

    # Creating of the game
    class MyGame(Game):
        steps: Steps
        deck: Deck
        shaker: Shaker
        bag: Bag
        players: list[Player] = []

    # The Player and Game are an obstract containeers for tools and stuff.
    # Deck, Bag, Shaker and Steps are tools. Dice, Card and Step are items.

    G = MyGame(
        id='one board game',
        steps=Steps(id='steps'),
        deck=Deck(id='deck'),
        shaker=Shaker(id='shaker'),
        bag=Bag(id='bag'),
        players=[Player(id='player1'), Player(id='player2')]
            )

    # The tool objects must be filled by items by method add().
    # That because we use some other methods for check
    # data types and makes some operations with items inside tool.

    # Adding game tuns order in Steps tool
    G.steps.add(Step_(id='step0'))
    G.steps.add(Step_(id='step1', priority=1))

    # Starting of new turn
    current_steps = G.steps.deal()

    # Game steps is a priority queue, ordered by "priority" attribute
    last = G.steps.pop()

    # Adding of cards to deck. "count" parameter define how mutch
    # copies of card we must deal.
    G.deck.add(
        Card(id='First', description='story', count=2)
            )
    G.deck.add(Card(id='Second', count=1))

    # All items in tools are saved in spetial object Component.
    # Is a dict-like class. Component is predefined as attribute "c".
    # A component usied as base for other operations with items.
    cards_component = G.deck.c

    # Any item is available in Component with dot or classic dict
    # notation. Names for that notation is transited from ids of items.
    card = G.deck.c.first
    card = G.deck.c['first']

    # You can get item by its id
    card = G.deck.c.by_id('First')

    # If you relocate some bult-in attrs, inherite from stuff classes,
    # then define aliases for attributes. In this example we use two
    # different solution: Field aliase and config.
    # Dont forget use G.dict(by_alias=True) to get aliases.
    # More infoshere:
    # https://docs.pydantic.dev/usage/model_config/#alias-generator
    # Finaly, if you need use callbacs to export data from some
    # function as field values - define properties.
    class MyCard(Card):
        description: Optional[str] = Field(None, alias='some_bla_bla')
        some_text: Optional[str] = 'some texts'

        class Config(Card.Config):
            fields = {'opened': 'is_open'}

        @property
        def my_calculated_field(self) -> str:
            return self.some_text.upper()

    G.deck.add(
        MyCard(id='Thierd', description='story', count=3)
            )

    # Use default counters of any objects - counters not added to schema
    G.deck.c.first.counter['yellow'] = 12
    G.deck.c.second.counter['banana'] = 0

    # Dealing and shuffling of deck
    G.deck.deal().shuffle()

    # Adding dices to shaker
    G.shaker.add(
        Dice(id='dice#8', sides=8, count=10)
            )

    # Roll dices
    result = G.shaker.c.dice_8.roll()

    # Use bag as collection of any items
    G.bag.add(Dice(id='dice'))
    G.bag.add(Card(id='card'))
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
\* project based on [pydantic](https://github.com/pydantic/pydantic)
