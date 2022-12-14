import pytest
import json
from collections import Counter
from bgameb.base import Component, Base
from bgameb.errors import ComponentNameError


class TestComponent:
    """Test CardText class
    """

    @pytest.fixture(scope='function')
    def comp(self) -> Component:
        return Component(some=Base('some'))

    def test_components_access_to_attr(self, comp: Component) -> None:
        """Test components acces to attrs
        """
        assert comp.some.id == 'some', 'not set or cant get'
        assert comp['some'].id == 'some', 'not set or cant get'

        del comp.some
        with pytest.raises(AttributeError):
            comp.some
        with pytest.raises(KeyError):
            comp['some']

        with pytest.raises(AttributeError, match='newer'):
            del comp.newer
        with pytest.raises(KeyError, match='newer'):
            del comp['newer']

        with pytest.raises(NotImplementedError):
            comp.this = Base('this')
        with pytest.raises(NotImplementedError):
            comp['this'] = Base('this')

    def test_components_repr(self, comp: Component) -> None:
        """Test components repr
        """
        assert "{some=" in comp.__repr__(), 'wrong repr'

    def test_components_len(self, comp: Component) -> None:
        """Test components len
        """
        assert len(comp) == 1, 'wrong len'
        assert len(comp.__dict__) == 2, 'wrong dict len'

    def test_components_items(self, comp: Component) -> None:
        """Test components items access
        """
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

    def test_is_unique(self, comp: Component) -> None:
        """Test _is_unique()
        """
        assert comp._is_unique('this'), 'not unique'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):
            comp._is_unique('some')

    @pytest.mark.parametrize("example", ['this', 'a222', 'a3b_'])
    def test_is_valid(self, example: str) -> None:
        """Test _is_valid()
        """
        comp = Component()
        assert comp._is_valid(example), 'not valid'

    @pytest.mark.parametrize(
        "example", ['###', '.', '222', '_ ', 'A2n_', 'e5E_', '_a']
            )
    def test_is_not_valid(self, example: str) -> None:
        """Test _is_valid() fail validation
        """
        comp = Component()
        with pytest.raises(ComponentNameError, match='wrong name'):
            comp._is_valid(example)

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

    def test_update_component(self) -> None:
        """Test update component
        """
        comp = Component()
        cl = Base('that')
        comp._update(cl)
        comp['that'].id == 'that', 'wrong id'
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):
            comp._update(cl)
        assert id(cl) != id(comp['that']), 'not a copy'

    def test_get_names(self) -> None:
        """Test get_names() method
        """
        comp = Component()
        assert comp.get_names() == [], 'nonempty list of names'
        comp._update(Base('that'))
        assert comp.get_names() == ['that', ], 'empty list of names'
        comp._update(Base('this'))
        assert comp.get_names() == ['that', 'this'], 'empty list of names'

    def test_by_id(self, comp: Component) -> None:
        """Test get stuff by id
        """
        assert comp.by_id('some').id == 'some', 'wrong returnt'
        assert comp.by_id('something') is None, 'wrong component'


class TestBaseClass:
    """Test Base class
    """

    def test_base_class_creation(self) -> None:
        """Test Base instancing
        """
        obj_ = Base('9 this is Fine #')
        assert obj_.id == '9 this is Fine #', 'not set id for instance'
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
