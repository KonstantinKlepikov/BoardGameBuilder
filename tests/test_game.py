import json
import pytest
from bgameb.game import Game
from bgameb.base import Component, Base
from bgameb.items import Dice, Card
from bgameb.tools import Steps, Deck, Shaker
from bgameb.types import COMPONENTS
from bgameb.errors import ComponentClassError, ComponentNameError


class TestGame:
    """Test Game class
    """

    def test_game_class_created(self) -> None:
        """Test Game instancing
        """
        obj_ = Game('this game')
        assert obj_.id == 'this game', 'not set id for instance'
        assert isinstance(obj_, Component), 'isnt component'
        assert obj_._types_to_add == COMPONENTS, 'wrong _types_to_add'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Game('game')
        j = json.loads(obj_.to_json())
        assert j['id'] == 'game', 'not converted to json'

    components = [
        (Game, 'subgame'),
        (Dice, 'dice_nice'),
        (Card, 'card_ward'),
        (Steps, 'steps_new'),
        (Deck, 'deck_some'),
        (Shaker, 'shaker_this'),
        ]

    @pytest.mark.parametrize("_class, _id", components)
    def test_add_new_component_to_game(
        self, _class: Base, _id: str
            ) -> None:
        """Test add new component to Game
        """
        obj_ = Game('game')
        cl = _class(_id)
        obj_.add(component=_class(_id))
        assert obj_[cl.id].id == _id, 'component not added'

    def test_add_new_wrong_component_to_game(self) -> None:
        """Test cant add new wrong component to game
        """
        obj_ = Game('game')

        class G():
            _type = 'wrong'

        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.add(G())

    @pytest.mark.parametrize("_class, _id", components)
    def test_cant_add_new_existed_component(
        self, _class: Base, _id: str
            ) -> None:
        """Test cant add new object with same existed name in a game
        """
        obj_ = Game('game')
        cl = _class(_id)
        obj_.add(component=cl)
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):

            obj_.add(component=cl)
