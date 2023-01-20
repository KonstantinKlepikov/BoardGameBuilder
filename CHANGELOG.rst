==========================
BoardGameBuilder changelog
==========================

.. release notes
Release v0.1.0 (2023-01-20)
===========================

Features
--------

- #270:
      - Added pydantic
      - Added PropertyBaseModel - is expanding subclass of pydantic BaseModel. It used for get properties as pydantic fields
      - Component is a pydantic generic and mapping class with dict interface
      - now we not check unique name of object in Component
      - all classes are pydantic classes. dataclasses-json dependencies removed
      - for relocate attrs is used pydantic aliaces of fields
      - for fill shcemas by calable inside classes is used properties
      - method by_id of tools return list of objects
      - tests refactoring and tested all
      - docs and readme changes
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/270)


Deprecations and Removals
-------------------------

- # 270:
      - dataclasses-json dependecie is removed
      - attr c is removed from all classes except tools
      - some methods, that get stuff from Component in stuff classes are removed (like get_items())
      - from Bag class removed current and last attributes. Bag cant be dealt
      - Component now isnt set-like dict - we can add copies with identical keys, it replace old objects. Ids not check now.
      - other attribute (for not defined in shcema data) is removed
      - are removed relocate() and relocate_all() methods
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/270)


Release v0.0.39 (2023-01-14)
============================

Bugfixes
--------

- #257:
      - get(0 from __dict__ is changed to __geattribute__ for relocate() method of Base class)
      - tests
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/267)


Release v0.0.38 (2023-01-13)
============================

Features
--------

- #263:
      - current_ids() is a property now
      - get_items(), get_players(), get_rools() property to
      - last is added to BaseTool - is available to Bag
      - clear() now clear last
      - pull() is renamed to pop() in Steps class
      - result of pop() is added to last
      - last_id property added in to tools
      - by_id() is added to get item from current by id
      - test all
      - check.py changes
      - docs and readme changes
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/263)


Deprecations and Removals
-------------------------

- #263:
      - build_json() is removed from Game object
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/265)


Release v0.0.37 (2023-01-10)
============================

Bugfixes
--------

- #260:
      - is changed _to_relocate type - now values in dict sre a string and we uses only methods of class to meke something to relocation
      - is fixed relovate() method to use methods of class or attributes
      - _to_relocate is exclude from init
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/260)


Release v0.0.36 (2023-01-06)
============================

Features
--------

- #29:
      - added mapping attr to Dice - as a dict with int keys and Any values
      - added roll_mapped() to Dice object
      - added roll_maped() to shaker
      - tested all
      - docs changed
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/29)
- #250:
       - added reorder() ,reorderleft() and reorderfrom() methods to Deck object
       - added _check_order_len() and _check_is_to_arrange_valid() methods
       - tested all
       - readme changed
       - docs changed
       - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/250)
- #253:
      - added _to_relocate attr to Base class. Is a dict with str keys and str/Calable values
      - addede relocate() function to Base class
      - is changed check.py example
      - test all
      - changes in docs and README
      - "NEW game" now is logged in BaseGame class
      - is removed repr=False from @dataclass declaration
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/253)
- #254:
      - added get_items_val(), get_tools_val() and get_players_val() methods to game - they returns a lists of dict representation of nested dataclasses
      - added build_json() method to Game
      - added relocate_all() to Game
      - relocate() and reloacate_all() returns self
      - tested all
      - added example, changed docs and README
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/254)
- #256:
      - added last and last_mapped to Dice and Shaker object
      - roll() and roll_mapped() write values to last and last_mapped and returns this result
      - tests all
      - dock changes
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/256)


Deprecations and Removals
-------------------------

- #250:
      - to_arrange() and arrange() methods of Deck object are removed
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/250)


Release v0.0.35 (2022-12-22)
============================

Bugfixes
--------

- #247:
      - get_names() renamed to ids()
      - ids() return ids ov __included__ of Component
      - deal() methods of rools changed - now used ids() mor fill current from list
      - all tests
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/247)


Release v0.0.34 (2022-12-21)
============================

Features
--------

- #243:
      - added keys(), keys(), items() methods to Component
      - added __inclusion__ attr to Component - all stuff is placed here, all operation get/repr/len and ets is maked with this attribute
      - _update() renamed to update
      - fix some problems with get_{stuff} methods
      - fix bug with replace - add type check to yools add() methods, remove check from deal()
      - changed docs
      - tests
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/243)


Bugfixes
--------

- #242:
      - fix Bag get_items()
      - some changes in example of code in README and check.py
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/242)


Release v0.0.33 (2022-12-19)
============================

Features
--------

- #236:
      - clear last when current is clear for Steps
      - to Deck added last, last is clear with clear() and changed with pop() and popleft()
      - test all, add docs for some objects
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/236)
- #237:
      - added attr c to Game, Player, and tools - is a Component classsfor any stuff
      - added methods to get dict of Olayers, Tools and Items from game c
      - test all and docs changing
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/237)


Deprecations and Removals
-------------------------

- #237:
      - is removed t, i, p attrs
      - now we not used union of classes for annotation - only union of base classes
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/237)


Release v0.0.32 (2022-12-14)
============================

Features
--------

- #233:
      - to all subclasses is added base classes (BasePlayer and etc)
      - Component - now is a dict, used as base for store some players, items or tools
      - Game obgect gains attributes p, t, i - are Component() for players, tools or items objects
      - tool classes gained i attributr to for item storage
      - Game and tools classes now have add() methods to add objects to his components
      - you cant get access to write attributes of components directly. Use add()
      - all now is typed, except dynamicaly added objects to Components
      - to some methods added pipeline interface
      - tested all
      - changed docs and README
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/233)


Bugfixes
--------

- #233:
      - project now suported python 3.9+
      - security: some package upgrades
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/233)


Deprecations and Removals
-------------------------

- #233:
      - is removed additional args from Player class
      - get_component_by_id() renamed to by_id()
      - get_current_ids() -> current_id()
      - current_step attr -> last
      - consttraint.py is removed
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/233)


Release v0.0.31 (2022-12-09)
============================

Features
--------

- #225:
      - is renamed get_current_names() method to get_current_ids() method
      - implemented get_component_by_id() method in Base class
      - test all
      - docs changes
      - readme changes
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/225)
- #226:
      * attributes for Player are optional
      - added current_step attr to Steps
      - rewrited _card_replace() for Deck
      - to Deck added deque methods: append(), appendleft(), pop(), popleft(), insert(), index(), remove(). reverse(), clear(), count(), extend(), extendleft(), rotate()
      - test all
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/226)
- #227:
      - added Bag class
      - to Deck added list methods: append(), pop(), insert(), index(), remove(). reverse(), clear(), count(), extend()
      - test all
      - -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/227)


Release v0.0.30 (2022-12-01)
============================

Features
--------

- #219:
      * Step now is an item
      * BaseIteme now hasnt count attr - this attribute moved to Card and Dice classes
      * tests all
      * docs changes
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/219)


Bugfixes
--------

- #218:
      * added ``make draft`` to makefile and now with ``make release`` is bulded doc after version bump but before taged and push to github
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/218)


Deprecations and Removals
-------------------------

- #219:
      * markers.py, markers types and test are removed.
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/219)


Release v0.0.29 (2022-12-01)
============================

Features
--------

- #208:
      * added get_current_names to Deck and Steps classes
      * methods put() and get() for Steps renamed to push() and pull() (for compatibility with dict)
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/208)
- #209:
      * add Undefined.INCLUDE in Base class. Now all undefined attributes is saved in other attribute
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/209)
- #210:
      * added to Deck and Steps deal() method posibility to deal with list of stuff names
      * deal() now are not shuffle deck by defolt
      * test it
      * docs and readme changes
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/210)


Bugfixes
--------

- #206:
      * changed github-release actions - added latest tag and removed autogeneration of changelog
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/206)


Deprecations and Removals
-------------------------

- #208:
      * removed technical attributes of Component from len and get_names methods
      * removed Order class. Now Steps has an heapq interface
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/208)


Release v0.0.28 (2022-11-28)
============================

Features
--------

- #9:
      * added github-release workflow that starts after deoloy documentations and create github tagged release
      * changed Makefile - now `make release` makes tagged commit and push to origin
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/9)


Bugfixes
--------

- #200:
      * fix version in docs and links fixes
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/200)
- #178:
      * change version of actions/setup-python to @4 for release.yml
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/178)


Release v0.0.27 (2022-11-20)
============================

Features
--------

- #36:
      * _is_unique() method for Component class
      * _is_valid() method for Component class
      * Components renamed to Component
      * added ComponentIdError
      * name attr of Base class is id now
      * all id is converted to safe before making attributes fir dot interface of Component
      * convertation with snake case
      * test all
      * change docks and readme
      * som fixes for logging
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/36)


Release v0.0.26 (2022-11-17)
============================

Features
--------

- #187:
      * all object inherited from Base gain counter attr that contains Counter() from collections
      * name now isnt in __repr__ and __str__ of dataclasses
      * test all
      * changes in docs
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/187)


Bugfixes
--------

- #186:
      * fix doc deplot workflow
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/186)
- #192:
      * fix readme example
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/192)


Deprecations and Removals
-------------------------

- #187:
      * Counter() dataclass is removed
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/187)


Release v0.0.25 (2022-11-09)
============================

Features
--------

- 180:
      * method add() added to Base class
      * _types_to_add attr and _type for check added components
      * redefined types.py - is removed Literal types and classes collections
      * added game stuff to __init__.py
      * redefine README Example
      * docs fixes
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/180)


Deprecations and Removals
-------------------------

- 180:
      * _add_replace() is removed from Componenys
      * _add method is removed from Components
      * new() and copy() methods are removed from Game
      * owner_off attr removed from Players class
      * game_steps attr is removed from Game
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/180)


Release v0.0.24 (2022-11-06)
============================

Features
--------

- #150:
      * added get_random() method for Deck class
      * is tested
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/150)
- #177:
      * deal() now return self.current
      * arrange() now return self.current
      * shuffle() now return self.current
      * Steps.deal() return current Order
      * added logging to get_random()
      * added doc, changing readme
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/179)


Bugfixes
--------

- #178:
      * fix docs building
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/178)


Deprecations and Removals
-------------------------

- #150:
      * removed Bag class
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/150)


Release v0.0.23 (2022-11-03)
============================

Features
--------

- #148:
      * Order class is moved to tools.py
      * added markers.py, ite,s.py, Counter and Step classes moved to markers.py
      * Card, Dice moved to items.py
      * redefine deal() methods and test it for tools
      * redefine copy() and new() for game class with hierarchy of stuffs
      * redefine tools - is removed stuff_to_add and stuff attrs
      * is added check of stuff class, that can be added to current attrs
      * for Components class moved creatong instances with kwargs from _add() and _add_replace() to _update()
      * test all
      * added dock
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/148)


Deprecations and Removals
-------------------------

- #148:
      * BaseGame class is removed. Functional now is Game.
      * counter attributes removed from all classes
      * stuff.py is removed
      * type_ are removed from all objacts. Now is an lower() __name__ of class
      * BasePlayer class is removed
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/148)


Release v0.0.22 (2022-10-31)
============================

Features
--------

- #147:
      * tests.yml for grid tests
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/147)
- #167:
      * added mypy check to test.yml workflow
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/167)


Bugfixes
--------

- #166:
      * add ``synchronize`` to pull_request trigger for tests.yml
      * remove start action on push
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/166)
- #168:
      * custom newsfragments are removed
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/168)


Release v0.0.21 (2022-10-28)
============================

Features
--------

- #145:
      * added custom dataclass queue - Order with ordering by priority attr
      * added Steps class to define game order
      * added Step class with priority to define priority of game turns
      * Order is moved to base.py
      * renamed dealt to current. All names of attrs not shown in repr, if starts with _ or current
      * __repr__ now is custom, __str__ is same as __repr__
      * renamed methods of Card object
      * test all
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/145)


Improved Documentation
----------------------

- #148:
      * modified and cleaned project dock
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/148)


Deprecations and Removals
-------------------------

- #145:
      * removed Rule class form stuff.py
      * removed Rules and Turns classes
      * remove attrs game_turn and game_rules from game object
      * all delt attrs removed from dict/jsone output
      * is_active property removed from all objects
      * type_ removed from Game class
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/145)
- #146:
      * is removed used_of attr from player
      * -> (https://github.com/KonstantinKlepikov/BoardGameBuilder/issues/146)


Release v0.0.20 (2022-10-18)
============================

Features
--------

- #139:
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
