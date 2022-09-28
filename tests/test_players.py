import json, pytest
from collections import Counter
from bgameb.players import Player


class TestPlayer:
    """Test creation with names and json schemes
    """

    def test_players_classes_created_with_name(self) -> None:
        """Test players classes instancing
        """
        player = Player(name='player')
        assert player.name == 'player', 'not set name for instance'

    def test_players_classes_are_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        player = Player(name='player')
        j = json.loads(player.to_json())
        assert j['name'] == 'player', 'not converted to json'

    def test_players_attributes(self) -> None:
        """Test players attributes
        """
        player = Player(name='player')
        assert player.is_active == True, 'wrong is_active'
        assert player.has_priority == False, 'wrong priority'
        assert player.team is None, 'wrong tram'
        assert player.owner_of == [], 'wrong owner of'
        assert player.user_of == [], 'wrong user of'
        assert isinstance(player.counter, Counter), 'wrong counter'
