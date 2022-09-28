#118
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
    * ->