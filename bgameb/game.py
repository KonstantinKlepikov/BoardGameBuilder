"""Main engine to create game
"""
# import json
from typing import Union, Any
from dataclasses import dataclass, field
from dataclasses_json import (
    DataClassJsonMixin, dataclass_json, Undefined, config
        )
from bgameb.base import Base, Component
from bgameb.players import BasePlayer
from bgameb.items import BaseItem
from bgameb.tools import BaseTool


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class BaseGame(Base):

    c: Component[Union[BaseItem, BaseTool, BasePlayer]] = field(
        default_factory=Component,
        metadata=config(exclude=lambda x: True),  # type: ignore
            )

    def __post_init__(self) -> None:
        super().__post_init__()
        self.c = Component()

        self._logger.info('===========NEW GAME============')
        self._logger.info(
            f'{self.__class__.__name__} created with id="{self.id}".'
                )

    @property
    def get_items(self) -> dict[str, BaseItem]:
        """Get items from Component

        Returns:
            dict[str, BaseItem]: items mapping
        """
        return {
            key: val for key, val
            in self.c.items()
            if issubclass(val.__class__, BaseItem)
                }

    @property
    def get_tools(self) -> dict[str, BaseTool]:
        """Get tools from Component

        Returns:
            dict[str, BaseTool]: tools mapping
        """
        return {
            key: val for key, val
            in self.c.items()
            if issubclass(val.__class__, BaseTool)
                }

    @property
    def get_players(self) -> dict[str, BasePlayer]:
        """Get players from Component

        Returns:
            dict[str, BasePlayer]: players mapping
        """
        return {
            key: val for key, val
            in self.c.items()
            if issubclass(val.__class__, BasePlayer)
                }

    def add(self, stuff: Union[BaseItem, BaseTool, BasePlayer]) -> None:
        """Add stuff to component

        Args:
            stuff (BaseItem|BaseTool|BasePlayer): game stuff
        """
        self.c.update(stuff)
        self._logger.info(
            f'Component updated by stuff with id="{stuff.id}".'
                )

    @staticmethod
    def get_items_val(
        obj_: Union['BaseGame', BaseTool, BasePlayer]
            ) -> list[dict[str, Any]]:
        """Get items values represented as list of dicts

        Args:
            obj_ (Union['BaseGame', BaseTool, BasePlayer]): parrent class

        Returns:
            list[dict[str, Any]]: items
        """
        return [val.to_dict() for val in obj_.get_items.values()]

    def get_tools_val(
        self,
        obj_: Union['BaseGame', BasePlayer],
            ) -> list[dict[str, Any]]:
        """Get tools values represented as list of dicts

        Args:
            obj_ (Union[BaseTool, BasePlayer]): parrent class

        Returns:
            list[dict[str, Any]]: tools
        """
        result = []
        for tool in obj_.get_tools.values():
            t = tool.to_dict()
            t['items'] = self.get_items_val(tool)
            result.append(t)
        return result

    def get_players_val(self, obj_: 'BaseGame') -> list[dict[str, Any]]:
        """Get players values represented as list of dicts

        Args:
            obj_ (BaseGame): parrent class

        Returns:
            list[dict[str, Any]]: players
        """
        result = []
        for player in obj_.get_players.values():
            p = player.to_dict()
            p['tools'] = self.get_tools_val(player)
            p['items'] = self.get_items_val(player)
            result.append(p)
        return result

    def relocate_all(self) -> 'BaseGame':
        """Relocate all objects in game

        Returns:
            BaseGame
        """
        for item in self.get_items.values():
            item.relocate()

        for tool in self.get_tools.values():
            tool.relocate()
            for item in tool.get_items.values():
                item.relocate()

        for player in self.get_players.values():
            player.relocate()
            for tool in player.get_tools.values():
                tool.relocate()
                for item in tool.get_items.values():
                    item.relocate()

        self.relocate()

        return self


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Game(BaseGame, DataClassJsonMixin):
    """The main game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()
