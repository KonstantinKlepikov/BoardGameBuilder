"""Game tools classes like shakers or decks
"""
import random
from collections import deque
from typing import Optional, Tuple, Dict, Literal, List, Deque
from dataclasses import dataclass, field
from bgameb.stuff import Roller, Card, BaseStuff
from bgameb.constructs import BaseTool


@dataclass
class Shaker(BaseTool):
    """Create shaker for roll dices or flip coins
    """
    name: Optional[str] = None
    last: Dict[str, Tuple[int]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.last = {}
        self._stuff_to_add = Roller

    def roll(self) -> Dict[str, Tuple[int]]:
        """Roll all stuff with shaker and return results

        Return:
            Dict[str, Tuple[int]]: result of roll

        .. code-block::
            :caption: Example:

                {
                    "six_dice": (5, 3, 2, 5),
                    "twenty_dice": {2, 12, 4},
                }
        """
        roll = {}

        for name, roller in self.stuff.items():
            roll[name] = roller.roll()

        self.last = roll
        self.logger.debug(f'Result of roll: {roll}')

        return self.last


@dataclass
class Deck(BaseTool):
    """Create deck for cards

    You can add cards, define it counts and deal a deck.
    Result is saved in dealt attr as deque object. This object
    has all methods of
    `python deque
    <https://docs.python.org/3/library/collections.html#deque-objects>`_

    .. code-block::
        :caption: Example:

            deque(Card1, Card3, Card2, Card4)

    """
    name: Optional[str] = None
    dealt: Deque[BaseStuff] = field(
        default_factory=deque,
        init=False,
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Card
        self.dealt = deque()

    def deal(self) -> List[str]:
        """Deal new random shuffled deck and save it to
        self.dealt: List[str]
        """
        self.clear()
        for val in self.stuff.values():
            for _ in range(val.count):
                self.dealt.append(self._stuff_to_add(**val.to_dict()))
        self.shuffle()
        self.logger.debug(f'Is dealt cards: {self.dealt}')

    def shuffle(self) -> None:
        """Shuffle dealt deck
        """
        random.shuffle(self.dealt)
        self.logger.debug(f'Is shuffled: {self.dealt}')

    def arrange(self) -> None:
        """Arrange  cards in dealt deck
        """

    def search(self, name: str) -> None:
        """Search for cards in dealt deck

        Args:
            name (str): name of card
        """
        raise NotImplementedError

    def move(self) -> None:
        """Move stuff from this dealt deck to another
        """
        raise NotImplementedError

    def clear(self) -> None:
        """Clean dealt deack
        """
        self.dealt.clear()


TOOLS = {
    'shaker': Shaker,
    'deck': Deck,
}
TOOLS_TYPES = Literal['roller', 'card']
