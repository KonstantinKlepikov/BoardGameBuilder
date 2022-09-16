"""Game tools classes like shakers or decks
"""
from typing import Optional, Tuple, List, Dict
from dataclasses import dataclass, field
from dataclasses_json import config
from bgameb.errors import StuffDefineError
from bgameb.constructs import Components, BaseTool, BaseStuff


shaker_rollers_type = Dict[str, Dict[str, int]]
shaker_result_type = Dict[str, Dict[str, Tuple[int]]]
deck_cards_type = Dict[str, int]
deck_result_type = Tuple[Optional[BaseStuff]]
dealt_cards_type = Tuple[List[str]]


@dataclass
class Shaker(BaseTool):
    """Create shaker for roll dices or flip coins
    """
    _game_rollers: Components = field(
        metadata=config(exclude=lambda x: True),
        repr=False
        )
    name: Optional[str] = None
    rollers: shaker_rollers_type = field(default_factory=dict, init=False)
    last: shaker_result_type = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.rollers = {}
        self.last = {}
        super().__post_init__()

    def add(
        self,
        name: str,
        color: str = 'colorless',
        count: int = 1
            ) -> None:
        """Add roller to shaker

        Args:
            roller (str): roller name
            color (str, optional): color groupe. Defaults to 'colorless'.
            count (int, optional): count of rollers copy. Defaults to 1.

        Raises:
            StuffDefineError: coutn of stuff not defined
                              or stuff not exist
        """

        if not self._chek_name(name, self._game_rollers.keys()):
            raise StuffDefineError(
                message=f"Roller with {name=} not exist in a game.",
                logger=self.logger
                )

        if count < 1:
            raise StuffDefineError(
                message=f"Can't add {count} rollers.",
                logger=self.logger
                )
        if self.rollers.get(color):

            if name not in self.rollers[color].keys():
                self.rollers[color][name] = 0

            self.rollers[color][name] += count
            self.logger.debug(
                f'Number of rollers with "{name=}" increased by {count}. ' +
                f'Result count is {self.rollers[color][name]}'
                )

        else:
            self.rollers[color] = {name: count}
            self.logger.debug(
                f'Added {count} rollers with "{name=}" and {color=}.'
                )

    def _decrease(self, name: str, color: str, count: int) -> None:
        """Decrease number of rollers by count
        # TODO: test me

        Args:
            name (str): name of rollers
            color (str): color group
            count (int): count
        """
        self.rollers[color][name] -= count
        self.logger.debug(
            f'Removed {count} rollers with {name=} and {color=}. ' +
            f'Result count is {self.rollers[color].get(name, 0)}'
            )
        if self.rollers[color][name] <= 0:
            self._remove_by_name(name, color)

    def _remove_by_name(self, name: str, color: str) -> None:
        """Remove rollers by name
        # TODO: test me
        Args:
            name (str): name of roller
            color (str): color group
        """

        self.rollers[color].pop(name, 0)
        self.logger.debug(
            f'Remove all rollers with {name=} and {color=}'
            )

    def _remove_empry_color(self) -> None:
        """Check mapping object and delete all colors if empty
        # TODO: test me
        """
        colors = {
            color: self.rollers.pop(color)
            for color in list(self.rollers.keys())
            if not self.rollers[color]
            }
        self.logger.debug(
            f'Is removed empty colors={list(colors.keys())} from shaker'
            )

    def remove(
        self,
        name: Optional[str] = None,
        count: Optional[int] = None,
        color: Optional[str] = None
            ) -> None:
        """Remove any kind of roller copy from shaker by name and color

        Args:
            name (str, optional): name of removed stuff. Defaults to None.
            count (int, optional): count removed stuf. Defaults to None.
            color (str, optional): color froup of rollers. Defaults to None.

        You can use any combination for colors, names and counts to remove all
        rollers, all by color or by name or by count or rollers vit given count
        of choosen color or/and name.


        Raises:
            StuffDefineError: nopositive integer for count
        """

        if count is not None and count <= 0:
            raise StuffDefineError(
                f"Count must be a positive integer greater than 0.",
                logger=self.logger
                )

        col_keys = list(self.rollers.keys())

        if color is None:

            if name is None:

                if count is None:
                    self.rollers = {}
                    self.logger.debug('Removed all rollers from shaker')
                    return
                else:
                    for col in col_keys:
                        for na in list(self.rollers[col].keys()):
                            self._decrease(na, col, count)

            else:

                if count is None:
                    for col in col_keys:
                        self._remove_by_name(name, col)
                else:
                    for col in col_keys:
                        if self.rollers[col].get(name):
                            self._decrease(name, col, count)

        elif color not in col_keys:

            raise StuffDefineError(
                message=f"{color=} not exist in shaker.",
                logger=self.logger
                )

        else:

            if name is None:

                if count is None:
                    del self.rollers[color]
                else:
                    for na in list(self.rollers[color].keys()):
                        self._decrease(na, color, count)

            elif name in self.rollers[color].keys():

                if count is None:
                    self._remove_by_name(name, color)
                else:
                    self._decrease(name, color, count)

        self._remove_empry_color()

    def roll(self) -> shaker_result_type:
        """Roll all rollers with shaker and return results

        Return:
            Dict[str, Dict[str, Tuple[int]]]: result of roll

        .. code-block::
            :caption: Example:

                {"white": {"six_dice": (5, 3, 2, 5)}}
        """
        roll = {}
        for color, rollers in self.rollers.items():
            roll[color] = {}
            for name, count in rollers.items():
                roll[color][name] = tuple(
                    self._game_rollers[name].roll() for _ in range(count)
                    )
        if roll:
            self.last = roll
            self.logger.debug(f'Rolled: {roll}')
            return self.last
        else:
            self.logger.debug(f'No one roller rolled.')
            return {}


@dataclass
class Deck(BaseTool):
    """Create deck for cards
    """
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
            name (str): name of rollers
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
                self.logger.debug('Removed all rollers from shaker')
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