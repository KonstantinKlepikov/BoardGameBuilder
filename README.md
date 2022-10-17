# BoardGameBuilder

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
from bgameb import Game

# create the game
game = Game('one_board_game')

# add dice and coin types to game
game.new('six', ctype='dice', sides=6)
game.new('twenty', ctype='dice', sides=20)
game.new('coin', ctype='dice') # 2 is default number of sides

# or define sides for dice and coin types
game.coin.sides = 3

# add shaker and add count of stuff to shaker
game.new('red_shaker', ctype='shaker')
game.add_to('red_shaker', 'six', count=50)
game.add_to('red_shaker', 'twenty', count=10)
game.add_to('red_shaker', 'coin', count=42)

# roll all stuff and get result
result = game.red_shaker.roll()

# or define new shaker with default count == 1 and roll each stuff separatly
game.add('blue_shaker', ctype='shaker')
game.add_to('blue_shaker', 'six')
game.add_to('blue_shaker', 'coin')

result = game.blue_shaker.six_dice.roll()
result = game.blue_shaker.coin.roll()

# get last roll (this store only full shaker roll)
last_roll = game.blue_shaker.last

# you can use dict notation offcourse
result = game['blue_shaker']['coin'].roll()

# delete components from any collections
del game.blue_shaker
del game.six

# define a cards and decks
game.new('one_card', ctype='card')
game.new('cards_deck', ctype='deck')
game.add_to('cards_deck', 'one_card', count=100)

# deal card from deck
game.cards_deck.deal()

# dealt cards is a python deque
deck = game.cards_deck.dealt

# all rule is store in Game class
game.new('phase_one', ctype='rule', text='Important text')
game.new('phase_two', ctype='rule', text='Another important text')

# rule is a dict-like object
game.phase_one.additional = 'Add something else'

# lets create game turn structure
game.add_to('turn_order', 'phase_one')
game.add_to('turn_order', 'phase_two')
game.turn_order.deal()
current_turn = game.turn_order.dealt
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
- .cicd: Integration tasks

`make release` - to bump version and build changelog. You can use `towncrier build --draft` to check changelog output

\* for version management are used [incremental](https://github.com/twisted/incremental) and [towncrier](https://pypi.org/project/towncrier/) for changelog
