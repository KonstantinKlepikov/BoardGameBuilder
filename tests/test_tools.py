import json
import pytest
import random
from typing import Tuple
from collections import deque
from bgameb.game import Game
from bgameb.tools import Shaker, Deck, Bag, Order, Steps, BaseTool
from bgameb.stuff import Step, BaseStuff
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
def game_inst() -> Game:
    game = Game(name='game')
    game.new('dice', type_='dice')
    game.new('dice_nice', type_='dice')
    game.new('card', type_='card')
    game.new('card_nice', type_='card')
    game.new('step1', type_='step', priority=1)
    game.new('astep', type_='step', priority=2)
    return game


class TestTool:
    """Test tools classes
    """
    params = [
        (Bag, Bag._type, ('card', 'card_nice')),
        (Deck, Deck._type, ('card', 'card_nice')),
        (Shaker, Shaker._type, ('dice', 'dice_nice')),
        (Steps, Steps._type, ('step1', 'astep'))
        ]

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_increase_stuff_raise_errors_if_wrong_count(
        self,
        game_inst: Game,
        _class: BaseTool,
        name: str,
        stuff: Tuple[str]
            ) -> None:
        """Test need count of stuff no less than 1
        """
        obj_ = _class(name=name)
        with pytest.raises(
            StuffDefineError, match="Can't add"
                ):
            obj_._increase(stuff[0], game=game_inst, count=0)

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_increase_stuff_to_raise_errors_if_wrong_name(
        self,
        game_inst: Game,
        _class: BaseTool,
        name: str,
        stuff: Tuple[str]
            ) -> None:
        """Test need exist stuff
        """
        obj_ = _class(name=name)
        with pytest.raises(
            StuffDefineError, match="'somestuff' not exist in a game"
                ):
            obj_._increase('somestuff', game=game_inst)

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_double_increase_stuff_encrease_count(
        self,
        game_inst: Game,
        _class: BaseTool,
        name: str,
        stuff: Tuple[str]
            ) -> None:
        """Test double add dice with same name increase count,
        not raises error
        """
        obj_ = _class(name=name)
        obj_._increase(stuff[0], game=game_inst)
        obj_._increase(stuff[0], game=game_inst)
        assert obj_[stuff[0]].count == 2, 'not increased'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_increase_stuff(
        self,
        game_inst: Game,
        _class: BaseTool,
        name: str,
        stuff: Tuple[str]
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
        self,
        game_inst: Game,
        _class: BaseTool,
        name: str,
        stuff: Tuple[str]
            ) -> None:
        """Test remove all stuff from shaker
        """
        obj_ = _class(name=name)
        obj_._increase(stuff[0], game=game_inst)
        obj_._increase(stuff[1], game=game_inst)
        assert len(obj_._stuff) == 2, 'wrong number of stuff'
        obj_.remove()
        assert len(obj_._stuff) == 0, 'wrong number of stuff'
        assert isinstance(obj_._stuff, list), 'wrong type os stuff attr'

    @pytest.mark.parametrize("_class, name, stuff", params)
    def test_remove_by_name(
        self,
        game_inst: Game,
        _class: BaseTool,
        name: str,
        stuff: Tuple[str]
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
        self,
        game_inst: Game,
        _class: BaseTool,
        name: str,
        stuff: Tuple[str]
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

    def test_shaker_instanciation(self) -> None:
        """Test shaker correct created
        """
        obj_ = Shaker(name='shaker')
        assert obj_.name == 'shaker', 'wrong name'
        assert isinstance(obj_, Components), 'wrong type of stuff'
        assert len(obj_._stuff) == 0, 'nonempty stuff'
        assert issubclass(obj_._stuff_to_add, BaseStuff), \
            'wrong stuff _stuff_to_add'

    def test_shaker_are_converted_to_json(self, game_inst: Game) -> None:
        """Test to json convertatrion
        """
        obj_ = Shaker(name='shaker')
        obj_._increase('dice', game=game_inst)
        j = json.loads(obj_.to_json())
        assert j['name'] == 'shaker', 'wrong name'
        assert j['dice']['name'] == 'dice', 'wrong name of stuff'

    def test_roll_shaker(self, game_inst: Game) -> None:
        """Test roll shaker
        """
        obj_ = Shaker(name='shaker')
        obj_._increase('dice', game=game_inst, count=5)
        obj_._increase('dice_nice', game=game_inst, count=5)
        roll = obj_.roll()
        assert len(roll) == 2, 'wrong roll result'
        assert len(roll['dice']) == 5, 'wrong roll result'

    def test_roll_empty_shaker(self, game_inst: Game) -> None:
        """Test roll empty shaker
        """
        obj_ = Shaker(name='shaker')
        roll = obj_.roll()
        assert roll == {}, 'wrong roll result'


class TestDeck:
    """Test Deck class
    """

    def test_deck_instanciation(self) -> None:
        """Test deck correct created
        """
        obj_ = Deck(name='deck')
        assert obj_.name == 'deck', 'wrong name'
        assert isinstance(obj_, Components), 'wrong type of stuff'
        assert len(obj_._stuff) == 0, 'nonempty stuff'
        assert isinstance(obj_.current, deque), 'wrong type of current'
        assert len(obj_.current) == 0, 'nonempty current'
        assert issubclass(obj_._stuff_to_add, BaseStuff), \
            'wrong stuff _stuff_to_add'

    def test_deck_are_converted_to_json(self, game_inst: Game) -> None:
        """Test to json convertatrion
        """
        obj_ = Deck(name='deck')
        obj_._increase('card', game=game_inst)
        j = json.loads(obj_.to_json())
        assert j['name'] == 'deck', 'wrong name'
        assert j['card']['name'] == 'card', 'wrong name of stuff'

    def test_deck_deal(self, game_inst: Game) -> None:
        """Test obj_ deal() randomizing
        """
        with FixedSeed(42):
            obj_ = Deck(name='deck')
            obj_._increase('card', game=game_inst, count=20)
            obj_._increase('card_nice', game=game_inst, count=20)
            obj_.deal()
            assert len(obj_.current) == 40, 'wrong current len'
            names = [stuff.name for stuff in obj_.current]
            assert 'card' in names, 'wrong cards names inside current'
            assert 'card_nice' in names, 'wrong cards names inside current'
            before = [id(card) for card in obj_.current]
            obj_.deal()
            after = [id(card) for card in obj_.current]
            assert before != after, 'not random order'

    def test_deck_shuffle(self, game_inst: Game) -> None:
        """Test deck shuffle()
        """
        obj_ = Deck(name='deck')
        obj_._increase('card', game=game_inst, count=5)
        obj_._increase('card_nice', game=game_inst, count=5)
        obj_.deal()
        current0 = obj_.current.copy()
        obj_.shuffle()
        assert obj_.current != current0, 'not changed order'

    def test_clear(self, game_inst: Game) -> None:
        """Test deck clean()
        """
        obj_ = Deck(name='deck')
        obj_._increase('card', game=game_inst, count=5)
        obj_._increase('card_nice', game=game_inst, count=5)
        obj_.current.clear()
        assert isinstance(obj_.current, deque), 'nonempty current'
        assert len(obj_.current) == 0, 'nonempty current'

    def test_search(self, game_inst: Game) -> None:
        """Test deck search() one or many or no one cards
        """
        obj_ = Deck(name='deck')
        obj_._increase('card', game=game_inst, count=2)
        obj_._increase('card_nice', game=game_inst, count=2)
        obj_.deal()
        search = obj_.search(query={'card': 1})
        assert len(search) == 1, 'wrong search len'
        assert isinstance(search[0], BaseStuff), 'wrong search type'
        assert search[0].name == 'card', 'wrong finded name'
        assert len(obj_.current) == 3, 'wrong current len'

        search = obj_.search(query={'card_nice': 2}, remove=False)
        assert len(search) == 2, 'wrong search len'
        assert search[0].name == 'card_nice', 'wrong finded name'
        assert len(obj_.current) == 3, 'wrong current len'

        search = obj_.search(query={'card': 1, 'card_nice': 1})
        assert len(search) == 2, 'wrong search len'
        assert len(obj_.current) == 1, 'wrong current len'

        search = obj_.search(query={'card_nice': 50})
        assert len(search) == 1, 'wrong search len'
        assert len(obj_.current) == 0, 'wrong current len'

        obj_.deal()
        search = obj_.search(query={'wrong_card': 1})
        assert len(search) == 0, 'wrong search len'
        assert len(obj_.current) == 4, 'wrong current len'

    def test_to_arrange(self, game_inst: Game) -> None:
        """Test to_arrange() deck
        """
        obj_ = Deck(name='deck')
        obj_._increase('card', game=game_inst, count=2)
        obj_._increase('card_nice', game=game_inst, count=2)
        obj_.deal()

        arranged, last = obj_.to_arrange(0, 1)
        assert len(last) == 2, 'wrong last len'
        assert isinstance(last[0], list), 'wrong left'
        assert isinstance(last[1], list), 'wrong right'
        assert isinstance(arranged, list), 'wrong center'
        assert arranged[0].name == obj_.current[0].name, 'wrong arranged'
        assert last[0] == [], 'wrong split'
        assert len(last[1]) == 3, 'wrong split'

        arranged, last = obj_.to_arrange(1, 2)
        assert len(last[0]) == 1, 'wrong split'
        assert len(last[1]) == 2, 'wrong split'
        assert len(arranged) == 1, 'wrong center'

        arranged, last = obj_.to_arrange(1, 50)
        assert len(last[0]) == 1, 'wrong split'
        assert len(last[1]) == 0, 'wrong split'
        assert len(arranged) == 3, 'wrong center'

        with pytest.raises(
            ArrangeIndexError,
            match='Nonpositive or broken'
                ):
            arranged, last = obj_.to_arrange(-3, 0)
        with pytest.raises(
            ArrangeIndexError,
            match='Nonpositive or broken'
                ):
            arranged, last = obj_.to_arrange(5, -55)
        with pytest.raises(
            ArrangeIndexError,
            match='Nonpositive or broken'
                ):
            arranged, last = obj_.to_arrange(5, 3)

    def test_arrrange_random(self, game_inst: Game) -> None:
        """Test arrange() randomaising
        """
        with FixedSeed(42):
            obj_ = Deck(name='deck')
            obj_._increase('card', game=game_inst, count=2)
            obj_._increase('card_nice', game=game_inst, count=2)
            obj_.deal()
            arranged, last = obj_.to_arrange(0, 3)
            arranged.sort(key=lambda x: x.name)
            before = [stuff.name for stuff in obj_.current]
            obj_.arrange(arranged, last)
            after = [stuff.name for stuff in obj_.current]
            assert after != before, 'not arranged'

    def test_arrrange_returns_same_len(self, game_inst: Game) -> None:
        """Test arrange() returns same len
        """
        obj_ = Deck(name='deck')
        obj_._increase('card', game=game_inst, count=2)
        obj_._increase('card_nice', game=game_inst, count=2)

        obj_.deal()
        arranged, last = obj_.to_arrange(0, 4)
        arranged.pop()
        with pytest.raises(
            ArrangeIndexError,
            match="Wrong to_arranged parts"
                ):
            obj_.arrange(arranged, last)


class TestOrder:
    """Test order class
    """

    def test_init_order(self) -> None:
        """Test correct inity order
        """
        obj_ = Order()
        assert isinstance(obj_.current, list), 'wrong current'
        assert len(obj_.current) == 0, 'wrong len current'

    def test_order_methods(self) -> None:
        """Test order methods
        """
        obj_ = Order()
        item_in = Step('one', priority=0)
        assert len(obj_) == 0, 'wrong len Order'
        obj_.put(item_in)
        assert len(obj_) == 1, 'wrong len Order'
        item_out = obj_.get()
        assert len(obj_) == 0, 'wrong len Order'
        assert item_out is item_in, 'wrong item'
        obj_.put(item_in)
        obj_.clear()
        assert len(obj_) == 0, 'wrong len Order'
        assert isinstance(obj_.current, list), 'wrong current'

    def test_order_ordering(self) -> None:
        """Test order priority ordering
        """
        obj_ = Order()
        for i in range(3):
            item_in = Step('step', priority=i)
            obj_.put(item_in)
        for i in range(3):
            item_out = obj_.get()
            assert item_out.priority == i, 'wrong priority'


class TestSteps:
    """Test Steps class
    """

    def test_steps_instance(self) -> None:
        """Test Steps class instance
        """
        obj_ = Steps('game_turns')
        assert isinstance(obj_, Components), 'wrong turn type'
        assert isinstance(obj_.current, Order), 'wrong current type'
        assert len(obj_.current) == 0, 'wrong current len'
        assert len(obj_._stuff) == 0, 'wrong turn len'

    def test_steps_add_steps(self, game_inst: Game) -> None:
        """Test add step to steps
        """
        obj_ = Steps('game_turns')
        obj_._increase('step1', game=game_inst)
        assert len(obj_._stuff) == 1, 'wrong stuff len'
        assert isinstance(obj_.step1, Step), 'wrong type'
        assert obj_.step1.name == 'step1', 'wrong name'
        assert obj_.step1.priority == 1, 'wrong priority'

    def test_steps_deal(self, game_inst: Game) -> None:
        """Test start new cycle of turn
        """
        obj_ = Steps('game_turns')
        obj_._increase('step1', game=game_inst)
        obj_._increase('astep', game=game_inst)
        obj_.deal()
        assert len(obj_.current) == 2, 'wrong len'
        current = obj_.current.get()
        assert len(obj_.current) == 1, 'wrong len'
        assert current.name == 'step1', 'wrong current step'
        current = obj_.current.get()
        assert len(obj_.current) == 0, 'wrong len'
        assert current.name == 'astep', 'wrong current step'
        with pytest.raises(
            IndexError,
            match='index out of range'
                ):
            obj_.current.get()
        obj_.deal()
        assert len(obj_.current) == 2, 'turn not clean'
