import pytest
import json
from collections import Counter
from bgameb.base import Components, Base
from bgameb.items import Dice, Card, BaseItem
from bgameb.errors import ComponentNameError


class TestComponents:
    """Test CardText class
    """
    components = [
        (Dice, 'dice_nice'),
        (Card, 'card_ward'),
        ]

    @pytest.mark.parametrize("_class, name", components)
    def test_components_access_to_attr(
        self, _class: BaseItem, name: str
            ) -> None:
        """Test components acces to attrs
        """
        comp = Components()
        comp.__dict__.update(
            {'some': _class(name=name), 'many': _class(name=name)}
            )

        assert comp.some.name == name, 'not set or cant get'
        assert comp['some'].name == name, 'not set or cant get'

        comp.this = _class(name=name)
        assert comp.this.name == name, 'not setted attr'
        comp['that'] = _class(name=name)
        assert comp.that.name == name, 'not setted attr'

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
    def test_components_repr(self, _class: BaseItem, name: str) -> None:
        """Test components repr
        """
        comp = Components()
        comp.__dict__.update({'some': _class(name=name)})
        assert "Components(some=" in comp.__repr__(), 'wrong repr'

    @pytest.mark.parametrize("_class, name", components)
    def test_components_len(self, _class: BaseItem, name: str) -> None:
        """Test components len
        """
        comp1 = Components()
        comp2 = Components()
        comp1.__dict__.update({'some': _class(name=name)})
        assert len(comp1) == 1, 'wrong len'
        assert len(comp2) == 0, 'wrong len'

    @pytest.mark.parametrize("_class, name", components)
    def test_components_items(self, _class: BaseItem, name: str) -> None:
        """Test components items access
        """
        comp = Components()
        comp.__dict__.update({'some': _class(name=name)})
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

    @pytest.mark.parametrize("_class, name", components)
    def test_update_component(self, _class: BaseItem, name: str) -> None:
        """Test update component
        """
        comp = Components()
        cl = _class(name)
        comp._update(cl)
        comp[name].name == name, 'wrong name'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
        ):
            comp._update(cl)
        assert id(cl) != id(comp[name]), 'not a copy'

    @pytest.mark.parametrize("_class, name", components)
    def test_get_names(self, _class: BaseItem, name: str) -> None:
        """Test get_names() method
        """
        comp = Components()
        assert comp.get_names() == [], 'nonempty list of names'
        comp._update(_class(name))
        assert comp.get_names() == [name], 'empty list of names'
        comp._update(_class('this'))
        assert comp.get_names() == [name, 'this'], 'empty list of names'


class TestBase:
    """Test Base class
    """

    def test_base_class_created_with_name(self) -> None:
        """Test Base name instancing
        """
        obj_ = Base(name='this')
        assert obj_.name == 'this', 'not set name for instance'
        assert isinstance(obj_, Components), 'isnt component'
        assert obj_._types_to_add == [], 'wrong _types_to_add'
        assert obj_._type == 'base', 'wrong type'
        assert isinstance(obj_.counter, Counter), 'wrong counter type'
        assert len(obj_.counter) == 0, 'counter not empty'

    def test_base_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Base(name='this')
        j = json.loads(obj_.to_json())
        assert j['name'] == 'this', 'not converted to json'
