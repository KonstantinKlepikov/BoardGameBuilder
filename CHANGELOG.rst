==========================
BoardGameBuilder changelog
==========================

.. release notes
Release v0.0.20 (2022-10-18)
============================

Features
--------

- # 139:
      * To Game object added methods new() and copy() for create new components and copy components
      * Added make check to check flake8 and mypy to Makefile
      * add nonstuff types to types.py
      * _increase() method for tool classes is replaces by update() method
      * add type_ for each component/ Types is constructed from classes type_
      * now to tools and players can be added only stuffs
      * test all
      * chenges in README
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/139)


Deprecations and Removals
-------------------------

- #139:
      * Is removed anstracted classes from project
      * add() method is deprecated and removed from Game class
      * add_to() is deprecated and removed from Game class
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/139)


Release v0.0.19 (2022-10-12)
============================

Bugfixes
--------

- #61:
      * added mypy
      * fixed type annotation
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/61)


Release v0.0.18 (2022-10-05)
============================

Features
--------

- #79:
      * logger now is a part of base.py and log_me not a global
      * Added ``make ipython``
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/79)
- #103:
      * Added Stream class
      * turn_order added to Game class - is a Stream object
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/103)
- #106:
      * Added CardsBag class - construct for nonqueued deck, like hands, graveyards, exiles and etc
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/106)
- #132:
      * _stufff attr of tolls now is a list (not set) - this grant order
      * Rule is a stuff now and realize Components interface
      * Added types.py with types and objects constants of stuff and tools
      * Added Rules tool and Turn tool for storage rules and turn rules
      * Added Bag type for ordered but not queued lists of cards
      * Roller class now is a Dice
      * Test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/132)


Deprecations and Removals
-------------------------

- #128:
      * Removed rules.py. All rules classes are Components now - tools or stuff
      * Remove add_rules() method of Game
      * Removed List[str] rules attributes from all classes
      * Removed clear method for Deck - use deck.dealt.clear() deque method
      * Removed dtata types constrants of each components - now we use constants from types.py
      * Last properti of Shaker is removed
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/132)


Misc
----

- https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/128


Release v0.0.17 (2022-10-01)
============================

Features
--------

- #89:
      * Add Rule class. It is dataclass dict like object
      * Add is_active to all game objects
      * Some tests changes
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/89)
- #123:
      * Remove RollerType and CardType classes
      * Now all logic in Roller and Card classes
      * Added add_to() method to Game class - now we can add stuff to tool from Game() obgect
      * Method add() of tools objects is closed and renamed to update()
      * Added simple check code to game.py -> run by ``python bgameb/game.py``
      * Default count of stuff is 1
      * last attr of Shaker class and dealt attr of Deck class are hidden from repr
      * Test all
      * Example in README changes
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/123)
- #124:
      * Changing add_to() method of Game. Now add_to(to, name, ...)
      * README example changes
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/124)
- #125:
      * Added RulesMixin class
      * Some minore changes in Rules class
      * Game obgect recieve rules attr - is na Component for Rules
      * Game has method add_phase()
      * Added rules attrs to stuff and players classes - is are list of str for save names of rules for this object
      * README changes
      * Test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/125)


Deprecations and Removals
-------------------------

- #90:
      * Now is removed CardText class
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/90)


Release v0.0.16 (2022-09-28)
============================

Features
--------

- #104:
      * Add counter attribute to Card, Player and Game classes
      * counter is a collections.Counter
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/104)
- #115:
      * add() method of a Game class now use kwargs to unpack any number of named args.
      * Change example in README
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/115)
- #118
      * removed constructs.py and test_constructs.py
      * added base.py. Move Components, CardTexts, Base to base.py
      * Base now is child of Constructs. Constructs is dataclass with init=False, repr=False
      * Constructs can be accessed by setitems
      * setaatr is removed from Constructs
      * moved BaseGame to game.py
      * remove stuff, tools, players attrs from Game class
      * moved BasePlayer to players.py/ Remove bot class
      * moved base stuffs to stuff.py
      * moved base tools to tools.py
      * remove stuff attr from tools. Now _tools is used for check names of added stuffs
      * dict-like acces to dealt from tool is removed
      * test randomizing arrange and deal() with fixed seed
      * README changing
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/118)
- #119:
      * Is removed random name definition from project
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/119)


Bugfixes
--------

- #104:
      * Remove redundant attribute definition for dataclasses postinit.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/104)
- #111:
      * Fix recursion problems in to_json() method.
      * Now is changed interface - tools classes needs game object in method add()
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/111)
- #112:
      * Fix arrange dealt Deck fail test.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/112)


Release v0.0.15 (2022-09-24)
============================

Features
--------

- #41:
      * Add Player class and methods for BasePlayer
      * Add player to add() method of game. Add attr playrs to Game
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/41)


Release v0.0.14 (2022-09-22)
============================

Features
--------

- #77:
      * implement to_arrnaage() and arrange() methods
      * add ArrangeIndexError
      * add key access to self.dealt of Deck
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/77)
- #81:
      * Add and test search() method to deck.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/81)


Release v0.0.13 (2022-09-21)
============================

Features
--------

- #76:
      * implenemt deal() method and add deal attr to Deck class. When we deal() the cards - the names of all cards in deck multiplied by its copies are random shuffled in to a list, saved in dealt attr
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/76)
- #78:
      * Add shuffle() method of Deck class implenebtation.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/78)
- #80:
      * create copy of deck stuff cards to use in ``dealt``
      * implement clean method - remove all dealt cards
      * dealt now is deque and it has all methods of python deque
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/80)


Bugfixes
--------

- #71:
      * Changed method _update() of Components class to check - is None name of added component.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/71)


Improved Documentation
----------------------

- #76:
      * Fix example of usage in readme.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/76)


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
- #47:
      * Move logging errors inside StuffDefineError.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/47)


Release v0.0.10 (2022-09-10)
============================

Features
--------

- #57:
      * Add get_names() method to Components class.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/57)
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
- #64:
      * Hide rollers field for json/dict from shaker instance.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/64)


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

- #30:
      * Parametrize shaker tests with Dice, Coin objects.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/30)
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
- #37:
      * Add flake8 support.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/37)


Bugfixes
--------

- #40:
      * Fix release run if closed pullrequest without merge.
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
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/3)
