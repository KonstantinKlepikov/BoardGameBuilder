# BoardGameBuilder

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
# create the game
game = Game('one_board_game')

# add dice and coin types to game
game.add('roller', name='six_dice', sides=6)
game.add('roller', name='twenty_dice', sides=20)
game.add('roller', name='coin') # 2 is defoult number of sides

# or define sides for dice and coin types
game.stuff.coin.sides = 3

# add shaker and add count of stuff to shaker
game.add('shaker', name='red_shaker')
game.tools.red_shaker.add('six_dice', game=game, count=50)
game.tools.red_shaker.add('twenty_dice', game=game, count=10)
game.tools.red_shaker.add('coin', game=game, count=42)

# roll all stuff and get result
result = game.tools.red_shaker.roll()

# or define new shaker with default count == 1 and roll each stuff separatly
game.add('shaker', name='blue_shaker')
game.tools.blue_shaker.add('six_dice', game=game)
game.tools.blue_shaker.add('coin', game=game)

result = game.tools.blue_shaker.stuff.six_dice.roll()
result = game.tools.blue_shaker.stuff.coin.roll()

# you can use dict notation offcourse
result = game['tools']['blue_shaker']['stuff']['coin'].roll()

# you can use another game object to construct tools
game_2 = Game('another_board_game')
game_2.add('roller', name='four_dice', sides=4)
game.tools.red_shaker.add('four_dice', game=game_2, count=22)
result = game.tools.red_shaker.roll()

# delete components from any collections
del game.tools.blue_shaker
del game.stuff.six_dice

# define a cards and decks
game.add('card', name='one_card')
game.add('deck', name='cards_deck')
game.tools.cards_deck.add('one_card', game=game, count=100)

# deal card from deck
game.tools.cards_deck.deal()

# dealt crds is a python deque
deck = game.tools.cards_deck.dealt
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
