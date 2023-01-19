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


class Game_(BaseGame_):
    """The main game object
    """
