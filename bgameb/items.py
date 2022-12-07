"""Game dices, coins, cards and other items
"""
import random
from typing import List, Optional, NoReturn
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from bgameb.base import Base
from bgameb.errors import StuffDefineError


@dataclass_json
@dataclass(repr=False)
class BaseItem(Base):
    """Base class for game items (like dices or cards)
    """

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json
@dataclass(order=True, repr=False)
class Step(BaseItem):
    """Game steps or turns

    Attr:
        - priority (int): priority queue number. Default to 0.
    """
    priority: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json
@dataclass(repr=False)
class Dice(BaseItem):
    """Rolled or fliped objects, like dices or coins.

    Sides attr define number of sides of roller. Default to 2.
    Sides can't be less than 2.

    .. code-block::
        :caption: Example:

            dice = Dice('coin', sides=2)

    Attr:
        - count (int): count of items. Default to 1.
        - sides (int): sides of dice or coin. Default to 2.

    Raises:
        StuffDefineError: number of sides less than 2
    """
    count: int = 1
    sides: int = 2
    _range: List[int] = field(
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

    def roll(self) -> List[int]:
        """Roll and return result

        Returns:
            List[int]: result of roll
        """
        roll = [
            random.choices(self._range, k=1)[0] for _
            in list(range(self.count))
            ]
        self._logger.debug(f'Is rolled {roll=}')
        return roll


@dataclass_json
@dataclass(repr=False)
class Card(BaseItem):
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

    def flip(self) -> None:
        """Face up or face down the card regardles of it condition
        """
        if self.opened:
            self.opened = False
            self._logger.debug('Card face down.')
        else:
            self.opened = True
            self._logger.debug('Card face up.')

    def open(self) -> None:
        """Face up the card
        """
        self.opened = True
        self._logger.debug('Card face up.')

    def hide(self) -> None:
        """Face down the card
        """
        self.opened = False
        self._logger.debug('Card face down.')

    def tap(self, side='right') -> None:
        """Tap the card to the given side

        Args:
            side (str, optional): side to tap. Defaults to 'right'.
        """
        self.tapped = True
        self.side = side
        self._logger.debug(f'Card taped to side {side}.')

    def untap(self) -> None:
        """Untap the card
        """
        self.tapped = False
        self.side = None
        self._logger.debug('Card untaped. Side set to None.')

    def alter(self) -> NoReturn:
        """Many cards have alter views. For example
        card can have main view, that apply most time of the game
        and second view, that apply only if card played as
        that alternative. For ease of understanding, consider that
        different views of the same card are not related directly
        to each other.
        """
        raise NotImplementedError
