import json
import pytest
from collections import Counter
from bgameb.stuff import Dice, Card, Step
from bgameb.errors import StuffDefineError


class TestBaseStuff:
    """Test creation with names and json schemes
    """
    params = [
        (Dice, 'dice'),
        (Card, 'card'),
        ]

    @pytest.mark.parametrize("_class, name", params)
    def test_stuff_classes_created_with_name(self, _class, name: str) -> None:
        """Test stuff classes instancing
        """
        obj_ = _class(name='this_stuff')
        assert obj_.name == 'this_stuff', 'not set name for instance'
        assert obj_.count == 1, 'wrong count'

    @pytest.mark.parametrize("_class, name", params)
    def test_stuff_classes_are_converted_to_json(
        self, _class, name: str
            ) -> None:
        """Test to json convertatrion
        """
        obj_ = _class(name=name)
        j = json.loads(obj_.to_json())
        assert j['name'] == name, 'not converted to json'


class TestStep:
    """Test Step class
    """

    def test_step_instance(self) -> None:
        """Test Step class instance
        """
        obj_ = Step(name='first_step')
        assert obj_.priority == 0, 'wrong priority'
        assert obj_._type == 'step', 'wrong type'
        obj1 = Step(name='first_step', priority=20)
        assert obj1.priority == 20, 'wrong priority'
        assert obj1 > obj_, 'wong comparison'


class TestDices:
    """Test Dice class
    """

    def test_dice_instanciation(self) -> None:
        """Test dice correct created
        """
        obj_ = Dice(name='dice')
        assert obj_.name == 'dice', 'wrong name'
        assert obj_.sides == 2, 'wrong sides'
        assert obj_.count == 1, 'wrong count'
        assert len(obj_._range) == 2, 'wrong range'

    def test_dice_type_have_sides_defined_less_than_two(self) -> None:
        """Test dice class initialised with less than 2 sides
        """
        with pytest.raises(
            StuffDefineError,
            match='Needed >= 2'
                ):
            Dice(name='base', sides=1)

    def test_dice_roll(self) -> None:
        """Test dice roll return result
        """
        obj_ = Dice(name='dice', count=5)
        result = obj_.roll()
        assert isinstance(result, list), 'roll returns not list'
        assert len(result) == 5, 'wrong count of rolls'
        assert isinstance(result[0], int), 'ot an int in a list'
        obj_ = Dice(name='dice')
        result = obj_.roll()
        assert len(result) == 1, 'is rolled, but count is 0'


class TestCard:
    """Test Card classes"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        obj_ = Card(name='card')
        assert obj_.name == 'card', 'wrong name'
        assert obj_.open is False, 'card is open'
        assert obj_.tapped is False, 'card is tapped'
        assert obj_.side is None, 'defined wrong side'
        assert obj_.count == 1, 'wrong count'
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
