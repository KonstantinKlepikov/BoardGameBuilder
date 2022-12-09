"""Game tools classes
"""
import random
from collections import deque
from heapq import heappop, heappush
from typing import Tuple, Dict, List, Deque, Optional, Iterable
from dataclasses import dataclass, field, replace
from dataclasses_json import config, dataclass_json
from bgameb.base import Base
from bgameb.items import Card, Dice, Step, BaseItem
from bgameb.errors import ArrangeIndexError
from bgameb.constraints import ITEMS


@dataclass_json
@dataclass(repr=False)
class BaseTool(Base):
    """Base class for game tools (like decks or shakers)
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        self._types_to_add = ITEMS


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
class Bag(BaseTool):
    """_summary_
    """
    current: List[BaseItem] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def _item_replace(self, item: BaseItem) -> BaseItem:
        """Replace item in a current
        """
        return replace(item)

    def append(self, item: BaseItem) -> List[BaseItem]:
        """_summary_

        Args:
            item (BaseItem): _description_

        Returns:
            List[BaseItem]: _description_
        """
        item = self._item_replace(item)
        self.current.append(item)
        self._logger.debug(f'To current is appended item: {item.id}')
        return self.current

    def clear(self) -> None:
        """Clear the current bag
        """
        self.current.clear()
        self._logger.debug('Bag is clear')

    def count(self, item_id: str) -> int:
        """Count the number of current bag items with by id.

        Args:
            item_id (str: an item id

        Returns:
            int: count of items
        """
        count = self.get_current_ids().count(item_id)
        self._logger.debug(f'Count of {item_id} in current is {count}')
        return count

    def get_current_ids(self) -> List[str]:
        """Get ids of current items

        Returns:
            List[str]: list ids in current attribut of tool
        """
        return [obj.id for obj in self.current]

    def extend(self, items: Iterable[BaseItem]) -> List[BaseItem]:
        """Extend the the current deck by appending items
        started from the left side of iterable.

        Args:
            items (Iterable[Card]): iterable with items

        Returns:
            List[BaseItem]: current bag
        """
        items = [self._item_replace(item) for item in items]
        self.current.extend(items)
        self._logger.debug(
            f'Current are extended by {[item.id for item in items]} from right'
                )
        return self.current

    def index(
        self,
        item_id: str,
        start: int = 0,
        end: Optional[int] = None
            ) -> int:
        """Return the position of item_id in the current deck
        (at or after index start and before index stop).
        Returns the first match or raises ValueError if not found.

        Args:
            item_id (str): an item id
            start (int): start index. Default to 0.
            end (int, optional): stop index. Default to None.

        Returns:
            int: index of the the first match
        """
        names = self.get_current_ids()
        ind = names.index(item_id, start) if end is None \
            else names.index(item_id, start, end)
        self._logger.debug(f'Index of {item_id} in current is {ind}')
        return ind

    def insert(self, item: BaseItem, pos: int) -> List[BaseItem]:
        """Insert item into the current bag at position pos.

        Args:
            item (BaseItem): an item object
            pos (int): position

        Returns:
            List[BaseItem]: current bag
        """
        item = self._item_replace(item)
        self.current.insert(pos, item)
        self._logger.debug(f'To current is inserted {item.id} on {pos=}')
        return self.current

    def pop(self) -> BaseItem:
        """Remove and return an item from the current bag.
        If no cards are present, raises an IndexError.

        Returns:
            BaseItem: an item object
        """
        item = self.current.pop()
        self._logger.debug(f'{item.id} is poped from current')
        return item

    def remove(self, item_id: str) -> List[BaseItem]:
        """Remove the first occurrence of item from current bag.
        If not found, raises a ValueError.
        Args:
            item_id (str): an item id

        Returns:
            List[BaseItem]: current bag
        """
        ind = self.index(item_id)
        item = self.current[ind]
        self.current.remove(item)
        self._logger.debug(f'Is removed from current {item_id}')
        return self.current

    def reverse(self) -> List[BaseItem]:
        """Reverse the items of the current bag.

        Returns:
            List[BaseItem]: current bag
        """
        self.current.reverse()
        self._logger.debug('Current is reversed')
        return self.current

    def deal(self, items: Optional[List[str]] = None) -> List[BaseItem]:
        """Deal new bag and save it to current

        Args:
            items (Optional[List[str]]): list of items ids
        """
        self.current.clear()

        # FIXME: ambiculous
        if not items:

            for comp in self:
                if issubclass(type(self[comp]), BaseItem):
                    self.append(self[comp])

        else:

            for name in items:
                for comp in self:
                    if issubclass(type(self[comp]), BaseItem) \
                            and self[comp].id == name:
                        self.append(self[comp])
                        break

        self._logger.debug(f'Is deal cards: {self.current}')
        return self.current


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

    Attr:
        - current (Deque[Card]): current cards deque.

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

    def _item_replace(self, item: Card) -> Card:
        """Replace item in a current

        Args:
            item (Card): a card object

        Returns:
            Card: a card object
        """
        item = replace(item)
        del item.count
        return item

    def append(self, item: Card) -> Deque[Card]:
        """Add card to the right side of the current deck.

        Args:
            item (Card): a card object

        Returns:
            Deque[Card]: current deck
        """
        item = self._item_replace(item)
        self.current.append(item)
        self._logger.debug(f'To right of current is appended card: {item.id}')
        return self.current

    def appendleft(self, item: Card) -> Deque[Card]:
        """Add card to the left side of the current deck.

        Args:
            item (Card): a card object

        Returns:
            Deque[Card]: current deck
        """
        item = self._item_replace(item)
        self.current.appendleft(item)
        self._logger.debug(f'To left of current is appended card: {item.id}')
        return self.current

    def clear(self) -> None:
        """Clear the current deck
        """
        self.current.clear()
        self._logger.debug('Deck is clear')

    def count(self, item_id: str) -> int:
        """Count the number of current deck cards with card id.

        Args:
            item_id (str: a card id

        Returns:
            int: count of cards
        """
        count = self.get_current_ids().count(item_id)
        self._logger.debug(f'Count of {item_id} in current is {count}')
        return count

    def extend(self, items: Iterable[Card]) -> Deque[Card]:
        """Extend the right side of the current
        deck by appending cards started from the left side of iterable.

        Args:
            items (Iterable[Card]): iterable with cards

        Returns:
            Deque[Card]: current deck
        """
        items = [self._item_replace(item) for item in items]
        self.current.extend(items)
        self._logger.debug(
            f'Current are extended by {[item.id for item in items]} from right'
                )
        return self.current

    def extendleft(self, items: Iterable[Card]) -> Deque[Card]:
        """Extend the left side of the current deck by appending
        cards started from the right side of iterable.
        The series of left appends results in reversing the order
        of cards in the iterable argument.

        Args:
            items (Iterable[Card]): iterable with cards

        Returns:
            Deque[Card]: current deck
        """
        items = [self._item_replace(item) for item in items]
        self.current.extendleft(items)
        self._logger.debug(
            f'Current are extended by {[item.id for item in items]} from left'
                )
        return self.current

    def index(
        self,
        item_id: str,
        start: int = 0,
        end: Optional[int] = None
            ) -> int:
        """Return the position of item_id in the current deck
        (at or after index start and before index stop).
        Returns the first match or raises ValueError if not found.

        Args:
            item_id (str): a card id
            start (int): start index. Default to 0.
            end (int, optional): stop index. Default to None.

        Returns:
            int: index of the the first match
        """
        names = self.get_current_ids()
        ind = names.index(item_id, start) if end is None \
            else names.index(item_id, start, end)
        self._logger.debug(f'Index of {item_id} in current is {ind}')
        return ind

    def insert(self, item: Card, pos: int) -> Deque[Card]:
        """Insert card into the current deck at position pos.

        If the insertion would cause deck to grow beyond maxlen,
        an IndexError is raised.

        Args:
            item (Card): a card object
            pos (int): position

        Returns:
            Deque[Card]: current deck
        """
        item = self._item_replace(item)
        self.current.insert(pos, item)
        self._logger.debug(f'To current is inserted {item.id} on {pos=}')
        return self.current

    def pop(self) -> Card:
        """Remove and return a card from the right side of the current deck.
        If no cards are present, raises an IndexError.

        Returns:
            Card: a card object
        """
        item = self.current.pop()
        self._logger.debug(f'{item.id} is poped from right of current')
        return item

    def popleft(self) -> Card:
        """Remove and return a card from the left side of the current deck.
        If no cards are present, raises an IndexError.

        Returns:
            Card: a card object
        """
        item = self.current.popleft()
        self._logger.debug(f'{item.id} is poped from left of current')
        return item

    def remove(self, item_id: str) -> Deque[Card]:
        """Remove the first occurrence of card from current deck.
        If not found, raises a ValueError.
        Args:
            item_id (str): a card id

        Returns:
            Deque[Card]: current deck
        """
        ind = self.index(item_id)
        item = self.current[ind]
        self.current.remove(item)
        self._logger.debug(f'Is removed from current {item_id}')
        return self.current

    def reverse(self) -> Deque[Card]:
        """Reverse the cards of the current deck.

        Returns:
            Deque[Card]: current deck
        """
        self.current.reverse()
        self._logger.debug('Current is reversed')
        return self.current

    def rotate(self, n: int) -> Deque[Card]:
        """Rotate the current deck n steps to the right.
        If n is negative, rotate to the left.

        Args:
            n (int): steps to rotation

        Returns:
            Deque[Card]: _description_
        """
        self.current.rotate(n)
        self._logger.debug(f'Current is rotate by {n}')
        return self.current

    def deal(self, items: Optional[List[str]] = None) -> Deque[Card]:
        """Deal new deck and save it to current

        Args:
            items (Optional[List[str]]): list of cards ids
        """
        self.current.clear()

        # FIXME: ambiculous
        if not items:

            for comp in self:
                if isinstance(self[comp], Card):
                    for _ in range(self[comp].count):
                        self.append(self[comp])

        else:

            names = self.get_names()
            used: Dict[str, Card] = {}

            for name in items:
                if name in names:
                    if not used.get(name):
                        for comp in self:
                            if isinstance(self[comp], Card) \
                                    and self[comp].id == name:
                                self.append(self[comp])
                                used[name] = self[comp]
                                break
                    else:
                        self.append(self[comp])

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
            Tuple[List[Card], Tuple[List[Card]]: parts to arrange
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

    def get_current_ids(self) -> List[str]:
        """Get ids of current objects

        Returns:
            List[str]: list ids in current attribut of tool
        """
        return [obj.id for obj in self.current]


@dataclass_json
@dataclass(repr=False)
class Steps(BaseTool):
    """Game steps order object

    Attr:
        - current (List[Tuple[int, Step]]): current order of steps.
        - current_step (Step): last pulled from current step
    """
    current: List[Tuple[int, Step]] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )
    current_step: Step = field(
        default=None,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
    )

    def __post_init__(self) -> None:
        super().__post_init__()

    def clear(self) -> None:
        """Clear the current queue
        """
        self.current = []

    def push(self, item: Step) -> None:
        """Push Step object to current

        Args:
            item (Step): Step class instance
        """
        replaced = replace(item)
        heappush(self.current, (replaced.priority, replaced))

    def pull(self) -> Step:
        """Pull Step object from current with lowest priority

        Returns:
            Step: Step instance object
        """
        self.current_step = heappop(self.current)[1]
        return self.current_step

    def deal(
        self,
        items: Optional[List[str]] = None
            ) -> List[Tuple[int, Step]]:
        """Clear current order and create new current order

        Args:
            items (Optional[List[str]]): list of stuff ids

        Returns:
            List[Tuple[int, Step]] - list of priority and steps
        """
        self.clear()

        # FIXME: ambiculous
        if not items:
            for comp in self:
                if comp != 'current_step' \
                        and isinstance(self[comp], Step):
                    self.push(self[comp])

        else:

            names = self.get_names()
            used: Dict[str, Step] = {}

            for name in items:
                if name != 'current_step' and name in names:
                    if not used.get(name):
                        for comp in self:
                            if isinstance(self[comp], Step) \
                                    and self[comp].id == name:
                                self.push(self[comp])
                                break
                    else:
                        self.push(self[comp])

        self._logger.debug(f'Is deal order of turn: {self.current}')
        return self.current

    def get_current_ids(self) -> List[str]:
        """Get ids of current objects

        Returns:
            List[str]: list ids in current attribut of tool
        """
        return [obj[1].id for obj in self.current]
