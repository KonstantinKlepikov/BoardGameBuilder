"""Game tools classes
"""
import random
from collections import deque
from typing import (
    Optional, Tuple, Dict, Literal, List, Deque, Type
    )
from dataclasses import dataclass, field, replace
from dataclasses_json import config, dataclass_json
from bgameb.base import Base, Order
from bgameb.stuff import Card, Dice, Step, BaseStuff
from bgameb.errors import ArrangeIndexError, StuffDefineError


@dataclass_json
@dataclass(repr=False)
class BaseTool(Base):
    """Base class for game tools (like decks or shakers)
    """
    _stuff_to_add: Type[BaseStuff] = field(
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        init=False,
        )
    _stuff: List[str] = field(
        default_factory=list,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        init=False,
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def update(self, name: str, game: Base, count: int = 1) -> None:
        """Add or increase count of stuff in tool

        Args:
            name (str): name of stuff.
            game (BaseGame): game instance object.
            count (int, optional): count of stuff copies. Defaults to 1.

        Raises:
            StuffDefineError: count of stuff nonpositive
                              or stuff not exist
        """
        if name not in game.keys():
            raise StuffDefineError(
                message=f"Stuff with {name=} not exist in a game.",
                logger=self._logger
                )

        if count < 1:
            raise StuffDefineError(
                message=f"Can't add {count} stuff.",
                logger=self._logger
                )

        if name not in self._stuff:
            self._add(
                self._stuff_to_add,
                **game[name].to_dict()
                )
            self[name].count = count
            self._stuff.append(name)
            self._logger.debug(
                f'Added stuff with "{name=}" and {count=}.'
                )

        else:
            self[name].count += count
            self._logger.debug(
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
        self._logger.debug(
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
        """Remove any kind of stuff copies from tool by its name and count

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
                "Count must be a integer greater than 0.",
                logger=self._logger
                )

        if name is None:

            if count is None:
                for n in self._stuff:
                    del self[n]
                self._stuff = []
                self._logger.debug('Removed all stuff')
            else:
                for stuff in self._stuff:
                    self._decrease(stuff, count)

        elif self.get(name):
            if count is None:
                del self[name]
                self._stuff.remove(name)
                self._logger.debug(
                    f'Removed all stuff with {name=}.'
                    )
            else:
                self._decrease(name, count)

        else:
            raise StuffDefineError(
                message=f"Stuff with {name=} not exist in tool.",
                logger=self._logger
                )


@dataclass_json
@dataclass(repr=False)
class Shaker(BaseTool):
    """Create shaker for roll dices or flip coins
    """
    _type: str = field(
        default='shaker',
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Dice

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

        for name in self._stuff:
            roll[name] = self[name].roll()

        self._logger.debug(f'Result of roll: {roll}')

        return roll


@dataclass_json
@dataclass(repr=False)
class Bag(BaseTool):
    """Datastorage for ordered list of stuff. Isnt queue or stack.
    Use it for hand with cards, graveyards, outside of the game cards
    and etc.
    """
    _type: str = field(
        default='bag',
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Card


@dataclass_json
@dataclass(repr=False)
class Deck(Bag):
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
    current: Deque[BaseStuff] = field(
        default_factory=deque,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )
    _type: str = field(
        default='deck',
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def deal(self) -> None:
        """Deal new random shuffled deck and save it to
        self.current
        """
        self.current.clear()
        for stuff in self._stuff:
            for _ in range(self[stuff].count):
                card = replace(self[stuff])
                card.count = 1
                self.current.append(card)

        self.shuffle()
        self._logger.debug(f'Is deal cards: {self.current}')

    def shuffle(self) -> None:
        """Random shuffle current deck
        """
        random.shuffle(self.current)
        self._logger.debug(f'Is shuffled: {self.current}')

    def to_arrange(
        self,
        start: int,
        end: int
            ) -> Tuple[
                List[BaseStuff],
                Tuple[List[BaseStuff], List[BaseStuff]]
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
            Tuple[List[BaseStuff], Tuple[List[BaseStuff]]: part to arrange
        """
        if start < 0 or end < 0 or end < start:
            raise ArrangeIndexError(
                message=f'Nonpositive or broken {start=} or {end=}',
                logger=self._logger
                )
        to_split = list(self.current)
        splited = (to_split[start:end], (to_split[0:start], to_split[end:]))
        self._logger.debug(f'To arrange result: {splited=}')

        return splited

    def arrange(
        self,
        arranged: List[BaseStuff],
        last: Tuple[List[BaseStuff], List[BaseStuff]]
            ) -> None:
        """Concatenate new current deck from given arranged list and last of
        deck. Use to_arrange() method to get list to arrange and last.

        Args:
            arranged (List[BaseStuff]): arranged list of cards
            last: (Tuple[List[BaseStuff], List[BaseStuff]]): last of deck
        """
        reorranged: Deque = deque()
        reorranged.extend(last[0])
        reorranged.extend(arranged)
        reorranged.extend(last[1])

        if len(reorranged) == len(self.current):
            self.current = reorranged
            self._logger.debug(f'Arrange result: {reorranged=}')
        else:
            raise ArrangeIndexError(
                f'Wrong to_arranged parts: {arranged=}, {last=}',
                logger=self._logger
                )

    def search(
        self,
        query: Dict[str, int],
        remove: bool = True
            ) -> List[BaseStuff]:
        """Search for cards in current deck

        Args:
            query (Dict[str, int]): dict with name of searched
                                    cards and count of searching
            remove (bool): if True - remove cards from current deck.
                           Default to True.

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
                if card.name in query.keys() and query[card.name] > 0:
                    result.append(card)
                    query[card.name] -= 1
                    if not remove:
                        for_deque.append(card)
                else:
                    for_deque.append(card)
            except IndexError:
                break
        self.current = for_deque
        self._logger.debug(f'Search result: {result}')

        return result


@dataclass_json
@dataclass(repr=False)
class Steps(BaseTool):
    """Game steps order object

    Args:

        - current (Order): current order of steps.
    """
    current: Order = field(
        default_factory=Order,
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False,
        )
    _type: str = field(
        default='steps',
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()
        self._stuff_to_add = Step

    def deal(self):
        """Clear current order and create new current order
        """
        self.current.clear()
        for step in self._stuff:
            step = replace(self[step])
            self.current.put(step)
        self._logger.debug(f'Is deal order of turn: {self.current}')


TOOLS = {
    Shaker._type: Shaker,
    Bag._type: Bag,
    Deck._type: Deck,
    Steps._type: Steps,
    }
TOOLS_TYPES = Literal['shaker', 'bag', 'deck', 'steps']
