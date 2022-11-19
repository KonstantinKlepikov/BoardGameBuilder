import json
import pytest
from bgameb.markers import Step


class TestBaseMarker:
    """Test creation with id and json schemes
    """
    params = [
        (Step, 'step_bep'),
        ]

    @pytest.mark.parametrize("_class, _id", params)
    def test_markers_classes_created_with_name(
        self, _class, _id: str
            ) -> None:
        """Test marker classes instancing
        """
        obj_ = _class(_id)
        assert obj_.id == _id, 'not set id for instance'

    @pytest.mark.parametrize("_class, _id", params)
    def test_marker_classes_are_converted_to_json(
        self, _class, _id: str
            ) -> None:
        """Test to json convertatrion
        """
        obj_ = _class(_id)
        j = json.loads(obj_.to_json())
        assert j['id'] == _id, 'not converted to json'


class TestStep:
    """Test Step class
    """

    def test_step_instance(self) -> None:
        """Test Step class instance
        """
        obj_ = Step('first_step')
        assert obj_.priority == 0, 'wrong priority'
        assert obj_.__class__.__name__.lower() == 'step', 'wrong type'
        obj1 = Step('first_step', priority=20)
        assert obj1.priority == 20, 'wrong priority'
        assert obj1 > obj_, 'wong comparison'
