"""Game dices, coins, cards and other items
"""
import random
from typing import Optional, NoReturn, Any
from pydantic import Field, conint, PositiveInt, NonNegativeInt
from bgameb.base_ import Base_
from bgameb.errors import StuffDefineError


class BaseItem_(Base_):
    """Base class for game items (like dices or cards)
    """


class Step_(BaseItem_):
    """Game steps or turns

    Attr:
        - priority (NonNegativeInt): priority queue number. Default to 0.
    """
    priority: NonNegativeInt = 0


class Dice_(BaseItem_):
    """Rolled or fliped objects, like dices or coins.

    Sides attr define number of sides of roller. Default to 2.
    Sides can't be less than 2.

    .. code-block::
        :caption: Example:

            dice = Dice('coin', sides=2)

    Attr:
        - count (PositiveInt): count of items. Default to 1.
        - sides (ositiveInt): sides of dice or coin. Default to 2.
        - mapping (dict[int, Any]): nonnumerik mapping of roll result.
        - last_roll (Optional[list[int]]): last roll value.
        - last_roll_mapped: (Optional[list[Any]]): last maped roll value.

    Raises:
        StuffDefineError: number of sides less than 2.
        StuffDefineError: mapping keys is not equal of roll range.
    """
    count: PositiveInt = 1
    sides: conint(gt=1) = 2
    mapping: dict[int, Any] = {}
    last_roll: list[int] = []
    last_roll_mapped: Optional[list[Any]] = {}
    _range: list[int] = []

    def __init__(self, **data):
        super().__init__(**data)
        self._range = list(range(1, self.sides + 1))

        if self.mapping and set(self.mapping.keys()) ^ set(self._range):
            raise StuffDefineError(
                message='Mapping must define values for each side.',
                logger=self._logger
                    )

    def roll(self) -> list[int]:
        """Roll and return result

        Returns:
            List[int]: result of roll
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


class Card_(BaseItem_):
    """Card object

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

    def flip(self) -> 'Card_':
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

    def open(self) -> 'Card_':
        """Face up the card

        Returns:
            Card
        """
        self.opened = True
        self._logger.debug('Card face up.')
        return self

    def hide(self) -> 'Card_':
        """Face down the card

        Returns:
            Card
        """
        self.opened = False
        self._logger.debug('Card face down.')
        return self

    def tap(self, side='right') -> 'Card_':
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

    def untap(self) -> 'Card_':
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
