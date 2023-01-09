import json
import pytest
from typing import Union, Optional
from dataclasses import dataclass, field
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
        assert game.c[cl.id].id == _id, 'stuff not added'

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
        assert game.c[cl.id].id == _id, 'stuff not added'

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
        assert game.c[cl.id].id == _id, 'stuff not added'

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

    def test_game_get_from_component(self, game: Game) -> None:
        """Test Game get stuff from component
        """
        game.add(Dice('this'))
        game.add(Card('one'))
        game.add(Step('fy'))
        game.add(Player('that'))
        game.add(Deck('some'))
        game.add(Shaker('width'))
        game.add(Steps('err'))
        game.add(Bag('pff'))
        assert len(game.get_items()) == 3, 'wrong items'
        assert len(game.get_tools()) == 4, 'wrong tools'
        assert len(game.get_players()) == 1, 'wrong players'

    def test_get_items_val(self, game: Game) -> None:
        """Test get_items_val
        """
        game.add(Dice('why'))
        result = game.get_items_val(game)
        assert len(result) == 1, 'wrong number of items'
        assert result[0]['id'] == 'why', 'wrong item'

    def test_get_tools_val(self, game: Game) -> None:
        """Test get_tools_val
        """
        game.add(Shaker('what'))
        game.c.what.add(Dice('why'))
        result = game.get_tools_val(game)
        assert len(result) == 1, 'wrong number of tools'
        assert result[0]['id'] == 'what', 'wrong tool'
        assert len(result[0]['items']) == 1, 'wrong number of items'
        assert result[0]['items'][0]['id'] == 'why', 'wrong item'

    def test_get_players_val(self, game: Game) -> None:
        """Test get_playerss_val
        """
        game.add(Player('billy'))
        game.c.billy.add(Shaker('what'))
        game.c.billy.add(Dice('hey'))
        game.c.billy.c.what.add(Dice('why'))
        result = game.get_players_val(game)
        assert len(result) == 1, 'wrong number of players'
        assert result[0]['id'] == 'billy', 'wrong player'
        assert len(result[0]['items']) == 1, 'wrong number of items'
        assert result[0]['items'][0]['id'] == 'hey', 'wrong item'
        assert len(result[0]['tools']) == 1, 'wrong number of tools'
        assert result[0]['tools'][0]['id'] == 'what', 'wrong item'
        assert len(result[0]['tools'][0]['items']) == 1, \
            'wrong number of items'
        assert result[0]['tools'][0]['items'][0]['id'] == 'why', 'wrong item'

    def test_build_json(self, game: Game) -> None:
        """Test build_json
        """
        game.add(Player('billy'))
        game.c.billy.add(Shaker('what'))
        game.c.billy.add(Dice('hey'))
        game.c.billy.c.what.add(Dice('why'))
        result = game.build_json()
        assert isinstance(result, str), 'wrong result'
        assert 'billy' in result, 'no player'
        assert 'what' in result, 'no tools'
        assert 'why' in result, 'no dices'
        assert 'hey' in result, 'no dices'

    def test_relocate_all(self, game: Game) -> None:
        """Test relocations of attrs in game class
        """
        @dataclass
        class PlayMe(Player):
            this: str = field(default_factory=str)

            def __post_init__(self) -> None:
                super().__post_init__()
                self._to_relocate = {
                    'this': 'id'
                }

        @dataclass
        class ShakeMe(Shaker):
            ups: list = field(default_factory=list)
            this: Optional[dict[str, list[int]]] = None

            def __post_init__(self) -> None:
                super().__post_init__()
                self._to_relocate = {
                    'ups': 'current',
                    'this': 'last'
                        }

        game.add(PlayMe('billy'))
        game.add(ShakeMe('some'))
        game.c.some.add(Dice('six'))
        game.c.some.deal()
        assert isinstance(game.relocate_all(), Game), 'wrong return'
        assert game.c.billy.this == game.c.billy.id, 'not relocated'
        assert game.c.some.ups == game.c.some.current, 'not relocated'
        assert game.c.some.this == game.c.some.last, 'not relocated'
