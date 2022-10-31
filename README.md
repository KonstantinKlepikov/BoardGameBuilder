# BoardGameBuilder

[![Release and upload to pypi](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/release.yml)
[![Deploy static content to Pages](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml/badge.svg)](https://github.com/KonstantinKlepikov/BoardGameBuilder/actions/workflows/build-docs.yml)

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
from bgameb import Game

# create the game
game = Game('one_board_game')

# add dice and coin types to game
game.new('six', type_='dice', sides=6)
game.new('twenty', type_='dice', sides=20)
game.new('coin', type_='dice') # 2 is default number of sides

# or define sides for dice and coin types
game.coin.sides = 3

# add shaker and add count of stuff to shaker
game.new('red_shaker', type_='shaker')
game.copy('six', 'red_shaker', count=50)
game.copy('twenty', 'red_shaker', count=10)
game.copy('coin', 'red_shaker', count=42)

# roll all stuff and get result
result = game.red_shaker.roll()

# or define new shaker and add stuff directly
game.new('blue_shaker', type_='shaker')
game.new('eight', type_='dice', target='blue_shaker', sides=8, count=10)
result = game.blue_shaker.eight.roll()

# you can use dict notation offcourse
result = game['blue_shaker']['coin'].roll()

# delete components from any collections
del game.blue_shaker
del game.six

# define a cards and decks
game.new('one_card', type_='card')
game.new('cards_deck', type_='deck')
game.copy('one_card', 'cards_deck', count=100)

# deal card from deck
game.cards_deck.deal()

# current deck is a python deque
deck = game.cards_deck.current

# lets create game turn structure
game.new('phase_one', 'game_steps', priority=0)
game.copy('phase_two', 'game_steps', priority=1)
game.game_steps.deal()

# game_steps is a priority queue, that linked to priority attribute
current_game_steps = game.game_steps.current
current_step = current_game_steps.get()
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

`make release` - to bump version and build changelog. You can use `towncrier build --draft` to check changelog output

\* for version management are used [incremental](https://github.com/twisted/incremental) and [towncrier](https://pypi.org/project/towncrier/) for changelog
