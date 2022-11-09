import json
from bgameb.players import Player
from bgameb.types import MARKERS_ITEMS_TOOLS


class TestPlayer:
    """Test creation with names and json schemes
    """

    def test_players_classes_created_with_name(self) -> None:
        """Test players classes instancing
        """
        obj_ = Player(name='player')
        assert obj_.name == 'player', 'not set name for instance'
        assert obj_._types_to_add == MARKERS_ITEMS_TOOLS, \
            'wrong _type_to_add'

    def test_players_classes_are_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Player(name='player')
        j = json.loads(obj_.to_json())
        assert j['name'] == 'player', 'not converted to json'

    def test_players_attributes(self) -> None:
        """Test players attributes
        """
        obj_ = Player(name='player')
        assert obj_.has_priority is False, 'wrong priority'
        assert obj_.team is None, 'wrong tram'
