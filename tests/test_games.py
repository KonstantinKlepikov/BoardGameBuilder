import json, pytest
from typing import Tuple
from bgameb.game import Game, Shaker, Components
from bgameb.stuff import Dice, Coin, Card, BaseRoller
from bgameb.errors import (
    ComponentNameError, ComponentClassError, RollerDefineError
)


class TestComponents:
    """Test CardText class
    """

    components = [
        (Dice, 'dice'),
        (Coin, 'coin'),
        (Card, 'card'),
    ]

    @pytest.mark.parametrize("_class, name", components)
    def test_components_access_to_attr(self, _class, name: str) -> None:
        """Test components acces to attrs
        """
        comp = Components()
        comp.__dict__.update({'some': _class(name=name), 'many': _class(name=name)})

        assert comp.some.name == name, 'not set or cant get'
        assert comp['some'].name == name, 'not set or cant get'

        with pytest.raises(
            NotImplementedError,
            match='This method not implementd for Components',
            ):
            comp.this = _class(name=name)
        with pytest.raises(
            NotImplementedError,
            match='This method not implementd for Components',
            ):
            comp['that'] = _class(name=name)

        del comp.some
        with pytest.raises(AttributeError, match='some'):
            comp.some
        with pytest.raises(KeyError, match='some'):
            comp['some']

        with pytest.raises(AttributeError, match='newer'):
            del comp.newer
        with pytest.raises(KeyError, match='newer'):
            del comp['newer']

    @pytest.mark.parametrize("_class, name", components)
    def test_components_repr(self, _class, name: str) -> None:
        """Test components repr
        """
        comp = Components()
        comp.__dict__.update({'some': _class(name=name)})
        assert "Components(some=" in comp.__repr__(), 'wrong repr'

    @pytest.mark.parametrize("_class, name", components)
    def test_components_len(self, _class, name: str) -> None:
        """Test components len
        """
        comp1 = Components()
        comp2 = Components()
        comp1.__dict__.update({'some':_class(name=name)})
        assert len(comp1) == 1, 'wrong len'
        assert len(comp2) == 0, 'wrong len'

    @pytest.mark.parametrize("_class, name", components)
    def test_components_items(self, _class, name: str) -> None:
        """Test components items access
        """
        comp = Components()
        comp.__dict__.update({'some': _class(name=name)})
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

    @pytest.mark.parametrize("_class, name", components)
    def test_add_component(self, _class, name: str) -> None:
        """Test add component with add() method
        """
        comp = Components()
        comp.add(_class, name=name)
        assert comp[name], 'component not added'
        with pytest.raises(
            ComponentNameError,
            match=name
        ):
            comp.add(_class, name=name)
        comp.add(Dice, name='this_is')
        assert comp.this_is, 'component not added'
        with pytest.raises(
            ComponentNameError,
            match='this_is'
        ):
            comp.add(_class, name='this_is')
        if isinstance(_class, BaseRoller):
            comp.add(_class, name='this_is_five', sides=5)
            assert comp.this_is_five.sides == 5, 'component not added'

    @pytest.mark.parametrize("_class, name", components)
    def test_add_replace_component(self, _class, name: str) -> None:
        """Test add_replace() method
        """
        comp = Components()
        comp.add_replace(_class, name=name)
        add1 = id(comp[name])
        assert comp[name], 'component not added'
        comp.add_replace(_class, name=name)
        assert id(comp[name]) != add1, 'not replaced'
        comp.add(_class, name='this_is')
        assert comp.this_is, 'component not added'
        if isinstance(_class, BaseRoller):
            comp.add(_class, name='this_is_five', sides=5)
            assert comp.this_is_five.sides == 5, 'component not added'

    @pytest.mark.parametrize("_class, name", components)
    def test_get_names(self, _class, name: str) -> None:
        """Test get_names() method
        """
        comp = Components()
        assert comp.get_names() == [], 'nonempty list of names'
        comp.add(_class, name=name)
        assert comp.get_names() == [name], 'empty list of names'
        comp.add(_class, name='this')
        assert comp.get_names() == [name, 'this'], 'empty list of names'

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
        assert isinstance(game.shakers, Components), 'wrong shakers'

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


class TestGameShaker:
    """Test Shaker class
    """

    @pytest.fixture(params=[
        (Dice, 'dice'),
        (Coin, 'coin'),
        ])
    def rollers(self, request) -> Tuple[Components, str]:
        game = Game(name='game')
        game.add_stuff(request.param[0], name=request.param[1])
        return game.game_rollers, request.param[1]

    def test_shaker_instanciation(self, rollers: Tuple[Components, str]) -> None:
        """Test shaker correct created
        """
        assert not Shaker.name, 'Shaker class has name'
        shaker = Shaker(rollers[0])
        assert isinstance(shaker.name, str), 'wrong name'
        assert isinstance(shaker.last, dict), 'nondict last'
        assert isinstance(shaker.rollers, dict), 'nondict rollers'
        assert len(shaker.rollers) == 0, 'nonempty rollers'

    def testadd_rollers_to_shaker_raise_errors_if_wrong_count(
        self, rollers: Tuple[Components, str]
            ) -> None:
        """Test need count of rollers no less than 1
        """
        shaker = Shaker(rollers[0], name='shaker')
        with pytest.raises(
            RollerDefineError, match='Need at least one roller'
            ):
            shaker.add(rollers[1], count=0)

    def testadd_rollers_to_shaker_raise_errors_if_wrong_name(
        self, rollers: Tuple[Components, str]
            ) -> None:
        """Test need exist roller
        """
        shaker = Shaker(rollers[0], name='shaker')
        with pytest.raises(
            RollerDefineError, match="'somestuff' not exist in a game"
            ):
            shaker.add('somestuff')

    def testadd_rollers_to_shaker(self, rollers: Tuple[Components, str]) -> None:
        """Test shaker add()
        """
        shaker = Shaker(rollers[0], name='shaker')
        shaker.add(rollers[1])
        assert shaker.rollers == {'colorless': {rollers[1]: 1}}, 'wrong roller added'
        shaker.add(rollers[1], color="white")
        assert shaker.rollers == {
            'colorless': {rollers[1]: 1},
            'white': {rollers[1]: 1},
            }, 'wrong roller added'
        shaker.add(rollers[1], count=50)
        assert shaker.rollers == {
            'colorless': {rollers[1]: 51},
            'white': {rollers[1]: 1},
            }, 'wrong roller added'
        shaker.add(rollers[1], color='red', count=50)
        assert shaker.rollers == {
            'colorless': {rollers[1]: 51},
            'white': {rollers[1]: 1},
            'red': {rollers[1]: 50},
            }, 'wrong roller added'

    def test_shaker_are_converted_to_json(self, rollers: Tuple[Components, str]) -> None:
        """Test to json convertatrion
        """
        shaker = Shaker(rollers[0], name='shaker')
        shaker.add(rollers[1])
        j = json.loads(shaker.to_json())
        assert j['name'] == 'shaker', 'wrong name'
        assert j['last'] == {}, 'wrong name'
        assert len(j['rollers']['colorless']) == 1, 'wrong num of rollers'

    def test_remove_all(self, rollers: Tuple[Components, str]) -> None:
        """Test remove all rollers from shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove_all()
        assert len(shaker.rollers) == 0, 'wrong number of rollers'
        assert isinstance(shaker.rollers, dict), 'wrong type os rollers attr'

    def test_remove_by_colors(self, rollers: Tuple[Components, str]) -> None:
        """Test remove rollers by color from shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove_all_by_color(color='white')
        assert len(shaker.rollers) == 2, 'wrong number of rollers'

    def test_remove_by_name(self, rollers: Tuple[Components, str]) -> None:
        """Test remove rollers by name from shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        rollers[0].__dict__.update({'this': Dice('this')})
        shaker.add('this', color='white')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        assert len(shaker.rollers['white']) == 2, 'wrong number of rollers'
        shaker.remove_all_by_name(name='this')
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        assert len(shaker.rollers['white']) == 1, 'wrong number of rollers'
        shaker.remove_all_by_name(name=rollers[1])
        assert len(shaker.rollers) == 0, 'wrong number of rollers'

    def test_remove_rollers(self, rollers: Tuple[Components, str]) -> None:
        """Test remove rollers
        """
        shaker = Shaker(rollers[0], name='shaker')
        rollers[0].__dict__.update({'this': Dice('this')})
        shaker.add('this', color='white')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i, count=5)

        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove(rollers[1], color="red", count=3)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        assert shaker.rollers['red'][rollers[1]] == 2, \
            'wrong count of rollers'
        shaker.remove(rollers[1], color="red", count=50)
        assert len(shaker.rollers) == 2, 'wrong number of rollers'
        with pytest.raises(
            RollerDefineError, match="Need at least one roller"
        ):
            shaker.remove(rollers[1], color="white", count=0)
        with pytest.raises(
            RollerDefineError, match="Roller with color"
        ):
            shaker.remove(rollers[1], color="black", count=1)
        with pytest.raises(
            RollerDefineError, match="Roller with name"
        ):
            shaker.remove('who', color="white", count=1)
        with pytest.raises(
            RollerDefineError, match="Roller with name"
        ):
            shaker.remove('this', color="green", count=50)

    def test_roll_shaker(self, rollers: Tuple[Components, str]) -> None:
        """Test roll shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        for i in ['white', 'red', 'white']:
            shaker.add(rollers[1], color=i)
        roll = shaker.roll()
        assert len(roll['red'][rollers[1]]) == 1, 'wrong roll result'
        assert len(roll['white'][rollers[1]]) == 2, 'wrong roll result'
        assert isinstance(roll['white'][rollers[1]][0], int), 'wrong roll result'
        assert len(shaker.last) == 2, 'wrong last'

    def test_roll_empty_shaker(self, rollers: Tuple[Components, str]) -> None:
        """Test roll empty shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        roll = shaker.roll()
        assert roll == {}, 'wrong roll result'
        assert shaker.last == {}, 'wrong last'
