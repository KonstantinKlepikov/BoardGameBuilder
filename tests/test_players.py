import json, pytest
from bgameb.players import Player, Bot
from bgameb.constructs import BasePlayer


class TestBasePlayer:
    """Test creation with names and json schemes
    """
    params = [
        (Player, 'player'),
        (Bot, 'bot'),
    ]

    @pytest.mark.parametrize("_class, name", params)
    def test_players_classes_created_with_name(
        self, _class: BasePlayer, name: str
            ) -> None:
        """Test players classes instancing
        """
        assert not _class.name, 'class has name'
        player = _class()
        assert isinstance(player.name, str), 'wrong default name'
        player = _class(name=name)
        assert player.name == name, 'not set name for instance'

    @pytest.mark.parametrize("_class, name", params)
    def test_players_classes_are_converted_to_json(
        self, _class: BasePlayer, name: str
            ) -> None:
        """Test to json convertatrion
        """
        player = _class(name=name)
        j = json.loads(player.to_json())
        assert j['name'] == name, 'not converted to json'
        with pytest.raises(
            KeyError,
            match='_range'
            ):
            j['_range']

    @pytest.mark.parametrize("_class, name", params)
    def test_players_attributes(
        self, _class: BasePlayer, name: str
            ) -> None:
        """Test players attributes
        """
        player = _class(name=name)
        assert player.is_active == True, 'wrong is_active'
        assert player.has_priority == False, 'wrong priority'
        assert player.team is None, 'wrong tram'
        assert player.owner_of == [], 'wrong owner of'
        assert player.user_of == [], 'wrong user of'
