import json
import pytest
from bgameb.game import Game
from bgameb.base import Components, Base
from bgameb.items import Dice, Card
from bgameb.tools import Steps, Deck, Shaker
from bgameb.markers import Counter
from bgameb.types import COMPONENTS
from bgameb.errors import ComponentClassError, ComponentNameError


class TestGame:
    """Test Game class
    """

    def test_game_class_created_with_name(self) -> None:
        """Test Game name instancing
        """
        obj_ = Game(name='this_game')
        assert obj_.name == 'this_game', 'not set name for instance'
        assert isinstance(obj_, Components), 'isnt component'
        assert obj_._types_to_add == COMPONENTS, 'wrong _types_to_add'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Game(name='game')
        j = json.loads(obj_.to_json())
        assert j['name'] == 'game', 'not converted to json'

    components = [
        (Game, 'subgame'),
        (Dice, 'dice_nice'),
        (Card, 'card_ward'),
        (Steps, 'steps_new'),
        (Deck, 'deck_some'),
        (Shaker, 'shaker_this'),
        (Counter, 'counter_less'),
        ]

    @pytest.mark.parametrize("_class, name", components)
    def test_add_new_component_to_game(
        self, _class: Base, name: str
            ) -> None:
        """Test add new component to Game
        """
        obj_ = Game(name='game')
        cl = _class(name)
        obj_.add(component=_class(name))
        assert obj_[cl.name].name == name, \
            'component not added'

    def test_add_new_wrong_component_to_game(self) -> None:
        """Test cant add new wrong component to game
        """
        obj_ = Game(name='game')

        class G():
            _type = 'wrong'

        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.add(G())

    @pytest.mark.parametrize("_class, name", components)
    def test_cant_add_new_existed_component(
        self, _class: Base, name: str
            ) -> None:
        """Test cant add new object with same existed name in a game
        """
        obj_ = Game(name='game')
        cl = _class(name)
        obj_.add(component=cl)
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):

            obj_.add(component=cl)
