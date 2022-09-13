"""Main engine to create games
"""
from typing import (
    Union, Dict, List, Optional, Any,
    Tuple, Sequence, Iterable, Type
    )
from dataclasses import dataclass, field
from collections.abc import Mapping
from abc import ABC, abstractmethod
from dataclasses_json import DataClassJsonMixin, config
from bgameb.stuff import BaseRoller, BaseCard
from bgameb.errors import (
    ComponentNameError, ComponentClassError, StuffDefineError
    )
from bgameb.utils import log_me, get_random_name


game_stuff_type = Union[BaseRoller, BaseCard]
shaker_rollers_type = Dict[str, Dict[str, int]]
shaker_result_type = Dict[str, Dict[str, Tuple[int]]]
deck_cards_type = Dict[str, int]
deck_result_type = Tuple[Optional[BaseCard]]
dealt_cards_type = Tuple[List[str]]


class Components(Mapping):
    """Components mapping.

    This class inherit from dict and not implemets
    __setattr__ and __setitems__. Class represents
    additional dot-acces for attributes of dict
    """
    def __init__(
        self,
        *args,
        **kwargs
            ) -> None:
        """Args must be a dicts
        """
        super().__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                self.__dict__.update(arg)
            else:
                raise AttributeError('Args must be a dicts')
        if kwargs:
            self.__dict__.update(kwargs)

    def __iter__(self) -> Iterable:
        return iter(self.__dict__)

    def __getattr__(self, attr: str):
        try:
            return self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setattr__(self, attr: str, value) -> None:
        raise NotImplementedError('This method not implementd for Components')

    def __delattr__(self, attr: str) -> None:
        try:
            del self.__dict__[attr]
        except KeyError:
            raise AttributeError(attr)

    def __setitem__(self, key: str, value) -> None:
        raise NotImplementedError('This method not implementd for Components')

    def __getitem__(self, key: str):
        return self.__dict__[key]

    def __delitem__(self, key: str) -> None:
        del self.__dict__[key]

    def __repr__(self):
        items = (f"{k}={v!r}" for k, v in self.__dict__.items())
        return "{}({})".format(type(self).__name__, ", ".join(items))

    def __len__(self) -> int:
        return len(self.__dict__)

    def _chek_in(self, name: str) -> Optional[bool]:
        """Chek is name of component is unique

        Args:
            name (str): name for component

        Raises:
            ComponentNameError: name id not unique

        Returns:
            Optional[bool]: if it is in
        """
        if name in self.__dict__.keys():
            raise ComponentNameError(name=name)
        return True

    def _update(
        self,
        component,
        kwargs: Dict[str, Any]
            ) -> None:
        """Update components dict

        Args:
            component: component class
            kwargs (Dict[str, Any]): aditional args
        """
        self.__dict__.update(
            {kwargs['name']: component(**kwargs)}
            )

    def add(self, component, **kwargs) -> None:
        """Add component to Components dict. Components with
        same names as existed cant be added.

        Raises:
            ComponentNameError: name id not unique

        Args:
            component (Component): component class
            kwargs: aditional args
        """
        if kwargs.get('name'):
            self._chek_in(kwargs['name'])
        else:
            self._chek_in(component.name)
            kwargs['name'] = component.name
        self._update(component, kwargs)

    def add_replace(self, component, **kwargs) -> None:
        """Add or replace component in Components dict.

        Args:
            component (Component): component class
            kwargs: aditional args
        """
        if not kwargs.get('name'):
            kwargs['name'] = component.name
        self._update(component, kwargs)

    def get_names(self) -> List[str]:
        """Get names of all components of class

        Returns:
            List[str]: lisct of names of conatined components
        """
        return list(self.__dict__)


@dataclass
class BaseGame(DataClassJsonMixin, ABC):
    """Base game class

    Inherited classes needs attr name implementation
    """

    def __post_init__(self) -> None:
        # set random name
        if not self.name:
            self.name = get_random_name()

        # set logger
        self.logger = log_me.bind(
            classname=self.__class__.__name__,
            name=self.name)
        self.logger.info(
            f'{self.__class__.__name__} created with {self.name=}.'
            )


@dataclass
class BaseGameTools(BaseGame, ABC):
    """Base game tools (like Decs or Shakers) class

    Inherited classes needs attr name implementation
    """

    @staticmethod
    def _chek_name(name: str, chek: Sequence[str]) -> bool:
        """Chek exist roller in game
        # TODO: test me

        Args:
            name (str): stuff name
            check (Sequence[str]): cheked collection

        Returns:
            bool: stuff is exist or not in collection
        """
        if name in chek:
            return True
        return False

    @abstractmethod
    def add(self, name: str, count: int = 1) -> None:
        """Add stuff to tool
        Args:
            name (str): name of added stuff
            count (int, optional): count added stuf. Defaults to 1.
        """

    @abstractmethod
    def remove(
        self,
        name: Optional[str] = None,
        count: Optional[int] = None
            ) -> None:
        """Remove stuff from tool

        Args:
            name (str, optional): name of removed stuff. Defaults to None.
            count (int, optional): count removed stuf. Defaults to None.
        """


@dataclass
class Shaker(BaseGameTools):
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
class Deck(BaseGameTools):
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


@dataclass
class Game(BaseGame):
    """Create the game object
    """
    name: Optional[str] = None
    shakers: Components = field(default_factory=Components, init=False)
    decks: Components = field(default_factory=Components, init=False)
    game_rollers: Components = field(default_factory=Components, init=False)
    game_cards: Components = field(default_factory=Components, init=False)

    def __post_init__(self) -> None:
        self.shakers = Components()
        self.decks = Components()
        self.game_rollers = Components()
        self.game_cards = Components()
        super().__post_init__()

    def add_stuff(self, stuff: Type[game_stuff_type], **kwargs) -> None:
        """Add component to game

        Args:
            stuff (Type[game_stuff_type]): any class instance of game stuffs
            like rollers, cards etc
            kwargs: additional arguments of component
        """
        if issubclass(stuff, BaseRoller):
            self.game_rollers.add(stuff, **kwargs)
            self.logger.info(f'Roller added: {self.game_rollers=}.')
        elif issubclass(stuff, BaseCard):
            self.game_cards.add(stuff, **kwargs)
            self.logger.info(f'Card added: {self.game_cards=}.')
        else:
            raise ComponentClassError(class_=stuff)

    def add_shaker(self, name: Optional[str] = None) -> None:
        """Add shaker to game shakers

        Args:
            name (str): name for added shaker
        """
        if name:
            self.shakers.add(
                Shaker, name=name, _game_rollers=self.game_rollers
                )
        else:
            self.shakers.add(
                Shaker, name=Shaker.name, _game_rollers=self.game_rollers
                )
