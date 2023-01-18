"""Main engine to create game
"""
from bgameb.base_ import Base_


class BaseGame_(Base_):

    def __init__(self, **data):
        super().__init__(**data)

        self._logger.info('===========NEW GAME============')
        self._logger.info(
            f'{self.__class__.__name__} created with id="{self.id}".'
                )

    # def relocate_all(self) -> 'BaseGame':
    #     """Relocate all objects in game

    #     Returns:
    #         BaseGame
    #     """
    #     for item in self.get_items.values():
    #         item.relocate(), Component

    #     for tool in self.get_tools.values():
    #         tool.relocate()
    #         for item in tool.get_items.values():
    #             item.relocate()

    #     for player in self.get_players.values():
    #         player.relocate()
    #         for tool in player.get_tools.values():
    #             tool.relocate()
    #             for item in tool.get_items.values():
    #                 item.relocate()

    #     self.relocate()

    #     return self


class Game_(BaseGame_):
    """The main game object
    """
