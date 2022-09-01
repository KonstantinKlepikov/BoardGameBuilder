import json
import bgameb


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


    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        game = bgameb.Game()
        j = json.loads(game.to_json())
        assert j['name'] == 'game', 'not converted to json'
