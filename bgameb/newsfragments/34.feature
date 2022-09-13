#34:
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