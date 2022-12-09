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
game = bgameb.Game('one board game')

# add shaker to game
game.add(bgameb.Shaker('red shaker'))

# add dices and coin to shaker
game.red_shaker.add(bgameb.Dice('six', sides=6, count=50))
game.red_shaker.add(bgameb.Dice('twenty', sides=20, count=50))
game.red_shaker.add(bgameb.Dice('coin', count=10))

# roll all stuff and get result
result = game.red_shaker.roll()

# you can use dict notation offcourse, but remember -
# the name of attr is converted from id to snake case
result = game['red_shaker']['coin'].roll()

# delete components from any collections
del game.red_shaker.six
del game.red_shaker

# define a cards and decks
game.add(bgameb.Deck('cards deck'))
game.cards_deck.add(bgameb.Card('one card', count=100))

# deal card from deck. current deck is a python deque
game.cards_deck.deal()
current = game.cards_deck.shuffle()

# lets create game turn structure and start turn
game.add(bgameb.Steps('game steps'))
game.game_steps.add(bgameb.Step('phase one', priority=0))
game.game_steps.add(bgameb.Step('phase two', priority=1))
current = game.game_steps.deal()

# game_steps is a priority queue, linked with priority attribute
current_step = game.game_steps.pull()

# last pulled step is available as current_step to
current_step = game.game_steps.current_step

# get the schema
schema = game.to_json()

# if you want, you can add additional attrs directly, but
# this attributes not added to the schema
game.red_chaker.IS_ACTIVE = True

# you can add any data as declaration of object instance.
# This data is store in other attribute, it is a dict and is in schema
dice = bgameb.Dice('six', sides=6, description='my important data')
deacription = dice.other['deacription']
```

## Documentation

- [docs](https://konstantinklepikov.github.io/BoardGameBuilder/)
- [pypi](https://pypi.org/project/bgameb/)

## Development

[how install project for development](https://konstantinklepikov.github.io/BoardGameBuilder/usage.html).

### Available cli

`make proj-doc`

`make test`

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
