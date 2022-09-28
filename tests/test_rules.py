import pytest
from bgameb.rules import Rule


class TestRule:
    """Test Rule class
    """

    def test_rule_instance(self) -> None:
        """Test Rule class instance
        """
        obj_ = Rule(name='this_rule')
        assert obj_.name == 'this_rule', 'wrong name'
        assert obj_.is_active, 'wrong is_active'
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

    def test_rule_equal(self) -> None:
        """Test equal of Rules
        """
        obj_1 = Rule(name='this_rule')
        obj_2 = Rule(name='this_rule')
        assert obj_1 == obj_2, 'not equal'
        obj_2.this = 'this'
        assert obj_1 != obj_2, 'equal'
