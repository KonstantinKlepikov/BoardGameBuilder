"""Game dices, coins, cards and other stuffs
"""
import random
from abc import ABC
from typing import List, Optional
from dataclasses import dataclass, field
from dataclasses_json import config
from bgameb.constructs import BaseStuff, CardTexts
from bgameb.errors import StuffDefineError


@dataclass
class BaseRoller(BaseStuff, ABC):
    """Base class for rollers or fliped objects

    Inherited classes needs attr name implementation

    Define name to identify later BaseRoller object by unique name.
    For example: 'six_side_dice'

    .. code-block::
        :caption: Example:

            dice = Dice(name='six_side_dice', sides=12)
    """
    name: Optional[str] = None
    sides: int = 0
    _range: List[int] = field(
        default_factory=list,
        init=False,
        metadata=config(exclude=lambda x: True),
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.sides <= 0:
            raise StuffDefineError(
                message=f'Number {self.sides=} for {self.name}. Needed > 0.',
                logger=self.logger
                )
        else:
            self._range = list(range(1, self.sides + 1))

    def roll(self) -> int:
        """Roll or flip and return result

        Raises:
            StuffDefineError: is not defined number of sides

        Returns:
            int: result of roll
        """
        if self.sides:
            choice = random.choices(self._range, k=1)[0]
            self.logger.debug(f'Is rolled {choice=}')
            return choice

        else:
            raise StuffDefineError(
                message=f'Number {self.sides=} for {self.name}. Needed > 0.',
                logger=self.logger
                )


@dataclass
class Dice(BaseRoller):
    """Create dice

    You can define number of sides for dice.
    Default 6
    """
    name: Optional[str] = None
    sides: int = 6

    def __post_init__(self) -> None:
        super().__post_init__()
        self.logger.info(f'Dice {self.sides=}.')


@dataclass
class Coin(BaseRoller):
    """Create coin like a dice with two sides
    """
    name: Optional[str] = None

    def __post_init__(self) -> None:
        self.sides = 2
        self._range = list(range(1, 3))

        super().__post_init__()
        self.logger.info(f'Coin {self.sides=}.')


# class CardTexts(dict):
#     """Cards texts collection
#     """
#     def __init__(self, **kwargs) -> None:
#         self.__dict__.update(kwargs)

#     def __getattr__(self, attr: str) -> str:
#         try:
#             return self[attr]
#         except KeyError:
#             raise AttributeError(attr)

#     def __setattr__(self, attr: str, value: str) -> None:
#         self[attr] = value

#     def __delattr__(self, attr: str) -> None:
#         del self[attr]

#     def __repr__(self):
#         items = (f"{k}={v!r}" for k, v in self.items())
#         return "{}({})".format(type(self).__name__, ", ".join(items))

#     def __eq__(self, other: Any) -> bool:
#         if isinstance(self, dict) and isinstance(other, dict):
#             return self.__dict__ == other.__dict__
#         return NotImplemented


@dataclass
class BaseCard(BaseStuff, ABC):
    """Base class for cards
    """


@dataclass
class Card(BaseCard):
    """Create the card
    """
    name: Optional[str] = None
    open: bool = False
    tapped: bool = False
    side: Optional[str] = None
    text: CardTexts = field(default_factory=CardTexts, init=False)

    def __post_init__(self) -> None:
        self.text = CardTexts()
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

    def face_up(self) -> CardTexts:
        """Face up the card and return text
        """
        self.open = True
        self.logger.debug(f'Card face up.')
        return self.text

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









@dataclass
class RollerType(BaseStuff):
    """Base class for define types of rollers or fliped objects

    If name isn't given - it is randomly generated.

    Define name to identify later this object by unique name.
    For example: 'six_side_dice'

    Sides attr define number of sides of roller. Default to 2.
    Sides cant be less than 2, because one-sided roller is
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

    _range: List[int] = field(
        default_factory=list,
        init=False,
        metadata=config(exclude=lambda x: True),
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()
        self._range = list(range(1, self.sides + 1))

    def roll(self) -> int:
        """Roll and return result

        Returns:
            int: result of roll
        """
        choice = random.choices(self._range, k=1)[0]
        self.logger.debug(f'Is rolled {choice=}')
        return choice


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
class _Card(CardType):
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

    def face_up(self) -> CardTexts:
        """Face up the card and return text
        """
        self.open = True
        self.logger.debug(f'Card face up.')
        return self.text

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
