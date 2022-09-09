"""Game dices, coins, cards and other stuffs
"""
import random
from typing import List, Optional, Any
from dataclasses import dataclass, field
from abc import ABC
from dataclasses_json import DataClassJsonMixin, config
from bgameb.errors import RollerSidesError
from bgameb.utils import log_me, get_random_name


@dataclass
class BaseStuff(DataClassJsonMixin, ABC):
    """Base class for stuff
    """
    name: Optional[str] = None

    def __post_init__(self) -> None:
        # set random name
        if not self.name:
            self.name = get_random_name()


@dataclass
class BaseRoller(BaseStuff, ABC):
    """Base class for rollers or fliped objects

    Define name to identify later BaseRoller object by unique name.
    For example: 'six_side_dice'

    .. code-block::
        :caption: Example:

            dice = Dice(name='six_side_dice', sides=12)
    """
    name: Optional[str] = None
    sides: Optional[int] = field(default=None, init=False)
    _range: List[int] = field(
        default_factory=list, init=False, metadata=config(exclude=lambda x:True)
        )

    def __post_init__(self) -> None:
        super().__post_init__()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)

    def roll(self) -> int:
        """Roll or flip and return result

        Raises:
            RollerSidesError: is not defined number of sides

        Returns:
            int: result of roll
        """
        if self.sides:
            choice = random.choices(self._range, k=1)[0]
            self.logger.debug(f'Is rolled {choice=}')
            return choice
            # TODO: add weights
            # https://docs.python.org/dev/library/random.html#random.choices

        else:
            self.logger.debug(
                f'Is not defined number of sizes for {self.name}'
                )
            raise RollerSidesError(
                f'Is not defined number of sizes for {self.name}'
                )


@dataclass
class Dice(BaseRoller):
    """Create dice

    You can define number of sides for dice.
    Default 6
    """
    sides: int = 6

    def __post_init__(self) -> None:
        super().__post_init__()

        if not isinstance(self.sides, int):
            self.logger.debug(
                f'Is not defined number of sizes for {self.name}'
                )
            raise RollerSidesError(
                f'Is not defined number of sizes for dice {self.name}'
                )
        else:
            self._range = list(range(1, self.sides + 1))

        self.logger.info(f'Dice created with {self.sides} sides.')


@dataclass
class Coin(BaseRoller):
    """Create coin like a dice with two sides
    """

    def __post_init__(self) -> None:
        super().__post_init__()

        self.sides = 2
        self._range = list(range(1, 3))

        self.logger.info(f'Coin created with {self.sides} sides.')


class CardTexts(dict):
    """Cards texts collection
    """
    def __init__(self, /, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def __getattr__(self, attr: str) -> str:
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr: str, value: str) -> None:
        self[attr] = value

    def __delattr__(self, attr: str) -> None:
        del self[attr]

    def __repr__(self):
        items = (f"{k}={v!r}" for k, v in self.items())
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __eq__(self, other: Any) -> bool:
        if isinstance(self, dict) and isinstance(other, dict):
            return self.__dict__ == other.__dict__
        return NotImplemented


@dataclass
class BaseCard(BaseStuff, ABC):
    """Base class for cards
    """


@dataclass
class Card(BaseCard):
    """Create the card
    """
    open: bool = False
    tapped: bool = False
    side: Optional[str] = None
    text: CardTexts = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

        self.text = CardTexts()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(f'Card created.')

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

