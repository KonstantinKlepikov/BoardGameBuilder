"""Classes taht implements game dices and coins
"""
import random
from typing import List, Set, Optional
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.utils import DiceWithoutSidesError


@dataclass
class Dice(DataClassJsonMixin):
    """Base class to create the dice

    Define name to identify later Dice object by unique name.
    For example: 'six_side_dice'

    Colors is a list of unique colors that can be used for
    separate dices by colors if you roll ,many in dice tower.
    You can implenemt it with pythonic set API.

    .. code-block::
        :caption: Example of colors usage

            dice = Dice(name='six_side_dice')
            dice.colors.update(['red', 'green'])
            dice.add('white')

    """
    name: str = 'default_dice'
    sides: Optional[int] = field(default=None, init=False)
    colors: Set[str] = field(default_factory=set, init=False)
    _range_to_roll: List[int] = field(default_factory=list, init=False)


    def __post_init__(self) -> None:
        """Set class attributes after initialiusation
        """
        self.colors = set()

    def roll(self) -> int:
        """Return result of roll

        Raises:
            DiceWithoutSidesError: is not defined number of sides

        Returns:
            int: result of roll
        """
        if self.sides:
            return random.choices(self._range_to_roll, k=1)[0]

        else:
            raise DiceWithoutSidesError(
                f'Is not defined number of sizes for {self.name}'
                )


@dataclass
class TrueDice(Dice):
    """Class to create true dices with sides

    With sides you can define number of sides for dice.
    Default 6
    """
    sides: int = 6

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.sides, int):
            raise DiceWithoutSidesError(
                f'Is not defined number of sizes for dice {self.name}'
                )
        else:
            self._range_to_roll = list(range(1, self.sides + 1))

    # def roll(self) -> int:
    #     """Return result of roll

    #     Raises:
    #         NotImplementedError: _description_

    #     Returns:
    #         int: result of roll
    #     """
    #     if self.sides:
    #         return random.choices(self._range_to_roll, k=1)[0]

    #     else:
    #         raise DiceWithoutSidesError(
    #             f'Is not defined number of sizes for {self.name}'
    #             )


@dataclass
class Coin(Dice):
    """_summary_
    """

    def __post_init__(self):
        super().__post_init__(self)
        self.sides= 2
        self._range_to_roll = list(range(1, 3))

    def flip_coin(self):
        raise NotImplementedError




@dataclass
class DiceTower(DataClassJsonMixin):
    """Base class to create dice towers
    """