import json, pytest
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
        assert isinstance(obj_.turn_order, COMPONENTS['turn']), 'turn_order isnt component'
        assert isinstance(obj_.game_rules, COMPONENTS['rules']), 'rules isnt component'
        assert isinstance(obj_, Components), 'isnt component'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Game(name='game')
        j = json.loads(obj_.to_json())
        assert j['name'] == 'game', 'not converted to json'

    def test_add_component(self) -> None:
        """Test add tool or stuff to game
        """
        obj_ = Game(name='game')
        for n in COMPONENTS.keys():
            if n == 'rule':
                obj_.add(n, name=n, text='this')
            else:
                obj_.add(n, name=n)
            assert obj_[n].name == n, 'component not added'

    def test_add_component_with_kwargs(self) -> None:
        """Test add with kwargs
        """
        obj_ = Game(name='game')
        obj_.add('dice', name='dice', sides=42)
        assert obj_.dice.sides == 42, 'wrong count'

    def test_add_wrong_component_to_game(self) -> None:
        """Test we cant add notexisted tool or stuff to game
        """
        obj_ = Game(name='game')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
            ):
            obj_.add('chocho', name='this')

    def test_add_to(self) -> None:
        """Test add_to() method
        """
        obj_ = Game(name='game')
        obj_.add('dice', name='that')
        obj_.add('shaker', name='this')
        obj_.add_to('this', 'that', count=10)
        assert obj_.this.that.count == 10, 'not added'

    def test_add_notexisted(self) -> None:
        """Test add_to() notexisted stuff or tool
        """
        obj_ = Game(name='game')
        obj_.add('dice', name='that')
        obj_.add('shaker', name='this')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
            ):
            obj_.add_to('this', 'what', count=10)
        with pytest.raises(
            ComponentClassError,
            match='not a component'
            ):
            obj_.add_to('what', 'that', count=10)

    def test_add_rule_to_rules(self) -> None:
        """Test add rule to game rules
        """
        obj_ = Game(name='game')
        obj_.add('rule', name='this', text='that')
        print(obj_)
        obj_.add_to('game_rules', 'this')
        assert isinstance(obj_.game_rules.this, COMPONENTS['rule']), 'wrong type of rule'
        assert obj_.game_rules.this.name == 'this', 'wrong name of rule'
        assert obj_.game_rules.this.text == 'that', 'wrong text rule'

    @pytest.mark.skip('# TODO: define logic')
    def test_add_not_stuff_or_not_to_tool(self) -> None:
        """Test add_to() missed type
        """
        obj_ = Game(name='game')
        obj_.add('dice', name='that')
        obj_.add('shaker', name='this')
        with pytest.raises(
            ComponentClassError,
            match='not a component'
            ):
            obj_.add_to('this', 'this', count=10)
        with pytest.raises(
            ComponentClassError,
            match='not a component'
            ):
            obj_.add_to('that', 'that', count=10)
