import json
import pytest
import random
from collections import deque
from bgameb.base import Components
from bgameb.markers import Step
from bgameb.items import Dice, Card, BaseItem
from bgameb.tools import Shaker, Deck, Order, Steps, BaseTool
from bgameb.errors import ArrangeIndexError


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


class TestTool:
    """Test tools classes
    """
    params = [
        (Deck, 'deck_yeah'),
        (Shaker, 'shaker_wzzzz'),
        (Steps, 'steps_to')
        ]

    @pytest.mark.parametrize("_class, name", params)
    def test_tool_classes_created_with_name(
        self,
        _class: BaseTool,
        name: str,
            ) -> None:
        """Test stuff classes instancing
        """
        obj_ = _class(name=name)
        assert obj_.name == name, 'not set name for instance'

    @pytest.mark.parametrize("_class, name", params)
    def test_stuff_classes_are_converted_to_json(
        self,
        _class: BaseTool,
        name: str,
            ) -> None:
        """Test to json convertatrion
        """
        obj_ = _class(name=name)
        j = json.loads(obj_.to_json())
        assert j['name'] == name, 'not converted to json'


class TestShaker:
    """Test Shaker class
    """

    def test_roll_shaker(self) -> None:
        """Test roll shaker
        """
        obj_ = Shaker(name='shaker')
        obj_['dice'] = Dice('dice', count=5)
        obj_['dice_nice'] = Dice('dice_nice', count=5)
        roll = obj_.roll()
        assert len(roll) == 2, 'wrong roll result'
        assert len(roll['dice']) == 5, 'wrong roll result'

    def test_roll_empty_shaker(self) -> None:
        """Test roll empty shaker
        """
        obj_ = Shaker(name='shaker')
        roll = obj_.roll()
        assert roll == {}, 'wrong roll result'


class TestDeck:
    """Test Deck class
    """

    @pytest.fixture
    def obj_(self) -> Deck:
        obj_ = Deck(name='deck')
        obj_['card'] = Card('card', count=20)
        obj_['card_nice'] = Card('card_nice', count=20)
        return obj_

    def test_deck_instanciation(self) -> None:
        """Test deck correct created
        """
        obj_ = Deck(name='deck')
        assert obj_.name == 'deck', 'wrong name'
        assert isinstance(obj_.current, deque), 'wrong type of current'
        assert len(obj_.current) == 0, 'nonempty current'

    def test_deck_deal(self, obj_: Deck) -> None:
        """Test obj_ deal() randomizing
        """
        with FixedSeed(42):
            result = obj_.deal()
            assert len(result) == 40, 'wrong current len'
            names = [stuff.name for stuff in result]
            assert 'card' in names, 'wrong cards names inside current'
            assert 'card_nice' in names, 'wrong cards names inside current'
            before = [id(card) for card in result]
            result = obj_.deal()
            after = [id(card) for card in result]
            assert before != after, 'not random order'

    def test_deck_shuffle(self, obj_: Deck) -> None:
        """Test deck shuffle()
        """
        obj_.card.count = 5
        obj_.card_nice.count = 5
        current0 = obj_.deal().copy()
        obj_.shuffle()
        assert obj_.current != current0, 'not changed order'

    def test_clear(self, obj_: Deck) -> None:
        """Test deck clean()
        """
        obj_.card.count = 5
        obj_.card_nice.count = 5
        obj_.current.clear()
        assert isinstance(obj_.current, deque), 'nonempty current'
        assert len(obj_.current) == 0, 'nonempty current'

    def test_search(self, obj_: Deck) -> None:
        """Test deck search() one or many or no one cards
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        obj_.deal()
        search = obj_.search(query={'card': 1})
        assert len(search) == 1, 'wrong search len'
        assert isinstance(search[0], BaseItem), 'wrong search type'
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

    def test_to_arrange(self, obj_: Deck) -> None:
        """Test to_arrange() deck
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
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

    def test_arrrange_random(self, obj_: Deck) -> None:
        """Test arrange() randomaising
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        with FixedSeed(42):
            obj_.deal()
            arranged, last = obj_.to_arrange(0, 3)
            arranged.sort(key=lambda x: x.name)
            before = [stuff.name for stuff in obj_.current]
            result = obj_.arrange(arranged, last)
            after = [stuff.name for stuff in result]
            assert after != before, 'not arranged'

    def test_arrrange_returns_same_len(self, obj_: Deck) -> None:
        """Test arrange() returns same len
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        obj_.deal()
        arranged, last = obj_.to_arrange(0, 4)
        arranged.pop()
        with pytest.raises(
            ArrangeIndexError,
            match="Wrong to_arranged parts"
                ):
            obj_.arrange(arranged, last)

    def test_get_random_from_empty_current(self, obj_: Deck) -> None:
        """Test get_random from empty current
        """
        result = obj_.get_random()
        assert isinstance(result, list), 'wrong type'
        assert len(result) == 0, 'nonempty result'

    def test_get_random_without_removing(self, obj_: Deck) -> None:
        """Test get_random without removing cards
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        with FixedSeed(42):
            obj_.deal()
            result = obj_.get_random(4, remove=False)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            result_names = [card.name for card in result]
            assert result_names == [
                'card_nice', 'card_nice', 'card_nice', 'card_nice'
                    ], 'not random result'
            assert len(obj_.current) == 4, 'wrong result'

    def test_get_random_with_removing(self, obj_: Deck) -> None:
        """Test get_random with removing cards
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        with FixedSeed(42):
            obj_.deal()
            result = obj_.get_random(4)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            result_names = [card.name for card in result]
            assert result_names == [
                'card', 'card_nice', 'card_nice', 'card'
                    ], 'not random result'
            assert len(obj_.current) == 0, 'wrong result'

    def test_get_random_with_removing_much_more(self, obj_: Deck) -> None:
        """Test get_random with removing cards
        and count mor than len of current
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        with FixedSeed(42):
            obj_.deal()
            result = obj_.get_random(12)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            assert len(obj_.current) == 0, 'wrong result'


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

    @pytest.fixture
    def obj_(self) -> Steps:
        obj_ = Steps('game_turns')
        obj_['step1'] = Step('step1', priority=1)
        obj_['astep'] = Step('astep', priority=2)
        return obj_

    def test_steps_instance(self) -> None:
        """Test Steps class instance
        """
        obj_ = Steps('game_turns')
        assert isinstance(obj_, Components), 'wrong turn type'
        assert isinstance(obj_.current, Order), 'wrong current type'
        assert len(obj_.current) == 0, 'wrong current len'

    def test_steps_add_steps(self, obj_: Steps) -> None:
        """Test add step to steps
        """
        assert isinstance(obj_.step1, Step), 'wrong type'
        assert obj_.step1.name == 'step1', 'wrong name'
        assert obj_.step1.priority == 1, 'wrong priority'

    def test_steps_deal(self, obj_: Steps) -> None:
        """Test start new cycle of turn
        """
        result = obj_.deal()
        assert len(result) == 2, 'wrong len'
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
        result = obj_.deal()
        assert len(result) == 2, 'turn not clean'
