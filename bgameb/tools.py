"""Game tools classes like shakers or decks
"""
from typing import Optional, Tuple, List, Dict, Literal
from dataclasses import dataclass, field
from dataclasses_json import config
from bgameb.stuff import Roller
from bgameb.errors import StuffDefineError
from bgameb.constructs import Components, BaseTool, BaseStuff, BaseGame


deck_cards_type = Dict[str, int]
deck_result_type = Tuple[Optional[BaseStuff]]
dealt_cards_type = Tuple[List[str]]


@dataclass
class Shaker(BaseTool):
    """Create shaker for roll dices or flip coins
    """
    _game: BaseGame = field(
        metadata=config(exclude=lambda x: True),
        repr=False
        )
    name: Optional[str] = None
    stuff: Components = field(default_factory=Components, init=False)
    last: Dict[str, Tuple[int]] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.stuff = Components()
        self.last = {}
        super().__post_init__()

    def add(
        self,
        name: str,
        count: int = 1
            ) -> None:
        """Add roller to shaker

        Args:
            name (str): roller name
            count (int, optional): count of stuff copy. Defaults to 1.

        Raises:
            StuffDefineError: coutn of stuff not defined
                              or stuff not exist
        """

        if not self._chek_name(name, self._game.stuff.keys()):
            raise StuffDefineError(
                message=f"Roller with {name=} not exist in a game.",
                logger=self.logger
                )

        if count < 1:
            raise StuffDefineError(
                message=f"Can't add {count} stuff.",
                logger=self.logger
                )

        # add roller and set a count
        if name not in self.stuff.get_names():
            self.stuff.add(component=Roller, **self._game.stuff[name].to_dict())
            self.stuff[name].count = count
            self.logger.debug(
                f'Added roller with "{name=}" and {count=}.'
                )

        # if exist increase a count
        else:
            self.stuff[name].count += count
            self.logger.debug(
                f'Number of stuff with "{name=}" increased by {count}. ' +
                f'Result count is {self.stuff[name].count}'
                )

    def _decrease(self, name: str, count: int) -> None:
        """Decrease number of stuff by count
        # TODO: test me

        Args:
            name (str): name of stuff
            count (int): count
        """
        self.stuff[name].count -= count
        self.logger.debug(
            f'Removed {count} stuff with {name=}. ' +
            f'Result count is {self.stuff.get(name, 0)}'
            )
        if self.stuff[name].count <= 0:
            del self.stuff[name]

    def remove(
        self,
        name: Optional[str] = None,
        count: Optional[int] = None,
            ) -> None:
        """Remove any kind of roller copy from shaker by name and color

        Args:
            name (str, optional): name of removed stuff. Defaults to None.
            count (int, optional): count removed stuf. Defaults to None.

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
                self.stuff = Components()
                self.logger.debug('Removed all stuff')
            else:
                for stuff in list(self.stuff.keys()):
                    self._decrease(stuff, count)

        elif self.stuff.get(name):
            if count is None:
                del self.stuff[name]
                self.logger.debug(
                    f'Removed all stuff with {name=}.'
                    )
            else:
                self._decrease(name, count)

        else:
            raise StuffDefineError(
                message=f"Stuff with {name=} not exist in shaker.",
                logger=self.logger
                )

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
    _game: BaseGame = field(
        metadata=config(exclude=lambda x: True),
        repr=False
        )
    _game_cards: Components = field(
        default_factory=Components,
        repr=False
        )
    name: Optional[str] = None
    deck_cards: deck_cards_type = field(default_factory=dict, init=False)
    dealt_cards: dealt_cards_type = field(default_factory=tuple, init=False)

    def __post_init__(self) -> None:
        self.deck_cards = {}
        self.dealt_cards = ([], [])  # TODO: make named class
        super().__post_init__()

    def add(self, name: str, count: int = 1) -> None:
        """Add card to the deck collection

        Args:
            name (str): name of card
            count (int, optional): count of cards copy Defaults to 1.

        Raises:
            StuffDefineError: count of stuff not defined
                              or stuff not exist
        """
        if not self._chek_name(name, self._game_cards.keys()):
            raise StuffDefineError(
                message=f"Card with {name=} not exist in a game.",
                logger=self.logger
                )

        if count < 1:
            raise StuffDefineError(
                message=f"Can't add {count} cards.",
                logger=self.logger
                )

        if not self.deck_cards.get(name):
            self.deck_cards[name] = 0

        self.deck_cards[name] += count
        self.logger.debug(
            f'Number of cards with "{name=}" increased by {count}. ' +
            f'Result count is {self.deck_cards[name]}'
            )

    def _decrease(self, name: str, count: int) -> None:
        """Decrease number of cards by count
        # TODO: test me

        Args:
            name (str): name of stuff
            count (int): count
        """
        self.deck_cards[name] -= count
        self.logger.debug(
            f'Removed {count} cards with {name=}. ' +
            f'Result count is {self.deck_cards.get(name, 0)}'
            )
        if self.deck_cards[name] <= 0:
            del self.deck_cards[name]
            self.logger.debug(f'Removed all cards with {name=}.')

    def remove(
        self,
        name: Optional[str] = None,
        count: Optional[int] = None
            ) -> None:
        """Remove all cards by cards name and count from Deck.

        Args:
            name (str, optional): name of removed stuff. Defaults to None.
            count (int, optional): count removed stuf. Defaults to None.
        Raises:
            ComponentClassError: _description_
        """
        if count is not None and count <= 0:
            raise StuffDefineError(
                f"Count must be a positive integer greater than 0.",
                logger=self.logger
                )

        keys = list(self.deck_cards.keys())

        if name is None:

            if count is None:
                self.deck_cards = {}
                self.logger.debug('Removed all stuff from shaker')
                return
            else:
                for na in keys:
                    self._decrease(na, count)

        elif name not in keys:

            raise StuffDefineError(
                f"{name=} not exist in deck.",
                logger=self.logger
                )

        else:

            if count is None:
                del self.deck_cards[name]
                self.logger.debug(f'Removed all cards with {name=}.')
            else:
                self._decrease(name, count)

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

    def look(self) -> deck_result_type:
        """Look cards in in/out deal_cards
        """
        raise NotImplementedError

    def pop(self) -> deck_result_type:
        """Pop cards from in to out or visa versa
        """
        raise NotImplementedError

    def search(self, name: str) -> deck_result_type:
        """Search for cards in in/out deal_cards

        Args:
            name (str): name of card
        """
        raise NotImplementedError


TOOLS = {
    'shaker': Shaker,
    'deck': Deck,
}
TOOLS_TYPES = Literal['roller', 'card']