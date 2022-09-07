import json
import bgameb
from bgameb.shakers import Shaker
from bgameb.games import GameShakers


class TestGame:
    """Test Game class
    """

    def test_game_class_created_with_name(self) -> None:
        """Test Game name instancing
        """
        game = bgameb.Game()
        assert game.name == 'game', 'wrong default name'
        game = bgameb.Game(name='This Game')
        assert game.name == 'This Game', 'not set name for instance'
        assert isinstance(game.shakers, GameShakers), 'wrong shakers'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        game = bgameb.Game()
        j = json.loads(game.to_json())
        assert j['name'] == 'game', 'not converted to json'

    def test_add_shaker_to_game(self) -> None:
        """Test add component shaker to game
        """
        game = bgameb.Game()
        shaker = Shaker(name='greate_shaker')
        game.add(shaker)
        assert game.shakers.greate_shaker.name == 'greate_shaker', 'shaker not added'
        assert game.shakers.greate_shaker.last == {}, 'wrong last roll'
