# BoardGameBuilder

Object-oriented framework for build board game logic in python

`pip install bgameb`

## Short example

```python
# create the game
game = Game('some_board_game')

# add dicec type to game
game.add_stuff('dice', name='six_dice', sides=6)
game.add_stuff('dice', name='twenty_dice', sides=20)

# add shakers for roll daces and add count of dices to shaker
game.add_tools('shaker', name='dicer')
game.tools.dicer.add('six_dice', count=50, color='white')
game.tools.dicer.add('six_dice', count=30, color='red')
game.tools.dicer.add('twenty_dice', count=10, color='red')

# rol dices and get result
result = game.tools.dicer.roll()

# get full public json data of any object, for examle of Game
schema = game.to_json()
```

## Documentation

[docs](https://konstantinklepikov.github.io/BoardGameBuilder/)

## Development

[dev install](https://konstantinklepikov.github.io/BoardGameBuilder/usage.html)

### Available cli

`make create-docs`

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

\* for version are used [incremental](https://github.com/twisted/incremental) and [towncrier](https://pypi.org/project/towncrier/) for changelog
