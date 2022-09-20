# BoardGameBuilder

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
# create the game
game = Game('one_board_game')

# add dice and coin types to game
game.add('roller', name='six_dice')
game.add('roller', name='twenty_dice')
game.add('roller', name='coin')

# define sides for dice and coin types
game.stuff.six_dice.sides = 6
game.stuff.six_dice.twenty_dice.sides = 20
game.stuff.six_dice.coin.sides = 2

# add shaker and add count of stuff to shaker
game.add('shaker', name='red_shaker')
game.tools.red_shaker.add('six_dice', count=50)
game.tools.red_shaker.add('twenty_dice', count=10)
game.tools.red_shaker.add('coin', count=42)

# roll all stuff and get result
result = game.tools.red_shaker.roll()

# or define new shaker with default count == 1 and roll each stuff separatly
game.add('shaker', name='blue_shaker')
game.tools.blue_shaker.add('six_dice')
game.tools.blue_shaker.add('coin')

result = game.tools.blue_shaker.six_dice.roll()
result = game.tools.blue_shaker.coin.roll()

# you can use dict notation offcourse
result = game['tools']['blue_shaker']['coin'].roll()

# delete components from any collections
del game.tools.blue_shaker
del game.stuff.six_dice

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
