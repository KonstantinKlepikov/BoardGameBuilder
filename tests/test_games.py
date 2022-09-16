import json, pytest
from bgameb.game import Game, Components
from bgameb.stuff import Dice, Coin, Card
from bgameb.errors import ComponentClassError


class TestGame:
    """Test Game class
    """

    rollers = [
        (Dice, 'dice'),
        (Coin, 'coin'),
    ]
    cards = [
        (Card, 'card'),
    ]

    def test_game_class_created_with_name(self) -> None:
        """Test Game name instancing
        """
        assert Game.name == None, 'Game has name'
        game = Game()
        assert isinstance(game.name, str), 'wrong default name'
        game = Game(name='This Game')
        assert game.name == 'This Game', 'not set name for instance'
        assert isinstance(game.game_rollers, Components), 'wrong rollers'
        assert isinstance(game.game_cards, Components), 'wrong cards'
        assert isinstance(game.shakers, Components), 'wrong shakers'
        assert isinstance(game.decks, Components), 'wrong decks'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        game = Game(name='game')
        j = json.loads(game.to_json())
        assert j['name'] == 'game', 'not converted to json'

    @pytest.mark.parametrize("_class, name", rollers)
    def test_add_stuff_rollers_to_game(self, _class, name: str) -> None:
        """Test we can add rollers to game
        """
        game = Game(name='game')
        game.add_stuff(_class, name=name)
        assert game.game_rollers[name].name == name, 'roller not added'

    @pytest.mark.parametrize("_class, name", cards)
    def test_add_stuff_cards_to_game(self, _class, name: str) -> None:
        """Test we can add rollers to game
        """
        game = Game(name='game')
        game.add_stuff(_class, name=name)
        assert game.game_cards[name].name == name, 'card not added'

    def test_add_stuff_noncomponent_class(self) -> None:
        """Test add noncomponent class
        """
        game = Game(name='game')
        with pytest.raises(
            ComponentClassError,
            match="Given class"
            ):
            game.add_stuff(Game)

    def test_add_shaker(self) -> None:
        """Test add shaker to game
        """
        game = Game(name='game')
        game.add_shaker(name='shaker')
        assert game.shakers.shaker.name == 'shaker', 'shaker not added'
        game.add_shaker('this')
        assert game.shakers.this.name == 'this', 'shaker not added'
