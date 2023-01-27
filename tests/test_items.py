import json
import pytest
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.errors import StuffDefineError
from tests.conftest import FixedSeed


class TestBaseStuff:
    """Test creation with id and json schemes
    """

    @pytest.mark.parametrize("_class,_id", [
        (BaseItem, 'item'),
        (Dice, 'dice'),
        (Card, 'card'),
        (Step, 'step'),
            ])
    def test_items_classes_created(self, _class, _id: str) -> None:
        """Test items classes instancing
        """
        obj_ = _class(id=_id)
        assert isinstance(obj_, BaseModel), 'wrong instance'
        assert obj_.id == _id, 'not set id for instance'
        j: dict = json.loads(obj_.json())
        assert j['id'] == _id, \
            'not converted to json'


class TestStep:
    """Test Step class
    """

    def test_step_instance(self) -> None:
        """Test Step class instance
        """
        obj_ = Step(id='first_step')
        assert obj_.priority == 0, 'wrong priority'
        obj1 = Step(id='first_step', priority=20)
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
        obj_ = Dice(id='dice nice')
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
        obj_ = Dice(id='dice nice', sides=3)
        obj1 = Dice(id='the_dice', sides=30)
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
            Dice(id='base', sides=1)

    def test_dice_roll(self) -> None:
        """Test dice roll()
        """
        obj_ = Dice(id='dice', count=5)
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
            Dice(id='base', mapping={1: 'this'})
        with pytest.raises(
            StuffDefineError,
            match='Mapping must define values for each side.'
                ):
            Dice(id='base', mapping={1: 'this', 3: 'that'})
        dice = Dice(id='base', mapping={1: 'this', 2: 'that'})
        assert dice.roll_mapped(), 'no result'

    def test_dice_roll_mapping(self) -> None:
        """Test roll_mapping()
        """
        obj_ = Dice(id='dice', count=5, mapping={1: 'this', 2: 'that'})
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
        obj_ = Dice(id='dice', count=5)
        result = obj_.roll_mapped()
        assert isinstance(result, list), 'roll returns not list'
        assert len(result) == 0, 'wrong count of rolls'


class TestCard:
    """Test Card classes"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        obj_ = Card(id='card')
        assert obj_.is_revealed is False, 'card is opened'
        assert obj_.is_active is True, 'card is tapped'
        assert obj_.side is None, 'defined wrong side'
        assert obj_.count == 1, 'wrong count'

    def test_flip(self) -> None:
        """Test flip card
        """
        obj_ = Card(id='card')
        obj_ = obj_.flip()
        assert isinstance(obj_, Card), 'wrong return'
        assert obj_.is_revealed, 'card not oppened'
        obj_.flip()
        assert not obj_.is_revealed, 'card oppened'

    def test_open(self) -> None:
        """Test face up is_revealed card
        """
        obj_ = Card(id='card')
        obj_ = obj_.open()
        assert isinstance(obj_, Card), 'wrong return'
        assert obj_.is_revealed, 'card not is_revealed'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        obj_ = Card(id='card')
        obj_.is_revealed = True
        obj_ = obj_.hide()
        assert isinstance(obj_, Card), 'wrong return'
        assert not obj_.is_revealed, 'card not is_revealed'

    def test_tap_card_and_set_side(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card(id='card')
        obj_ = obj_.tap(side='left')
        assert isinstance(obj_, Card), 'wrong return'
        assert obj_.is_active is False, 'card is not tapped'
        assert obj_.side == 'left', 'wrong side'

    def test_untap_card(self) -> None:
        """Test tap card tap and set side
        """
        obj_ = Card(id='card')
        obj_.is_active = False
        assert obj_.is_active is False, 'card not tapped'
        obj_.side = 'left'
        obj_ = obj_.untap()
        assert isinstance(obj_, Card), 'wrong return'
        assert obj_.is_active, 'card not untapped'
        assert obj_.side is None, 'wrong side'
