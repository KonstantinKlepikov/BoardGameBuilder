"""Classes taht implements game dices and coins
"""
import random
from typing import List, Set, Optional
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.utils import RolledWithoutSidesError


@dataclass
class RollOrFlip(DataClassJsonMixin):
    """Base class to create the rolled or fliped object

    Define name to identify later RollOrFlip object by unique name.
    For example: 'six_side_dice'

    # Colors is a list of unique colors that can be used for
    # separate dices by colors if you roll ,many in dice tower.
    # You can implenemt it with pythonic set API.

    # .. code-block::
    #     :caption: Example of colors usage

    #         dice = Dice(name='six_side_dice')
    #         dice.colors.update(['red', 'green'])
    #         dice.add('white')
    """
    name: str = 'default'
    sides: Optional[int] = field(default=None, init=False)
    # colors: Set[str] = field(default_factory=set, init=False)
    _range_to_roll: List[int] = field(default_factory=list, init=False)


    # def __post_init__(self) -> None:
    #     """Set class attributes after initialiusation
    #     """
    #     self.colors = set()

    def roll(self) -> int:
        """Roll or flip and return result

        Raises:
            RolledWithoutSidesError: is not defined number of sides

        Returns:
            int: result of roll
        """
        if self.sides:
            return random.choices(self._range_to_roll, k=1)[0]
            # TODO: add weights
            # https://docs.python.org/dev/library/random.html#random.choices

        else:
            raise RolledWithoutSidesError(
                f'Is not defined number of sizes for {self.name}'
                )


@dataclass
class Dice(RollOrFlip):
    """Create dice

    You can define number of sides for dice.
    Default 6
    """
    name: str = 'dice'
    sides: int = 6

    def __post_init__(self):
        # super().__post_init__()
        if not isinstance(self.sides, int):
            raise RolledWithoutSidesError(
                f'Is not defined number of sizes for dice {self.name}'
                )
        else:
            self._range_to_roll = list(range(1, self.sides + 1))


@dataclass
class Coin(RollOrFlip):
    """Create coin like a dice with two sides
    """
    name: str = 'coin'

    def __post_init__(self):
        # super().__post_init__()
        self.sides= 2
        self._range_to_roll = list(range(1, 3))
