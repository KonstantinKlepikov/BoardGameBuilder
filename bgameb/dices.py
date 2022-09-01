from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin


@dataclass
class Dice(DataClassJsonMixin):
    """Base class to create the dice
    """


@dataclass
class DiceTower(DataClassJsonMixin):
    """Base class to create dice towers
    """