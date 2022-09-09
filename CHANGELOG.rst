==========================
BoardGameBuilder changelog
==========================

.. release notes
Release v0.0.9 (2022-09-09)
===========================

Features
--------

- #51:
      * Add errors.py
      * All custom errors moved to errors.py
      * Add Components class to games.py. Is mapping from collection.abc
      * implenment getitem/getattr, delitem/delattr methods. setitem/setattr raises NotImplementedError
      * Implement len, iter, repr
      * Implement add() method with check id a name of added component in Components.__dict__.keys()
      * BaseStuff, BaseRoller, BaseCard now is ABC
      * Add rollers, cards attr to Game and switch all collections to Components class
      * Refactoring add() method for Game class
      * Add ComponentClassError for case, when given noncomponent class
      * Move Shaker to game.py
      * Add stuff.py and move all stuff components (dices, coins, etc) to stuff.py
      * Remove rollers.py, cards.py. shkers.py
      * namespaces refactoring
      * Tests all changes (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/51)


Bugfixes
--------

- #51:
      * Fixed isinstance check for component classes - now is used issubclas and __mro__ (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/51)


Release v0.0.8 (2022-09-07)
===========================

Features
--------

- Parametrize shaker tests with Dice, Coin objects. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/30)
- #33:
      * Add cards.py
      * Add class Cards
      * Add CardText class
      * Add methods flip(), face_up(), face_down(), tap(), untap()
      * Add CardText dict-like class dot-access (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/33)


Release v0.0.7 (2022-09-06)
===========================

Features
--------

- #15:
      * Add loguru.
      * Add logging to utils.py.
      * Add loggers to Game, Shaker and rollers.
      * Configure log format.
      * Add log_enable() method. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/15)
- #32:
      * add_component() -> add().
      * _range_roll -> _range.
      * last_roll() -> last()
      * remove name from shakers named tuple (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/32)
- Add flake8 support. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/37)


Bugfixes
--------

- Fix release run if closed pullrequest without merge. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/40)


Release v0.0.6 (2022-09-03)
===========================

Features
--------

- #13:
      * Add dataclass_json package.
      * Add name attr. Test name for instance.
      * Minor changes for pytest implementation. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/13)
- #14:
      * Add BaseRoller class and base attributes.
      * Add Dice class for true dices.
      * Add Coin class.
      * Implement number of sides.
      * Implement range of rolls.
      * Add roll method to rollers.
      * Add error to roll without sizes.
      * Test Dice and Coin.
      * Namespaces refactoring.
      * Remove colors from rolled.
      * Add shakers module for shakers.
      * Add shaker class.
      * Implement add, remove, roll and last for Shaker.
      * Add error for define roller for Shaker.
      * Implement of roll method and last for shaker
      * Add shakers as NamedTuple to Game (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/14)


Improved Documentation
----------------------

- #14:
      * Add documentation for Dice class.
      * Add documentation for Coin class.
      * Add documentation for Shakers.
      * Docs refactoring. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/14)
- #22:
      * Minor changes wit docs headers.
      * Add usage page.
      * Add sphinx.ext.viewcode.
      * Add documentation links to project setup. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/22)


Release v0.0.5 (2022-08-30)
===========================

Features
--------

- Add Sphynx docs builder
  Add custom theme to builder (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/12)
- Add flow to public docs on github pages
  Change manifest and makefile for xreate release
  Change readme (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/19)


Release v0.0.4 (2022-08-27)
===========================

Features
--------

- add towncrier to create changelog
  add incremental to autobump version
  add pytproject.toml to specify towncrier
  add release workflow
  (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/3)
