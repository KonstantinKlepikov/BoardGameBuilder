"""Game tools classes
"""
import random
from collections import deque
from heapq import heappop, heappush
from typing import Tuple, Dict, List, Deque
from dataclasses import dataclass, field, replace
from dataclasses_json import config, dataclass_json
from bgameb.base import Base
from bgameb.markers import Step
from bgameb.items import Card, Dice
from bgameb.errors import ArrangeIndexError
from bgameb.types import MARKERS_ITEMS


@dataclass_json
@dataclass(repr=False)
class BaseTool(Base):
    """Base class for game tools (like decks or shakers)
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        self._types_to_add = MARKERS_ITEMS


@dataclass_json
@dataclass(repr=False)
class Shaker(BaseTool):
    """Create shaker for roll dices or flip coins
    """

    def __post_init__(self) -> None:
        super().__post_init__()

    def roll(self) -> Dict[str, Tuple[int]]:
        """Roll all stuff in shaker and return results

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

        for comp in self:
            if isinstance(self[comp], Dice):
                roll[self[comp].id] = self[comp].roll()

        self._logger.debug(f'Result of roll: {roll}')

        return roll


@dataclass_json
@dataclass(repr=False)
class Deck(BaseTool):
    """Deck object

    Deck ia a Bag subclass that contains Cards for
    define curent game deque.

    You can add cards, define it counts and deal a deck.
    Result is saved in current deck attr as deque object. This object
    has all methods of
    `python deque
    <https://docs.python.org/3/library/collections.html#deque-objects>`_

    .. code-block::
        :caption: Example:

            deque(Card1, Card3, Card2, Card4)
    """
    current: Deque[Card] = field(
        default_factory=deque,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def deal(self) -> Deque[Card]:
        """Deal new random shuffled deck and save it to
        self.current
        """
        self.current.clear()

        for comp in self:
            if isinstance(self[comp], Card):
                for _ in range(self[comp].count):
                    card = replace(self[comp])
                    card.count = 1
                    self.current.append(self[comp])

        self.shuffle()
        self._logger.debug(f'Is deal cards: {self.current}')
        return self.current

    def shuffle(self) -> Deque[Card]:
        """Random shuffle current deck
        """
        random.shuffle(self.current)
        self._logger.debug(f'Is shuffled: {self.current}')
        return self.current

    def to_arrange(
        self,
        start: int,
        end: int
            ) -> Tuple[
                List[Card],
                Tuple[List[Card], List[Card]]
                    ]:
        """Prepare current deck to arrange

        Args:
            start (int): start of slice
            end (int): end of slice

        Start and end cant be less than 0 and end must be greater than start.
        Arranged deck are splited to two part - center (used for arrange part
        of deck) and tupple with last part of deck. You can rearrange center
        part and then concatenate it with last part in new deque by arrange()
        method.

        Return:
            Tuple[List[Card], Tuple[List[Card]]: part to arrange
        """
        if start < 0 or end < 0 or end < start:
            raise ArrangeIndexError(
                message=f'Nonpositive or broken {start=} or {end=}',
                logger=self._logger
                )
        to_split = list(self.current)
        splited = (to_split[start:end], (to_split[0:start], to_split[end:]))
        self._logger.debug(f'To arrange result: {splited}')

        return splited

    def arrange(
        self,
        arranged: List[Card],
        last: Tuple[List[Card], List[Card]]
            ) -> Deque[Card]:
        """Concatenate new current deck from given arranged list and last of
        deck. Use to_arrange() method to get list to arrange and last.

        Args:
            arranged (List[Card]): arranged list of cards
            last: (Tuple[List[Card], List[Card]]): last of deck
        """
        reorranged: Deque = deque()
        reorranged.extend(last[0])
        reorranged.extend(arranged)
        reorranged.extend(last[1])

        if len(reorranged) == len(self.current):
            self.current = reorranged
            self._logger.debug(f'Arrange result: {reorranged}')
        else:
            raise ArrangeIndexError(
                f'Wrong to_arranged parts: {arranged=}, {last=}',
                logger=self._logger
                )
        return self.current

    def search(
        self,
        query: Dict[str, int],
        remove: bool = True
            ) -> List[Card]:
        """Search for cards in current deck

        Args:
            query (Dict[str, int]): dict with id of searched
                                    cards and count of searching
            remove (bool): if True - remove searched cards from
                           current deck. Default to True.

        Return:
            List[Card]: list of find cards

        .. code-block::
            :caption: Example:

                game.deck1.search(
                    {'card1': 2,
                     'card2': 1 },
                    remove=False
                    )
        """
        for_deque: Deque = deque()
        result = []

        while True:
            try:
                card = self.current.popleft()
                if card.id in query.keys() and query[card.id] > 0:
                    result.append(card)
                    query[card.id] -= 1
                    if not remove:
                        for_deque.append(card)
                else:
                    for_deque.append(card)
            except IndexError:
                break
        self.current = for_deque
        self._logger.debug(f'Search result: {result}')

        return result

    def get_random(
        self,
        count: int = 1,
        remove: bool = True
            ) -> List[Card]:
        """Get random cards from current deck

        Args:
            count (int, optional): count of random cards. Defaults to 1.
            remove (bool, optional): if True - remove random cards from
                                     current deck. Default to True.

        Returns:
            List[Card]: list of random cards
        """
        if not self.current:
            self._logger.debug(
                'Is empty current deck. Random cards not choosed.'
                    )
            return []
        if not remove:
            result = random.choices(self.current, k=count)
            self._logger.debug(
                f'Random choised cards without remove: {result}'
                    )
            return result
        else:
            result = []
            for _ in range(count):
                if self.current:
                    choice = random.choice(self.current)
                    result.append(choice)
                    self.current.remove(choice)
                else:
                    break
            self._logger.debug(
                f'Random choised cards with remove: {result}'
                    )
            return result


@dataclass_json
@dataclass
class Order:
    """Order of steps priority queue. Isnt tradesafe.
    Is used only for define game steps order.

    Attr:
        - current List[Tuple[int, Component]]: priority queue list
    """
    current: List[Tuple[int, Step]] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )

    def __len__(self) -> int:
        """Len of queue

        Returns:
            int: len of current queue
        """
        return len(self.current)

    def clear(self) -> None:
        """Clear the current queue
        """
        self.current = []

    def put(self, item) -> None:
        """Put Step object to queue

        Args:
            item (Step): Step class instance
        """
        heappush(self.current, (item.priority, item))

    def get(self) -> Step:
        """Get Sеep object from queue with lowest priority

        Returns:
            Step: Step instance object
        """
        return heappop(self.current)[1]


@dataclass_json
@dataclass(repr=False)
class Steps(BaseTool):
    """Game steps order object

    Attr:
        - current (Order): current order of steps.
    """
    current: Order = field(
        default_factory=Order,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def deal(self) -> Order:
        """Clear current order and create new current order
        """
        self.current.clear()

        for comp in self:
            if isinstance(self[comp], Step):
                step = replace(self[comp])
                self.current.put(step)
        self._logger.debug(f'Is deal order of turn: {self.current.current}')
        return self.current
