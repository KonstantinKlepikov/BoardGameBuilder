import json
import pytest
from collections import Counter
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.errors import StuffDefineError
from tests.conftest import FixedSeed


class TestBaseStuff:
    """Test creation with id and json schemes
    """

    def test_items_classes_created(self) -> None:
        """Test items classes instancing
        """
        obj_ = BaseItem('item')
        assert obj_.id == 'item', 'not set id for instance'
        assert isinstance(obj_.counter, Counter), 'wrong counter type'
        assert len(obj_.counter) == 0, 'counter not empty'
        assert isinstance(obj_.other, dict), 'wrong other'

    def test_items_classes_are_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = BaseItem('item')
        j = json.loads(obj_.to_json())
        assert j['id'] == 'item', 'not converted to json'


class TestStep:
    """Test Step class
    """

    def test_step_instance(self) -> None:
        """Test Step class instance
        """
        obj_ = Step('first_step')
        assert obj_.priority == 0, 'wrong priority'
        obj1 = Step('first_step', priority=20)
        assert obj1.priority == 20, 'wrong priority'
        assert obj1 > obj_, 'wong comparison'


class TestDices:
    """Test Dice class
    """

    def test_dice_instanciation(self) -> None:
        """Test dice correct created
        """
        obj_ = Dice('dice nice')
        assert obj_.id == 'dice nice', 'wrong id'
        assert obj_.sides == 2, 'wrong sides'
        assert obj_.count == 1, 'wrong count'
        assert len(obj_._range) == 2, 'wrong range'
        assert isinstance(obj_.mapping, dict), 'wrong mapping'
        assert len(obj_.mapping) == 0, 'wrong maping len'
        assert obj_.last_roll is None, 'wrong last'
        assert obj_.last_roll_mapped is None, 'wrong last_mapped'

    def test_dice_type_have_sides_defined_less_than_two(self) -> None:
        """Test dice class initialised with less than 2 sides
        """
        with pytest.raises(
            StuffDefineError,
            match='Needed >= 2'
                ):
            Dice('base', sides=1)

    def test_dice_roll(self) -> None:
        """Test dice roll()
        """
        obj_ = Dice('dice', count=5)
        with FixedSeed(42):
            result = obj_.roll()
            assert isinstance(result, list), 'roll returns not list'
            assert len(result) == 5, 'wrong count of rolls'
            assert result == [2, 1, 1, 1, 2], \
                'wrong result'
            assert obj_.last_roll == result, 'wrong last'

    def test_mapping_must_contain_keys_equal_range(self) -> None:
        """Test mapping for dice must define correct
        number of embeddings
        """
        with pytest.raises(
            StuffDefineError,
            match='Mapping must define values for each side.'
                ):
            Dice('base', mapping={1: 'this'})
        with pytest.raises(
            StuffDefineError,
            match='Mapping must define values for each side.'
                ):
            Dice('base', mapping={1: 'this', 3: 'that'})
        dice = Dice('base', mapping={1: 'this', 2: 'that'})
        assert dice.roll_mapped(), 'no result'

    def test_dice_roll_mapping(self) -> None:
        """Test roll_mapping()
        """
        obj_ = Dice('dice', count=5, mapping={1: 'this', 2: 'that'})
        with FixedSeed(42):
            result = obj_.roll_mapped()
            assert isinstance(result, list), 'roll returns not list'
            assert len(result) == 5, 'wrong count of rolls'
            assert result == ['that', 'this', 'this', 'this', 'that'], \
                'wrong result'
            assert obj_.last_roll_mapped == result, 'wrong last_mapped'

    def test_roll_mapped_return_only_mapped_result(self) -> None:
        """Test roll maped return only maped result. If no mapping
        - is empty list returned
        """
        obj_ = Dice('dice', count=5)
        result = obj_.roll_mapped()
        assert isinstance(result, list), 'roll returns not list'
        assert len(result) == 0, 'wrong count of rolls'


class TestCard:
    """Test Card classes"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        obj_ = Card('card')
        assert obj_.id == 'card', 'wrong name'
        assert obj_.opened is False, 'card is opened'
        assert obj_.tapped is False, 'card is tapped'
        assert obj_.side is None, 'defined wrong side'
        assert obj_.count == 1, 'wrong count'

    def test_flip(self) -> None:
        """Test flip card
        """
        obj_ = Card('card')
        obj_ = obj_.flip()
        assert isinstance(obj_, Card), 'wrong return'
        assert obj_.opened, 'card not oppened'
        obj_.flip()
        assert not obj_.opened, 'card oppened'

    def test_open(self) -> None:
        """Test face up opened card
        """
        obj_ = Card('card')
        obj_ = obj_.open()
        assert isinstance(obj_, Card), 'wrong return'
        assert obj_.opened, 'card not opened'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        obj_ = Card('card')
        obj_.opened = True
        obj_ = obj_.hide()
        assert isinstance(obj_, Card), 'wrong return'
        assert not obj_.opened, 'card not opened'

    def test_tap_tap_card_and_set_side(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card('card')
        obj_ = obj_.tap(side='left')
        assert isinstance(obj_, Card), 'wrong return'
        assert obj_.tapped, 'card not tapped'
        assert obj_.side == 'left', 'wrong side'

    def test_untap_card(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card('card')
        obj_.tapped = True
        assert obj_.tapped, 'card not tapped'
        obj_.side = 'left'
        obj_ = obj_.untap()
        assert isinstance(obj_, Card), 'wrong return'
        assert not obj_.tapped, 'card not untapped'
        assert obj_.side is None, 'wrong side'
