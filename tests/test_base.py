import pytest
import json
from collections import Counter
from bgameb.constraints import COMPONENTS
from bgameb.base import Component, Base
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.errors import ComponentNameError


class TestComponent:
    """Test CardText class
    """
    components = [
        (Dice, 'dice_nice'),
        (Card, 'card_ward'),
        (Step, 'wild_step'),
        ]

    @pytest.mark.parametrize("_class, _id", components)
    def test_components_access_to_attr(
        self, _class: BaseItem, _id: str
            ) -> None:
        """Test components acces to attrs
        """
        comp = Component()
        comp.__dict__.update(
            {'some': _class(_id), 'many': _class(_id)}
            )

        assert comp.some.id == _id, 'not set or cant get'
        assert comp['some'].id == _id, 'not set or cant get'

        comp.this = _class(_id)
        assert comp.this.id == _id, 'not setted attr'
        comp['that'] = _class(_id)
        assert comp.that.id == _id, 'not setted attr'

        del comp.some
        with pytest.raises(AttributeError, match='some'):
            comp.some
        with pytest.raises(KeyError, match='some'):
            comp['some']

        with pytest.raises(AttributeError, match='newer'):
            del comp.newer
        with pytest.raises(KeyError, match='newer'):
            del comp['newer']

    @pytest.mark.parametrize("_class, _id", components)
    def test_components_repr(
        self, _class: BaseItem, _id: str
            ) -> None:
        """Test components repr
        """
        comp = Component()
        comp.__dict__.update({'some': _class(_id)})
        assert "Component(some=" in comp.__repr__(), 'wrong repr'

    @pytest.mark.parametrize("_class, _id", components)
    def test_components_len(
        self, _class: BaseItem, _id: str
            ) -> None:
        """Test components len
        """
        comp1 = Component()
        comp2 = Component()
        comp1.__dict__.update({'some': _class(_id)})
        comp2.__dict__.update({'_some': _class(_id)})
        assert len(comp1) == 1, 'wrong len'
        assert len(comp2) == 0, 'wrong len'

    @pytest.mark.parametrize("_class, _id", components)
    def test_components_items(
        self, _class: BaseItem, _id: str
            ) -> None:
        """Test components items access
        """
        comp = Component()
        comp.__dict__.update({'some': _class(_id)})
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

    @pytest.mark.parametrize("_class, _id", components)
    def test_is_unique(
        self, _class: BaseItem, _id: str
            ) -> None:
        """Test _is_unique()
        """
        comp = Component()
        comp.__dict__.update({'some': _class(_id)})
        assert comp._is_unique('this'), 'not unique'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):
            comp._is_unique('some')

    def test_is_valid(self) -> None:
        """Test _is_valid()
        """
        comp = Component()
        assert comp._is_valid('this'), 'not valid'
        assert comp._is_valid('a222'), 'not valid'
        assert comp._is_valid('a3b_'), 'not valid'
        assert not comp._is_valid('###'), 'valid'
        assert not comp._is_valid('.'), 'valid'
        assert not comp._is_valid('222'), 'valid'
        assert not comp._is_valid('_ '), 'valid'
        assert not comp._is_valid('A2n_'), 'valid'
        assert not comp._is_valid('e5E_'), 'valid'
        assert not comp._is_valid('_a'), 'valid'

    def test_make_name(self) -> None:
        """Test _make_name()
        """
        comp = Component()
        assert comp._make_name('this') == 'this', 'not maked'
        assert comp._make_name('tHIs') == 'this', 'not maked'
        assert comp._make_name('this222') == 'this222', 'not maked'
        assert comp._make_name('This 2') == 'this_2', 'not maked'
        assert comp._make_name('this#2') == 'this_2', 'not maked'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):
            comp._make_name('_this')
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):
            comp._make_name('123')

    def test_component_set_attr_with_dot(self) -> None:
        """Test set attr with dot notation
        """
        comp = Component()
        comp.AbcD23 = 'abcd'
        assert comp.AbcD23 == 'abcd', 'not seted'

    @pytest.mark.parametrize("_class, _id", components)
    def test_update_component(
        self, _class: BaseItem, _id: str
            ) -> None:
        """Test update component
        """
        comp = Component()
        cl = _class(_id)
        comp._update(cl)
        comp[_id].id == _id, 'wrong id'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):
            comp._update(cl)
        assert id(cl) != id(comp[_id]), 'not a copy'

    @pytest.mark.parametrize("_class, _id", components)
    def test_get_names(
        self, _class: BaseItem, _id: str
            ) -> None:
        """Test get_names() method
        """
        comp = Component()
        assert comp.get_names() == [], 'nonempty list of names'
        comp._update(_class(_id))
        assert comp.get_names() == [_id], 'empty list of names'
        comp._update(_class('this'))
        assert comp.get_names() == [_id, 'this'], 'empty list of names'


class TestBaseClass:
    """Test Base class
    """

    def test_base_class_creation(self) -> None:
        """Test Base instancing
        """
        obj_ = Base('9 this is Fine #')
        assert obj_.id == '9 this is Fine #', 'not set id for instance'
        assert isinstance(obj_, Component), 'isnt component'
        assert obj_._types_to_add == [], 'wrong _types_to_add'
        assert obj_._type == 'base', 'wrong type'
        assert isinstance(obj_.counter, Counter), 'wrong counter type'
        assert len(obj_.counter) == 0, 'counter not empty'
        assert isinstance(obj_.other, dict), 'wrong other'

    def test_base_class_creation_with_other(self) -> None:
        """Test Base instancing with other
        """
        obj_ = Base('9 this is Fine #', this_is='fine')
        assert len(obj_.other) == 1, 'wrong other len'
        assert obj_.other['this_is'] == 'fine', 'wrong other'
        del obj_.other['this_is']
        assert len(obj_.other) == 0, 'wrong other len'
        del obj_.other
        with pytest.raises(AttributeError, match='other'):
            obj_.other

    def test_base_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Base('9 this is Fine #')
        j = json.loads(obj_.to_json())
        assert j['id'] == '9 this is Fine #', 'not converted to json'

    def test_by_id(self) -> None:
        """Test get component by id
        """
        obj_ = Base('9 this is Fine #')
        obj_._types_to_add = COMPONENTS
        obj_.add(Dice('dice'))
        result = obj_.by_id('dice')
        assert result.id == 'dice', 'wrong component'
        result = obj_.by_id('notexist')
        assert result is None, 'wrong component'
