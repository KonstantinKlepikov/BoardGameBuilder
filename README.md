# BoardGameBuilder

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
# create the game
game = Game('one_board_game')

# add dices types to game
game.add('dice', name='six_dice')
game.add('dice', name='twenty_dice')
game.add('dice', name='hundred_dice')

# define dices types sides
game.stuff.six_dice.sides = 6
game.stuff.six_dice.twenty_dice = 20
game.stuff.six_dice.hundred_dice = 100

# add shakers for roll dices and add count of dices to shaker
game.add('shaker', name='red_dicer')
game.tools.red_dicer.add('six_dice', count=50)
game.tools.red_dicer.add('twenty_dice', count=10)
game.tools.red_dicer.add('hundred_dice', count=42)

# roll all dices and get result
result = game.tools.red_dicer.roll()

# or define new shaker with default count and roll each dice separatly
game.add('shaker', name='blue_dicer')
game.tools.blue_dicer.add('six_dice')
game.tools.blue_dicer.add('twenty_dice')
game.tools.blue_dicer.add('hundred_dice')

result = game.tools.blue_dicer.six_dice.roll()
result = game.tools.blue_dicer.hundred_dice.roll()

# you can use dict notation offcourse
result = game['tools']['blue_dicer']['hundred_dice'].roll()

# delete components from any collections
del game.tools.blue_dicer
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
