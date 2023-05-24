import pytest
from bgameb import Game, Components


class TestGame:
    """Test game
    """

    def test_game_init(self) -> None:
        """Test game init
        """
        G = Game(id="this game")
        assert G.id == 'this game', 'wrong game'

    @pytest.mark.skip("Fail because problem with init inside container")
    def test_game_inherit(self) -> None:
        """Test Game ingerit
        """
        class MyGame(Game):
            c: Components

        G = MyGame(id='this', c=Components())
        assert G.id == 'this', 'wrong game'
        assert isinstance(G.c, Components), 'wrong components'
