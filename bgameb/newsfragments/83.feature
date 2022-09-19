#83:
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