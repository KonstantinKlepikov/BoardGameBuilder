import json
from collections import Counter
from bgameb.players import Player
from bgameb.items import Dice, Card, Step
from bgameb.tools import Steps, Deck, Shaker, Bag


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

    def test_player_get_from_component(self) -> None:
        """Test Player get stuff from component
        """
        obj_ = Player('player')
        obj_.add(Dice('this'))
        obj_.add(Card('one'))
        obj_.add(Step('fy'))
        obj_.add(Deck('some'))
        obj_.add(Shaker('width'))
        obj_.add(Steps('err'))
        obj_.add(Bag('pff'))
        assert len(obj_.get_items()) == 3, 'wrong items'
        assert len(obj_.get_tools()) == 4, 'wrong tools'
