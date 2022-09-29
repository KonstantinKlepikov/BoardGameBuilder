import json, pytest
from collections import Counter
from bgameb.players import Player


class TestPlayer:
    """Test creation with names and json schemes
    """

    def test_players_classes_created_with_name(self) -> None:
        """Test players classes instancing
        """
        obj_ = Player(name='player')
        assert obj_.name == 'player', 'not set name for instance'
        assert obj_.is_active, 'wrong is_active'

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
        assert obj_.is_active == True, 'wrong is_active'
        assert obj_.has_priority == False, 'wrong priority'
        assert obj_.team is None, 'wrong tram'
        assert obj_.owner_of == [], 'wrong owner of'
        assert obj_.user_of == [], 'wrong user of'
        assert isinstance(obj_.counter, Counter), 'wrong counter'
