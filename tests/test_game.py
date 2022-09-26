import json, pytest
from bgameb.game import Game, Components
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
        assert Game.name == None, 'Game has name'
        game = Game()
        assert isinstance(game.name, str), 'wrong default name'
        game = Game(name='This Game')
        assert game.name == 'This Game', 'not set name for instance'
        assert isinstance(game.stuff, Components), 'wrong stuff'
        assert isinstance(game.tools, Components), 'wrong tools'
        assert isinstance(game.players, Components), 'wrong players'

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
            assert game.stuff[n].name == n, 'stuff not added'
        for n in TOOLS.keys():
            game.add(n, name=n)
            assert game.tools[n].name == n, 'tool not added'
        for n in PLAYERS.keys():
            game.add(n, name=n)
            assert game.players[n].name == n, 'player not added'

    def test_add_component_with_kwargs(self) -> None:
        """Test add with kwargs
        """
        game = Game(name='game')
        game.add('roller', name='dice', sides=42)
        assert game.stuff.dice.sides == 42, 'wrong count'

    def test_add_wrong_component_to_game(self) -> None:
        """Test we cant add notexisted tool or stuff to game
        """
        game = Game(name='game')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
            ):
            game.add('chocho', name='this')
