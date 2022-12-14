import json
from collections import Counter
from bgameb.players import Player


class TestPlayer:
    """Test creation with id and json schemes
    """

    def test_players_classes_created(self) -> None:
        """Test players classes instancing
        """
        obj_ = Player('player')
        assert obj_.id == 'player', 'not set id for instance'
        assert isinstance(obj_.counter, Counter), 'wrong counter type'
        assert len(obj_.counter) == 0, 'counter not empty'
        assert isinstance(obj_.other, dict), 'wrong other'

    def test_players_classes_are_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Player('player')
        j = json.loads(obj_.to_json())
        assert j['id'] == 'player', 'not converted to json'
