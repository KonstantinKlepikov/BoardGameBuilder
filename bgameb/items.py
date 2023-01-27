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


class Step(BaseItem):
    """Game steps or turns

    ..
        Attr:

            priority (NonNegativeInt): priority queue number. Default to 0.
    """
    #: priority queue number. Default to 0.
    priority: NonNegativeInt = 0

    def __eq__(self, other: 'Step') -> bool:  # type: ignore[override]
        return self.priority == other.priority

    def __lt__(self, other: 'Step') -> bool:
        return self.priority < other.priority

    def __le__(self, other: 'Step') -> bool:
        return self.priority <= other.priority

    def __ne__(self, other: 'Step') -> bool:  # type: ignore[override]
        return self.priority != other.priority

    def __gt__(self, other: 'Step') -> bool:
        return self.priority > other.priority

    def __ge__(self, other: 'Step') -> bool:
        return self.priority >= other.priority


class Sides(ConstrainedInt):
    """Int subtipe to define sides of dices
    """
    #: greate than 1 constraint
    gt = 1


class Dice(BaseItem):
    """Rolling or tossed objects, like dices or coins.

    .. code-block::
        :caption: Example:

            dice = Dice(id='coin', sides=2, mapping={1: 'this', 2: 'that'})

    ..
        Attr:

            count (PositiveInt): count of dices. Default to 1.

            sides (Sides): sides of dice or coin. Default to 2.

            mapping (dict[PositiveInt, Any]):
                optional mapping of roll result. Mapping must define
                values for each side.

            last roll (list[PositiveInt]), optional:
                last roll values.

            last roll mapped (list[Any]), optional:
                last mapped roll values.

            _range (list[PositiveInt]): range of roll, started from 1.

        Raises:

            StuffDefineError: mapping keys is not equal of roll range.
    """
    #: Count of dices.
    count: PositiveInt = 1
    #:  Sides of dice or coin.
    sides: Sides = cast(Sides, 2)
    #: Optional mapping of roll result
    #: Mapping must define values for each side.
    mapping: dict[PositiveInt, Any] = {}
    #: Last roll values
    last_roll: list[PositiveInt] = []
    #: Last mapped roll values
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

    ..
        Attr:

            count (PositiveInt): count of cards. Default to 1.

            is_revealed (bool): is card oppened. Default to False.

            is_active (bool): is card tapped. Default to False.

            side (str, optional): the side of tap. Default to None.

    .. code-block::
        :caption: Example:

            card = Card(id='unique_card')
            card.tap(side='left')
    """
    #: Count of cards.
    count: PositiveInt = 1
    #: Is card oppened.
    is_revealed: bool = False
    #: Is card is_active.
    is_active: bool = True
    #: The side of tap.
    side: Optional[str] = None

    def flip(self) -> 'Card':
        """Face up or face down the card regardles of it condition

        Returns:
            Card
        """
        if self.is_revealed:
            self.is_revealed = False
            self._logger.debug('Card face down.')
        else:
            self.is_revealed = True
            self._logger.debug('Card face up.')
        return self

    def open(self) -> 'Card':
        """Face up the card

        Returns:
            Card
        """
        self.is_revealed = True
        self._logger.debug('Card face up.')
        return self

    def hide(self) -> 'Card':
        """Face down the card

        Returns:
            Card
        """
        self.is_revealed = False
        self._logger.debug('Card face down.')
        return self

    def tap(self, side='right') -> 'Card':
        """Tap the card to the given side

        Args:
            side (str, optional): side to tap. Defaults to 'right'.

        Returns:
            Card
        """
        self.is_active = False
        self.side = side
        self._logger.debug(f'Card taped to side {side}.')
        return self

    def untap(self) -> 'Card':
        """Untap the card

        Returns:
            Card
        """
        self.is_active = True
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
