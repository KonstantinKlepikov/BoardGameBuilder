==========================
BoardGameBuilder changelog
==========================

.. release notes
Release v0.0.12 (2022-09-19)
============================

Bugfixes
--------

- #91:
      * Remove from sphinx.setup_command import BuildDoc from setup.py
      * Add project variavles to conf.py of docs
      * Add importlib.metadata to import project metadata for docs
      * Change command for build docs in Makefile - now ``make proj-doc``
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/91)


Release v0.0.12 (2022-09-19)
============================

Features
--------

- #73:
      * make log
      * make test
      * remove make deploy
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/73)
- #83:
      * add new structure of modules to project
      * move Component class to constructs.py and add test_constructs.py
      * define more clear inheritance structure of classes
      * add RollerType and Roller classes
      * add CardType and Card classes
      * temporaly move CardText to constructs.py
      * add add() and self.stuff, self.tools to Game class
      * Remove color from shaker, now use color to shaker identification in name - like 'red_shaker' and add different unique dices
      * result of roll() for Roller now is a list of roll, defined by count attr
      * stuff classes get game() object to operate by game components types
      * remove old stuff classes - Card, Dice, Coin. Remove stuff and tools classes from __init__
      * move all similar methods of tools to BaseTool
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/83)


Improved Documentation
----------------------

- #73:
      * Add mystparser for .md parsing and include dependencies to sphynx
      * README changes
      * Add setuptools support
      * Add example to readme
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/73)


Release v0.0.11 (2022-09-13)
============================

Features
--------

- #34:
      * Add ABC BaseGameTools class
      * Exclude some data of classes from repr
      * _post_init_ for all classes refactoring
      * sides attr for rollers refactoring
      * Add decks attr to Game class
      * Deck class implementation
      * Add add() deck methods
      * Add remove() deck methods
      * BaseGameTools refactoring -> split to BaseGame and child BaseGameTools. Add abstarct methods add(), remove(), remove_all() for BaseGameTools
      * refactoring of Shaker methods - remove() now is one method for all remove operation
      * tests all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/34)
- Move logging errors inside StuffDefineError. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/47)


Release v0.0.10 (2022-09-10)
============================

Features
--------

- Add get_names() method to Components class. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/57)
- #58:
      * Add random-word package
      * Add function to word generating
      * function can return None object - use recursion
      * Add `slow` marker for pytest
      * Use random names for Game and Shaker
      * Use random name for Dice, Coin Card
      * tests
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/58)
- #59:
      * Add add_replace() method to Components
      * parametrize Components tests
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/59)
- #62:
      * game_cards -> game_cards
      * game_rollers -> game_rollers
      * exclude fields fro json/dict by using `metadata=config(exclude=lambda x:True)`
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/62)
- Hide rollers field for json/dict from shaker instance. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/64)


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
      * Tests all changes
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/51)


Bugfixes
--------

- #51:
      * Fixed isinstance check for component classes - now is used issubclas and __mro__
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/51)


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
      * Add CardText dict-like class dot-access
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/33)


Release v0.0.7 (2022-09-06)
===========================

Features
--------

- #15:
      * Add loguru.
      * Add logging to utils.py.
      * Add loggers to Game, Shaker and rollers.
      * Configure log format.
      * Add log_enable() method.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/15)
- #32:
      * add_component() -> add().
      * _range_roll -> _range.
      * last_roll() -> last()
      * remove name from shakers named tuple
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/32)
- Add flake8 support. (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/37)


Bugfixes
--------

- Fix release run if closed pullrequest without merge.
* -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/40)


Release v0.0.6 (2022-09-03)
===========================

Features
--------

- #13:
      * Add dataclass_json package.
      * Add name attr. Test name for instance.
      * Minor changes for pytest implementation.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/13)
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
      * Add shakers as NamedTuple to Game
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/14)


Improved Documentation
----------------------

- #14:
      * Add documentation for Dice class.
      * Add documentation for Coin class.
      * Add documentation for Shakers.
      * Docs refactoring.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/14)
- #22:
      * Minor changes wit docs headers.
      * Add usage page.
      * Add sphinx.ext.viewcode.
      * Add documentation links to project setup.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/22)


Release v0.0.5 (2022-08-30)
===========================

Features
--------

- #12:
      * Add Sphynx docs builder
      * Add custom theme to builder
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/12)
- #19:
      * Add flow to public docs on github pages
      * Change manifest and makefile for xreate release
      * Change readme
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/19)


Release v0.0.4 (2022-08-27)
===========================

Features
--------

- #3:
      * add towncrier to create changelog
      * add incremental to autobump version
      * add pytproject.toml to specify towncrier
      * add release workflow
      * ->  (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/3)
