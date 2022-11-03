import json
import pytest
import collections
from bgameb.markers import Step, Counter


class TestBaseMarker:
    """Test creation with names and json schemes
    """
    params = [
        (Step, 'step_bep'),
        (Counter, 'counter_my'),
        ]

    @pytest.mark.parametrize("_class, name", params)
    def test_markers_classes_created_with_name(
        self, _class, name: str
            ) -> None:
        """Test marker classes instancing
        """
        obj_ = _class(name=name)
        assert obj_.name == name, 'not set name for instance'

    @pytest.mark.parametrize("_class, name", params)
    def test_marker_classes_are_converted_to_json(
        self, _class, name: str
            ) -> None:
        """Test to json convertatrion
        """
        obj_ = _class(name=name)
        j = json.loads(obj_.to_json())
        assert j['name'] == name, 'not converted to json'


class TestCounter:
    """Test counter object
    """

    def test_counter_instance(self) -> None:
        """Test Step class instance
        """
        obj_ = Counter(name='yellow')
        assert isinstance(obj_.current, collections.Counter), 'wrong current'
        assert obj_.__class__.__name__.lower() == 'counter', 'wrong type'
        obj_.current['bacon'] = 1
        assert len(obj_.current) == 1, 'wrong len of counter'
        obj_.clear()
        assert len(obj_.current) == 0, 'wrong len of counter'


class TestStep:
    """Test Step class
    """

    def test_step_instance(self) -> None:
        """Test Step class instance
        """
        obj_ = Step(name='first_step')
        assert obj_.priority == 0, 'wrong priority'
        assert obj_.__class__.__name__.lower() == 'step', 'wrong type'
        obj1 = Step(name='first_step', priority=20)
        assert obj1.priority == 20, 'wrong priority'
        assert obj1 > obj_, 'wong comparison'
