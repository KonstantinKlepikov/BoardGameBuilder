"""Game players classes
"""
from typing import Dict, TypeVar
from dataclasses import dataclass, field
from dataclasses_json import (
    DataClassJsonMixin, dataclass_json, Undefined, config
        )
from bgameb.base import Base, Component
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.tools import Shaker, Deck, Bag, Steps, BaseTool


# Item = Union[Card, Dice, Step]
# Tool = Union[Steps, Shaker, Bag, Deck]
# Stuff = Union[Item, Tool]

Item = TypeVar('Item', bound=BaseItem)
Tool = TypeVar('Tool', bound=BaseTool)
Stuff = TypeVar('Stuff', bound=BaseItem|BaseTool)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class BasePlayer(Base):

    c: Component[Stuff] = field(
        default_factory=Component,
        metadata=config(exclude=lambda x: True),  # type: ignore
            )

    def __post_init__(self) -> None:
        super().__post_init__()
        self.c = Component()

    def add(self, stuff: Stuff) -> None:
        """Add stuff to component

        Args:
            stuff (Stuff): game stuff
        """
        self.c._update(stuff)
        self._logger.info(
            f'Component updated by stuff with id="{stuff.id}".'
                )

    def get_items(self) -> Dict[str, Item]:
        return {
            key: val for key, val
            in self.__dict__.items()
            if issubclass(val.__class__, BaseItem)
                }

    def get_tools(self) -> Dict[str, Tool]:
        return {
            key: val for key, val
            in self.__dict__.items()
            if issubclass(val.__class__, BaseTool)
                }


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Player(BasePlayer, DataClassJsonMixin):
    """Player or bot
    """

    def __post_init__(self) -> None:
        super().__post_init__()
