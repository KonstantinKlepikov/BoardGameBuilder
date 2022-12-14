"""Game tools classes
"""
import random
from collections import deque
from heapq import heappop, heappush
from typing import (
    Tuple, Dict, List, Deque, Optional, Iterable, Union
        )
from dataclasses import dataclass, field, replace
from dataclasses_json import (
    config, DataClassJsonMixin, dataclass_json, Undefined
        )
from bgameb.base import Base, Component
from bgameb.items import Card, Dice, Step, BaseItem
from bgameb.errors import ArrangeIndexError, ComponentClassError


Item = Union[Card, Dice, Step]


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class BaseTool(Base, DataClassJsonMixin):
    """Base class for game tools (like decks or shakers)
    """
    current: List[Item] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def _item_replace(self, item: Item) -> Item:
        """Replace item in a current

        Returns:
            Item: an item object
        """
        return replace(item)

    def clear(self) -> None:
        """Clear the current bag
        """
        self.current.clear()
        self._logger.debug('Current clear!')

    def current_ids(self) -> List[str]:
        """Get ids of current objects

        Returns:
            List[str]: list ids of current
        """
        return [item.id for item in self.current]

    def append(self, item: Item) -> None:
        """Append item to current

        Args:
            item (Item): appended items
        """
        item = self._item_replace(item)
        self.current.append(item)
        self._logger.debug(f'To current is appended item: {item.id}')

    def count(self, item_id: str) -> int:
        """Count the number of current items with by id.

        Args:
            item_id (str: an item id

        Returns:
            int: count of items
        """
        count = self.current_ids().count(item_id)
        self._logger.debug(f'Count of {item_id} in current is {count}')
        return count

    def extend(self, items: Iterable[Item]) -> None:
        """Extend the current by appending items
        started from the left side of iterable.

        Args:
            items (Iterable[Item]): iterable with items
        """
        items = [self._item_replace(item) for item in items]
        self.current.extend(items)
        self._logger.debug(
            f'Current are extended by {[item.id for item in items]} from right'
                )

    def index(
        self,
        item_id: str,
        start: int = 0,
        end: Optional[int] = None
            ) -> int:
        """Return the position of item_id in the current
        (at or after index start and before index stop).
        Returns the first match or raises ValueError if not found.

        Args:
            item_id (str): an item id
            start (int): start index. Default to 0.
            end (int, optional): stop index. Default to None.

        Returns:
            int: index of the the first match
        """
        names = self.current_ids()
        ind = names.index(item_id, start) if end is None \
            else names.index(item_id, start, end)
        self._logger.debug(f'Index of {item_id} in current is {ind}')
        return ind

    def insert(self, item: Item, pos: int) -> None:
        """Insert item into the current at position pos.

        Args:
            item (Item): an item object
            pos (int): position
        """
        item = self._item_replace(item)
        self.current.insert(pos, item)
        self._logger.debug(f'To current is inserted {item.id} on {pos=}')

    def pop(self) -> Item:
        """Remove and return an item from the current.
        If no cards are present, raises an IndexError.

        Returns:
            Item: an item object
        """
        item = self.current.pop()
        self._logger.debug(f'{item.id} is poped from current')
        return item

    def remove(self, item_id: str) -> None:
        """Remove the first occurrence of item from current.
        If not found, raises a ValueError.
        Args:
            item_id (str): an item id
        """
        ind = self.index(item_id)
        item = self.current[ind]
        self.current.remove(item)
        self._logger.debug(f'Is removed from current {item_id}')

    def reverse(self) -> None:
        """Reverse the items of the current.
        """
        self.current.reverse()
        self._logger.debug('Current is reversed')


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Bag(BaseTool, DataClassJsonMixin):
    """Bag object
    """
    i: Component[Item] = field(default_factory=Component)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.i = Component()

    def deal(self, items: Optional[List[str]] = None) -> 'Bag':
        """Deal new bag current

        Args:
            items (Optional[List[str]]): list of items ids

        Returns:
            Bag
        """
        self.clear()

        if not items:
            for stuff in self.i.values():
                if issubclass(type(stuff), BaseItem):
                    self.append(stuff)
        else:
            for id in items:
                if id in self.i.keys():
                    self.append(self.i[id])

        self._logger.debug(f'Is deal current: {self.current_ids()}')
        return self

    def add(self, stuff: Item) -> None:
        """Add stuff to component

        Args:
            stuff (Item): game stuff
        """
        self.i._update(stuff)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Shaker(BaseTool, DataClassJsonMixin):
    """Create shaker for roll dices or flip coins
    """
    current: List[Dice] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )
    i: Component[Dice] = field(default_factory=Component)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.i = Component()

    def deal(self, items: Optional[List[str]] = None) -> 'Shaker':
        """Deal new shaker current

        Args:
            items (Optional[List[str]]): items ids

        Returns:
            Shaker
        """
        self.clear()

        if not items:
            for stuff in self.i.values():
                if issubclass(type(stuff), Dice):
                    self.append(stuff)
        else:
            for id in items:
                if id in self.i.keys():
                    self.append(self.i[id])

        self._logger.debug(f'Is deal current: {self.current_ids()}')
        return self

    def roll(self) -> Dict[str, List[int]]:
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

        for item in self.current:
            roll[item.id] = item.roll()

        self._logger.debug(f'Result of roll: {roll}')

        return roll

    def add(self, stuff: Dice) -> None:
        """Add stuff to component

        Args:
            stuff (Dice): game stuff
        """
        if isinstance(stuff.__class__, Dice) \
                or issubclass(stuff.__class__, Dice):
            self.i._update(stuff)
        else:
            raise ComponentClassError(stuff, self._logger)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Deck(BaseTool, DataClassJsonMixin):
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
    i: Component[Card] = field(default_factory=Component)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.i = Component()

    def _item_replace(self, item: Card) -> Card:  # type: ignore[override]
        """Replace item in a current

        Args:
            item (Card): a card object

        Returns:
            Card: a card object
        """
        item = replace(item)
        del item.count
        return item

    def appendleft(self, item: Card) -> None:
        """Add card to the left side of the current deck.

        Args:
            item (Card): a card object
        """
        item = self._item_replace(item)
        self.current.appendleft(item)
        self._logger.debug(f'To left of current is appended card: {item.id}')

    def extendleft(self, items: Iterable[Card]) -> None:
        """Extend the left side of the current deck by appending
        cards started from the right side of iterable.
        The series of left appends results in reversing the order
        of cards in the iterable argument.

        Args:
            items (Iterable[Card]): iterable with cards
        """
        items = [self._item_replace(item) for item in items]
        self.current.extendleft(items)
        self._logger.debug(
            f'Current are extended by {[item.id for item in items]} from left'
                )

    def popleft(self) -> Card:
        """Remove and return a card from the left side of the current deck.
        If no cards are present, raises an IndexError.

        Returns:
            Card: a card object
        """
        item = self.current.popleft()
        self._logger.debug(f'{item.id} is poped from left of current')
        return item

    def rotate(self, n: int) -> None:
        """Rotate the current deck n steps to the right.
        If n is negative, rotate to the left.

        Args:
            n (int): steps to rotation
        """
        self.current.rotate(n)
        self._logger.debug(f'Current is rotate by {n}')

    def deal(self, items: Optional[List[str]] = None) -> 'Deck':
        """Deal new deck current

        Args:
            items (Optional[List[str]]): list of cards ids

        Returns:
            Deck
        """
        self.clear()

        if not items:
            for stuff in self.i.values():
                if issubclass(type(stuff), Card):
                    for _ in range(stuff.count):
                        self.append(stuff)
        else:
            for id in items:
                if id in self.i.keys():
                    self.append(self.i[id])

        self._logger.debug(f'Is deal current: {self.current_ids()}')
        return self

    def shuffle(self) -> 'Deck':
        """Random shuffle current deck

        Returns:
            Deck
        """
        random.shuffle(self.current)
        self._logger.debug(f'Is shuffled: {self.current}')
        return self

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
            ) -> 'Deck':
        """Concatenate new current deck from given arranged list and last of
        deck. Use to_arrange() method to get list to arrange and last.

        Args:
            arranged (List[Card]): arranged list of cards
            last: (Tuple[List[Card], List[Card]]): last of deck

        Returns:
            Deck
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
        return self

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

    def add(self, stuff: Card) -> None:
        """Add stuff to component

        Args:
            stuff (Card): game stuff
        """
        if isinstance(stuff.__class__, Card) \
                or issubclass(stuff.__class__, Card):
            self.i._update(stuff)
        else:
            raise ComponentClassError(stuff, self._logger)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Steps(BaseTool, DataClassJsonMixin):
    """Game steps order object

    Attr:
        - current (List[Tuple[int, Step]]): current order of steps.
        - last (Step): last pulled from current step
    """
    current: List[Tuple[int, Step]] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
            )
    last: Step = field(
        default=None,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
    )
    i: Component[Step] = field(default_factory=Component)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.i = Component()

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
        self.last = heappop(self.current)[1]
        return self.last

    def deal(
        self,
        items: Optional[List[str]] = None
            ) -> 'Steps':
        """Clear current order and create new current order

        Args:
            items (Optional[List[str]]): list of stuff ids

        Returns:
            Steps
        """
        self.clear()

        if not items:
            for stuff in self.i.values():
                if issubclass(type(stuff), Step):
                    self.push(stuff)
        else:
            for id in items:
                if id in self.i.keys():
                    self.push(self.i[id])

        self._logger.debug(f'Is deal current: {self.current_ids()}')
        return self

    def current_ids(self) -> List[str]:
        """Get ids of current objects

        Returns:
            List[str]: list ids of current
        """
        return [item[1].id for item in self.current]

    def add(self, stuff: Step) -> None:
        """Add stuff to component

        Args:
            stuff (Step): game stuff
        """
        if isinstance(stuff.__class__, Step) \
                or issubclass(stuff.__class__, Step):
            self.i._update(stuff)
        else:
            raise ComponentClassError(stuff, self._logger)
