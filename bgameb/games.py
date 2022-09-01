"""Main engine to create game object
"""
from typing import List, Any
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.dices import Dice, DiceTower


@dataclass
class Game(DataClassJsonMixin):
    """Base class for creation of the game
    """

    name: str = 'Game'
    dices: List[Dice]  = field(default_factory=list)

    def add_component(self, component) -> None:
        raise NotImplementedError

    def add_components(self, component: List[Any]) -> None:
        raise NotImplementedError
