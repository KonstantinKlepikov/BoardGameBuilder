import json
import bgameb


class TestGame:
    """Test Game class
    """

    def test_game_class_created_with_name(self):
        """Test Game is created with default name or implent name
        given to instance
        """
        game = bgameb.Game()
        assert game.name == 'Game', 'wrong default name'
        game = bgameb.Game(name='This Game')
        assert game.name == 'This Game', 'not set name for instance'


    def test_game_class_is_converted_to_json(self):
        """Test to json convertatrion
        """
        game = bgameb.Game()
        j = json.loads(game.to_json())
        assert j['name'] == 'Game', 'not converted to json'
