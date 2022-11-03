#148:
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
    * ->