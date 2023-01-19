import json
import pytest
from collections import Counter
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from loguru._logger import Logger
from bgameb.items_ import Dice_, Card_, Step_, BaseItem_
from bgameb.errors import StuffDefineError
from tests.conftest import FixedSeed


class TestBaseStuff:
    """Test creation with id and json schemes
    """

    @pytest.mark.parametrize("_class,_id", [
        (BaseItem_, 'item'),
        (Dice_, 'dice'),
        (Card_, 'card'),
        (Step_, 'step'),
            ])
    def test_items_classes_created(self, _class, _id: str) -> None:
        """Test items classes instancing
        """
        obj_ = _class(id=_id)
        assert isinstance(obj_, BaseModel), 'wrong instance'
        assert obj_.id == _id, 'not set id for instance'
        assert isinstance(obj_.counter, Counter), 'wrong counter type'
        assert len(obj_.counter) == 0, 'counter not empty'
        assert isinstance(obj_._to_relocate, dict), 'wrong _to_relocate'
        assert isinstance(obj_._logger, Logger), 'wrong _to_relocate'
        j : dict = json.loads(obj_.json())
        assert j['id'] == _id, \
            'not converted to json'
        assert j.get('counter') is None, 'counter not excluded'
        assert j.get('_to_relocate') is None, '_to_relocat not excluded'
        assert j.get('_logger') is None, '_logger not excluded'


class TestStep:
    """Test Step class
    """

    def test_step_instance(self) -> None:
        """Test Step class instance
        """
        obj_ = Step_(id='first_step')
        assert obj_.priority == 0, 'wrong priority'
        obj1 = Step_(id='first_step', priority=20)
        assert obj1.priority == 20, 'wrong priority'
        assert obj1 > obj_, 'wong comparison'
        assert obj1 >= obj_, 'wong comparison'
        assert obj1 != obj_, 'wong comparison'
        assert not obj1 < obj_, 'wong comparison'
        assert not obj1 <= obj_, 'wong comparison'


class TestDices:
    """Test Dice class
    """

    def test_dice_instanciation(self) -> None:
        """Test dice correct created
        """
        obj_ = Dice_(id='dice nice')
        assert obj_.sides == 2, 'wrong sides'
        assert obj_.count == 1, 'wrong count'
        assert len(obj_._range) == 2, 'wrong range'
        assert isinstance(obj_.mapping, dict), 'wrong mapping'
        assert len(obj_.mapping) == 0, 'wrong maping len'
        assert obj_.last_roll == [], 'wrong last'
        assert obj_.last_roll_mapped == [], 'wrong last_mapped'

    def test_comparison_of_dices(self) -> None:
        """Test comparison of dices
        """
        obj_ = Dice_(id='dice nice', sides=3)
        obj1 = Dice_(id='the_dice', sides=30)
        assert obj1 > obj_, 'wong comparison'
        assert obj1 >= obj_, 'wong comparison'
        assert obj1 != obj_, 'wong comparison'
        assert not obj1 < obj_, 'wong comparison'
        assert not obj1 <= obj_, 'wong comparison'

    def test_dice_type_have_sides_defined_less_than_two(self) -> None:
        """Test dice class initialised with less than 2 sides
        """
        with pytest.raises(
            ValidationError,
            match='ensure this value is greater than 1'
                ):
            Dice_(id='base', sides=1)

    def test_dice_roll(self) -> None:
        """Test dice roll()
        """
        obj_ = Dice_(id='dice', count=5)
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
            Dice_(id='base', mapping={1: 'this'})
        with pytest.raises(
            StuffDefineError,
            match='Mapping must define values for each side.'
                ):
            Dice_(id='base', mapping={1: 'this', 3: 'that'})
        dice = Dice_(id='base', mapping={1: 'this', 2: 'that'})
        assert dice.roll_mapped(), 'no result'

    def test_dice_roll_mapping(self) -> None:
        """Test roll_mapping()
        """
        obj_ = Dice_(id='dice', count=5, mapping={1: 'this', 2: 'that'})
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
        obj_ = Dice_(id='dice', count=5)
        result = obj_.roll_mapped()
        assert isinstance(result, list), 'roll returns not list'
        assert len(result) == 0, 'wrong count of rolls'


class TestCard:
    """Test Card classes"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        obj_ = Card_(id='card')
        assert obj_.opened is False, 'card is opened'
        assert obj_.tapped is False, 'card is tapped'
        assert obj_.side is None, 'defined wrong side'
        assert obj_.count == 1, 'wrong count'

    def test_flip(self) -> None:
        """Test flip card
        """
        obj_ = Card_(id='card')
        obj_ = obj_.flip()
        assert isinstance(obj_, Card_), 'wrong return'
        assert obj_.opened, 'card not oppened'
        obj_.flip()
        assert not obj_.opened, 'card oppened'

    def test_open(self) -> None:
        """Test face up opened card
        """
        obj_ = Card_(id='card')
        obj_ = obj_.open()
        assert isinstance(obj_, Card_), 'wrong return'
        assert obj_.opened, 'card not opened'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        obj_ = Card_(id='card')
        obj_.opened = True
        obj_ = obj_.hide()
        assert isinstance(obj_, Card_), 'wrong return'
        assert not obj_.opened, 'card not opened'

    def test_tap_tap_card_and_set_side(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card_(id='card')
        obj_ = obj_.tap(side='left')
        assert isinstance(obj_, Card_), 'wrong return'
        assert obj_.tapped, 'card not tapped'
        assert obj_.side == 'left', 'wrong side'

    def test_untap_card(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card_(id='card')
        obj_.tapped = True
        assert obj_.tapped, 'card not tapped'
        obj_.side = 'left'
        obj_ = obj_.untap()
        assert isinstance(obj_, Card_), 'wrong return'
        assert not obj_.tapped, 'card not untapped'
        assert obj_.side is None, 'wrong side'
