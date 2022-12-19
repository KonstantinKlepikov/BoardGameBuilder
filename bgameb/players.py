"""Game players classes
"""
from typing import Union
from dataclasses import dataclass, field
from dataclasses_json import (
    DataClassJsonMixin, dataclass_json, Undefined, config
        )
from bgameb.base import Base, Component
from bgameb.items import BaseItem
from bgameb.tools import BaseTool


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class BasePlayer(Base):

    c: Component[Union[BaseItem, BaseTool]] = field(
        default_factory=Component,
        metadata=config(exclude=lambda x: True),  # type: ignore
            )

    def __post_init__(self) -> None:
        super().__post_init__()
        self.c = Component()

    def add(self, stuff: Union[BaseItem, BaseTool]) -> None:
        """Add stuff to component

        Args:
            stuff (BaseItem|BaseTool): game stuff
        """
        self.c._update(stuff)
        self._logger.info(
            f'Component updated by stuff with id="{stuff.id}".'
                )

    def get_items(self) -> dict[str, BaseItem]:
        """Get items from Component

        Returns:
            dict[str, BaseItem]: items mapping
        """
        return {
            key: val for key, val
            in self.c.__dict__.items()
            if issubclass(val.__class__, BaseItem)
                }

    def get_tools(self) -> dict[str, BaseTool]:
        """Get tools from Component

        Returns:
            dict[str, BaseTool]: tools mapping
        """
        return {
            key: val for key, val
            in self.c.__dict__.items()
            if issubclass(val.__class__, BaseTool)
                }


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Player(BasePlayer, DataClassJsonMixin):
    """Player or bot
    """

    def __post_init__(self) -> None:
        super().__post_init__()
