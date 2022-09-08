#51:
    * Add errors.py
    * All custom errors moved to errors.py
    * Add Components class to games.py. Is mapping from collection.abc
    * implenment getitem/getattr, delitem/delattr methods. setitem/setattr raises NotImplementedError
    * Implement len method
    * Implement repr
    * Implement add() method with check id a name of added component in Components.__dict__.keys()
    * BaseRoller now is ABC
    * Add rollers, cards attr to Game and switch all collections to Components class
    * Refactoring add() method for Game class
    * Add ComponentClassError for case, when given noncomponent class
    * Tests all changes