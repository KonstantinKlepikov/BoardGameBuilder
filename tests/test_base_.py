import pytest
import json
from pydantic import BaseModel
from loguru._logger import Logger
from collections import Counter
from bgameb.base_ import Base, Component
from bgameb.errors import ComponentNameError


class TestComponent:
    """Test CardText class
    """

    @pytest.fixture(scope='function')
    def comp(self) -> Component:
        return Component(some=Base(id='some'))

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

    def test_components_repr(self, comp: Component) -> None:
        """Test components repr
        """
        assert "'some'" in comp.__repr__(), 'wrong repr'

    def test_components_len(self, comp: Component) -> None:
        """Test components len
        """
        assert len(comp) == 1, 'wrong len'
        assert len(comp.__dict__) == 1, 'wrong dict len'

    def test_components_items(self, comp: Component) -> None:
        """Test components items access
        """
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

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
        cl = Base(id='that')
        comp.update(cl)
        comp['that'].id == 'that', 'wrong id'
        assert id(cl) != id(comp['that']), 'not a copy'

    def test_ids(self) -> None:
        """Test ids() method
        """
        comp = Component()
        print(comp)
        assert comp.ids == [], 'nonempty list of names'
        comp.update(Base(id='that'))
        assert comp.ids == ['that', ], 'empty list of names'
        comp.update(Base(id='this'))
        assert comp.ids == ['that', 'this'], 'empty list of names'

    def test_by_id(self, comp: Component) -> None:
        """Test get stuff by id
        """
        assert comp.by_id('some').id == 'some', 'wrong returnt'
        assert comp.by_id('something') is None, 'wrong component'

    def test_to_json_convertation(self, comp: Component) -> None:
        """Test to_json() method
        """
        j = json.loads(comp.to_json())
        assert isinstance(j['some'], dict), 'not converted'
        assert j['some']['id'] == 'some', 'not converted'


class TestBaseClass:
    """Test Base class
    """

    def test_base_class_creation(self) -> None:
        """Test Base instancing
        """
        obj_ = Base(id='9 this is Fine #')
        assert isinstance(obj_, BaseModel), 'wrong instance'
        assert obj_.id == '9 this is Fine #', 'not set id for instance'
        assert isinstance(obj_.counter, Counter), 'wrong counter type'
        assert len(obj_.counter) == 0, 'counter not empty'
        assert isinstance(obj_._to_relocate, dict), 'wrong _to_relocate'
        assert isinstance(obj_._logger, Logger), 'wrong _to_relocate'
        j : dict = json.loads(obj_.json())
        assert j['id'] == '9 this is Fine #', \
            'not converted to json'
        assert j.get('counter') is None, 'counter not excluded'
        assert j.get('_to_relocate') is None, '_to_relocat not excluded'
        assert j.get('_logger') is None, '_logger not excluded'
