import json, pytest
from collections import Counter
from bgameb.stuff import Roller, Card
from bgameb.errors import StuffDefineError


class TestBaseStuff:
    """Test creation with names and json schemes
    """
    params = [
        (Roller, 'roller'),
        (Card, 'card'),
        ]

    @pytest.mark.parametrize("_class, name", params)
    def test_stuff_classes_created_with_name(self, _class, name: str) -> None:
        """Test stuff classes instancing
        """
        obj_= _class(name='this_stuff')
        assert obj_.name == 'this_stuff', 'not set name for instance'
        assert obj_.is_active, 'wrong is_active'
        assert obj_.rules == [], 'no rules'

    @pytest.mark.parametrize("_class, name", params)
    def test_stuff_classes_are_converted_to_json(self, _class, name: str) -> None:
        """Test to json convertatrion
        """
        obj_ = _class(name=name)
        j = json.loads(obj_.to_json())
        assert j['name'] == name, 'not converted to json'


class TestRollers:
    """Test RollerType class
    """

    def test_roller_instanciation(self) -> None:
        """Test roller correct created
        """
        obj_ = Roller(name='dice')
        assert obj_.name == 'dice', 'wrong name'
        assert obj_.is_active, 'wrong is_active'
        assert obj_.sides == 2, 'wrong sides'
        assert obj_.count == 1, 'wrong count'
        assert obj_.rules == [], 'no rules'
        assert len(obj_._range) == 2, 'wrong range'

    def test_roller_type_have_sides_defined_less_than_two(self) -> None:
        """Test roller class initialised with less than 2 sides
        """
        with pytest.raises(
            StuffDefineError,
            match='Needed >= 2'
            ):
            Roller(name='base', sides=1)

    def test_roller_roll(self) -> None:
        """Test roller roll return result
        """
        obj_ = Roller(name='dice', count=5)
        result = obj_.roll()
        assert isinstance(result, list), 'roll returns not list'
        assert len(result) == 5, 'wrong count of rolls'
        assert isinstance(result[0], int), 'ot an int in a list'
        obj_ = Roller(name='dice')
        result = obj_.roll()
        assert len(result) == 1, 'is rolled, but count is 0'


class TestCard:
    """Test Card classes"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        obj_ = Card(name='card')
        assert obj_.name == 'card', 'wrong name'
        assert obj_.is_active, 'wrong is_active'
        assert obj_.open == False, 'card is open'
        assert obj_.tapped == False, 'card is tapped'
        assert obj_.side == None, 'defined wrong side'
        assert obj_.count == 1, 'wrong count'
        assert obj_.rules == [], 'no rules'
        assert isinstance(obj_.counter, Counter), 'wrong counter'

    def test_flip(self) -> None:
        """Test flip card
        """
        obj_ = Card(name='card')
        obj_.flip()
        assert obj_.open, 'card not oppened'
        obj_.flip()
        assert not obj_.open, 'card oppened'

    def test_fase_up(self) -> None:
        """Test face up open card
        """
        obj_ = Card(name='card')
        obj_.face_up()
        assert obj_.open, 'card not open'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        obj_ = Card(name='card')
        obj_.open = True
        obj_.face_down()
        assert not obj_.open, 'card not open'

    def test_tap_tap_card_and_set_side(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card(name='card')
        obj_.tap(side='left')
        assert obj_.tapped, 'card not tapped'
        assert obj_.side == 'left', 'wrong side'

    def test_untap_card(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card(name='card')
        obj_.tapped = True
        assert obj_.tapped, 'card not tapped'
        obj_.untap()
        assert not obj_.tapped, 'card not untapped'
