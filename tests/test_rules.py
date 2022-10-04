import pytest, json
from collections import deque
from bgameb.rules import Rule, Turn


class TestRule:
    """Test Rule class
    """

    def test_rule_instance(self) -> None:
        """Test Rule class instance
        """
        obj_ = Rule(name='this_rule', text='text of rule')
        assert obj_.name == 'this_rule', 'wrong name'
        assert obj_.text == 'text of rule', 'wrong rule'
        obj_.this = 'this'
        assert obj_.this == 'this', 'not set or cant get'
        assert "Rule(name='this_rule'" in obj_.__repr__(), 'wrong repr'
        obj_.this = 'that'
        assert obj_.this == 'that', 'not set or cant update'
        del obj_.this
        with pytest.raises(
            AttributeError, match='this'
            ):
            obj_.this

    def test_rule_are_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Rule(name='this_rule', text='text of rule')
        j = json.loads(obj_.to_json())
        assert j['name'] == 'this_rule', 'not converted to json'


class TestTurn:
    """Test Turn class
    """

    def test_Turn_instance(self) -> None:
        """Test Turn class instance
        """
        obj_ = Turn('game_Turn')
        assert isinstance(obj_, deque), 'wrong Turn type'
        assert isinstance(obj_._order, list), 'wrong order type'
        assert len(obj_._order) == 0, 'wrong order len'
        assert len(obj_) == 0, 'wrong Turn len'
        # print(obj_.__repr__())
        # assert 'game_Turn' in obj_.__repr__(), 'wrong Turn repr'

    def test_Turn_add_phase(self) -> None:
        """Add rule to Turn
        """
        obj_ = Turn('game_Turn')
        obj_.add_phase('this', 'rule_text')
        assert len(obj_._order) == 1, 'wrong order len'
        assert isinstance(obj_._order[0], Rule), 'wrong rule type'
        assert obj_._order[0].name == 'this', 'wrong rule name'
        assert obj_._order[0].text == 'rule_text', 'wrong rule text'
        obj_.add_phase('that', 'rule_text')
        assert obj_._order[1].name == 'that', 'wrong rule name'

    def test_new_cycle(self) -> None:
        """Test start new cycle of Turn
        """
        obj_ = Turn('game_Turn')
        obj_.add_phase('this', 'rule_text')
        obj_.add_phase('that', 'rule_text')
        obj_.new_cycle()
        assert len(obj_) == 2, 'wrong Turn len'
        assert obj_[0].name == 'this', 'wrong first element'
        assert obj_[1].name == 'that', 'wrong second element'
        obj_.pop()
        assert len(obj_) == 1, 'wrong Turn len'
        obj_.new_cycle()
        assert len(obj_) == 2, 'Turn not clean'
