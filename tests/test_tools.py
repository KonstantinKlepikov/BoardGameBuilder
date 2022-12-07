import json
import pytest
import random
from collections import deque
from bgameb.base import Component
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.tools import Shaker, Deck, Steps, BaseTool
from bgameb.errors import ArrangeIndexError
from bgameb.types import ITEMS


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
        (Steps, 'steps_to'),
            ]

    @pytest.mark.parametrize("_class, _id", params)
    def test_tool_init(
        self,
        _class: BaseTool,
        _id: str,
            ) -> None:
        """Test tool classes instancing
        """
        obj_ = _class(_id)
        assert obj_.id == _id, 'not set ID for instance'
        assert obj_._types_to_add == ITEMS, 'wrong _type_to_add'

    @pytest.mark.parametrize("_class, _id", params)
    def test_stuff_classes_are_converted_to_json(
        self,
        _class: BaseTool,
        _id: str,
            ) -> None:
        """Test to json convertatrion
        """
        obj_ = _class(_id)
        j = json.loads(obj_.to_json())
        assert j['id'] == _id, 'not converted to json'


class TestShaker:
    """Test Shaker class
    """

    def test_roll_shaker(self) -> None:
        """Test roll shaker
        """
        obj_ = Shaker('shaker')
        obj_['dice'] = Dice('dice', count=5)
        obj_.add(Dice('dice_nice', count=5))
        roll = obj_.roll()
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
        obj_['card'] = Card('card', count=5)
        obj_.add(Card('card_nice', count=5))
        return obj_

    @pytest.fixture
    def dealt_obj_(self, obj_: Deck) -> Deck:
        obj_.deal()
        return obj_

    def test_deck_instanciation(self) -> None:
        """Test deck correct created
        """
        obj_ = Deck('deck')
        assert obj_.id == 'deck', 'wrong id'
        assert isinstance(obj_.current, deque), 'wrong type of current'
        assert len(obj_.current) == 0, 'nonempty current'

    def test_card_replace(self, obj_: Deck) -> None:
        """Test _card_replace()
        """
        card = obj_._card_replace(obj_.card)
        assert card.id == 'card', 'wrong id'
        assert card.count == 1, 'wrong count in current'
        assert id(card) != id(obj_.card), 'not replaced'

    def test_append(self, dealt_obj_: Deck) -> None:
        """Test curent append
        """
        card = Card('unique')
        obj_ = dealt_obj_.append(card)
        assert len(obj_) == 11, 'wrong current len'
        assert obj_[10].id == 'unique', 'wrong append'
        assert id(card) != id(obj_[10]), 'not replaced'

    def test_appendleft(self, dealt_obj_: Deck) -> None:
        """Test current append left
        """
        card = Card('unique')
        obj_ = dealt_obj_.appendleft(card)
        assert len(obj_) == 11, 'wrong current len'
        assert obj_[0].id == 'unique', 'wrong append'
        assert id(card) != id(obj_[10]), 'not replaced'

    def test_clear(self, dealt_obj_: Deck) -> None:
        """Test current clear
        """
        dealt_obj_.clear()
        assert isinstance(dealt_obj_.current, deque), 'wrong current'
        assert len(dealt_obj_.current) == 0, 'wrong current len'

    def test_count(self, dealt_obj_: Deck) -> None:
        """Test current count of given card
        """
        assert dealt_obj_.count('card') == 5, 'wrong count'
        assert dealt_obj_.count('nothing') == 0, 'wrong count'

    def test_extend(self, dealt_obj_: Deck) -> None:
        """Test extend currend by cards
        """
        cards = [Card('unique'), Card('another')]
        obj_ = dealt_obj_.extend(cards)
        assert len(obj_) == 12, 'wrong current len'
        assert obj_[10].id == 'unique', 'wrong append'
        assert id(cards[0]) != id(obj_[10]), 'not replaced'
        assert obj_[11].id == 'another', 'wrong append'

    def test_extendleft(self, dealt_obj_: Deck) -> None:
        """Test extendleft currend by cards
        """
        cards = [Card('unique'), Card('another')]
        obj_ = dealt_obj_.extendleft(cards)
        assert len(obj_) == 12, 'wrong current len'
        assert obj_[1].id == 'unique', 'wrong append'
        assert id(cards[1]) != id(obj_[1]), 'not replaced'
        assert obj_[0].id == 'another', 'wrong append'

    def test_index(self, dealt_obj_: Deck) -> None:
        """Test index currend
        """
        assert dealt_obj_.index('card') == 0, 'wrong index'
        assert dealt_obj_.index('card_nice') == 5, 'wrong index'
        assert dealt_obj_.index('card_nice', start=6) == 6, 'wrong index'
        with pytest.raises(ValueError):
            dealt_obj_.index('card_nice', start=12)
        with pytest.raises(ValueError):
            dealt_obj_.index('imposible')
        with pytest.raises(ValueError):
            dealt_obj_.index('card', start=6, end=10)

    def test_insert(self, dealt_obj_: Deck) -> None:
        """Test insert into currend
        """
        card = Card('unique')
        obj_ = dealt_obj_.insert(card, 2)
        assert obj_[2].id == 'unique', 'not inserted'
        assert id(card) != id(obj_[2]), 'not replaced'
        obj_ = dealt_obj_.insert(card, 55)
        assert obj_[11].id == 'unique', 'not inserted'

    def test_pop(self, dealt_obj_: Deck) -> None:
        """Test pop right
        """
        assert dealt_obj_.pop().id == 'card_nice', 'wrong pop'
        dealt_obj_.current.clear()
        with pytest.raises(IndexError):
            dealt_obj_.pop()

    def test_popleft(self, dealt_obj_: Deck) -> None:
        """Test pop left
        """
        assert dealt_obj_.popleft().id == 'card', 'wrong pop'
        dealt_obj_.current.clear()
        with pytest.raises(IndexError):
            dealt_obj_.pop()

    def test_remove(self, dealt_obj_: Deck) -> None:
        """Test remove
        """
        assert dealt_obj_.current[4].id == 'card', 'wrong order'
        obj_ = dealt_obj_.remove('card')
        assert len(obj_) == 9, 'wrong len'
        assert obj_[4].id == 'card_nice', 'not removed'
        obj_ = dealt_obj_.remove('card_nice')
        assert len(obj_) == 8, 'wrong len'
        assert obj_[4].id == 'card_nice', 'not removed'
        with pytest.raises(ValueError):
            dealt_obj_.remove('not_exist')

    def test_reverse(self, dealt_obj_: Deck) -> None:
        """Test reverse
        """
        source = list(dealt_obj_.current)
        source.reverse()
        assert list(dealt_obj_.reverse()) == source, 'not reversed'

    def test_rotate(self, dealt_obj_: Deck) -> None:
        """Test rotate
        """
        obj_ = dealt_obj_.rotate(1)
        assert len(obj_) == 10, 'not rotated'
        assert obj_[0].id == 'card_nice', 'wrong side of rotation'
        obj_ = dealt_obj_.rotate(-1)
        assert len(obj_) == 10, 'not rotated'
        assert obj_[0].id == 'card', 'wrong side of rotation'

    def test_deck_deal(self, obj_: Deck) -> None:
        """Test obj_ deal() randomizing
        """
        result = obj_.deal()
        assert len(result) == 10, 'wrong current len'
        ids1 = [stuff.id for stuff in result]
        assert 'card' in ids1, 'wrong cards ids inside current'
        assert 'card_nice' in ids1, 'wrong cards ids inside current'
        before = [id(card) for card in result]
        result = obj_.deal()
        after = [id(card) for card in result]
        assert before != after, 'dont created new instances'
        ids2 = [stuff.id for stuff in result]
        assert ids1 == ids2, 'wrong order'

    def test_deck_deal_from_list(self, obj_: Deck) -> None:
        """Test deck deal() from source
        """
        source = ['card', 'card', 'card', 'card_nice']
        result = obj_.deal(source=source)
        assert len(result) == 4, 'wrong current len'
        ids = [stuff.id for stuff in result]
        assert ids == source, 'wrong deal'
        assert 'card' in ids, 'wrong cards ids inside current'
        assert 'card_nice' in ids, 'wrong cards ids inside current'
        before = [id(card) for card in result]
        result = obj_.deal(source=source)
        after = [id(card) for card in result]
        assert before != after, 'dont created new instances'
        assert ids == source, 'wrong order'

    def test_deck_shuffle(self, obj_: Deck) -> None:
        """Test deck shuffle()
        """
        with FixedSeed(42):
            current0 = obj_.deal().copy()
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
            result = obj_.arrange(arranged, last)
            after = [stuff.id for stuff in result]
            assert after != before, 'not arranged'

    def test_arrrange_returns_same_len(self, obj_: Deck) -> None:
        """Test arrange() returns same len
        """
        obj_.card.count = 2
        obj_.card_nice.count = 2
        obj_.deal()
        obj_.shuffle()
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
            obj_.shuffle()
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
            obj_.deal()
            obj_.shuffle()
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
            obj_.deal()
            obj_.shuffle()
            result = obj_.get_random(12)
            assert isinstance(result, list), 'wrong type'
            assert len(result) == 4, 'wrong result'
            assert len(obj_.current) == 0, 'wrong result'

    def test_get_current_names(self, dealt_obj_: Deck) -> None:
        """Test get_curren_names()
        """
        assert len(dealt_obj_.get_current_names()) == 10, \
            'wrong current names len'
        assert dealt_obj_.get_current_names()[0] == 'card', \
            'wrong current names'


class TestSteps:
    """Test Steps class
    """

    @pytest.fixture
    def obj_(self) -> Steps:
        obj_ = Steps('game_turns')
        obj_['step1'] = Step('step1', priority=1)
        obj_.add(Step('astep', priority=2))
        return obj_

    def test_steps_instance(self) -> None:
        """Test Steps class instance
        """
        obj_ = Steps('game_turns')
        assert isinstance(obj_, Component), 'wrong turn type'
        assert isinstance(obj_.current, list), 'wrong current type'
        assert len(obj_.current) == 0, 'wrong current len'
        assert obj_.current_step is None, 'wrong current_step'

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
        assert obj_.current_step.id == 'step1', 'wrong step'
        assert id(step) == id(obj_.current_step), 'wrong steps ids'

    def test_steps_deal(self, obj_: Steps) -> None:
        """Test start new cycle of turn
        """
        result = obj_.deal()
        assert len(result) == 2, 'wrong len'
        assert len(obj_.get_current_names()) == 2, 'wrong current names len'
        assert obj_.get_current_names()[0] == 'step1', 'wrong current names'
        current = obj_.pull()
        assert len(obj_.current) == 1, 'wrong len'
        assert current.id == 'step1', 'wrong current step'
        assert obj_.current_step.id == 'step1', 'wrong current step'
        current = obj_.pull()
        assert len(obj_.current) == 0, 'wrong len'
        assert current.id == 'astep', 'wrong current step'
        assert obj_.current_step.id == 'astep', 'wrong current step'
        with pytest.raises(
            IndexError,
            match='index out of range'
                ):
            obj_.pull()
        result = obj_.deal()
        assert len(result) == 2, 'turn not clean'

    def test_steps_deal_from_list(self, obj_: Steps) -> None:
        """Test steps deal() from source
        """
        source = ['step1', 'astep', 'astep']
        result = obj_.deal(source)

        assert len(result) == 3, 'wrong current len'
        assert len(obj_.get_current_names()) == 3, 'wrong current names len'
        assert obj_.get_current_names()[0] == 'step1', 'wrong current names'
        obj_.pull()
        assert len(result) == 2, 'wrong current len'
        assert obj_.get_current_names()[0] == 'astep', 'wrong current names'
