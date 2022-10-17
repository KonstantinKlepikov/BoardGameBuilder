import json
import pytest
from bgameb.game import Game
from bgameb.base import Components
from bgameb.types import COMPONENTS
from bgameb.errors import ComponentClassError


class TestGame:
    """Test Game class
    """

    def test_game_class_created_with_name(self) -> None:
        """Test Game name instancing
        """
        obj_ = Game(name='this_game')
        assert obj_.name == 'this_game', 'not set name for instance'
        assert obj_.is_active, 'wrong is_active'
        assert isinstance(obj_.turn_order, COMPONENTS['turns']), \
            'turn_order isnt component'
        assert isinstance(obj_.game_rules, COMPONENTS['rules']), \
            'rules isnt component'
        assert isinstance(obj_, Components), 'isnt component'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Game(name='game')
        j = json.loads(obj_.to_json())
        assert j['name'] == 'game', 'not converted to json'

    def test_add_new_component_to_game(self) -> None:
        """Test new() tool or stuff add to game
        """
        obj_ = Game(name='game')
        for n in COMPONENTS.keys():
            if n == 'rule':
                obj_.new(name=n, ctype=n, text='this')
            else:
                obj_.new(name=n, ctype=n)
            assert obj_[n].name == n, 'component not added'

    def test_add_new_component_with_kwargs(self) -> None:
        """Test new() add to game with kwargs
        """
        obj_ = Game(name='game')
        obj_.new('dice', ctype='dice', sides=42)
        assert obj_.dice.sides == 42, 'wrong count'

    def test_add_new_wrong_component_to_game(self) -> None:
        """Test we cant add new notexisted tool or stuff to game
        """
        obj_ = Game(name='game')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.new('chocho', ctype='this')

    def test_add_new_to_existed_object(self) -> None:
        """Test new() method for add new object to existed component
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='shaker')
        obj_.new('that', ctype='dice', target='this', count=10)
        assert obj_.this.that.name == 'that', 'not added'
        assert obj_.this.that.count == 10, 'not added'

    def test_add_new_wrong_component_to_existed_object(self) -> None:
        """Test new() cant add new wrong object to existed component
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='shaker')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.new('that', ctype='what', target='this', count=10)

    def test_add_new_wrong_component_to_notexisted_object(self) -> None:
        """Test new() cant add new wrong object to notexisted component
        """
        obj_ = Game(name='game')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.new('that', ctype='what', target='this', count=10)

    def test_add_new_component_to_notexisted_object(self) -> None:
        """Test new() cant add new object to notexisted component
        """
        obj_ = Game(name='game')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.new('that', ctype='dice', target='this', count=10)

    def test_add_new_stuff_to_nontools(self) -> None:
        """Test new() cant add new stuff to nontools/players
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='dice')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.new('that', ctype='dice', target='this')

    def test_add_new_nonstuff_to_tools(self) -> None:
        """Test new() cant add new stuff to nontools/players
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='shaker')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.new('that', ctype='shaker', target='this', count=10)

    def test_copy_component_from_game_to_another_component(self) -> None:
        """Test copy() existed component to another component
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='shaker')
        obj_.new('that', ctype='dice')
        obj_.copy('that', 'this')
        assert obj_.this.that.name == 'that', 'not copied'

    def test_copy_component_with_kwargs(self) -> None:
        """Test copy() existed component to another component
        with kwargs
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='shaker')
        obj_.new('that', ctype='dice')
        obj_.copy('that', 'this', count=6)
        assert obj_.that.count == 1, 'wrong count'
        assert obj_.this.that.count == 6, 'not copied with new count'

    def test_copy_notexisted_component_to_tool(self) -> None:
        """Test copy() cant copy notexisted stuff
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='shaker')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.copy('that', 'this', count=6)

    def test_copy_component_to_notexisted_tool(self) -> None:
        """Test copy() cant copy to notexisted tool
        """
        obj_ = Game(name='game')
        obj_.new('that', ctype='dice')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.copy('that', 'this', count=6)

    def test_add_rule_to_rules(self) -> None:
        """Test add rule to game rules
        """
        obj_ = Game(name='game')
        obj_.new('this', ctype='rule', text='that')
        obj_.copy('this', 'game_rules')
        assert isinstance(obj_.game_rules.this, COMPONENTS['rule']), \
            'wrong type of rule'
        assert obj_.game_rules.this.name == 'this', 'wrong name of rule'
        assert obj_.game_rules.this.text == 'that', 'wrong text rule'

    def test_copy_not_stuff_or_not_to_tool(self) -> None:
        """Test copy() missed type
        """
        obj_ = Game(name='game')
        obj_.new('that', 'shaker')
        obj_.new('this', 'dice')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.copy('this', 'this')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.copy('that', 'that', count=10)
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.copy('that', 'this', count=10)
