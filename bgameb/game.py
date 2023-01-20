"""Main engine to create game
"""
from bgameb.base import Base


class BaseGame(Base):

    def __init__(self, **data):
        super().__init__(**data)

        self._logger.info('===========NEW GAME============')
        self._logger.info(
            f'{self.__class__.__name__} created with id="{self.id}".'
                )


class Game(BaseGame):
    """The main game object
    """
