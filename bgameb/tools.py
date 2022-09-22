"""Game tools classes like shakers or decks
"""
import random
from collections import deque
from typing import Optional, Tuple, Dict, Literal, List, Deque
from dataclasses import dataclass, field
from bgameb.stuff import Roller, Card, BaseStuff
from bgameb.constructs import BaseTool
from bgameb.errors import ArrangeIndexError


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

    def __getitem__(self, key: int) -> BaseStuff:
        """Вefines access by key to dealt deck

        Args:
            key (int): index number

        Returns:
            BaseStuff: stuff from dealt object
        """
        return self.dealt[key]

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

    def to_arrange(
        self, start: int, end: int
            ) -> Tuple[List[BaseStuff], Tuple[List[BaseStuff]]]:
        """Prepare dealt deck to arrange

        Args:
            start (int): start of slice
            end (int): end of slice

        Start and end cant be less than 0 and end must be greater than start.
        Arranged deck are splited to three part - left, center and right.
        You can rearrange center part and concatenate that in new deque
        by arrange() method.

        Return:
            Tuple[List[BaseStuff], Tuple[List[BaseStuff]]]: part to arrange
        """
        if start < 0 or end < 0 or end < start:
            raise ArrangeIndexError(
                message=f'Nonpositive or broken {start=} or {end=}',
                logger=self.logger
                )
        to_split = list(self.dealt)
        splited = (to_split[start:end], (to_split[0:start], to_split[end:]))
        self.logger.debug(f'To arrange result: {splited=}')

        return splited

    def arrange(
        self,
        arranged: List[BaseStuff],
        last: List[Deque[BaseStuff]]
            ) -> None:
        """Compone new dealt deck with given arranged list and
        last of deck. Use to_arrange() method to get liat to arrange
        and last of deck before arrange.

        Args:
            arranged (List[BaseStuff]): arranged list of cards
            last: (Deque[BaseStuff]): last of deck deque
        """
        reorranged = deque()
        reorranged.extend(last[0])
        reorranged.extend(arranged)
        reorranged.extend(last[1])

        if len(reorranged) == len(self.dealt):
            self.dealt = reorranged
            self.logger.debug(f'Arrange result: {reorranged=}')
        else:
            raise ArrangeIndexError(
                f'Wrong to_arranged parts: {arranged=}, {last=}',
                logger=self.logger
                )

    def search(self, query: Dict[str, int], remove: bool = True) -> List[Card]:
        """Search for cards in dealt deck

        Args:
            query (Dict[str, int]): dict with name of searched
                                    card and count of seartching
            remove (bool): if True - remove cards from dealt deck.
                           Default to True

        Return:
            List[Card]: list of finded cards

        .. code-block::
            :caption: Example:

                game.tools.stuff.deck1.search(
                    {'card1': 2,
                     'card2': 1 },
                    remove=False
                    )
        """
        for_deque = deque()
        result = []

        while True:
            try:
                card = self.dealt.popleft()
                if card.name in query.keys() and query[card.name] > 0:
                    result.append(card)
                    query[card.name] -= 1
                    if not remove:
                        for_deque.append(card)
                else:
                    for_deque.append(card)
            except IndexError:
                break
        self.dealt = for_deque
        self.logger.debug(f'Search result: {result}')

        return result

    def clear(self) -> None:
        """Clean dealt deack
        """
        self.dealt.clear()
        self.logger.debug(f'Dealt deck is clear')


TOOLS = {
    'shaker': Shaker,
    'deck': Deck,
}
TOOLS_TYPES = Literal['roller', 'card']
