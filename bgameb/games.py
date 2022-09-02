"""Main engine to create game object
"""
from typing import List, Any
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.rolled import Dice, Coin


@dataclass
class Game(DataClassJsonMixin):
    """Create the game object
    """

    name: str = 'game'
    dices: List[Dice]  = field(default_factory=list, init=False)

    def add_component(self, component) -> None:
        raise NotImplementedError

    def add_components(self, component: List[Any]) -> None:
        raise NotImplementedError
