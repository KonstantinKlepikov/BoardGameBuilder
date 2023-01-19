import json
from collections import Counter
from pydantic import BaseModel
from loguru._logger import Logger
from bgameb.players_ import Player


class TestPlayer:
    """Test creation with id and json schemes
    """

    def test_players_classes_created(self) -> None:
        """Test players classes instancing
        """
        obj_ = Player(id='player')
        assert isinstance(obj_, BaseModel), 'wrong instance'
        assert obj_.id == 'player', 'not set id for instance'
        assert isinstance(obj_.counter, Counter), 'wrong counter type'
        assert len(obj_.counter) == 0, 'counter not empty'
        assert isinstance(obj_._to_relocate, dict), 'wrong _to_relocate'
        assert isinstance(obj_._logger, Logger), 'wrong _to_relocate'
        j : dict = json.loads(obj_.json())
        assert j['id'] == 'player', \
            'not converted to json'
        assert j.get('counter') is None, 'counter not excluded'
        assert j.get('_to_relocate') is None, '_to_relocat not excluded'
        assert j.get('_logger') is None, '_logger not excluded'
