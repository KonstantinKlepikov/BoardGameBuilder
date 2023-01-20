"""Game tools classes
"""
import random
from pydantic import Field, PositiveInt
from collections import deque
from collections.abc import KeysView
from heapq import heappop, heappush
from typing import Optional, Iterable, Union, Any
from bgameb.base import Base, Component
from bgameb.items import Card, Dice, Step_, BaseItem
from bgameb.errors import ArrangeIndexError, ComponentClassError


class BaseTool(Base):
    """Base class for game tools (like decks or shakers)
    """
    c: Component[str, BaseItem] = Field(
        default_factory=Component, exclude=True, repr=False
            )
    current: list[BaseItem] = []
    last: Optional[BaseItem] = None

    class Config(Base.Config):
        json_encoders = {
            Component: lambda c: c.to_json()
                }

    @property
    def current_ids(self) -> list[str]:
        """Get ids of current objects

        Returns:
            List[str]: list ids of current
        """
        return [item.id for item in self.current]

    @property
    def last_id(self) -> Optional[str]:
        """Get id of last

        Returns:
            Optional[str]: id
        """
        if self.last is not None:
            return self.last.id
        return None

    def get_items(self) -> dict[str, BaseItem]:
        """Get items from Component

        Returns:
            dict[str, BaseItem]: items mapping
        """
        return {item.id: item for item in self.c.values()}

    def _item_replace(self, item: BaseItem) -> BaseItem:
        """Get item replaced copy

        Returns:
            Item (BaseItem): an item object
        """
        return item.__class__(**item.dict())

    def by_id(self, id: str) -> list[BaseItem]:
        """Get item from current by its id

        Args:
            id (str): item id

        Returns:
            list[BaseItem]: items
        """
        return [item for item in self.current if item.id == id]

    def clear(self) -> None:
        """Clear the current and last
        """
        self.current.clear()
        self.last = None
        self._logger.debug('Current and last clear!')

    def append(self, item: BaseItem) -> None:
        """Append item to current

        Args:
            item (Item): appended items
        """
        item = self._item_replace(item)
        self.current.append(item)
        self._logger.debug(f'To current is appended item: {item.id}')

    def count(self, item_id: str) -> int:
        """Count the number of current items with given id.

        Args:
            item_id (str: an item id

        Returns:
            int: count of items
        """
        count = self.current_ids.count(item_id)
        self._logger.debug(f'Count of {item_id} in current is {count}')
        return count

    def extend(self, items: Iterable[BaseItem]) -> None:
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
        """Return the position of item in the current
        (after index start and before index stop).
        Returns the first match or raises ValueError if not found.

        Args:
            item_id (str): an item id
            start (int): start index. Default to 0.
            end (int, optional): stop index. Default to None.

        Returns:
            int: index of the the first match
        """
        names = self.current_ids
        ind = names.index(item_id, start) if end is None \
            else names.index(item_id, start, end)
        self._logger.debug(f'Index of {item_id} in current is {ind}')
        return ind

    def insert(self, item: BaseItem, pos: int) -> None:
        """Insert item into the current at given position.

        Args:
            item (Item): an item object
            pos (int): position
        """
        item = self._item_replace(item)
        self.current.insert(pos, item)
        self._logger.debug(f'To current is inserted {item.id} on {pos=}')

    def pop(self) -> BaseItem:
        """Remove and return an item from the current.
        If no items are present, raises an IndexError.

        Returns:
            Item: an item object
        """
        self.last = self.current.pop()
        self._logger.debug(f'{self.last.id} is poped from current')
        return self.last

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
        """Reverse the items in the current.
        """
        self.current.reverse()
        self._logger.debug('Current is reversed')


class Bag(Base):
    """Bag object

    Attr:
        - c (Component[BaseItem]) - items mapping
    """
    c: Component[str, BaseItem] = Field(
        default_factory=Component, exclude=True, repr=False
            )

    class Config(Base.Config):
        json_encoders = {
            Component: lambda c: c.to_json()
                }

    def add(self, stuff: BaseItem) -> None:
        """Add stuff to Bag component

        Args:
            stuff (BaseItem): game stuff
        """
        if issubclass(stuff.__class__, BaseItem):
            self.c.update(stuff)
            self._logger.info(
                f'Component updated by stuff with id="{stuff.id}".'
                    )
        else:
            raise ComponentClassError(stuff, self._logger)


class Shaker(BaseTool):
    """Create shaker for roll dices or flip coins

    Attr:
        - c (Component[Dice]): dices mapping
        - current (Deque[Dice]): current dice deque.
        - last (Optional[Dice]): last poped from current.
        - last_roll (Optional[dict[str, list[PositiveInt]]]): last roll result.
        - last_roll_mapped (Optional[dict[str, list[Any]]]): last mapped
                                                             roll result.
    """
    c: Component[str, Dice] = Field(  # type: ignore
        default_factory=Component, exclude=True, repr=False
            )
    current: list[Dice] = []  # type: ignore
    last: Optional[Dice] = None
    last_roll: dict[str, list[PositiveInt]] = {}
    last_roll_mapped: dict[str, list[Any]] = {}

    def add(self, stuff: Dice) -> None:
        """Add dice to component

        Args:
            stuff (Dice): dice object
        """
        if isinstance(stuff.__class__, Dice) \
                or issubclass(stuff.__class__, Dice):
            self.c.update(stuff)
            self._logger.info(
                f'Component updated by stuff with id="{stuff.id}".'
                    )
        else:
            raise ComponentClassError(stuff, self._logger)

    def deal(self, items: Optional[list[str]] = None) -> 'Shaker':
        """Deal new shaker current. The current is cleared
        before deal.

        Args:
            items (Optional[List[str]]): items ids

        Returns:
            Shaker
        """
        self.clear()

        if not items:
            for stuff in self.c.values():
                self.append(stuff)
        else:
            for id in items:
                if id in self.c.ids:
                    self.append(self.c[id])

        self._logger.debug(f'Is deal current: {self.current_ids}')
        return self

    def roll(self) -> dict[str, list[int]]:
        """Roll all stuff in shaker and return results

        Return:
            Dict[str, list[int]]: result of roll

        .. code-block::
            :caption: Example:

                {
                    "six_dice": [5, 3, 2, 5],
                    "twenty_dice": [2, 12, 4],
                }
        """
        self.last_roll = {}

        for item in self.current:
            self.last_roll[item.id] = item.roll()

        self._logger.debug(f'Result of roll: {self.last_roll}')

        return self.last_roll

    def roll_mapped(self) -> dict[str, list[Any]]:
        """Roll all stuff in shaker and return mapped results.
        If any stuff unmaped - empty list returned for this item.

        Returns:
            dict[str, list[Any]]: result of roll
        """
        self.last_roll_mapped = {}

        for item in self.current:
            self.last_roll_mapped[item.id] = item.roll_mapped()

        self._logger.debug(f'Result of roll: {self.last_roll_mapped}')

        return self.last_roll_mapped


class Deck(BaseTool):
    """Deck object

    Deck contains Cards for define curent game deque.

    You can add cards, define it counts and deal a deck.
    Result is saved in current deck attr as deque object. This object
    has all methods of
    `python deque
    <https://docs.python.org/3/library/collections.html#deque-objects>`_

    Attr:
        - c (Component[Card]): components of Deck
        - current (Deque[Card]): current cards deque.
        - last (Optional[Card]): last poped from current.

    .. code-block::
        :caption: Example:

            deque(Card1, Card3, Card2, Card4)
    """
    c: Component[str, Card] = Field(  # type: ignore
        default_factory=Component, exclude=True, repr=False
            )
    current: deque[Card] = Field(default_factory=deque)  # type: ignore
    last: Optional[Card] = None

    def add(self, stuff: Card) -> None:
        """Add card to component

        Args:
            stuff (Card): Card object
        """
        if isinstance(stuff.__class__, Card) \
                or issubclass(stuff.__class__, Card):
            self.c.update(stuff)
            self._logger.info(
                f'Component updated by stuff with id="{stuff.id}".'
                    )
        else:
            raise ComponentClassError(stuff, self._logger)

    def _item_replace(self, item: Card) -> Card:  # type: ignore[override]
        """Get replaced copy of card

        Args:
            item (Card): a card object

        Returns:
            Card: a card object
        """
        item = item.__class__(**item.dict())
        item.count = 1
        return item

    def deal(self, items: Optional[list[str]] = None) -> 'Deck':
        """Deal new deck current. Cured is cleared
        before deal.

        Args:
            items (Optional[List[str]]): list of cards ids

        Returns:
            Deck
        """
        self.clear()

        if not items:
            for stuff in self.c.values():
                for _ in range(stuff.count):
                    self.append(stuff)
        else:
            for id in items:
                comp = self.c.by_id(id)
                if comp:
                    self.append(comp)

        self._logger.debug(f'Is deal current: {self.current_ids}')
        return self

    def shuffle(self) -> 'Deck':
        """Random shuffle current deck.

        Returns:
            Deck
        """
        random.shuffle(self.current)
        self._logger.debug(f'Is shuffled: {self.current_ids}')
        return self

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
        self.last = self.current.popleft()
        self._logger.debug(f'{self.last.id} is poped from left of current')
        return self.last

    def rotate(self, n: int) -> None:
        """Rotate the current deck n steps to the right.
        If n is negative, rotate to the left.

        Args:
            n (int): steps to rotation
        """
        self.current.rotate(n)
        self._logger.debug(f'Current is rotate by {n}')

    def _check_order_len(self, len_: int) -> None:
        """Check is order len valid

        Args:
            l (int): len of order of cards

        Raises:
            ArrangeIndexError: Is given empty order
            ArrangeIndexError: The len of current deque not match order len
        """
        if not len_:
            raise ArrangeIndexError(
                'Given empty order',
                logger=self._logger
                    )

        if len_ > len(self.current):
            raise ArrangeIndexError(
                f'The len of current deque is {len(self.current)} '
                f'but given order has len {len_}.',
                logger=self._logger
                    )

    def _check_is_to_arrange_valid(
        self,
        order: list[str],
        to_arrange: Union[list[str], KeysView[str]]
            ) -> None:
        """Chek is order and deque contains same elements

        Args:
            order (List[str]): ordered list of cards ids
            to_arrange (list[str]): list of deque ids

        Raises:
            ArrangeIndexError: Given card ids and deque ids not match
        """
        if set(to_arrange) ^ set(order):
            raise ArrangeIndexError(
                'Given card ids and deque ids not match.',
                logger=self._logger
                    )

    def reorder(
        self,
        order: list[str],
            ) -> 'Deck':
        """Reorder current deque from right side.

        Args:
            order (List[str]): ordered list of cards ids
            ordered from left side to right

        Returns:
            Deck
        """
        len_ = len(order)
        self._check_order_len(len_)

        to_arrange = {
            self.current[len_-ind-1].id: self.current[len_-ind-1]
            for ind in range(len_)
                }
        self._check_is_to_arrange_valid(order, to_arrange.keys())

        for _ in range(len_):
            self.pop()

        for card in order:
            self.append(to_arrange[card])

        self._logger.debug(f'Is reordered right side of deque: {order}')

        return self

    def reorderleft(
        self,
        order: list[str],
            ) -> 'Deck':
        """Reorder current deque from left side.

        Args:
            order (List[str]): ordered list of cards ids
            ordered from left side to right

        Returns:
            Deck
        """
        len_ = len(order)
        self._check_order_len(len_)

        to_arrange = {
            self.current[ind].id: self.current[ind]
            for ind in range(len_)
                }
        self._check_is_to_arrange_valid(order, to_arrange.keys())

        for _ in range(len_):
            self.popleft()

        for card in reversed(order):
            self.appendleft(to_arrange[card])

        self._logger.debug(f'Is reordered left side of deque: {order}')

        return self

    def reorderfrom(
        self,
        order: list[str],
        start: int,
            ) -> 'Deck':
        """Reorder current deque from right side started
        with given position.

        Args:
            start (int): start of reordering
            order (List[str]): ordered list of cards ids
            ordered from right side to left

        Returns:
            Deck
        """
        len_ = len(order)
        self._check_order_len(len_)
        if start <= 0 or start > len(self.current)-len_:
            raise ArrangeIndexError(
                'Given range is out of current index.',
                logger=self._logger
                    )

        old_deck = list(self.current)
        to_arrange = {
            card.id: card
            for card in old_deck[start:start+len_]
                }
        self._check_is_to_arrange_valid(order, to_arrange.keys())

        for ind1, ind2 in enumerate(range(start, start+len_)):
            self.current[ind2] = to_arrange[order[ind1]]

        return self

    def search(
        self,
        query: dict[str, int],
        remove: bool = True
            ) -> list[Card]:
        """Search for cards in current by its id.

        Args:
            query (Dict[str, int]): dict with id of searched
                                    cards and count of searching
            remove (bool): if True - remove searched cards from
                           current deck. Default to True.

        Return:
            List[Card]: list of find cards, equal searching count

        .. code-block::
            :caption: Example:

                game.deck1.search(
                    {'card1': 2,
                     'card2': 1 },
                    remove=False
                    )
        """
        for_deque: deque = deque()
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
            ) -> list[Card]:
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


class Steps(BaseTool):
    """Game steps order object

    Attr:
        - c (Component[Step]): components of Steps.
        - current (List[Tuple[int, Step]]): current order of steps.
        - last (Step): last poped from current step.
    """
    c: Component[str, Step_] = Field(  # type: ignore
        default_factory=Component, exclude=True, repr=False
            )
    current: list[tuple[int, Step_]] = []  # type: ignore
    last: Optional[Step_] = None

    @property
    def current_ids(self) -> list[str]:
        """Get ids of current objects

        Returns:
            List[str]: list ids of current
        """
        return [item[1].id for item in self.current]

    def add(self, stuff: Step_) -> None:
        """Add Step to component

        Args:
            stuff (Step): Step object
        """
        if isinstance(stuff.__class__, Step_) \
                or issubclass(stuff.__class__, Step_):
            self.c.update(stuff)
            self._logger.info(
                f'Component updated by stuff with id="{stuff.id}".'
                    )
        else:
            raise ComponentClassError(stuff, self._logger)

    def deal(
        self,
        items: Optional[list[str]] = None
            ) -> 'Steps':
        """Clear current order and create new current order

        Args:
            items (Optional[List[str]]): list of stuff ids

        Returns:
            Steps
        """
        self.clear()

        if not items:
            for stuff in self.c.values():
                self.push(stuff)
        else:
            for id in items:
                comp = self.c.by_id(id)
                if comp:
                    self.push(comp)

        self._logger.debug(f'Is deal current: {self.current_ids}')
        return self

    def by_id(self, id: str) -> list[BaseItem]:
        """Get items from current by its id

        Args:
            id (str): item id

        Returns:
            list[BaseItem]: items
        """
        return [item[1] for item in self.current if item[1].id == id]

    def push(self, item: Step_) -> None:
        """Push Step object to current

        Args:
            item (Step): Step class instance
        """
        replaced: Step_ = self._item_replace(item)  # type: ignore
        heappush(self.current, (replaced.priority, replaced))

    def pop(self) -> Step_:
        """Pop Step object from current with lowest priority

        Returns:
            Step: Step instance object
        """
        self.last = heappop(self.current)[1]
        self._logger.debug(f'{self.last.id} is poped from current')
        return self.last

    def append(self, item: BaseItem) -> None:
        raise NotImplementedError

    def extend(self, items: Iterable[BaseItem]) -> None:
        raise NotImplementedError

    def index(
        self,
        item_id: str,
        start: int = 0,
        end: Optional[int] = None
            ) -> int:
        raise NotImplementedError

    def insert(self, item: BaseItem, pos: int) -> None:
        raise NotImplementedError

    def remove(self, item_id: str) -> None:
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError
