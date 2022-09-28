import json, pytest
from bgameb.game import Game
from bgameb.base import Components
from bgameb.stuff import STUFF
from bgameb.tools import TOOLS
from bgameb.players import PLAYERS
from bgameb.errors import ComponentClassError


class TestGame:
    """Test Game class
    """

    def test_game_class_created_with_name(self) -> None:
        """Test Game name instancing
        """
        game = Game(name='this_game')
        assert game.name == 'this_game', 'not set name for instance'
        assert isinstance(game, Components), 'isnt component'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        game = Game(name='game')
        j = json.loads(game.to_json())
        assert j['name'] == 'game', 'not converted to json'

    def test_add_component(self) -> None:
        """Test add tool or stuff to game
        """
        game = Game(name='game')
        for n in STUFF.keys():
            game.add(n, name=n)
            assert game[n].name == n, 'stuff not added'
        for n in TOOLS.keys():
            game.add(n, name=n)
            assert game[n].name == n, 'tool not added'
        for n in PLAYERS.keys():
            game.add(n, name=n)
            assert game[n].name == n, 'player not added'

    def test_add_component_with_kwargs(self) -> None:
        """Test add with kwargs
        """
        game = Game(name='game')
        game.add('roller', name='dice', sides=42)
        assert game.dice.sides == 42, 'wrong count'

    def test_add_wrong_component_to_game(self) -> None:
        """Test we cant add notexisted tool or stuff to game
        """
        game = Game(name='game')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
            ):
            game.add('chocho', name='this')
