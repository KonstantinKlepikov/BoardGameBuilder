"""Game dices, coins, cards and other items
"""
import random
from typing import Optional, NoReturn, Any, cast
from pydantic import PositiveInt, NonNegativeInt, ConstrainedInt
from bgameb.base import Base
from bgameb.errors import StuffDefineError


class BaseItem(Base):
    """Base class for game items (like dices or cards)
    """


class Step_(BaseItem):
    """Game steps or turns

    Attr:
        - priority (NonNegativeInt): priority queue number. Default to 0.
    """
    priority: NonNegativeInt = 0

    def __eq__(self, other: 'Step_') -> bool:  # type: ignore[override]
        return self.priority == other.priority

    def __lt__(self, other: 'Step_') -> bool:
        return self.priority < other.priority

    def __le__(self, other: 'Step_') -> bool:
        return self.priority <= other.priority

    def __ne__(self, other: 'Step_') -> bool:  # type: ignore[override]
        return self.priority != other.priority

    def __gt__(self, other: 'Step_') -> bool:
        return self.priority > other.priority

    def __ge__(self, other: 'Step_') -> bool:
        return self.priority >= other.priority


class Sides(ConstrainedInt):
    """Int subtipe to define sides of dices
    """
    gt = 1


class Dice(BaseItem):
    """Rolling or tossed objects, like dices or coins.

    Sides attr define number of sides of roller. Default to 2.
    Sides can't be less than 2.

    .. code-block::
        :caption: Example:

            dice = Dice(id='coin', sides=2)

    Attr:
        - count (PositiveInt): count of items. Default to 1.
        - sides (Sides): sides of dice or coin. Default to 2.
        - mapping (dict[PositiveInt, Any]): optional mapping of roll result.
        - last_roll (Optional[list[PositiveInt]]): last roll values.
        - last_roll_mapped (Optional[list[Any]]): last mapped roll values.
        - _range list[PositiveInt] - range of roll, started from 1.

    Raises:
        StuffDefineError: mapping keys is not equal of roll range.
    """
    count: PositiveInt = 1
    sides: Sides = cast(Sides, 2)
    mapping: dict[PositiveInt, Any] = {}
    last_roll: list[PositiveInt] = []
    last_roll_mapped: list[Any] = []
    _range: list[PositiveInt] = []

    def __init__(self, **data):
        super().__init__(**data)
        self._range = list(range(1, self.sides + 1))

        if self.mapping and set(self.mapping.keys()) ^ set(self._range):
            raise StuffDefineError(
                message='Mapping must define values for each side.',
                logger=self._logger
                    )

    def __eq__(self, other: 'Dice') -> bool:  # type: ignore[override]
        return self.sides == other.sides

    def __lt__(self, other: 'Dice') -> bool:
        return self.sides < other.sides

    def __le__(self, other: 'Dice') -> bool:
        return self.sides <= other.sides

    def __ne__(self, other: 'Dice') -> bool:  # type: ignore[override]
        return self.sides != other.sides

    def __gt__(self, other: 'Dice') -> bool:
        return self.sides > other.sides

    def __ge__(self, other: 'Dice') -> bool:
        return self.sides >= other.sides

    def roll(self) -> list[PositiveInt]:
        """Roll and return result

        Returns:
            List[PositiveInt]: result of roll
        """
        self.last_roll = [
            random.choices(self._range, k=1)[0] for _
            in list(range(self.count))
                ]
        return self.last_roll

    def roll_mapped(self) -> list[Any]:
        """Roll and return mapped result

        Returns:
            list[Any]: result of roll
        """
        self.last_roll_mapped = [
            self.mapping[roll] for roll in self.roll()
            if self.mapping.get(roll)
                ]
        return self.last_roll_mapped


class Card(BaseItem):
    """Card objects

    Attr:
        - count (PositiveInt): count of items. Default to 1.
        - opened (bool): is card oppened. Default to False.
        - tapped (bool): is card tapped. Default to False.
        - side (str, optional): the side of tap. Default to None.

    .. code-block::
        :caption: Example:

            card = CardType('unique_card')
            card.tap(side='left')
    """
    count: PositiveInt = 1
    opened: bool = False
    tapped: bool = False
    side: Optional[str] = None

    def flip(self) -> 'Card':
        """Face up or face down the card regardles of it condition

        Returns:
            Card
        """
        if self.opened:
            self.opened = False
            self._logger.debug('Card face down.')
        else:
            self.opened = True
            self._logger.debug('Card face up.')
        return self

    def open(self) -> 'Card':
        """Face up the card

        Returns:
            Card
        """
        self.opened = True
        self._logger.debug('Card face up.')
        return self

    def hide(self) -> 'Card':
        """Face down the card

        Returns:
            Card
        """
        self.opened = False
        self._logger.debug('Card face down.')
        return self

    def tap(self, side='right') -> 'Card':
        """Tap the card to the given side

        Args:
            side (str, optional): side to tap. Defaults to 'right'.

        Returns:
            Card
        """
        self.tapped = True
        self.side = side
        self._logger.debug(f'Card taped to side {side}.')
        return self

    def untap(self) -> 'Card':
        """Untap the card

        Returns:
            Card
        """
        self.tapped = False
        self.side = None
        self._logger.debug('Card untaped. Side set to None.')
        return self

    def alter(self) -> NoReturn:
        """Many cards have alter views. For example
        card can have main view, that apply most time of the game
        and second view, that apply only if card played as
        that alternative. For ease of understanding, consider that
        different views of the same card are not related directly
        to each other.
        """
        raise NotImplementedError
