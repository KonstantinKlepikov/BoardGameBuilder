import json
import pytest
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
        j: dict = json.loads(game.json())
        assert j['id'] == 'game', \
            'not converted to json'
