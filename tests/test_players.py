import json
from bgameb.players import Player


class TestPlayer:
    """Test creation with id and json schemes
    """

    def test_players_classes_created(self) -> None:
        """Test players classes instancing
        """
        obj_ = Player(id='player')
        assert isinstance(obj_, Player), 'wrong instance'
        assert obj_.id == 'player', 'not set id for instance'
        j: dict = json.loads(obj_.json())
        assert j['id'] == 'player', \
            'not converted to json'
