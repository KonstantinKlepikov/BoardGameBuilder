import json, pytest
from typing import Tuple
from bgameb.game import Game
from bgameb.tools import Shaker, Deck, BaseTool
from bgameb.stuff import BaseStuff
from bgameb.constructs import Components, BaseGame
from bgameb.errors import StuffDefineError


@pytest.fixture
def game_inst() -> BaseGame:
    game = Game(name='game')
    game.add('roller', name='dice')
    game.add('roller', name='dice_nice')
    game.add('card', name='card')
    game.add('card', name='card_nice')
    return game


class TestTool:
    """Test tools classes
    """
    params = [
        (Deck, 'deck', ('card', 'card_nice')),
        (Shaker, 'shaker', ('dice', 'dice_nice')),
    ]

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_add_stuff_to_tool_raise_errors_if_wrong_count(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test need count of stuff no less than 1
        """
        tool = _class(name=name, _game=game_inst)
        with pytest.raises(
            StuffDefineError, match="Can't add"
            ):
            tool.add(stuff[0], count=0)

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_add_stuff_to_tool_raise_errors_if_wrong_name(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test need exist stuff
        """
        tool = _class(name=name, _game=game_inst)
        with pytest.raises(
            StuffDefineError, match="'somestuff' not exist in a game"
            ):
            tool.add('somestuff')

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_double_add_stuff_to_tool_encrease_count(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test double add roller with same name increase count,
        not raises error
        """
        tool = _class(name=name, _game=game_inst)
        tool.add(stuff[0])
        tool.add(stuff[0])
        assert tool.stuff[stuff[0]].count == 2, 'not increased'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_add_stuff_to_shaker(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test shaker add()
        """
        tool = _class(name=name, _game=game_inst)
        tool.add(stuff[0])
        assert tool.stuff[stuff[0]].count == 1, 'wrong count added'
        tool.add(stuff[0], count=10)
        assert tool.stuff[stuff[0]].count == 11, 'wrong count added'
        tool.add(stuff[1])
        assert len(tool.stuff) == 2, 'wrong count of stuff'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_remove_all(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test remove all stuff from shaker
        """
        tool = _class(name=name, _game=game_inst)
        tool.add(stuff[0])
        tool.add(stuff[1])
        assert len(tool.stuff) == 2, 'wrong number of stuff'
        tool.remove()
        assert len(tool.stuff) == 0, 'wrong number of stuff'
        assert isinstance(tool.stuff, Components), 'wrong type os stuff attr'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_remove_by_name(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test remove stuff by name from shaker
        """
        tool = _class(name=name, _game=game_inst)
        tool.add(stuff[0])
        tool.add(stuff[1])
        assert len(tool.stuff) == 2, 'wrong number of stuff'
        tool.remove(name=stuff[0])
        assert len(tool.stuff) == 1, 'wrong number of stuff'
        tool.remove(name=stuff[1])
        assert len(tool.stuff) == 0, 'wrong number of stuff'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_remove_stuff(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test remove stuff
        """
        tool = _class(name=name, _game=game_inst)
        tool.add(stuff[0], count=5)
        tool.add(stuff[1], count=5)

        assert len(tool.stuff) == 2, 'wrong number of stuff'
        tool.remove(stuff[0], count=3)
        assert len(tool.stuff) == 2, 'wrong number of stuff'
        assert tool.stuff[stuff[0]].count == 2, 'wrong count of stuff'
        tool.remove(stuff[0], count=50)
        assert len(tool.stuff) == 1, 'wrong number of stuff'
        with pytest.raises(
            StuffDefineError, match="Count must be a integer"
        ):
            tool.remove(stuff[1], count=0)
        with pytest.raises(
            StuffDefineError, match="not exist in tool"
        ):
            tool.remove(stuff[0], count=1)
        tool.remove(count=50)
        assert len(tool.stuff) == 0, 'stuff not removed'


class TestShaker:
    """Test Shaker class
    """

    def test_shaker_instanciation(self, game_inst: BaseGame) -> None:
        """Test shaker correct created
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        assert shaker.name == 'shaker', 'wrong name'
        assert isinstance(shaker.last, dict), 'nondict last'
        assert isinstance(shaker.stuff, Components), 'wrong type of stuff'
        assert len(shaker.stuff) == 0, 'nonempty stuff'
        assert issubclass(shaker._stuff_to_add, BaseStuff), 'wrong stuff _stuff_to_add'

    def test_shaker_are_converted_to_json(self, game_inst: BaseGame) -> None:
        """Test to json convertatrion
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice')
        j = json.loads(shaker.to_json())
        assert j['name'] == 'shaker', 'wrong name'
        assert j['last'] == {}, 'wrong last result'
        assert len(j['stuff']) == 1, 'wrong num of stuff'

    def test_roll_shaker(self, game_inst: BaseGame) -> None:
        """Test roll shaker
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice', count=5)
        shaker.add('dice_nice', count=5)
        roll = shaker.roll()
        assert len(roll) == 2, 'wrong roll result'
        assert len(roll['dice']) == 5, 'wrong roll result'
        assert len(shaker.last) == 2, 'wrong last'

    def test_roll_empty_shaker(self, game_inst: BaseGame) -> None:
        """Test roll empty shaker
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        roll = shaker.roll()
        assert roll == {}, 'wrong roll result'
        assert shaker.last == {}, 'wrong last'


class TestDeck:
    """Test Deck class
    """

    def test_shaker_instanciation(self, game_inst: BaseGame) -> None:
        """Test sdeck correct created
        """
        deck = Deck(name='deck', _game=game_inst)
        assert deck.name == 'deck', 'wrong name'
        assert isinstance(deck.stuff, Components), 'wrong type of stuff'
        assert len(deck.stuff) == 0, 'nonempty stuff'
        assert issubclass(deck._stuff_to_add, BaseStuff), 'wrong stuff _stuff_to_add'

    def test_deck_are_converted_to_json(
        self, game_inst: BaseGame) -> None:
        """Test to json convertatrion
        """
        deck = Deck(name='deck', _game=game_inst)
        deck.add('card')
        j = json.loads(deck.to_json())
        assert j['name'] == 'deck', 'wrong name'
        assert len(j['stuff']) == 1, 'wrong num of cards'