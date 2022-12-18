"""Main engine to create game
"""
from typing import TypeVar
from dataclasses import dataclass, field
from dataclasses_json import (
    DataClassJsonMixin, dataclass_json, Undefined, config
        )
from bgameb.base import Base, Component
from bgameb.players import BasePlayer
from bgameb.items import BaseItem
from bgameb.tools import  BaseTool


Item = TypeVar('Item', bound=BaseItem)
Tool = TypeVar('Tool', bound=BaseTool)
Player_ = TypeVar('Player_', bound=BasePlayer)
Stuff = TypeVar('Stuff', bound=BaseItem|BaseTool|BasePlayer)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class BaseGame(Base):

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

    def get_items(self) -> dict[str, Item]:
        return {
            key: val for key, val
            in self.c.__dict__.items()
            if issubclass(val.__class__, BaseItem)
                }

    def get_tools(self) -> dict[str, Tool]:
        return {
            key: val for key, val
            in self.c.__dict__.items()
            if issubclass(val.__class__, BaseTool)
                }

    def get_players(self) -> dict[str, Player_]:
        return {
            key: val for key, val
            in self.c.__dict__.items()
            if issubclass(val.__class__, BasePlayer)
                }


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Game(BaseGame, DataClassJsonMixin):
    """The main game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()
