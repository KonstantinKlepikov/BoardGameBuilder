import pytest
from bgameb.rules import Rule, RulesMixin
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
