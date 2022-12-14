"""Main engine to create game
"""
from typing import Union
from dataclasses import dataclass, field
from dataclasses_json import (
    DataClassJsonMixin, dataclass_json, Undefined
        )
from bgameb.base import Base, Component
from bgameb.players import Player, BasePlayer
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.tools import Shaker, Deck, Bag, Steps, BaseTool
from bgameb.errors import ComponentClassError


Item = Union[Card, Dice, Step]
Tool = Union[Steps, Shaker, Bag, Deck]
Stuff = Union[Player, Item, Tool]


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class BaseGame(Base, DataClassJsonMixin):
    """Base class for game object
    """
    p: Component[Player] = field(default_factory=Component)
    i: Component[Item] = field(default_factory=Component)
    t: Component[Tool] = field(default_factory=Component)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.p = Component()
        self.i = Component()
        self.t = Component()

    def add(self, stuff: Stuff) -> None:
        """Add stuff to component

        Args:
            stuff (Stuff): game stuff
        """
        if issubclass(stuff.__class__, BasePlayer):
            self.p._update(stuff)
        elif issubclass(stuff.__class__, BaseItem):
            self.i._update(stuff)
        elif issubclass(stuff.__class__, BaseTool):
            self.t._update(stuff)
        else:
            raise ComponentClassError(stuff, self._logger)
        self._logger.info(
            f'Component updated by stuff with id="{stuff.id}".'
                )


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Game(BaseGame, DataClassJsonMixin):
    """The main game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()
