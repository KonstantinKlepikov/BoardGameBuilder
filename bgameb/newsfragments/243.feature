#243:
    - added keys(), keys(), items() methods to Component
    - added __inclusion__ attr to Component - all stuff is placed here, all operation get/repr/len and ets is maked with this attribute
    - _update() renamed to update
    - fix some problems with get_{stuff} methods
    - fix bug with replace - add type check to yools add() methods, remove check from deal()
    - changed docs
    - tests
    - ->