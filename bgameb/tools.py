"""Game tools classes like shakers or decks
"""
import random
from abc import ABC
from collections import deque
from typing import Optional, Tuple, Dict, Literal, List, Deque
from dataclasses import dataclass, field, replace
from dataclasses_json import config
from bgameb.base import Base
from bgameb.stuff import Card, Dice, Rule, BaseStuff
from bgameb.errors import ArrangeIndexError, StuffDefineError


@dataclass
class BaseTool(Base, ABC):
    """Base class for game tools (like decks or shakers)
    """
    _stuff_to_add: BaseStuff = field(
        metadata=config(exclude=lambda x: True),
        repr=False,
        init=False,
        )
    _stuff: List[str] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),
        repr=False,
        init=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def _increase(self, name: str, game, count: int = 1) -> None:
        """Add or increase count of stuff in tool

        Args:
            name (str): name of stuff.
            game (BaseGame): game instance object.
            count (int, optional): count of stuff copy Defaults to 1.

        Raises:
            StuffDefineError: count of stuff nonpositive
                              or stuff not exist
        """
        if name not in game.keys():
            raise StuffDefineError(
                message=f"Stuff with {name=} not exist in a game.",
                logger=self.logger
                )

        if count < 1:
            raise StuffDefineError(
                message=f"Can't add {count} stuff.",
                logger=self.logger
                )

        # add stuff and set a count
        if name not in self._stuff:
            self._add(
                self._stuff_to_add,
                **game[name].to_dict()
                )
            self[name].count = count
            self._stuff.append(name)
            self.logger.debug(
                f'Added stuff with "{name=}" and {count=}.'
                )

        # if exist increase a count
        else:
            self[name].count += count
            self.logger.debug(
                f'Number of stuff with "{name=}" increased by {count}. ' +
                f'Result count is {self[name].count}'
                )

    def _decrease(self, name: str, count: int) -> None:
        """Decrease number of stuff by count

        Args:
            name (str): name of stuff
            count (int): count
        """
        self[name].count -= count
        self.logger.debug(
            f'Removed {count} stuff with {name=}. ' +
            f'Result count is {self.get(name, 0)}'
            )
        if self[name].count <= 0:
            del self[name]
            self._stuff.remove(name)

    def remove(
        self,
        name: Optional[str] = None,
        count: Optional[int] = None
            ) -> None:
        """Remove any kind of stuff copy from tool by its name and count

        Args:
            name (str, optional): name of stuff. Defaults to None.
            count (int, optional): count of stuff. Defaults to None.

        You can use any combination for names and counts to remove all
        stuff, all or any by name or by count.

        Raises:
            StuffDefineError: nonpositive integer for count
        """
        if count is not None and count <= 0:
            raise StuffDefineError(
                f"Count must be a integer greater than 0.",
                logger=self.logger
                )

        if name is None:

            if count is None:
                for n in self._stuff:
                    del self[n]
                self._stuff = set()
                self.logger.debug('Removed all stuff')
            else:
                for stuff in self._stuff:
                    self._decrease(stuff, count)

        elif self.get(name):
            if count is None:
                del self[name]
                self._stuff.remove(name)
                self.logger.debug(
                    f'Removed all stuff with {name=}.'
                    )
            else:
                self._decrease(name, count)

        else:
            raise StuffDefineError(
                message=f"Stuff with {name=} not exist in tool.",
                logger=self.logger
                )


@dataclass
class Shaker(BaseTool):
    """Create shaker for roll dices or flip coins
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Dice

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

        for name in self._stuff:
            roll[name] = self[name].roll()

        self.logger.debug(f'Result of roll: {roll}')

        return roll


@dataclass
class Bag(BaseTool):
    """Datastorage for nonqueued list of stuff. Use it for
    hand with cards, graveyards, outside of the game cards and etc
    """
    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Card


@dataclass
class Deck(Bag):
    """Create deck for cards

    Deck ia a Bag class that conyain dealt property for
    define queued deck representation

    You can add cards, define it counts and deal a deck.
    Result is saved in dealt attr as deque object. This object
    has all methods of
    `python deque
    <https://docs.python.org/3/library/collections.html#deque-objects>`_

    .. code-block::
        :caption: Example:

            deque(Card1, Card3, Card2, Card4)
    """
    dealt: Deque[BaseStuff] = field(
        default_factory=deque,
        repr=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def deal(self) -> List[str]:
        """Deal new random shuffled deck and save it to
        self.dealt: List[str]
        """
        self.dealt.clear()
        for stuff in self._stuff:
            for _ in range(self[stuff].count):
                card = replace(self[stuff])
                card.count = 1
                self.dealt.append(card)

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

                game.deck1.search(
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


@dataclass
class Rules(BaseTool):
    """Basic rules storage
    """
    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Rule


@dataclass
class Turn(Rules):
    """Turn is data storage for turn rules

    Args:
        name (str): name of Turn.
        _order (List[Rule]): list of default elements of Turn.
    """
    dealt: Deque[BaseStuff] = field(
        default_factory=deque,
        repr=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def deal(self):
        """Clear the Turn and instantiate new turn
        """
        self.dealt.clear()
        for stuff in self._stuff:
            phase = replace(self[stuff])
            self.dealt.append(phase)
        self.logger.debug(f'Is dealt order of turn: {self.dealt}')


TOOLS = {
    'shaker': Shaker,
    'cards_bag': Bag,
    'deck': Deck,
    'rules': Rules,
    'turn': Turn,
    }
TOOLS_TYPES = Literal['rule_book', 'shaker', 'cards_bag', 'deck', 'turn']
