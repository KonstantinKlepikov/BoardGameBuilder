import pytest
from collections import deque
from bgameb.rules import Rule, RulesMixin, Stream
from bgameb.base import Components


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
        assert "this='this'" in obj_.__repr__(), 'wrong repr'
        obj_.this = 'that'
        assert obj_.this == 'that', 'not set or cant update'
        del obj_.this
        with pytest.raises(
            AttributeError, match='this'
            ):
            obj_.this
        with pytest.raises(
            KeyError, match='this'
            ):
            del obj_.this

class TestRulesMixin:
    """Test RulesMixin
    """

    def test_rulesmixin_instance(self) -> None:
        """Test RulesMixin instance
        """
        obj_ = RulesMixin()
        assert isinstance(obj_.rules, Components), 'wrong type'
        obj_.add_rule('this', 'that')
        assert isinstance(obj_.rules.this, Rule), 'wrong type of rule'
        assert obj_.rules.this.name == 'this', 'wrong name of rule'
        assert obj_.rules.this.text == 'that', 'wrong text rule'


class TestStream:
    """Test Stream class
    """

    def test_stream_instance(self) -> None:
        """Test Stream class instance
        """
        obj_ = Stream('game_stream')
        assert isinstance(obj_, deque), 'wrong stream type'
        assert isinstance(obj_._order, list), 'wrong order type'
        assert len(obj_._order) == 0, 'wrong order len'
        assert len(obj_) == 0, 'wrong stream len'
        assert 'game_stream' in obj_.__repr__(), 'wrong stream repr'

    def test_stream_add_rule(self) -> None:
        """Add rule to stream
        """
        obj_ = Stream('game_stream')
        obj_.add_rule('this', 'rule_text')
        assert len(obj_._order) == 1, 'wrong order len'
        assert isinstance(obj_._order[0], Rule), 'wrong rule type'
        assert obj_._order[0].name == 'this', 'wrong rule name'
        assert obj_._order[0].text == 'rule_text', 'wrong rule text'
        obj_.add_rule('that', 'rule_text')
        assert obj_._order[1].name == 'that', 'wrong rule name'

    def test_new_cycle(self) -> None:
        """Test start new cycle of Stream
        """
        obj_ = Stream('game_stream')
        obj_.add_rule('this', 'rule_text')
        obj_.add_rule('that', 'rule_text')
        obj_.new_cycle()
        assert len(obj_) == 2, 'wrong stream len'
        assert obj_[0].name == 'this', 'wrong first element'
        assert obj_[1].name == 'that', 'wrong second element'
        obj_.pop()
        assert len(obj_) == 1, 'wrong stream len'
        obj_.new_cycle()
        assert len(obj_) == 2, 'stream not clean'
