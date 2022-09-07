import json, pytest
import bgameb
from bgameb.shakers import Shaker
from bgameb.rollers import Dice, Coin
from bgameb.errors import ComponentNameError
from bgameb.games import GameShakers, Components


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
        print(comp)
        assert comp.this_is_five.sides == 5, 'component not added'

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
