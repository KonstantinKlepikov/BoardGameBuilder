import json
import pytest
import random
from typing import Union
from collections import deque
from bgameb.base import Component
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.tools import Shaker, Deck, Steps, Bag, BaseTool
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

    @pytest.fixture
    def obj_(self) -> BaseTool:
        tool = BaseTool('this')
        tool.c = Component(
            dice=Dice('dice'), card=Card('card')
                )
        return tool

    @pytest.fixture
    def dealt_obj_(self, obj_: BaseTool) -> BaseTool:
        obj_.current.append(Dice('dice'))
        obj_.current.append(Card('card'))
        return obj_

    def test_tool_init(self, obj_: BaseTool) -> None:
        """Test tool classes instancing
        """
        assert isinstance(obj_.current, list), 'wrong type of current'
        assert len(obj_.current) == 0, 'wrong current len'
        assert obj_.id == 'this', 'not set ID for instance'
        assert len(obj_.c) == 2, 'wrong items'

    def test_stuff_classes_are_converted_to_json(self, obj_: BaseTool) -> None:
        """Test to json convertatrion
        """
        j = json.loads(obj_.to_json())
        assert j['id'] == 'this', 'not converted to json'

    def test_item_replace(self, obj_: BaseTool) -> None:
        """Test _item_replace()
        """
        card = Card('card')
        item = obj_._item_replace(card)
        assert item.id == 'card', 'wrong id'
        assert item.count == 1, 'wrong count'
        assert id(item) != id(card), 'not replaced'
        dice = Dice('dice')
        item = obj_._item_replace(dice)
        assert item.id == 'dice', 'wrong id'
        assert item.count == 1, 'wrong count'
        assert item.sides == 2, 'wrong sides'
        assert id(item) != id(dice), 'not replaced'

    def test_clear(self, dealt_obj_: BaseTool) -> None:
        """Test current clear
        """
        assert len(dealt_obj_.current) == 2, 'wrong current len'
        dealt_obj_.clear()
        assert isinstance(dealt_obj_.current, list), 'wrong current'
        assert len(dealt_obj_.current) == 0, 'wrong current len'

    def test_current_ids(self, dealt_obj_: BaseTool) -> None:
        """Test get_curren_names()
        """
        assert len(dealt_obj_.current_ids()) == 2, \
            'wrong current names len'
        assert dealt_obj_.current_ids()[0] == 'dice', \
            'wrong current names'

    def test_append(self, dealt_obj_: BaseTool) -> None:
        """Test curent append
        """
        card = Card('card')
        dealt_obj_.append(card)
        assert len(dealt_obj_.current) == 3, 'wrong current len'
        assert dealt_obj_.current[1].id == 'card', 'wrong append'
        assert id(card) != id(dealt_obj_.current[2]), 'not replaced'

    def test_count(self, dealt_obj_: BaseTool) -> None:
        """Test current count of given item
        """
        assert dealt_obj_.count('dice') == 1, 'wrong count'
        assert dealt_obj_.count('nothing') == 0, 'wrong count'

    def test_extend(self, dealt_obj_: BaseTool) -> None:
        """Test extend currend by items
        """
        items = [Card('unique'), Dice('dice')]
        dealt_obj_.extend(items)
        assert len(dealt_obj_.current) == 4, 'wrong current len'
        assert dealt_obj_.current[2].id == 'unique', 'wrong append'
        assert id(items[0]) != id(dealt_obj_.current[2]), 'not replaced'
        assert dealt_obj_.current[3].id == 'dice', 'wrong append'

    def test_index(self, dealt_obj_: BaseTool) -> None:
        """Test index currend
        """
        assert dealt_obj_.index('card') == 1, 'wrong index'
        assert dealt_obj_.index('dice') == 0, 'wrong index'
        assert dealt_obj_.index('card', start=1) == 1, 'wrong index'
        with pytest.raises(ValueError):
            dealt_obj_.index('card', start=12)
        with pytest.raises(ValueError):
            dealt_obj_.index('imposible')
        with pytest.raises(ValueError):
            dealt_obj_.index('card', start=6, end=10)

    def test_insert(self, dealt_obj_: BaseTool) -> None:
        """Test insert into currend
        """
        item = Card('unique')
        dealt_obj_.insert(item, 1)
        assert len(dealt_obj_.current) == 3, 'wrong len'
        assert dealt_obj_.current[1].id == 'unique', 'not inserted'
        assert id(item) != id(dealt_obj_.current[1]), 'not replaced'
        dealt_obj_.insert(item, 55)
        assert dealt_obj_.current[3].id == 'unique', 'not inserted'

    def test_pop(self, dealt_obj_: BaseTool) -> None:
        """Test pop
        """
        assert dealt_obj_.pop().id == 'card', 'wrong pop'
        dealt_obj_.current.clear()
        with pytest.raises(IndexError):
            dealt_obj_.pop()

    def test_remove(self, dealt_obj_: BaseTool) -> None:
        """Test remove
        """
        assert dealt_obj_.current[0].id == 'dice', 'wrong order'
        dealt_obj_.remove('dice')
        assert len(dealt_obj_.current) == 1, 'wrong len'
        with pytest.raises(ValueError):
            dealt_obj_.remove('not_exist')

    def test_reverse(self, dealt_obj_: BaseTool) -> None:
        """Test reverse
        """
        items = dealt_obj_.current
        items.reverse()
        dealt_obj_.reverse()
        assert dealt_obj_.current == items, 'not reversed'


class TestBag:
    """Test Bag class
    """

    @pytest.fixture(scope='function')
    def obj_(self) -> Bag:
        obj_ = Bag('bag')
        obj_.c = Component(
            card=Card('card'), dice=Dice('Dice')
                )
        return obj_

    @pytest.fixture(scope='function')
    def dealt_obj_(self, obj_: Bag) -> Bag:
        obj_.deal()
        return obj_

    @pytest.mark.parametrize(
        "_class,_id",
        [(Dice, 'dice_nice'), (Card, 'card_ward'), (Step, 'next_step')]
            )
    def test_add_new_item_to_bag(
        self,
        _class: Union[Card, Dice, Step],
        _id: str,
        obj_: Bag
            ) -> None:
        """Test add new item to bag
        """
        cl = _class(_id)
        obj_.add(cl)
        assert obj_.c[cl.id].id == _id, 'stuff not added'

    def test_bag_deal(self, dealt_obj_: Bag) -> None:
        """Test obj_ deal()
        """
        assert len(dealt_obj_.current) == 2, 'wrong current len'
        ids1 = dealt_obj_.current_ids()
        assert 'card' in ids1, 'wrong cards ids inside current'
        assert 'Dice' in ids1, 'wrong dice ids inside current'
        dealt_obj_.deal()
        comp = [id(item) for item in dealt_obj_.c.values()]
        cur = [id(item) for item in dealt_obj_.current]
        assert comp != cur, 'dont created new instances'
        ids2 = dealt_obj_.current_ids()
        assert ids1 == ids2, 'wrong order'

    def test_bag_deal_from_list(self, obj_: Bag) -> None:
        """Test bag deal() from items
        """
        items = ['card', 'card', 'card', 'Dice']
        result = obj_.deal(items).current
        assert len(result) == 4, 'wrong current len'
        ids = obj_.current_ids()
        assert ids == items, 'wrong deal'
        assert 'card' in ids, 'wrong cards ids inside current'
        assert 'Dice' in ids, 'wrong dice id inside current'
        result = obj_.deal(items).current
        comp = [id(item) for item in obj_.c.values()]
        cur = [id(item) for item in result]
        assert comp != cur, 'dont created new instances'
        assert ids == items, 'wrong order'


class TestShaker:
    """Test Shaker class
    """

    @pytest.fixture
    def obj_(self) -> Shaker:
        obj_ = Shaker('shaker')
        obj_.c = Component(
            dice=Dice('dice', count=5), dice_nice=Dice('dice_nice', count=5)
                )
        return obj_

    @pytest.fixture
    def dealt_obj_(self, obj_: Shaker) -> Shaker:
        obj_.deal()
        return obj_

    def test_add_new_item_to_shaker(self, obj_: Bag) -> None:
        """Test add new item to bag
        """
        obj_.add(Dice('omg'))
        assert obj_.c.omg.id == 'omg', 'stuff not added'

    def test_roll_shaker(self, dealt_obj_: Shaker) -> None:
        """Test roll shaker
        """
        roll = dealt_obj_.roll()
        assert len(roll) == 2, 'wrong roll result'
        assert len(roll['dice']) == 5, 'wrong roll result'

    def test_roll_empty_shaker(self) -> None:
        """Test roll empty shaker
        """
        obj_ = Shaker('shaker')
        roll = obj_.roll()
        assert roll == {}, 'wrong roll result'


class TestDeck:
    """Test Deck class
    """

    @pytest.fixture
    def obj_(self) -> Deck:
        obj_ = Deck('deck')
        obj_.c = Component(
            card=Card('card', count=5), card_nice=Card('Card_nice', count=5)
                )
        return obj_

    @pytest.fixture
    def dealt_obj_(self, obj_: Deck) -> Deck:
        obj_.deal()
        return obj_

    def test_deck_instanciation(self, obj_: Deck) -> None:
        """Test deck correct created
        """
        assert obj_.id == 'deck', 'wrong id'
        assert isinstance(obj_.current, deque), 'wrong type of current'
        assert len(obj_.current) == 0, 'nonempty current'

    def test_add_new_item_to_deck(self, obj_: Bag) -> None:
        """Test add new item to bag
        """
        obj_.add(Card('omg'))
        assert obj_.c.omg.id == 'omg', 'stuff not added'

    def test_item_replace(self, obj_: Deck) -> None:
        """Test _item_replace()
        """
        c = Card('wow')
        card = obj_._item_replace(c)
        assert card.id == 'wow', 'wrong id'
        assert card.count == 1, 'wrong count'
        assert id(card) != id(c), 'not replaced'

    def test_steps_clear_last(self, dealt_obj_: Deck) -> None:
        """Test clear() clear last
        """
        dealt_obj_.pop()
        assert dealt_obj_.last, 'empty last'
        dealt_obj_.clear()
        assert dealt_obj_.last is None, 'nonempty last'

    def test_appendleft(self, dealt_obj_: Deck) -> None:
        """Test current append left
        """
        card = Card('unique')
        dealt_obj_.appendleft(card)
        assert len(dealt_obj_.current) == 11, 'wrong current len'
        assert dealt_obj_.current[0].id == 'unique', 'wrong append'
        assert id(card) != id(dealt_obj_.current[10]), 'not replaced'

    def test_extendleft(self, dealt_obj_: Deck) -> None:
        """Test extendleft currend by cards
        """
        cards = [Card('unique'), Card('another')]
        dealt_obj_.extendleft(cards)
        assert len(dealt_obj_.current) == 12, 'wrong current len'
        assert dealt_obj_.current[1].id == 'unique', 'wrong append'
        assert id(cards[1]) != id(dealt_obj_.current[1]), 'not replaced'
        assert dealt_obj_.current[0].id == 'another', 'wrong append'

    def test_popleft(self, dealt_obj_: Deck) -> None:
        """Test pop left
        """
        assert dealt_obj_.popleft().id == 'card', 'wrong pop'
        assert dealt_obj_.last.id == 'card', 'empty last'
        dealt_obj_.current.clear()
        with pytest.raises(IndexError):
            dealt_obj_.pop()

    def test_pop(self, dealt_obj_: Deck) -> None:
        """Test pop left
        """
        assert dealt_obj_.pop().id == 'Card_nice', 'wrong pop'
        assert dealt_obj_.last.id == 'Card_nice', 'empty last'
        dealt_obj_.current.clear()
        with pytest.raises(IndexError):
            dealt_obj_.pop()

    def test_rotate(self, dealt_obj_: Deck) -> None:
        """Test rotate
        """
        dealt_obj_.rotate(1)
        assert len(dealt_obj_.current) == 10, 'not rotated'
        assert dealt_obj_.current[0].id == 'Card_nice', \
            'wrong side of rotation'
        dealt_obj_.rotate(-1)
        assert len(dealt_obj_.current) == 10, 'not rotated'
        assert dealt_obj_.current[0].id == 'card', 'wrong side of rotation'

    def test_deck_deal(self, obj_: Deck) -> None:
        """Test deck deal()
        """
        result = obj_.deal().current
        assert len(result) == 10, 'wrong current len'
        ids1 = [stuff.id for stuff in result]
        assert 'card' in ids1, 'wrong cards ids inside current'
        assert 'Card_nice' in ids1, 'wrong cards ids inside current'
        result = obj_.deal().current
        comp = [id(card) for card in obj_.c.values()]
        cur = [id(card) for card in result]
        assert comp != cur, 'dont created new instances'
        ids2 = [stuff.id for stuff in result]
        assert ids1 == ids2, 'wrong order'

    def test_deck_deal_from_list(self, obj_: Deck) -> None:
        """Test deck deal() from items
        """
        items = ['card', 'card', 'card', 'Card_nice']
        result = obj_.deal(items).current
        assert len(result) == 4, 'wrong current len'
        ids = [stuff.id for stuff in result]
        assert ids == items, 'wrong deal'
        assert 'card' in ids, 'wrong cards ids inside current'
        assert 'Card_nice' in ids, 'wrong cards ids inside current'
        result = obj_.deal(items).current
        comp = [id(card) for card in obj_.c.values()]
        cur = [id(card) for card in result]
        assert comp != cur, 'dont created new instances'
        assert ids == items, 'wrong order'

    def test_deck_shuffle(self, obj_: Deck) -> None:
        """Test deck shuffle()
        """
        with FixedSeed(42):
            current0 = obj_.deal().current.copy()
            obj_.shuffle()
            assert obj_.current != current0, 'not changed order'

    def test_check_order_len(self, dealt_obj_: Deck) -> None:
        """Test _check_order_len()
        """
        assert dealt_obj_._check_order_len(10) is None, 'not checked'
        with pytest.raises(
            ArrangeIndexError,
            match='len of current deque'
                ):
            dealt_obj_._check_order_len(11)
        with pytest.raises(
            ArrangeIndexError,
            match='Given empty order'
                ):
            dealt_obj_._check_order_len(0)

    def test_check_is_to_arrange_valid(self, dealt_obj_: Deck) -> None:
        """Test _check_is_to_arrange_valid()
        """
        order = dealt_obj_.current_ids()
        order1 = order.copy()
        order1.reverse()
        assert dealt_obj_._check_is_to_arrange_valid(order1, order) is None, \
            'not checked'
        order1[0] = 'uncown'
        with pytest.raises(
            ArrangeIndexError,
            match='ids not match'
                ):
            dealt_obj_._check_is_to_arrange_valid(order1, order)

    def test_deck_reorder(self, dealt_obj_: Deck) -> None:
        """Test deck reorder()
        """
        order = dealt_obj_.current_ids()
        order.reverse()
        dealt_obj_.reorder(order)
        assert dealt_obj_.current_ids() == order, 'wrong order'

        with FixedSeed(42):
            dealt_obj_.shuffle()
            old_oder = dealt_obj_.current_ids().copy()
            order = dealt_obj_.current_ids()[5:]
            order.reverse()
            dealt_obj_.reorder(order)
            assert dealt_obj_.current_ids()[5:] == order, 'wrong order'
            assert dealt_obj_.current_ids()[0:5] == old_oder[0:5], \
                'wrong order'

    def test_deck_reorderleft(self, dealt_obj_: Deck) -> None:
        """Test deck reorderleft()
        """
        order = dealt_obj_.current_ids()
        order.reverse()
        dealt_obj_.reorderleft(order)
        assert dealt_obj_.current_ids() == order, 'wrong order'

        with FixedSeed(42):
            dealt_obj_.shuffle()
            old_oder = dealt_obj_.current_ids().copy()
            order = dealt_obj_.current_ids()[0:5]
            order.reverse()
            dealt_obj_.reorderleft(order)
            assert dealt_obj_.current_ids()[0:5] == order, 'wrong order'
            assert dealt_obj_.current_ids()[5:0] == old_oder[5:0], \
                'wrong order'

    def test_deck_reorderfrom(self, dealt_obj_: Deck) -> None:
        """Test deck reorderfrom()
        """
        with FixedSeed(42):
            dealt_obj_.shuffle()
            old_oder = dealt_obj_.current_ids().copy()
            order = dealt_obj_.current_ids()[2:6]
            order.reverse()
            dealt_obj_.reorderfrom(order, 2)
            assert dealt_obj_.current_ids()[2:6] == order, 'wrong order'
            assert dealt_obj_.current_ids()[0:2] == old_oder[0:2], \
                'wrong order'
            assert dealt_obj_.current_ids()[6:] == old_oder[6:], 'wrong order'

            with pytest.raises(
                ArrangeIndexError,
                match='range is out of current index'
                    ):
                dealt_obj_.reorderfrom(order, 0)

            with pytest.raises(
                ArrangeIndexError,
                match='range is out of current index'
                    ):
                dealt_obj_.reorderfrom(order, 7)

    def test_search(self, obj_: Deck) -> None:
        """Test deck search() one or many or no one cards
        """
        obj_.c.card.count = 2
        obj_.c.card_nice.count = 2
        obj_.deal()
        search = obj_.search(query={'card': 1})
        assert len(search) == 1, 'wrong search len'
        assert isinstance(search[0], BaseItem), 'wrong search type'
        assert search[0].id == 'card', 'wrong finded id'
        assert len(obj_.current) == 3, 'wrong current len'

        search = obj_.search(query={'Card_nice': 2}, remove=False)
        assert len(search) == 2, 'wrong search len'
        assert search[0].id == 'Card_nice', 'wrong finded id'
        assert len(obj_.current) == 3, 'wrong current len'

        search = obj_.search(query={'card': 1, 'Card_nice': 1})
        assert len(search) == 2, 'wrong search len'
        assert len(obj_.current) == 1, 'wrong current len'

        search = obj_.search(query={'Card_nice': 50})
        assert len(search) == 1, 'wrong search len'
        assert len(obj_.current) == 0, 'wrong current len'

        obj_.deal()
        search = obj_.search(query={'wrong_card': 1})
        assert len(search) == 0, 'wrong search len'
        assert len(obj_.current) == 4, 'wrong current len'

    def test_get_random_from_empty_current(self, obj_: Deck) -> None:
        """Test get_random from empty current
        """
        result = obj_.get_random()
        assert isinstance(result, list), 'wrong type'
        assert len(result) == 0, 'nonempty result'

    def test_get_random_without_removing(self, obj_: Deck) -> None:
        """Test get_random without removing cards
        """
        obj_.c.card.count = 2
        obj_.c.card_nice.count = 2
        with FixedSeed(42):
            obj_.deal().shuffle()
            result = obj_.get_random(4, remove=False)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            result_ids = [card.id for card in result]
            assert result_ids == [
                'Card_nice', 'Card_nice', 'Card_nice', 'Card_nice'
                    ], 'not random result'
            assert len(obj_.current) == 4, 'wrong result'

    def test_get_random_with_removing(self, obj_: Deck) -> None:
        """Test get_random with removing cards
        """
        obj_.c.card.count = 2
        obj_.c.card_nice.count = 2
        with FixedSeed(42):
            obj_.deal().shuffle()
            result = obj_.get_random(4)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            result_ids = [card.id for card in result]
            assert result_ids == [
                'card', 'Card_nice', 'Card_nice', 'card'
                    ], 'not random result'
            assert len(obj_.current) == 0, 'wrong result'

    def test_get_random_with_removing_much_more(self, obj_: Deck) -> None:
        """Test get_random with removing cards
        and count mor than len of current
        """
        obj_.c.card.count = 2
        obj_.c.card_nice.count = 2
        with FixedSeed(42):
            obj_.deal().shuffle()
            result = obj_.get_random(12)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            assert len(obj_.current) == 0, 'wrong result'


class TestSteps:
    """Test Steps class
    """

    @pytest.fixture
    def obj_(self) -> Steps:
        obj_ = Steps('game_turns')
        obj_.c = Component(
            step1=Step('step1', priority=1), astep=Step('asteP', priority=2)
                )
        return obj_

    def test_steps_instance(self) -> None:
        """Test Steps class instance
        """
        obj_ = Steps('game_turns')
        assert isinstance(obj_.current, list), 'wrong current type'
        assert len(obj_.current) == 0, 'wrong current len'
        assert obj_.last is None, 'wrong last'

    def test_steps_clear_last(self, obj_: Steps) -> None:
        """Test clear() clear last
        """
        obj_.deal()
        obj_.pull()
        assert obj_.last, 'empty last'
        obj_.clear()
        assert obj_.last is None, 'nonempty last'

    def test_steps_add_step(self, obj_: Steps) -> None:
        """Test add step to steps
        """
        obj_.add(Step('omg', priority=42))
        assert obj_.c.omg.id == 'omg', 'stuff not added'

    def test_push(self, obj_: Steps) -> None:
        """Test push to steps
        """
        s = Step('omg', priority=42)
        obj_.push(s)
        assert len(obj_.current) == 1, 'not pushed'
        assert obj_.current[0][1].id == 'omg', 'wrong id'
        assert id(obj_.current[0][1].id) != id(s), 'not replaced'

    def test_pull(self, obj_: Steps) -> None:
        """Test pull step from steps
        """
        s = Step('omg', priority=42)
        obj_.push(s)
        step = obj_.pull()
        assert step.id == 'omg', 'wrong step'
        assert obj_.last.id == 'omg', 'wrong step'
        assert id(step) == id(obj_.last), 'wrong steps ids'

    def test_steps_deal(self, obj_: Steps) -> None:
        """Test start new cycle of turn
        """
        result = obj_.deal().current
        assert len(result) == 2, 'wrong len'
        assert len(obj_.current_ids()) == 2, 'wrong current names len'
        assert obj_.current_ids()[0] == 'step1', 'wrong current names'
        current = obj_.pull()
        assert len(obj_.current) == 1, 'wrong len'
        assert current.id == 'step1', 'wrong current step'
        assert obj_.last.id == 'step1', 'wrong current step'
        current = obj_.pull()
        assert len(obj_.current) == 0, 'wrong len'
        assert current.id == 'asteP', 'wrong current step'
        assert obj_.last.id == 'asteP', 'wrong current step'
        with pytest.raises(
            IndexError,
            match='index out of range'
                ):
            obj_.pull()
        result = obj_.deal().current
        assert len(result) == 2, 'turn not clean'

    def test_steps_deal_from_list(self, obj_: Steps) -> None:
        """Test steps deal() from items
        """
        items = ['step1', 'asteP', 'asteP']
        result = obj_.deal(items).current
        assert len(result) == 3, 'wrong current len'
        assert len(obj_.current_ids()) == 3, 'wrong current names len'
        assert obj_.current_ids()[0] == 'step1', 'wrong current names'
        obj_.pull()
        assert len(result) == 2, 'wrong current len'
        assert obj_.current_ids()[0] == 'asteP', 'wrong current names'
