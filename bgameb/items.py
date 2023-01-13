"""Game dices, coins, cards and other items
"""
import random
from typing import Optional, NoReturn, Any
from dataclasses import dataclass, field
from dataclasses_json import (
    config, DataClassJsonMixin, dataclass_json, Undefined
        )
from bgameb.base import Base
from bgameb.errors import StuffDefineError


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class BaseItem(Base, DataClassJsonMixin):
    """Base class for game items (like dices or cards)
    """

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(order=True)
class Step(BaseItem, DataClassJsonMixin):
    """Game steps or turns

    Attr:
        - priority (int): priority queue number. Default to 0.
    """
    priority: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Dice(BaseItem, DataClassJsonMixin):
    """Rolled or fliped objects, like dices or coins.

    Sides attr define number of sides of roller. Default to 2.
    Sides can't be less than 2.

    .. code-block::
        :caption: Example:

            dice = Dice('coin', sides=2)

    Attr:
        - count (int): count of items. Default to 1.
        - sides (int): sides of dice or coin. Default to 2.
        - mapping (dict[int, Any]): nonnumerik mapping of roll result.
        - last_roll (Optional[list[int]]): last roll value.
        - last_roll_mapped: (Optional[list[Any]]): last maped roll value.

    Raises:
        StuffDefineError: number of sides less than 2.
        StuffDefineError: mapping keys is not equal of roll range.
    """
    count: int = 1
    sides: int = 2
    mapping: dict[int, Any] = field(
        default_factory=dict,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )
    last_roll: Optional[list[int]] = field(
        default=None,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )
    last_roll_mapped: Optional[list[Any]] = field(
        default=None,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )
    _range: list[int] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        init=False,
        repr=False
            )

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.sides < 2:
            raise StuffDefineError(
                message=f'Number of sides={self.sides} '
                        f'for "{self.id}". Needed >= 2.',
                logger=self._logger
                )
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


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Card(BaseItem, DataClassJsonMixin):
    """Card object

    Attr:
        - count (int): count of items. Default to 1.
        - opened (bool): is card oppened. Default to False.
        - tapped (bool): is card tapped. Default to False.
        - side (str, optional): the side of tap. Default to None.

    .. code-block::
        :caption: Example:

            card = CardType('unique_card')
            card.tap(side='left')
    """
    count: int = 1
    opened: bool = False
    tapped: bool = False
    side: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()

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
