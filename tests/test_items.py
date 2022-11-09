import json
import pytest
from bgameb.items import Dice, Card, BaseItem
from bgameb.markers import Counter, BaseMarker
from bgameb.errors import StuffDefineError, ComponentClassError
from bgameb.types import MARKERS


class TestBaseStuff:
    """Test creation with names and json schemes
    """
    params = [
        (Dice, 'dice_me'),
        (Card, 'card_you'),
        ]

    @pytest.mark.parametrize("_class, name", params)
    def test_items_classes_created_with_name(
        self, _class: BaseItem, name: str
            ) -> None:
        """Test items classes instancing
        """
        obj_ = _class(name=name)
        assert obj_.name == name, 'not set name for instance'
        assert obj_.count == 1, 'wrong count'
        assert obj_._types_to_add == MARKERS, 'wrong _type_to_add'

    @pytest.mark.parametrize("_class, name", params)
    def test_items_classes_are_converted_to_json(
        self, _class: BaseItem, name: str
            ) -> None:
        """Test to json convertatrion
        """
        obj_ = _class(name=name)
        j = json.loads(obj_.to_json())
        assert j['name'] == name, 'not converted to json'

    components = [
        (Counter, 'counter_less'),
        ]

    @pytest.mark.parametrize("_class1, name1", components)
    @pytest.mark.parametrize("_class, name", params)
    def test_add_new_component_to_item(
        self,
        _class: BaseItem,
        name: str,
        _class1: BaseMarker,
        name1: str
            ) -> None:
        """Test add new component to item
        """
        obj_ = _class(name=name)
        cl = _class1(name1)
        obj_.add(component=cl)
        assert obj_[name1].name == name1, \
            'component not added'

    @pytest.mark.parametrize("_class, name", params)
    def test_add_new_wrong_component_to_item(
        self, _class: BaseItem, name: str
            ) -> None:
        """Test cant add new wrong component to item
        """
        obj_ = _class(name=name)

        class G():
            _type = 'wrong'

        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.add(G())


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
        assert obj_._type == 'dice', 'wrong _type'
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
        assert obj_._type == 'card', 'wrong _type'
        assert obj_.opened is False, 'card is opened'
        assert obj_.tapped is False, 'card is tapped'
        assert obj_.side is None, 'defined wrong side'
        assert obj_.count == 1, 'wrong count'

    def test_flip(self) -> None:
        """Test flip card
        """
        obj_ = Card(name='card')
        obj_.flip()
        assert obj_.opened, 'card not oppened'
        obj_.flip()
        assert not obj_.opened, 'card oppened'

    def test_open(self) -> None:
        """Test face up opened card
        """
        obj_ = Card(name='card')
        obj_.open()
        assert obj_.opened, 'card not opened'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        obj_ = Card(name='card')
        obj_.opened = True
        obj_.hide()
        assert not obj_.opened, 'card not opened'

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
        obj_.side = 'left'
        obj_.untap()
        assert not obj_.tapped, 'card not untapped'
        assert obj_.side is None, 'wrong side'
