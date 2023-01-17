"""Game players classes
"""
from typing import Union
from bgameb.base_ import Base_
# from bgameb.items import BaseItem
# from bgameb.tools import BaseTool


class BasePlayer_(Base_):
    """Base class for players
    """


    # @property
    # def get_items(self) -> dict[str, BaseItem]:
    #     """Get items from Component

    #     Returns:
    #         dict[str, BaseItem]: items mapping
    #     """
    #     return {
    #         key: val for key, val
    #         in self.c.items()
    #         if issubclass(val.__class__, BaseItem)
    #             }

    # @property
    # def get_tools(self) -> dict[str, BaseTool]:
    #     """Get tools from Component

    #     Returns:
    #         dict[str, BaseTool]: tools mapping
    #     """
    #     return {
    #         key: val for key, val
    #         in self.c.items()
    #         if issubclass(val.__class__, BaseTool)
    #             }

    # def add(self, stuff: Union[BaseItem, BaseTool]) -> None:
    #     """Add stuff to component

    #     Args:
    #         stuff (BaseItem|BaseTool): game stuff
    #     """
    #     self.c.update(stuff)
    #     self._logger.info(
    #         f'Component updated by stuff with id="{stuff.id}".'
    #             )


class Player_(BasePlayer_):
    """Player or bot
    """
