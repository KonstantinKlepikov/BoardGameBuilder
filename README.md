# BoardGameBuilder

!!! Project now is in very early stage. Dont use it in any apps :)

[![Release and upload to pypi](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml)
[![Deploy static content to Pages](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml)

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
import bgameb

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
```

## Documentation

- [docs](https://konstantinklepikov.github.io/BoardGameBuilder/)
- [pypi](https://pypi.org/project/bgameb/)

## Development

[how install project for development](https://konstantinklepikov.github.io/BoardGameBuilder/usage.html).

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
