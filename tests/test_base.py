import pytest
import json
from pydantic import BaseModel
from loguru._logger import Logger
from collections import Counter
from bgameb.base import (
    Base, Component, Components, BaseItem, BaseTool, BaseToolListMixin
        )
from bgameb.errors import ComponentNameError


# class TestComponent:
#     """Test CardText class
#     """

#     @pytest.fixture(scope='function')
#     def comp(self) -> Component:
#         return Component(some=BaseItem(id='some'))

#     def test_components_access_to_attr(self, comp: Component) -> None:
#         """Test components acces to attrs
#         """
#         assert comp.some.id == 'some', 'not set or cant get'
#         assert comp['some'].id == 'some', 'not set or cant get'

#         del comp.some
#         with pytest.raises(AttributeError):
#             comp.some
#         with pytest.raises(KeyError):
#             comp['some']

#         with pytest.raises(AttributeError, match='newer'):
#             del comp.newer
#         with pytest.raises(KeyError, match='newer'):
#             del comp['newer']

#     def test_components_repr(self, comp: Component) -> None:
#         """Test components repr
#         """
#         assert "'some'" in comp.__repr__(), 'wrong repr'

#     def test_components_len(self, comp: Component) -> None:
#         """Test components len
#         """
#         assert len(comp) == 1, 'wrong len'
#         assert len(comp.__dict__) == 1, 'wrong dict len'

#     def test_components_items(self, comp: Component) -> None:
#         """Test components items access
#         """
#         assert len(comp.items()) == 1, 'items not accessed'
#         assert len(comp.keys()) == 1, 'keys not accessed'
#         assert len(comp.values()) == 1, 'values not accessed'

#     @pytest.mark.parametrize("example", ['this', 'a222', 'a3b_'])
#     def test_is_valid(self, example: str) -> None:
#         """Test _is_valid()
#         """
#         comp = Component()
#         assert comp._is_valid(example), 'not valid'

#     @pytest.mark.parametrize(
#         "example", ['###', '.', '222', '_ ', 'A2n_', 'e5E_', '_a']
#             )
#     def test_is_not_valid(self, example: str) -> None:
#         """Test _is_valid() fail validation
#         """
#         comp = Component()
#         with pytest.raises(ComponentNameError, match='wrong name'):
#             comp._is_valid(example)

#     def test_make_name(self) -> None:
#         """Test _make_name()
#         """
#         comp = Component()
#         assert comp._make_name('this') == 'this', 'not maked'
#         assert comp._make_name('tHIs') == 'this', 'not maked'
#         assert comp._make_name('this222') == 'this222', 'not maked'
#         assert comp._make_name('This 2') == 'this_2', 'not maked'
#         assert comp._make_name('this#2') == 'this_2', 'not maked'
#         with pytest.raises(
#             ComponentNameError,
#             match='is exist in'
#                 ):
#             comp._make_name('_this')
#         with pytest.raises(
#             ComponentNameError,
#             match='is exist in'
#                 ):
#             comp._make_name('123')

#     def test_update_component(self) -> None:
#         """Test update component
#         """
#         comp = Component()
#         cl = BaseItem(id='that')
#         comp.update(cl)
#         comp['that'].id == 'that', 'wrong id'
#         assert id(cl) != id(comp['that']), 'not a copy'

#     def test_ids(self) -> None:
#         """Test ids() method
#         """
#         comp = Component()
#         assert comp.ids == [], 'nonempty list of names'
#         comp.update(BaseItem(id='that'))
#         assert comp.ids == ['that', ], 'empty list of names'
#         comp.update(BaseItem(id='this'))
#         assert comp.ids == ['that', 'this'], 'empty list of names'

#     def test_by_id(self, comp: Component) -> None:
#         """Test get stuff by id
#         """
#         assert comp.by_id('some').id == 'some', 'wrong returnt'
#         assert comp.by_id('something') is None, 'wrong component'

#     def test_to_json_convertation(self, comp: Component) -> None:
#         """Test to_json() method
#         """
#         j = json.loads(comp.to_json())
#         assert isinstance(j['some'], dict), 'not converted'
#         assert j['some']['id'] == 'some', 'not converted'


class TestComponents:
    """Test CardText class
    """

    @pytest.fixture(scope='function')
    def comp(self) -> Components:
        return Components(some=BaseItem(id='some'))

    def test_components_access_to_attr(self, comp: Components) -> None:
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

    def test_components_repr(self, comp: Components) -> None:
        """Test components repr
        """
        assert "'some'" in comp.__repr__(), 'wrong repr'

    def test_components_len(self, comp: Components) -> None:
        """Test components len
        """
        assert len(comp) == 1, 'wrong len'
        assert len(comp.__dict__) == 1, 'wrong dict len'

    def test_components_items(self, comp: Components) -> None:
        """Test components items access
        """
        assert len(comp.items()) == 1, 'items not accessed'
        assert len(comp.keys()) == 1, 'keys not accessed'
        assert len(comp.values()) == 1, 'values not accessed'

    @pytest.mark.parametrize("example", ['this', 'a222', 'a3b_'])
    def test_is_valid(self, example: str) -> None:
        """Test _is_valid()
        """
        comp = Components()
        assert comp._is_valid(example), 'not valid'

    @pytest.mark.parametrize(
        "example", ['###', '.', '222', '_ ', 'A2n_', 'e5E_', '_a']
            )
    def test_is_not_valid(self, example: str) -> None:
        """Test _is_valid() fail validation
        """
        comp = Components()
        with pytest.raises(ComponentNameError, match='wrong name'):
            comp._is_valid(example)

    def test_make_name(self) -> None:
        """Test _make_name()
        """
        comp = Components()
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
        comp = Components()
        cl = BaseItem(id='that')
        comp.update(cl)
        comp['that'].id == 'that', 'wrong id'
        assert id(cl) != id(comp['that']), 'not a copy'

    def test_ids(self) -> None:
        """Test ids() method
        """
        comp = Components()
        assert comp.ids == [], 'nonempty list of names'
        comp.update(BaseItem(id='that'))
        assert comp.ids == ['that', ], 'empty list of names'
        comp.update(BaseItem(id='this'))
        assert comp.ids == ['that', 'this'], 'empty list of names'

    def test_by_id(self, comp: Components) -> None:
        """Test get stuff by id
        """
        assert comp.by_id('some').id == 'some', 'wrong returnt'
        assert comp.by_id('something') is None, 'wrong component'

    def test_to_json_convertation(self, comp: Components) -> None:
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
        obj_ = Base()
        assert isinstance(obj_, BaseModel), 'wrong instance'
        assert isinstance(obj_._counter, Counter), 'wrong counter type'
        assert len(obj_._counter) == 0, 'counter not empty'
        assert isinstance(obj_._logger, Logger), 'wrong _to_relocate'
        j: dict = json.loads(obj_.json())
        assert j.get('_counter') is None, 'counter not excluded'
        assert j.get('_logger') is None, '_logger not excluded'


class TestBaseTool:
    """Test tools classes
    """

    @pytest.fixture
    def obj_(self) -> BaseTool:
        tool = BaseTool()
        tool.c = Component(
            dice=BaseItem(id='dice'), card=BaseItem(id='card')
                )
        return tool

    @pytest.fixture
    def dealt_obj_(self, obj_: BaseTool) -> BaseTool:
        obj_.current.append(BaseItem(id='dice'))
        obj_.current.append(BaseItem(id='card'))
        return obj_

    def test_tool_init(self, obj_: BaseTool) -> None:
        """Test tool classes instancing
        """
        assert isinstance(obj_, BaseModel), 'wrong instance'
        assert isinstance(obj_.current, list), 'wrong type of current'
        assert len(obj_.current) == 0, 'wrong current len'
        assert isinstance(obj_.c, Component), 'wrong component type'
        assert len(obj_.c) == 2, 'wrong items'
        assert obj_.last is None, 'wrong last'

    def test_last_id(self, dealt_obj_: BaseTool) -> None:
        """Test get_last_id
        """
        dealt_obj_.pop()
        assert dealt_obj_.last_id == 'card', 'wrong id'
        dealt_obj_.last = None
        assert dealt_obj_.last_id is None, 'wrong id'

    def test_by_id(self, dealt_obj_: BaseTool) -> None:
        """Test by_id()
        """
        dealt_obj_.current.append(BaseItem(id='card'))
        assert isinstance(dealt_obj_.by_id('card'), list), 'wrong type'
        assert len(dealt_obj_.by_id('card')) == 2, 'wrong len'
        assert dealt_obj_.by_id('card')[0].id == 'card', 'wrong search'
        assert dealt_obj_.by_id('why') == [], 'wrong search'
        dealt_obj_.clear()
        assert dealt_obj_.by_id('card') == [], 'wrong search'

    def test_get_items(self, obj_: BaseTool) -> None:
        """Test get items
        """
        result = obj_.get_items()
        assert len(result) == 2, 'wrong number of items'
        assert result['dice'], 'wrong item'
        assert result['card'], 'wrong item'

    def test_item_replace(self, obj_: BaseTool) -> None:
        """Test _item_replace()
        """
        card = BaseItem(id='card')
        item = obj_._item_replace(card)
        assert item.id == 'card', 'wrong id'
        assert id(item) != id(card), 'not replaced'

    def test_clear(self, dealt_obj_: BaseTool) -> None:
        """Test current clear
        """
        dealt_obj_.pop()
        dealt_obj_.clear()
        assert isinstance(dealt_obj_.current, list), 'wrong current'
        assert len(dealt_obj_.current) == 0, 'wrong current len'
        assert dealt_obj_.last is None, 'wrong last'

    def test_current_ids(self, dealt_obj_: BaseTool) -> None:
        """Test get_curren_ids
        """
        assert len(dealt_obj_.current_ids) == 2, \
            'wrong current names len'
        assert dealt_obj_.current_ids[0] == 'dice', \
            'wrong current names'

    def test_count(self, dealt_obj_: BaseTool) -> None:
        """Test current count of given item
        """
        assert dealt_obj_.count('dice') == 1, 'wrong count'
        assert dealt_obj_.count('nothing') == 0, 'wrong count'

    def test_pop(self, dealt_obj_: BaseTool) -> None:
        """Test pop
        """
        assert dealt_obj_.pop().id == 'card', 'wrong pop'
        assert dealt_obj_.last.id == 'card', 'not added to last'
        dealt_obj_.current.clear()
        with pytest.raises(IndexError):
            dealt_obj_.pop()


class TestBaseToolListMixin:
    """Test BaseToolListMixin
    """

    @pytest.fixture
    def obj_(self) -> BaseToolListMixin:
        tool = BaseToolListMixin(id='this')
        tool.c = Component(
            dice=BaseItem(id='dice'), card=BaseItem(id='card')
                )
        return tool

    @pytest.fixture
    def dealt_obj_(self, obj_: BaseToolListMixin) -> BaseToolListMixin:
        obj_.current.append(BaseItem(id='dice'))
        obj_.current.append(BaseItem(id='card'))
        return obj_

    def test_append(self, dealt_obj_: BaseTool) -> None:
        """Test curent append
        """
        card = BaseItem(id='card')
        dealt_obj_.append(card)
        assert len(dealt_obj_.current) == 3, 'wrong current len'
        assert dealt_obj_.current[1].id == 'card', 'wrong append'
        assert id(card) != id(dealt_obj_.current[2]), 'not replaced'

    def test_extend(self, dealt_obj_: BaseTool) -> None:
        """Test extend currend by items
        """
        items = [BaseItem(id='unique'), BaseItem(id='dice')]
        dealt_obj_.extend(items)
        assert len(dealt_obj_.current) == 4, 'wrong current len'
        assert dealt_obj_.current[2].id == 'unique', 'wrong append'
        assert id(items[0]) != id(dealt_obj_.current[2]), 'not replaced'
        assert dealt_obj_.current[3].id == 'dice', 'wrong append'

    def test_index(self, dealt_obj_: BaseTool) -> None:
        """Test index currend
        """
        assert dealt_obj_.index('card') == 1, 'wrong index'
        assert dealt_obj_.index('dice') == 0, 'wrong index'
        assert dealt_obj_.index('card', start=1) == 1, 'wrong index'
        with pytest.raises(ValueError):
            dealt_obj_.index('card', start=12)
        with pytest.raises(ValueError):
            dealt_obj_.index('imposible')
        with pytest.raises(ValueError):
            dealt_obj_.index('card', start=6, end=10)

    def test_insert(self, dealt_obj_: BaseTool) -> None:
        """Test insert into currend
        """
        item = BaseItem(id='unique')
        dealt_obj_.insert(item, 1)
        assert len(dealt_obj_.current) == 3, 'wrong len'
        assert dealt_obj_.current[1].id == 'unique', 'not inserted'
        assert id(item) != id(dealt_obj_.current[1]), 'not replaced'
        dealt_obj_.insert(item, 55)
        assert dealt_obj_.current[3].id == 'unique', 'not inserted'

    def test_remove(self, dealt_obj_: BaseTool) -> None:
        """Test remove
        """
        assert dealt_obj_.current[0].id == 'dice', 'wrong order'
        dealt_obj_.remove('dice')
        assert len(dealt_obj_.current) == 1, 'wrong len'
        with pytest.raises(ValueError):
            dealt_obj_.remove('not_exist')

    def test_reverse(self, dealt_obj_: BaseTool) -> None:
        """Test reverse
        """
        items = dealt_obj_.current
        items.reverse()
        dealt_obj_.reverse()
        assert dealt_obj_.current == items, 'not reversed'
