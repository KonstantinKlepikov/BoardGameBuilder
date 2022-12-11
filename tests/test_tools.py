import json
import pytest
import random
from collections import deque
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.tools import Shaker, Deck, Steps, Bag, BaseTool
from bgameb.errors import ArrangeIndexError
from bgameb.constraints import ITEMS


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
        tool.add(Dice('dice'))
        tool.add(Card('card'))
        return BaseTool('this')

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
        assert obj_._types_to_add == ITEMS, 'wrong _type_to_add'

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

    @pytest.fixture
    def obj_(self) -> Bag:
        obj_ = Bag('bag')
        obj_.add(Card('card'))
        obj_.add(Dice('dice'))
        return obj_

    @pytest.fixture
    def dealt_obj_(self, obj_: Bag) -> Bag:
        obj_.deal()
        return obj_

    def test_bag_deal(self, dealt_obj_: Bag) -> None:
        """Test obj_ deal()
        """
        assert len(dealt_obj_.current) == 2, 'wrong current len'
        ids1 = dealt_obj_.current_ids()
        assert 'card' in ids1, 'wrong cards ids inside current'
        assert 'card' in ids1, 'wrong dice ids inside current'
        before = [id(item) for item in dealt_obj_.current]
        dealt_obj_.deal()
        after = [id(item) for item in dealt_obj_.current]
        assert before != after, 'dont created new instances'
        ids2 = dealt_obj_.current_ids()
        assert ids1 == ids2, 'wrong order'

    def test_bag_deal_from_list(self, obj_: Bag) -> None:
        """Test bag deal() from items
        """
        items = ['card', 'card', 'card', 'dice']
        result = obj_.deal(items).current
        assert len(result) == 4, 'wrong current len'
        ids = obj_.current_ids()
        assert ids == items, 'wrong deal'
        assert 'card' in ids, 'wrong cards ids inside current'
        assert 'dice' in ids, 'wrong dice id inside current'
        before = [id(item) for item in result]
        result = obj_.deal(items).current
        after = [id(item) for item in result]
        assert before != after, 'dont created new instances'
        assert ids == items, 'wrong order'


class TestShaker:
    """Test Shaker class
    """

    @pytest.fixture
    def obj_(self) -> Shaker:
        obj_ = Shaker('shaker')
        obj_.add(Dice('dice', count=5))
        obj_.add(Dice('dice_nice', count=5))
        return obj_

    @pytest.fixture
    def dealt_obj_(self, obj_: Shaker) -> Shaker:
        obj_.deal()
        return obj_

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
        obj_.add(Card('card', count=5))
        obj_.add(Card('card_nice', count=5))
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

    def test_item_replace(self, obj_: Deck) -> None:
        """Test _item_replace()
        """
        card = obj_._item_replace(obj_.card)
        assert card.id == 'card', 'wrong id'
        assert card.count == 1, 'wrong count'
        assert id(card) != id(obj_.card), 'not replaced'

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
        dealt_obj_.current.clear()
        with pytest.raises(IndexError):
            dealt_obj_.pop()

    def test_rotate(self, dealt_obj_: Deck) -> None:
        """Test rotate
        """
        dealt_obj_.rotate(1)
        assert len(dealt_obj_.current) == 10, 'not rotated'
        assert dealt_obj_.current[0].id == 'card_nice', \
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
        assert 'card_nice' in ids1, 'wrong cards ids inside current'
        before = [id(card) for card in result]
        result = obj_.deal().current
        after = [id(card) for card in result]
        assert before != after, 'dont created new instances'
        ids2 = [stuff.id for stuff in result]
        assert ids1 == ids2, 'wrong order'

    def test_deck_deal_from_list(self, obj_: Deck) -> None:
        """Test deck deal() from items
        """
        items = ['card', 'card', 'card', 'card_nice']
        result = obj_.deal(items).current
        assert len(result) == 4, 'wrong current len'
        ids = [stuff.id for stuff in result]
        assert ids == items, 'wrong deal'
        assert 'card' in ids, 'wrong cards ids inside current'
        assert 'card_nice' in ids, 'wrong cards ids inside current'
        before = [id(card) for card in result]
        result = obj_.deal(items).current
        after = [id(card) for card in result]
        assert before != after, 'dont created new instances'
        assert ids == items, 'wrong order'

    def test_deck_shuffle(self, obj_: Deck) -> None:
        """Test deck shuffle()
        """
        with FixedSeed(42):
            current0 = obj_.deal().current.copy()
            obj_.shuffle()
            assert obj_.current != current0, 'not changed order'

    def test_search(self, obj_: Deck) -> None:
        """Test deck search() one or many or no one cards
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        obj_.deal()
        search = obj_.search(query={'card': 1})
        assert len(search) == 1, 'wrong search len'
        assert isinstance(search[0], BaseItem), 'wrong search type'
        assert search[0].id == 'card', 'wrong finded id'
        assert len(obj_.current) == 3, 'wrong current len'

        search = obj_.search(query={'card_nice': 2}, remove=False)
        assert len(search) == 2, 'wrong search len'
        assert search[0].id == 'card_nice', 'wrong finded id'
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
        assert arranged[0].id == obj_.current[0].id, 'wrong arranged'
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
        """Test arrange()
        """
        with FixedSeed(42):
            obj_.deal(['card_nice', 'card', 'card'])
            arranged, last = obj_.to_arrange(0, 2)
            arranged.sort(key=lambda x: x.id)
            before = [stuff.id for stuff in obj_.current]
            result = obj_.arrange(arranged, last).current
            after = [stuff.id for stuff in result]
            assert after != before, 'not arranged'

    def test_arrrange_returns_same_len(self, obj_: Deck) -> None:
        """Test arrange() returns same len
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        obj_.deal().shuffle()
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
            obj_.deal().shuffle()
            result = obj_.get_random(4, remove=False)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            result_names = [card.id for card in result]
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
            obj_.deal().shuffle()
            result = obj_.get_random(4)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            result_names = [card.id for card in result]
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
        obj_.add(Step('step1', priority=1))
        obj_.add(Step('astep', priority=2))
        return obj_

    def test_steps_instance(self) -> None:
        """Test Steps class instance
        """
        obj_ = Steps('game_turns')
        assert isinstance(obj_.current, list), 'wrong current type'
        assert len(obj_.current) == 0, 'wrong current len'
        assert obj_.last is None, 'wrong last'

    def test_steps_add_step(self, obj_: Steps) -> None:
        """Test add step to steps
        """
        assert isinstance(obj_.step1, Step), 'wrong type'
        assert obj_.step1.id == 'step1', 'wrong id'
        assert obj_.step1.priority == 1, 'wrong priority'

    def test_push(self, obj_: Steps) -> None:
        """Test push to steps
        """
        obj_.push(obj_.step1)
        assert len(obj_.current) == 1, 'not pushed'
        assert obj_.current[0][1].id == 'step1', 'wrong id'
        assert id(obj_.step1) != id(obj_.current[0][1]), 'not replaced'

    def test_pull(self, obj_: Steps) -> None:
        """Test pull step from steps
        """
        obj_.push(obj_.step1)
        step = obj_.pull()
        assert step.id == 'step1', 'wrong step'
        assert obj_.last.id == 'step1', 'wrong step'
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
        assert current.id == 'astep', 'wrong current step'
        assert obj_.last.id == 'astep', 'wrong current step'
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
        items = ['step1', 'astep', 'astep']
        result = obj_.deal(items).current
        assert len(result) == 3, 'wrong current len'
        assert len(obj_.current_ids()) == 3, 'wrong current names len'
        assert obj_.current_ids()[0] == 'step1', 'wrong current names'
        obj_.pull()
        assert len(result) == 2, 'wrong current len'
        assert obj_.current_ids()[0] == 'astep', 'wrong current names'
