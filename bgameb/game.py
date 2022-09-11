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


game_stuff = Union[BaseRoller, BaseCard]
shaker_rollers = Dict[str, Dict[str, int]]
shaker_result = Dict[str, Dict[str, Tuple[int]]]
deck_cards = Dict[str, int]
deck_result = Tuple[Optional[BaseCard]]


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
        self.logger.info(f'{self.__class__.__name__} created with {self.name=}.')


@dataclass
class BaseGameTools(BaseGame):
    """Base game tools (like Decs or Shakers) class

    Inherited classes needs attr name implementation
    """

    def _chek(self, name: str, chek: Sequence[str]) -> bool:
        """Chek exist roller in game

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
    def add(self) -> None:
        """Add stuff to tool
        """

    @abstractmethod
    def remove_all(self) -> None:
        """Remove all stuff from tool
        """

    @abstractmethod
    def remove_all(self) -> None:
        """Remove stuff from tool
        """


@dataclass
class Shaker(BaseGameTools):
    """Create shaker for roll dices or flip coins
    """
    _game_rollers: Components = field(
        metadata=config(exclude=lambda x:True),
        repr=False
        )
    name: Optional[str] = None
    rollers: shaker_rollers = field(default_factory=dict, init=False)
    last: shaker_result= field(default_factory=dict, init=False)

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

        if not self._chek(name, self._game_rollers.keys()):
            raise StuffDefineError(
                f"Roller with {name=} not exist in a game."
                )

        if count < 1:
            self.logger.debug(f"Can't add 0 rollers.")
            raise StuffDefineError(
                "Need at least one roller. Can't add 0 rollers."
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

    def remove(self, name: str, count: int, color: str) -> None:
        """Remove any kind of roller copy from shaker by name and color

        Args:
            name (str): name of roller
            count (int): count of rollers to delete
            color (str): color froup of rollers

        Raises:
            StuffDefineError: name or color not match or
                              count of rollers not defined
        """
        if not self._chek(color, self.rollers.keys()):
            raise StuffDefineError(
                f"Roller with {color=} not exist in a shaker."
                )

        if not self._chek(name, self.rollers[color].keys()):
            raise StuffDefineError(
                f"Roller with {name=} not exist in a shaker."
                )

        if count < 1:
            self.logger.debug(
                "Can't remove 0 rollers. Need at least one roller."
                )
            raise StuffDefineError(
                "Can't remove 0 rollers. Need at least one roller."
                )

        if self.rollers[color][name] <= count:
            del self.rollers[color][name]
            self.logger.debug(
                f'Removed rollers with {color=} and {name=}'
                )

            if len(self.rollers[color]) == 0:
                del self.rollers[color]
                self.logger.debug(
                    f'Removed empty {color=} from shaker'
                    )

        else:
            self.rollers[color][name] -= count
            self.logger.debug(
                f'Number of rollers with "{name=}" decreased by {count}. ' +
                f'Result count is {self.rollers[color][name]}'
                )


    def remove_all_by_color(self, color: str) -> None:
        """Remove all rollers by color from shaker.
        If no any color is match, nostuff happens.

        Args:
            name (str): name of roller
        """
        if color in self.rollers.keys():
            del self.rollers[color]
            self.logger.debug(f'Removed rollers with {color=}')

    def remove_all_by_name(self, name: str) -> None:
        """Remove all rollers by roller name from shaker.
        If no any name is match, nostuff happens.

        Args:
            name (str): name of roller
        """
        to_del = []
        for color in self.rollers.keys():
            self.rollers[color].pop(name, None)

            if len(self.rollers[color]) == 0:
                to_del.append(color)

        self.logger.debug(f'Removed rollers with {name=}')

        if to_del:
            self._remove_empty_colors(to_del)

    def remove_all(self) -> None:
        """Remove all rollers from shaker
        """
        self.rollers = {}
        self.logger.debug('Removed all rollers from shaker')

    def _remove_empty_colors(self, to_del: List[str]) -> None:
        """Remove empty colors items from rollers dict

        Args:
            to_del (List[str]): list of colors
        """
        for color in to_del:
            del self.rollers[color]
            self.logger.debug(f'Removed empty {color=} from shaker')

    def roll(self) -> shaker_result:
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
    cards: deck_cards = field(default_factory=dict, init=False)
    dealt: deck_cards = field(default_factory=dict, init=False) # TODO: this is stack

    def __post_init__(self) -> None:
        self.cards = {}
        self.dealt = {}
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
        if not self._chek(name, self._game_cards.keys()):
            raise StuffDefineError(
                f"Card with {name=} not exist in a game."
                )

        if count < 1:
            self.logger.debug(
                f"Need at least one card. Can't add 0 cards."
                )
            raise StuffDefineError(
                "Need at least one card. Can't add 0 cards."
                )

        if not self.cards.get(name):
            self.cards[name] = 0

        self.cards[name] += count
        self.logger.debug(
            f'Number of cards with "{name=}" increased by {count}. ' +
            f'Result count is {self.cards[name]}'
            )

    def remove_all(self) -> None:
        """Remove all cards from deck
        """
        self.cards = {}
        self.logger.debug('Removed all cards from deck')


    def remove(self, name: str, count: int) -> None:
        """_summary_

        Args:
            name (str): _description_
            count (int): _description_

        Raises:
            ComponentClassError: _description_
        """

    def deal(self) -> None:
        """_summary_

        Raises:
            ComponentClassError: _description_
        """

    def shuffle(self) -> None:
        """
        """

    def reveal(self, start_from: int = 1, count: int = 1) -> deck_result:
        """_summary_
        """

    def draw(self, start_from: int = 1, count: int = 1) -> deck_result:
        """_summary_
        """

    def search(
        self, name: str, all: bool = False, count: int = 1
        ) -> deck_result:
        """_summary_

        Args:
            name (str): _description_

        Returns:
            Optional[BaseCard]: _description_
        """

    def __len__(self) -> int:
        """_summary_

        Raises:
            ComponentClassError: _description_

        Returns:
            int: _description_
        """


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

    def add_stuff(self, stuff: Type[game_stuff], **kwargs) -> None:
        """Add component to game

        Args:
            stuff (Type[game_stuff]): any class instance of game stuffs
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
