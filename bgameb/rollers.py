"""Game dices and coins
"""
import random
from typing import List, Optional
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin


@dataclass
class BaseRoller(DataClassJsonMixin):
    """Base class to create the rolled or fliped object

    Define name to identify later BaseRoller object by unique name.
    For example: 'six_side_dice'

    .. code-block::
        :caption: Example:

            dice = Dice(name='six_side_dice', sides=12)
    """
    name: str = 'base_roller'
    sides: Optional[int] = field(default=None, init=False)
    _range_to_roll: List[int] = field(default_factory=list, init=False)

    def roll(self) -> int:
        """Roll or flip and return result

        Raises:
            RollerSidesError: is not defined number of sides

        Returns:
            int: result of roll
        """
        if self.sides:
            return random.choices(self._range_to_roll, k=1)[0]
            # TODO: add weights
            # https://docs.python.org/dev/library/random.html#random.choices

        else:
            raise RollerSidesError(
                f'Is not defined number of sizes for {self.name}'
                )


@dataclass
class Dice(BaseRoller):
    """Create dice

    You can define number of sides for dice.
    Default 6
    """
    name: str = 'dice'
    sides: int = 6

    def __post_init__(self):
        if not isinstance(self.sides, int):
            raise RollerSidesError(
                f'Is not defined number of sizes for dice {self.name}'
                )
        else:
            self._range_to_roll = list(range(1, self.sides + 1))


@dataclass
class Coin(BaseRoller):
    """Create coin like a dice with two sides
    """
    name: str = 'coin'

    def __post_init__(self):
        self.sides= 2
        self._range_to_roll = list(range(1, 3))


class RollerSidesError(RuntimeError):
    """Count of sides not defined for this rolled object
    """
    pass
