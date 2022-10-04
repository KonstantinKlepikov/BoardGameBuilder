import json, pytest, random
from typing import Tuple
from collections import deque
from bgameb.game import Game, BaseGame
from bgameb.tools import Shaker, Deck, CardsBag, BaseTool
from bgameb.stuff import BaseStuff
from bgameb.base import Components
from bgameb.errors import StuffDefineError, ArrangeIndexError


class FixedSeed:
    """Context manager to set random seed
    """
    def __init__(self, seed):
        self.seed = seed
        self.state = None

    def __enter__(self):
        self.state = random.getstate()
        random.seed(self.seed)

    def __exit__(self, exc_type, exc_value, traceback):
        random.setstate(self.state)


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
        (CardsBag, 'hand', ('card', 'card_nice')),
        (Deck, 'deck', ('card', 'card_nice')),
        (Shaker, 'shaker', ('dice', 'dice_nice')),
        ]

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_increase_stuff_to_tool_raise_errors_if_wrong_count(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test need count of stuff no less than 1
        """
        obj_ = _class(name=name)
        with pytest.raises(
            StuffDefineError, match="Can't add"
            ):
            obj_._increase(stuff[0], game=game_inst, count=0)

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_increase_stuff_to_tool_raise_errors_if_wrong_name(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test need exist stuff
        """
        obj_ = _class(name=name)
        with pytest.raises(
            StuffDefineError, match="'somestuff' not exist in a game"
            ):
            obj_._increase('somestuff', game=game_inst)

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_double_increase_stuff_to_tool_encrease_count(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test double add roller with same name increase count,
        not raises error
        """
        obj_ = _class(name=name)
        obj_._increase(stuff[0], game=game_inst)
        obj_._increase(stuff[0], game=game_inst)
        assert obj_[stuff[0]].count == 2, 'not increased'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_increase_stuff_to_shaker(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test shaker add()
        """
        obj_ = _class(name=name)
        obj_._increase(stuff[0], game=game_inst)
        assert obj_[stuff[0]].count == 1, 'wrong count added'
        obj_._increase(stuff[0], game=game_inst, count=10)
        assert obj_[stuff[0]].count == 11, 'wrong count added'
        obj_._increase(stuff[1], game=game_inst)
        assert len(obj_._stuff) == 2, 'wrong count of stuff'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_remove_all(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test remove all stuff from shaker
        """
        obj_ = _class(name=name)
        obj_._increase(stuff[0], game=game_inst)
        obj_._increase(stuff[1], game=game_inst)
        assert len(obj_._stuff) == 2, 'wrong number of stuff'
        obj_.remove()
        assert len(obj_._stuff) == 0, 'wrong number of stuff'
        assert isinstance(obj_._stuff, set), 'wrong type os stuff attr'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_remove_by_name(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test remove stuff by name from shaker
        """
        obj_ = _class(name=name)
        obj_._increase(stuff[0], game=game_inst)
        obj_._increase(stuff[1], game=game_inst)
        assert len(obj_._stuff) == 2, 'wrong number of stuff'
        obj_.remove(name=stuff[0])
        assert len(obj_._stuff) == 1, 'wrong number of stuff'
        obj_.remove(name=stuff[1])
        assert len(obj_._stuff) == 0, 'wrong number of stuff'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_remove_stuff(
        self, game_inst: BaseGame, _class: BaseTool, name: str, stuff: Tuple[str]
            ) -> None:
        """Test remove stuff
        """
        obj_ = _class(name=name)
        obj_._increase(stuff[0], game=game_inst, count=5)
        obj_._increase(stuff[1], game=game_inst, count=5)

        assert len(obj_._stuff) == 2, 'wrong number of stuff'
        obj_.remove(stuff[0], count=3)
        assert len(obj_._stuff) == 2, 'wrong number of stuff'
        assert obj_[stuff[0]].count == 2, 'wrong count of stuff'
        obj_.remove(stuff[0], count=50)
        assert len(obj_._stuff) == 1, 'wrong number of stuff'
        with pytest.raises(
            StuffDefineError, match="Count must be a integer"
        ):
            obj_.remove(stuff[1], count=0)
        with pytest.raises(
            StuffDefineError, match="not exist in tool"
        ):
            obj_.remove(stuff[0], count=1)
        obj_.remove(count=50)
        assert len(obj_._stuff) == 0, 'stuff not removed'


class TestShaker:
    """Test Shaker class
    """

    def test_shaker_instanciation(self, game_inst: BaseGame) -> None:
        """Test shaker correct created
        """
        shaker = Shaker(name='shaker')
        assert shaker.name == 'shaker', 'wrong name'
        assert shaker.is_active, 'wrong is_active'
        assert isinstance(shaker.last, dict), 'nondict last'
        assert isinstance(shaker, Components), 'wrong type of stuff'
        assert len(shaker._stuff) == 0, 'nonempty stuff'
        assert issubclass(shaker._stuff_to_add, BaseStuff), 'wrong stuff _stuff_to_add'

    def test_shaker_are_converted_to_json(self, game_inst: BaseGame) -> None:
        """Test to json convertatrion
        """
        shaker = Shaker(name='shaker')
        shaker._increase('dice', game=game_inst)
        j = json.loads(shaker.to_json())
        assert j['name'] == 'shaker', 'wrong name'
        assert j['last'] == {}, 'wrong last result'
        assert j['dice']['name'] == 'dice', 'wrong name of stuff'

    def test_roll_shaker(self, game_inst: BaseGame) -> None:
        """Test roll shaker
        """
        shaker = Shaker(name='shaker')
        shaker._increase('dice', game=game_inst, count=5)
        shaker._increase('dice_nice', game=game_inst, count=5)
        roll = shaker.roll()
        assert len(roll) == 2, 'wrong roll result'
        assert len(roll['dice']) == 5, 'wrong roll result'
        assert len(shaker.last) == 2, 'wrong last'

    def test_roll_empty_shaker(self, game_inst: BaseGame) -> None:
        """Test roll empty shaker
        """
        shaker = Shaker(name='shaker')
        roll = shaker.roll()
        assert roll == {}, 'wrong roll result'
        assert shaker.last == {}, 'wrong last'


class TestDeck:
    """Test Deck class
    """

    def test_shaker_instanciation(self, game_inst: BaseGame) -> None:
        """Test sdeck correct created
        """
        deck = Deck(name='deck')
        assert deck.name == 'deck', 'wrong name'
        assert deck.is_active, 'wrong is_active'
        assert isinstance(deck, Components), 'wrong type of stuff'
        assert len(deck._stuff) == 0, 'nonempty stuff'
        assert isinstance(deck.dealt, deque), 'wrong type of dealt'
        assert len(deck.dealt) == 0, 'nonempty dealt'
        assert issubclass(deck._stuff_to_add, BaseStuff), 'wrong stuff _stuff_to_add'

    def test_deck_are_converted_to_json(
        self, game_inst: BaseGame) -> None:
        """Test to json convertatrion
        """
        deck = Deck(name='deck')
        deck._increase('card', game=game_inst)
        j = json.loads(deck.to_json())
        assert j['name'] == 'deck', 'wrong name'
        assert j['card']['name'] == 'card', 'wrong name of stuff'

    def test_deck_deal(
        self, game_inst: BaseGame) -> None:
        """Test deck deal() randomizing
        """
        with FixedSeed(42):
            deck = Deck(name='deck')
            deck._increase('card', game=game_inst, count=20)
            deck._increase('card_nice', game=game_inst, count=20)
            deck.deal()
            assert len(deck.dealt) == 40, 'wrong dealt len'
            names = [stuff.name for stuff in deck.dealt]
            assert 'card' in names, 'wrong cards names inside dealt'
            assert 'card_nice' in names, 'wrong cards names inside dealt'
            before = [id(card) for card in deck.dealt]
            deck.deal()
            after = [id(card) for card in deck.dealt]
            assert before != after, 'not random order'

    def test_deck_shuffle(
        self, game_inst: BaseGame) -> None:
        """Test deck shuffle()
        """
        deck = Deck(name='deck')
        deck._increase('card', game=game_inst, count=5)
        deck._increase('card_nice', game=game_inst, count=5)
        deck.deal()
        dealt0 = deck.dealt.copy()
        deck.shuffle()
        assert deck.dealt != dealt0, 'not changed order'

    def test_clear(
        self, game_inst: BaseGame) -> None:
        """Test deck clean()
        """
        deck = Deck(name='deck')
        deck._increase('card', game=game_inst, count=5)
        deck._increase('card_nice', game=game_inst, count=5)
        deck.clear()
        assert isinstance(deck.dealt, deque), 'nonempty dealt'
        assert len(deck.dealt) == 0, 'nonempty dealt'

    def test_search(
        self, game_inst: BaseGame) -> None:
        """Test deck search() one or many or no one cards
        """
        deck = Deck(name='deck')
        deck._increase('card', game=game_inst, count=2)
        deck._increase('card_nice', game=game_inst, count=2)
        deck.deal()
        search = deck.search(query={'card': 1})
        assert len(search) == 1, 'wrong search len'
        assert isinstance(search[0], BaseStuff), 'wrong search type'
        assert search[0].name == 'card', 'wrong finded name'
        assert len(deck.dealt) == 3, 'wrong dealt len'

        search = deck.search(query={'card_nice': 2}, remove=False)
        assert len(search) == 2, 'wrong search len'
        assert search[0].name == 'card_nice', 'wrong finded name'
        assert len(deck.dealt) == 3, 'wrong dealt len'

        search = deck.search(query={'card': 1, 'card_nice': 1})
        assert len(search) == 2, 'wrong search len'
        assert len(deck.dealt) == 1, 'wrong dealt len'

        search = deck.search(query={'card_nice': 50})
        assert len(search) == 1, 'wrong search len'
        assert len(deck.dealt) == 0, 'wrong dealt len'

        deck.deal()
        search = deck.search(query={'wrong_card': 1})
        assert len(search) == 0, 'wrong search len'
        assert len(deck.dealt) == 4, 'wrong dealt len'

    def test_to_arrange(
        self, game_inst: BaseGame) -> None:
        """Test to_arrange() deck
        """
        deck = Deck(name='deck')
        deck._increase('card', game=game_inst, count=2)
        deck._increase('card_nice', game=game_inst, count=2)
        deck.deal()

        arranged, last = deck.to_arrange(0, 1)
        assert len(last) == 2, 'wrong last len'
        assert isinstance(last[0], list), 'wrong left'
        assert isinstance(last[1], list), 'wrong right'
        assert isinstance(arranged, list), 'wrong center'
        assert arranged[0].name == deck.dealt[0].name, 'wrong arranged'
        assert last[0] == [], 'wrong split'
        assert len(last[1]) == 3, 'wrong split'

        arranged, last = deck.to_arrange(1, 2)
        assert len(last[0]) == 1, 'wrong split'
        assert len(last[1]) == 2, 'wrong split'
        assert len(arranged) == 1, 'wrong center'

        arranged, last = deck.to_arrange(1, 50)
        assert len(last[0]) == 1, 'wrong split'
        assert len(last[1]) == 0, 'wrong split'
        assert len(arranged) == 3, 'wrong center'

        with pytest.raises(
            ArrangeIndexError,
            match='Nonpositive or broken'
            ):
            arranged, last = deck.to_arrange(-3, 0)
        with pytest.raises(
            ArrangeIndexError,
            match='Nonpositive or broken'
            ):
            arranged, last = deck.to_arrange(5, -55)
        with pytest.raises(
            ArrangeIndexError,
            match='Nonpositive or broken'
            ):
            arranged, last = deck.to_arrange(5, 3)

    def test_arrrange_random(
        self, game_inst: BaseGame) -> None:
        """Test arrange() randomaising
        """
        with FixedSeed(42):
            deck = Deck(name='deck')
            deck._increase('card', game=game_inst, count=2)
            deck._increase('card_nice', game=game_inst, count=2)
            deck.deal()
            arranged, last = deck.to_arrange(0, 3)
            arranged.sort(key=lambda x: x.name)
            before = [stuff.name for stuff in deck.dealt]
            deck.arrange(arranged, last)
            after = [stuff.name for stuff in deck.dealt]
            assert after != before, 'not arranged'

    def test_arrrange_returns_same_len(
        self, game_inst: BaseGame) -> None:
        """Test arrange() returns same len
        """
        deck = Deck(name='deck')
        deck._increase('card', game=game_inst, count=2)
        deck._increase('card_nice', game=game_inst, count=2)

        deck.deal()
        arranged, last = deck.to_arrange(0, 4)
        arranged.pop()
        with pytest.raises(
            ArrangeIndexError,
            match="Wrong to_arranged parts"
            ):
            deck.arrange(arranged, last)
