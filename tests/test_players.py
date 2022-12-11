import json
from bgameb.players import Player
from bgameb.constraints import ITEMS_TOOLS


class TestPlayer:
    """Test creation with id and json schemes
    """

    def test_players_classes_created(self) -> None:
        """Test players classes instancing
        """
        obj_ = Player('player')
        assert obj_.id == 'player', 'not set id for instance'
        assert obj_._types_to_add == ITEMS_TOOLS, \
            'wrong _type_to_add'

    def test_players_classes_are_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Player('player')
        j = json.loads(obj_.to_json())
        assert j['id'] == 'player', 'not converted to json'
