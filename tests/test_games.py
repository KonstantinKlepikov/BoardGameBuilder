import json, pytest
from bgameb.games import Game
from bgameb.shakers import Shaker
from bgameb.rollers import Dice, Coin
from bgameb.cards import Card
from bgameb.errors import ComponentNameError, ComponentClassError
from bgameb.games import Components


class TestComponents:
    """Test CardText class
    """

    def test_components_access_to_attr(self) -> None:
        """Test components acces to attrs
        """
        comp = Components()
        comp.__dict__.update({'some': Dice(), 'many': Dice()})

        assert comp.some.name == 'dice', 'not set or cant get'
        assert comp['some'].name == 'dice', 'not set or cant get'

        with pytest.raises(
            NotImplementedError,
            match='This method not implementd for Components',
            ):
            comp.this = Dice()
        with pytest.raises(
            NotImplementedError,
            match='This method not implementd for Components',
            ):
            comp['that'] = Dice()

        del comp.some
        with pytest.raises(AttributeError, match='some'):
            comp.some
        with pytest.raises(KeyError, match='some'):
            comp['some']

        with pytest.raises(AttributeError, match='newer'):
            del comp.newer
        with pytest.raises(KeyError, match='newer'):
            del comp['newer']

    def test_components_repr(self) -> None:
        """Test components repr
        """
        comp = Components()
        comp.__dict__.update({'some': Dice()})
        assert "Components(some=" in comp.__repr__(), 'wrong repr'

    def test_components_len(self) -> None:
        """Test equal of CardTexts
        """
        comp1 = Components()
        comp2 = Components()
        comp1.__dict__.update({'some': Dice()})
        assert len(comp1) == 1, 'wrong len'
        assert len(comp2) == 0, 'wrong len'

    def test_components_items(self) -> None:
        """Test components items access
        """
        comp = Components()
        comp.__dict__.update({'some': Dice()})
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

    def test_add_component(self) -> None:
        """Test add component with add() method
        """
        comp = Components()
        comp.add(Dice)
        assert comp[Dice.name], 'component not added'
        with pytest.raises(
            ComponentNameError,
            match=Dice.name
        ):
            comp.add(Dice)
        comp.add(Dice, name='this_is')
        assert comp.this_is, 'component not added'
        with pytest.raises(
            ComponentNameError,
            match='this_is'
        ):
            comp.add(Dice, name='this_is')
        comp.add(Dice, name='this_is_five', sides=5)
        assert comp.this_is_five.sides == 5, 'component not added'

class TestGame:
    """Test Game class
    """

    rollers = [
        (Dice, Dice.name),
        (Coin, Coin.name),
    ]
    shakers = [
        (Shaker, Shaker.name),
    ]
    cards = [
        (Card, Card.name),
    ]

    def test_game_class_created_with_name(self) -> None:
        """Test Game name instancing
        """
        game = Game()
        assert game.name == 'game', 'wrong default name'
        game = Game(name='This Game')
        assert game.name == 'This Game', 'not set name for instance'
        assert isinstance(game.rollers, Components), 'wrong rollers'
        assert isinstance(game.shakers, Components), 'wrong shakers'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        game = Game()
        j = json.loads(game.to_json())
        assert j['name'] == 'game', 'not converted to json'

    @pytest.mark.parametrize("_class, name", shakers)
    def test_add_shakers_to_game(self, _class, name: str) -> None:
        """Test add component shaker to game
        """
        game = Game()
        game.add(_class)
        assert game.shakers[name].name == name, 'shakers not added'

    @pytest.mark.parametrize("_class, name", rollers)
    def test_add_rollers_to_game(self, _class, name: str) -> None:
        """Test we can add rollers to game
        """
        game = Game()
        game.add(_class)
        assert game.rollers[name].name == name, 'roller not added'

    @pytest.mark.parametrize("_class, name", cards)
    def test_add_cards_to_game(self, _class, name: str) -> None:
        """Test we can add rollers to game
        """
        game = Game()
        game.add(_class)
        assert game.cards[name].name == name, 'card not added'

    def test_add_noncomponent_class(self) -> None:
        """Test add noncomponent class
        """
        game = Game()
        with pytest.raises(
            ComponentClassError,
            match="Given class"
            ):
            game.add(Game)
