"""Game dices, coins, cards and other stuffs
"""
import random
from typing import List, Optional, Literal
from dataclasses import dataclass, field
from dataclasses_json import config
from bgameb.constructs import BaseStuff
from bgameb.errors import StuffDefineError


@dataclass
class RollerType(BaseStuff):
    """Base class for define types of rollers or fliped objects

    If name isn't given - it is randomly generated.

    Define name to identify later this object by unique name.
    For example: 'six_side_dice'

    Sides attr define number of sides of roller. Default to 2.
    Sides can't be less than 2, because one-sided roller is
    strongly determined and 0zero-sided is imposible.

    .. code-block::
        :caption: Example:

            dice = RollerType(name='coin', sides=2)

    Raises:
        StuffDefineError: number of sides less than 2
    """
    name: Optional[str] = None
    sides: int = 2

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.sides < 2:
            raise StuffDefineError(
                message=f'Number of sides={self.sides} '
                        f'for {self.name}. Needed >= 2.',
                logger=self.logger
                )


@dataclass
class Roller(RollerType):
    """Creare the roller (like dice or coin)
    """
    _range: List[int] = field(
        default_factory=list,
        init=False,
        metadata=config(exclude=lambda x: True),
        repr=False
        )
    count: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()
        self._range = list(range(1, self.sides + 1))

    def roll(self) -> List[int]:
        """Roll and return result

        Returns:
            List[int]: result of roll
        """
        roll = [random.choices(self._range, k=1)[0] for _ in list(range(self.count))]
        self.logger.debug(f'Is rolled {roll=}')
        return roll


@dataclass
class CardType(BaseStuff):
    """Create the card

    If name isn't given - it is randomly generated.

    Define name to identify later this object by unique name.
    For example: 'unique_card'

    .. code-block::
        :caption: Example:

            card = CardType(name='unique_card')
    """
    name: Optional[str] = None
    open: bool = False
    tapped: bool = False
    side: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass
class Card(CardType):
    """Create the card
    """

    def __post_init__(self) -> None:
        super().__post_init__()

    def flip(self) -> None:
        """Face up or face down the card regardles of it condition
        """
        if self.open:
            self.open = False
            self.logger.debug(f'Card face down.')
        else:
            self.open = True
            self.logger.debug(f'Card face up.')

    def face_up(self) -> None:
        """Face up the card and return text
        """
        self.open = True
        self.logger.debug(f'Card face up.')

    def face_down(self) -> None:
        """Face down the card
        """
        self.open = False
        self.logger.debug(f'Card face down.')

    def tap(self, side='right') -> None:
        """Tap the card to the given side
        """
        self.tapped = True
        self.side = side
        self.logger.debug(f'Card taped to side {side}.')

    def untap(self) -> None:
        """Untap the card
        """
        self.tapped = False
        self.logger.debug(f'Card untaped.')

    def alter(self) -> None:
        """Many cards have alter views. For example
        card can have main view, that apply most time of the game
        and second view, that apply only if card played as
        that alternative. For ease of understanding, consider that
        different views of the same card are not related directly
        to each other.
        """
        raise NotImplementedError

    def attach(self) -> None:
        """Some rules can attach any stuff to card
        """
        raise NotImplementedError


STUFF = {
    'roller': RollerType,
    'card': CardType,
}
STUFF_TYPES = Literal['roller', 'card']
