import json
import pytest
from loguru._logger import Logger
from collections import Counter
from bgameb.game import Game


class TestGame:
    """Test Game class
    """

    @pytest.fixture(scope='function')
    def game(self) -> Game:
        return Game(id='game')

    def test_game_class_created(self, game: Game) -> None:
        """Test Game instancing
        """
        assert game.id == 'game', 'not set id for instance'
        assert isinstance(game.counter, Counter), 'wrong counter type'
        assert len(game.counter) == 0, 'counter not empty'
        assert isinstance(game._to_relocate, dict), 'wrong _to_relocate'
        assert isinstance(game._logger, Logger), 'wrong _to_relocate'
        j : dict = json.loads(game.json())
        assert json.loads(game.json())['id'] == 'game', \
            'not converted to json'
        assert j.get('counter') is None, 'counter not excluded'
        assert j.get('_to_relocate') is None, '_to_relocat not excluded'
        assert j.get('_logger') is None, '_logger not excluded'
