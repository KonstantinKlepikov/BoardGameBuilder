"""Game tools classes like shakers or decks
"""
from typing import Optional, Tuple, Dict, Literal
from dataclasses import dataclass, field
from bgameb.stuff import Roller, Card
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
    """
    name: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Card

    def deal(self) -> None:
        """Deal deck for play from deck_cards
        """
        raise NotImplementedError

    def shuffle(self) -> None:
        """Shuffle in/out deal_cards
        """
        raise NotImplementedError

    def arrange(self) -> None:
        """Arrange in/out deal_cards
        """

    def look(self) -> None:
        """Look cards in in/out deal_cards
        """
        raise NotImplementedError

    def pop(self) -> None:
        """Pop cards from in to out or visa versa
        """
        raise NotImplementedError

    def search(self, name: str) -> None:
        """Search for cards in in/out deal_cards

        Args:
            name (str): name of card
        """
        raise NotImplementedError

    def move(self) -> None:
        """Move stuffs from this deck toi another
        """
        raise NotImplementedError


TOOLS = {
    'shaker': Shaker,
    'deck': Deck,
}
TOOLS_TYPES = Literal['roller', 'card']
