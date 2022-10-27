#145:
    * added custom dataclass queue - Order with ordering by priority attr
    * added Steps class to define game order
    * added Step class with priority to define priority of game turns
    * Order is moved to base.py
    * renamed dealt to current. All names of attrs not shown in repr, if starts with _ or current
    * __repr__ now is custom, __str__ is same as __repr__
    * ->