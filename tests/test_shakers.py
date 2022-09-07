import pytest, json
from bgameb.shakers import Shaker, RollerDefineError
from bgameb.rollers import Dice, Coin, BaseRoller


class TestShaker:
    """Test Shaker class
    """

    @pytest.fixture(params=[Dice, Coin])
    def rollers(self, request) -> BaseRoller:
        return request.param

    def test_shaker_instanciation(self) -> None:
        """Test shaker correct created
        """
        shaker = Shaker()
        assert shaker.name == 'shaker', 'wrong name'
        assert isinstance(shaker.last, dict), 'nondict last'
        assert isinstance(shaker.rollers, dict), 'nondict rollers'
        assert len(shaker.rollers) == 0, 'nonempty rollers'

    def test_add_rollers_to_shaker_raise_errors(self, rollers: BaseRoller) -> None:
        """Test need count of rollears mo less than 1
        """
        shaker = Shaker()
        roller = rollers()
        with pytest.raises(
            RollerDefineError, match='Need at least one roller'
        ):
            shaker.add(roller, count=0)

    def test_add_rollers_to_shaker(self, rollers: BaseRoller) -> None:
        """Test shaker add()
        """
        shaker = Shaker()
        roller = rollers()
        shaker.add(roller)
        assert shaker.rollers == {
            'white': {roller.name: {'roller': roller, 'count': 1}}
            }, 'roller added wrong'
        shaker.add(roller)
        assert shaker.rollers == {
            'white': {roller.name: {'roller': roller, 'count': 2}}
            }, 'roller added wrong'
        shaker.add(roller, count=50)
        assert shaker.rollers == {
            'white': {roller.name: {'roller': roller, 'count': 52}}
            }, 'roller added wrong'
        shaker.add(roller, color='red', count=50)
        assert shaker.rollers == {
            'white': {roller.name: {'roller': roller, 'count': 52}},
            'red': {roller.name: {'roller': roller, 'count': 50}},
            }, 'roller added wrong'

    def test_cant_be_added_different_instancers_with_same_names(
        self, rollers: BaseRoller
            ) -> None:
        """To chsker cant be added different instances with the same name
        """
        shaker = Shaker()
        roller1 = rollers()
        roller2 = rollers()
        assert roller1 is not roller2, 'same instances'
        shaker.add(roller1)
        with pytest.raises(
            RollerDefineError,
            match="Different instances of roller class"
        ):
            shaker.add(roller2)

    def test_shaker_are_converted_to_json(self, rollers: BaseRoller) -> None:
        """Test to json convertatrion
        """
        shaker = Shaker()
        roller = rollers()
        shaker.add(roller)
        j = json.loads(shaker.to_json())
        assert j['name'] == 'shaker', 'wrong name'
        assert j['last'] == {}, 'wrong name'
        assert len(j['rollers']['white']) == 1, 'wrong num of rollers'

    def test_remove_all(self, rollers: BaseRoller) -> None:
        """Test remove all rollers from shaker
        """
        shaker = Shaker()
        for i, j in [('this', 'white'), ('that', 'red'), ('some', 'green')]:
            roller = rollers(i)
            shaker.add(roller, color=j)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove_all()
        assert len(shaker.rollers) == 0, 'wrong number of rollers'
        assert isinstance(shaker.rollers, dict), 'wrong type os rollers attr'

    def test_remove_by_colors(self, rollers: BaseRoller) -> None:
        """Test remove rollers by color from shaker
        """
        shaker = Shaker()
        for i, j in [('this', 'white'), ('that', 'red'), ('some', 'green')]:
            roller = rollers(i)
            shaker.add(roller, color=j)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove_all_by_color(color='white')
        assert len(shaker.rollers) == 2, 'wrong number of rollers'

    def test_remove_by_name(self, rollers: BaseRoller) -> None:
        """Test remove rollers by name from shaker
        """
        shaker = Shaker()
        for i, j in [('this', 'white'), ('that', 'red'),
            ('this', 'green'), ('some', 'yellow'), ('that', 'yellow')]:
            roller = rollers(i)
            shaker.add(roller, color=j)
        assert len(shaker.rollers) == 4, 'wrong number of rollers'
        shaker.remove_all_by_name(name='that')
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove_all_by_name(name='some')
        assert len(shaker.rollers) == 2, 'wrong number of rollers'

    def test_remove_rollers(self, rollers: BaseRoller) -> None:
        """Test remove rollers
        """
        shaker = Shaker()
        for i, j in [
            ('this', 'white'), ('that', 'red'), ('this', 'green')
            ]:
            roller = rollers(i)
            shaker.add(roller, color=j, count=5)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove('this', color="white", count=3)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        assert shaker.rollers['white']['this']['count'] == 2, \
            'wrong count of rollers'
        shaker.remove('this', color="white", count=50)
        assert len(shaker.rollers) == 2, 'wrong number of rollers'
        with pytest.raises(
            RollerDefineError, match="Need at least one roller"
        ):
            shaker.remove('that', color="white", count=0)
        with pytest.raises(
            RollerDefineError, match="Cant find roller with collor"
        ):
            shaker.remove('that', color="black", count=1)
        with pytest.raises(
            RollerDefineError, match="Cant find roller with name"
        ):
            shaker.remove('who', color="red", count=1)
        with pytest.raises(
            RollerDefineError, match="Cant find roller with name"
        ):
            shaker.remove('that', color="green", count=50)

    def test_roll_shaker(self, rollers: BaseRoller) -> None:
        """Test roll shaker
        """
        shaker = Shaker()
        for i, j in [('this', 'white'), ('that', 'red'), ('some', 'white')]:
            roller = rollers(i)
            shaker.add(roller, color=j, count=2)
        roll = shaker.roll()
        assert len(roll['red']['that']) == 2, 'wrong roll result'
        assert len(roll['white']) == 2, 'wrong roll result'
        assert isinstance(roll['white']['some'][0], int), 'wrong roll result'
        assert len(shaker.last) == 2, 'wrong last'

    def test_roll_empty_shaker(self) -> None:
        """Test roll empty shaker
        """
        shaker = Shaker()
        roll = shaker.roll()
        assert roll == {}, 'wrong roll result'
        assert shaker.last == {}, 'wrong last'
