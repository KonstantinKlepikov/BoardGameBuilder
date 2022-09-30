#123:
    * Remove RollerType and CardType classes
    * Now all logic in Roller and Card classes
    * Added add_to() method to Game class - now we can add stuff to tool from Game() obgect
    * Method add() of tools objects is closed and renamed to _increase()
    * Added simple check code to game.py -> run by ``python bgameb/game.py``
    * Default count of stuff is 1
    * last attr of Shaker class and dealt attr of Deck class are hidden from repr
    * Test all
    * Example in README changes
    * ->