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

# add dice and coin types to game
six = bgameb.Dice('six', sides=6)
twenty = bgameb.Dice('twenty', sides=20)
coin = bgameb.Dice('coin') # 2 is default number of sides

# add shaker and add count of stuff to shaker
game.add(bgameb.Shaker('red shaker'))
for stuff in [six, twenty, coin]:
    game.red_shaker.add(stuff)
    # change coont of dices in shaker
    game.red_shaker[stuff.id].count = 50

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
current_game_steps = game.game_steps.deal()

# game_steps is a priority queue, that linked with priority attribute
current_step = current_game_steps.pull()

# get the schema
schema = game.to_json()

# if you want, you can add his own attrs directly, but
# this attributes not added to the schema
game.red_chaker.IS_ACTIVE = True

# you can add any own data as declaration of object instance.
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

`make release` - to bump version, build changelog, commit, push tags and changes. You can use `towncrier build --draft` to check changelog output before release.

\* for version management are used [incremental](https://github.com/twisted/incremental) and [towncrier](https://pypi.org/project/towncrier/) for changelog
