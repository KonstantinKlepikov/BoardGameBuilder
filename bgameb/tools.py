"""Game tools classes
"""
import random
from pydantic import Field, PositiveInt
from collections import deque
from collections.abc import KeysView
from heapq import heappop, heappush
from typing import Optional, Iterable, Union, Any
from bgameb.base import BaseTool, BaseToolExtended, Components
from bgameb.items import Card, Dice, Step
from bgameb.errors import ArrangeIndexError


class Shaker(BaseToolExtended[Dice]):
    """Shaker object

    ..
        Attr:

            current (list[Dice]): Current dices representation of shaker.
                                  This making from Components items.

            last (Dice), optional: last dice removed from current.

            last_roll (dict[str, list[PositiveInt]), optional:
                last roll result.

            last_roll_mapped (dict[str, list[Any]]), optional:
                last mapped roll result.
    """
    last_roll: dict[str, list[PositiveInt]] = {}
    last_roll_mapped: dict[str, list[Any]] = {}

    def deal(
        self,
        components: Components[Dice],
        items: Optional[list[str]] = None
            ) -> 'Shaker':
        """Deal new shaker current. The current is cleared
        before deal.

        Args:
            components (Components): game components
            items (Optional[list[str]]): item ids

        Returns:
            Shaker
        """
        self.clear()

        if not items:
            for stuff in components.values():
                if issubclass(stuff.__class__, Dice):
                    self.append(stuff)
        else:
            for id in items:
                if id in components.ids:
                    comp = components.by_id(id)
                    if issubclass(comp.__class__, Dice):
                        self.append(comp)

        self._logger.debug(f'Is deal current: {self.current_ids}')
        return self

    def roll(self) -> dict[str, list[int]]:
        """Roll all stuff in shaker and return results

        Return:
            dict[str, list[int]]: result of roll

        .. code-block::
            :caption: Example:

                {
                    "six_dice": [5, 3, 2, 5],
                    "twenty_dice": [2, 12, 4],
                }
        """
        self.last_roll = {}

        for item in self.current:
            self.last_roll[item.id] = item.roll()  # type: ignore

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
            self.last_roll_mapped[item.id] = item.roll_mapped()  # type: ignore

        self._logger.debug(f'Result of roll: {self.last_roll_mapped}')

        return self.last_roll_mapped


class Deck(BaseToolExtended[Card]):
    """Deck object

    ..
        You can add cards, define it counts and deal a deck.
        Result is saved in current attr as deque object. This object
        has all methods of
        `python deque
        <https://docs.python.org/3/library/collections.html#deque-objects>`_

        Attr:

            current (Deque[Card]): Current cards representation of deck.
                                   This making from Component items.

            last (Card), optional: last card, removed from current.
    """
    current: deque[Card] = Field(default_factory=deque)  # type: ignore

    def _item_replace(self, item: Card) -> Card:
        """Get replaced copy of card

        Args:
            item (Card): a card object

        Returns:
            Card
        """
        item = super()._item_replace(item)
        item.count = 1
        return item

    def deal(
        self,
        components: Components[Card],
        items: Optional[list[str]] = None
            ) -> 'Deck':
        """Deal new deck current. Curent is cleared
        before deal.

        Args:
            components (Components): game components
            items (Optional[list[str]]): list of cards ids

        Returns:
            Deck
        """
        self.clear()

        if not items:
            for stuff in components.values():
                if issubclass(stuff.__class__, Card):
                    for _ in range(stuff.count):
                        self.append(stuff)
        else:
            for id in items:
                if id in components.ids:
                    comp = components.by_id(id)
                    if issubclass(comp.__class__, Card):
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
            Card
        """
        self.last = self.current.popleft()  # type: ignore
        self._logger.debug(
            f'{self.last.id if self.last else None} '
            'is poped from left of current'
                )
        return self.last  # type: ignore

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
            order (list[str]): ordered list of cards ids
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
            order (list[str]): ordered list of cards ids
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
            order (list[str]): ordered list of cards ids
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
            order (list[str]): ordered list of cards ids
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
            query (dict[str, int]): dict with id of searched
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
        for_deque: deque[Card] = deque()
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
            list[Card]: list of random cards
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


class Steps(BaseTool[Step]):
    """Game steps order object

    ..
        Attr:

            current (list[Step]]):
                Current representation of order in steps.
                This making from Component items.

            last (Step), optional: last poped from current step.
    """
    current: list[Step] = []
    last: Optional[Step] = None

    def deal(
        self,
        components: Components[Step],
        items: Optional[list[str]] = None
            ) -> 'Steps':
        """Clear current order and create new current order

        Args:
            components (Components): game components
            items (Optional[list[str]]): list of stuff ids

        Returns:
            Steps
        """
        self.clear()

        if not items:
            for stuff in components.values():
                if issubclass(stuff.__class__, Step):
                    self.push(stuff)
        else:
            for id in items:
                if id in components.ids:
                    comp = components.by_id(id)
                    if issubclass(comp.__class__, Step):
                        self.push(comp)

        self._logger.debug(f'Is deal current: {self.current_ids}')
        return self

    def push(self, item: Step) -> None:
        """Push Step object to current

        Args:
            item (Step): Step class instance
        """
        replaced = self._item_replace(item)
        heappush(self.current, replaced)

    def pops(self) -> Step:
        """Pop Step object from current with smallest priority

        Returns:
            Step
        """
        self.last = heappop(self.current)
        self._logger.debug(f'{self.last.id} is poped from current')
        return self.last
