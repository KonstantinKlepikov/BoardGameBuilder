# BoardGameBuilder

!!! Project now is in very early stage.

[![Release and upload to pypi](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml)
[![Deploy static content to Pages](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml)

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
from typing import Optional
from pydantic import Field
from bgameb import (
    Game,
    Components,
    Player,
    Steps,
    Step,
    Deck,
    Card,
    Shaker,
    Dice,
    log_enable
        )


if __name__ == '__main__':
    log_enable()

    # Defining a classes
    class MyPlayer(Player):
        deck: Deck

    # Creating of the game
    class MyGame(Game):
        steps: Steps
        shaker: Shaker
        me: MyPlayer
        opp: MyPlayer

    # The Player and Game are an obstract containeers for tools and stuff.
    # Deck, Bag, Shaker and Steps are tools. Dice, Card and Step are items.
    # Use Components to fill Game class
    C = Components[Dice | Card | Step]()

    G = MyGame(
        id="my game",
        steps=Steps(id="game steps"),
        shaker=Shaker(id="dice shaker"),
        me=MyPlayer(
            id='Me',
            deck=Deck(id="my cards deck")
                ),
        opp=MyPlayer(
            id='Opponent',
            deck=Deck(id="opponent cards deck")
                )
            )

    # The tool objects must be filled by items by method add().
    # That because we use some other methods for check
    # data types and makes some operations with items inside tool.

    # Adding game tuns order in Steps tool
    C.step0 = Step(id='step0')
    C.step1 = Step(id='step1', priority=1)

    # Starting of new turn
    current_steps = G.steps.deal(C)

    # Game steps is a priority queue, ordered by "priority" attribute
    last = G.steps.pops()

    # Adding of cards to deck. "count" parameter define how mutch
    # copies of card we must deal.
    C.update(
        Card(id='First', description='story', count=2)
            )
    C.update(Card(id='Second', count=1))

    # All items in tools are saved in spetial object Components.
    # Is a dict-like class. A component usied as base for other operations with items.
    # Any item is available in Component with dot or classic dict
    # notation. Names for that notation is transited from ids of items.
    card = C.first
    card = C['first']
    step = C.step0

    # You can get item by its id
    card = C.by_id('First')

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
            fields = {'is_revealed': 'is_open'}

        @property
        def my_calculated_field(self) -> str:
            return self.some_text.upper()

    C.update(
        MyCard(id='Thierd', description='story', count=3)
            )

    # Use default counters of any objects - counters not added to schema
    G.me.deck._counter['yellow'] = 12
    G.me.deck._counter['banana'] = 0

    # Dealing and shuffling of deck
    G.me.deck.deal(C).shuffle()

    # Adding dices to shaker
    C.update(
        Dice(id='dice#8', sides=8, count=10)
            )
    G.shaker.deal(C)

    # You can use items from Components
    result = C.dice_8.roll()

    # Or use from tool
    result = G.shaker.roll()
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
