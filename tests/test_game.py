import json
import pytest
from typing import Union
from collections import Counter
from bgameb.game import Game
from bgameb.items import Dice, Card, Step
from bgameb.tools import Steps, Deck, Shaker, Bag
from bgameb.players import Player
from bgameb.errors import ComponentClassError, ComponentNameError


class TestGame:
    """Test Game class
    """

    @pytest.fixture(scope='function')
    def game(self) -> Game:
        return Game('game')

    def test_game_class_created(self, game: Game) -> None:
        """Test Game instancing
        """
        assert game.id == 'game', 'not set id for instance'
        assert isinstance(game.counter, Counter), 'wrong counter type'
        assert len(game.counter) == 0, 'counter not empty'
        assert isinstance(game.other, dict), 'wrong other'

    def test_game_class_is_converted_to_json(self, game: Game) -> None:
        """Test to json convertatrion
        """
        j = json.loads(game.to_json())
        assert j['id'] == 'game', 'not converted to json'

    @pytest.mark.parametrize("_class,_id", [(Player, 'me'), ])
    def test_add_new_player_to_game(
        self, _class: Player, _id: str, game: Game
            ) -> None:
        """Test add new player to Game
        """
        cl = _class(_id)
        game.add(cl)
        assert game.p[cl.id].id == _id, 'stuff not added'

    @pytest.mark.parametrize(
        "_class,_id",
        [(Dice, 'dice_nice'), (Card, 'card_ward'), (Step, 'next_step')]
            )
    def test_add_new_item_to_game(
        self, _class: Union[Card, Dice, Step], _id: str, game: Game
            ) -> None:
        """Test add new item to Game
        """
        cl = _class(_id)
        game.add(cl)
        assert game.i[cl.id].id == _id, 'stuff not added'

    @pytest.mark.parametrize(
        "_class,_id",
        [(Deck, 'deck_some'), (Shaker, 'shaker_this'),
         (Bag, 'my_bag'), (Steps, 'steps_new'), ]
            )
    def test_add_new_tool_to_game(
        self, _class: Union[Card, Dice, Step], _id: str, game: Game
            ) -> None:
        """Test add new tool to Game
        """
        cl = _class(_id)
        game.add(cl)
        assert game.t[cl.id].id == _id, 'stuff not added'

    def test_add_new_wrong_component_to_game(self, game: Game) -> None:
        """Test cant add new wrong component to game
        """
        class G():
            _type = 'wrong'

        with pytest.raises(
            ComponentClassError,
            match='cant be used as part of Component.'
                ):
            game.add(G())

    def test_cant_add_new_existed_component(self, game: Game) -> None:
        """Test cant add new object with same existed name in a game
        """
        p = Player('me')
        game.add(p)
        with pytest.raises(
            ComponentNameError,
            match='wrong name of stuff'
                ):
            game.add(p)
