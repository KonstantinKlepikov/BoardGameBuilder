# BoardGameBuilder

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
from bgameb import Game

# create the game
game = Game('one_board_game')

# add dice and coin types to game
game.add('roller', name='six_dice', sides=6)
game.add('roller', name='twenty_dice', sides=20)
game.add('roller', name='coin') # 2 is default number of sides

# or define sides for dice and coin types
game.coin.sides = 3

# add shaker and add count of stuff to shaker
game.add('shaker', name='red_shaker')
game.add_to('red_shaker', 'six_dice', count=50)
game.add_to('red_shaker', 'twenty_dice', count=10)
game.add_to('red_shaker', 'coin', count=42)

# roll all stuff and get result
result = game.red_shaker.roll()

# or define new shaker with default count == 1 and roll each stuff separatly
game.add('shaker', name='blue_shaker')
game.add_to('blue_shaker', 'six_dice')
game.add_to('blue_shaker', 'coin')

result = game.blue_shaker.six_dice.roll()
result = game.blue_shaker.coin.roll()

# get last roll (this store only full shaker roll)
last_roll = game.blue_shaker.last

# you can use dict notation offcourse
result = game['blue_shaker']['coin'].roll()

# delete components from any collections
del game.blue_shaker
del game.six_dice

# define a cards and decks
game.add('card', name='one_card')
game.add('deck', name='cards_deck')
game.add_to('cards_deck', 'one_card', count=100)

# deal card from deck
game.cards_deck.deal()

# dealt crds is a python deque
deck = game.cards_deck.dealt

# all rule is store in Game class
game.add_rule(name='this_rule', text='Important text')

# rule is a dict-like object
game.rules.this_rule.additional = 'Add something else'

# Any stuff or players objects in game have rules list to link to rules
game.one_card.rules.append(game.rules.this_rule.name)
for rule in game.one_card.rules:
    print(game.rules[rule].text)
```

## Documentation

- [docs](https://konstantinklepikov.github.io/BoardGameBuilder/)
- [pypi](https://pypi.org/project/bgameb/)

## Development

[how install project for development](https://konstantinklepikov.github.io/BoardGameBuilder/usage.html). Use IPython for dev mode `python -m IPython`.

### Available cli

`make proj-doc`

`make test`

`make test-pypi` to test deploy to testpypi

`make log` - insert fragmet name to store new about project

Available fragmet naming:

- .feature: Signifying a new feature.
- .bugfix: Signifying a bug fix.
- .doc: Signifying a documentation improvement.
- .removal: Signifying a deprecation or removal of public API.
- .misc: A ticket has been closed, but it is not of interest to users.
- .cicd: Integration tasks

`make release` - to bump version and build changelog. You can use `towncrier build --draft` to check changelog output

\* for version management are used [incremental](https://github.com/twisted/incremental) and [towncrier](https://pypi.org/project/towncrier/) for changelog
