import pytest
from collections import deque
from bgameb.base import Component
from bgameb.items import Dice, Card, Step
from bgameb.tools import Shaker, Deck, Steps
from bgameb.errors import ArrangeIndexError
from tests.conftest import FixedSeed


class TestShaker:
    """Test Shaker class
    """

    @pytest.fixture
    def obj_(self) -> Shaker:
        obj_ = Shaker(id='shaker')
        obj_.c = Component(
            dice=Dice(id='dice', count=5),
            dice_nice=Dice(id='dice_nice', count=5)
                )
        return obj_

    @pytest.fixture
    def dealt_obj_(self, obj_: Shaker) -> Shaker:
        obj_.deal()
        return obj_

    def test_shaker_instanciation(self, obj_: Shaker) -> None:
        """Test deck correct created
        """
        assert isinstance(obj_.current, list), 'wrong type of current'
        assert len(obj_.current) == 0, 'nonempty current'
        assert isinstance(obj_.last_roll, dict), 'wrong last'
        assert isinstance(obj_.last_roll_mapped, dict), 'wrong last mapped'

    def test_add_new_item_to_shaker(self, obj_: Shaker) -> None:
        """Test add new item to bag
        """
        obj_.add(Dice(id='omg'))
        assert obj_.c.omg.id == 'omg', 'stuff not added'

    def test_roll_shaker(self, dealt_obj_: Shaker) -> None:
        """Test roll shaker
        """
        roll = dealt_obj_.roll()
        assert len(roll) == 2, 'wrong roll result'
        assert len(roll['dice']) == 5, 'wrong roll result'
        assert len(dealt_obj_.last_roll) == 2, 'wrong last'

    def test_roll_mapped_shaker(self, obj_: Shaker) -> None:
        """Test roll mapped shaker
        """
        obj_.c.dice.mapping = {n: str(n) for n in obj_.c.dice._range}
        obj_.deal()
        roll = obj_.roll_mapped()
        assert len(roll) == 2, 'wrong roll result'
        assert len(roll['dice']) == 5, 'wrong roll result'
        assert len(roll['dice_nice']) == 0, 'wrong roll result'
        assert len(obj_.last_roll_mapped) == 2, 'wrong last_mapped'

    def test_roll_empty_shaker(self) -> None:
        """Test roll empty shaker
        """
        obj_ = Shaker(id='shaker')
        roll = obj_.roll()
        assert roll == {}, 'wrong roll result'
        roll = obj_.roll_mapped()
        assert roll == {}, 'wrong roll result'


class TestDeck:
    """Test Deck class
    """

    @pytest.fixture
    def obj_(self) -> Deck:
        obj_ = Deck(id='deck')
        obj_.c = Component(
            card=Card(id='card', count=5),
            card_nice=Card(id='Card_nice', count=5)
                )
        return obj_

    @pytest.fixture
    def dealt_obj_(self, obj_: Deck) -> Deck:
        obj_.deal()
        return obj_

    def test_deck_instanciation(self, obj_: Deck) -> None:
        """Test deck correct created
        """
        assert isinstance(obj_.current, deque), 'wrong type of current'
        assert len(obj_.current) == 0, 'nonempty current'
        assert obj_.last is None, 'nonempty last'

    def test_add_new_item_to_deck(self, obj_: Deck) -> None:
        """Test add new item to bag
        """
        obj_.add(Card(id='omg'))
        assert obj_.c.omg.id == 'omg', 'stuff not added'

    def test_item_replace(self, obj_: Deck) -> None:
        """Test _item_replace()
        """
        c = Card(id='wow', count=15)
        card = obj_._item_replace(c)
        assert card.id == 'wow', 'wrong id'
        assert card.count == 1, 'wrong count'
        assert id(card) != id(c), 'not replaced'

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

    def test_deck_clear_last(self, dealt_obj_: Deck) -> None:
        """Test clear() clear last
        """
        dealt_obj_.pop()
        assert dealt_obj_.last, 'empty last'
        dealt_obj_.clear()
        assert dealt_obj_.last is None, 'nonempty last'

    def test_appendleft(self, dealt_obj_: Deck) -> None:
        """Test current append left
        """
        card = Card(id='unique')
        dealt_obj_.appendleft(card)
        assert len(dealt_obj_.current) == 11, 'wrong current len'
        assert dealt_obj_.current[0].id == 'unique', 'wrong append'
        assert id(card) != id(dealt_obj_.current[10]), 'not replaced'

    def test_extendleft(self, dealt_obj_: Deck) -> None:
        """Test extendleft currend by cards
        """
        cards = [Card(id='unique'), Card(id='another')]
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
        order = dealt_obj_.current_ids
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
        order = dealt_obj_.current_ids
        order.reverse()
        dealt_obj_.reorder(order)
        assert dealt_obj_.current_ids == order, 'wrong order'

        with FixedSeed(42):
            dealt_obj_.shuffle()
            old_oder = dealt_obj_.current_ids.copy()
            order = dealt_obj_.current_ids[5:]
            order.reverse()
            dealt_obj_.reorder(order)
            assert dealt_obj_.current_ids[5:] == order, 'wrong order'
            assert dealt_obj_.current_ids[0:5] == old_oder[0:5], \
                'wrong order'

    def test_deck_reorderleft(self, dealt_obj_: Deck) -> None:
        """Test deck reorderleft()
        """
        order = dealt_obj_.current_ids
        order.reverse()
        dealt_obj_.reorderleft(order)
        assert dealt_obj_.current_ids == order, 'wrong order'

        with FixedSeed(42):
            dealt_obj_.shuffle()
            old_oder = dealt_obj_.current_ids.copy()
            order = dealt_obj_.current_ids[0:5]
            order.reverse()
            dealt_obj_.reorderleft(order)
            assert dealt_obj_.current_ids[0:5] == order, 'wrong order'
            assert dealt_obj_.current_ids[5:0] == old_oder[5:0], \
                'wrong order'

    def test_deck_reorderfrom(self, dealt_obj_: Deck) -> None:
        """Test deck reorderfrom()
        """
        with FixedSeed(42):
            dealt_obj_.shuffle()
            old_oder = dealt_obj_.current_ids.copy()
            order = dealt_obj_.current_ids[2:6]
            order.reverse()
            dealt_obj_.reorderfrom(order, 2)
            assert dealt_obj_.current_ids[2:6] == order, 'wrong order'
            assert dealt_obj_.current_ids[0:2] == old_oder[0:2], \
                'wrong order'
            assert dealt_obj_.current_ids[6:] == old_oder[6:], 'wrong order'

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
        assert isinstance(search[0], Card), 'wrong search type'
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
        obj_ = Steps(id='game_turns')
        obj_.c = Component(
            step1=Step(id='step1', priority=1),
            astep=Step(id='asteP', priority=2)
                )
        return obj_

    def test_steps_instance(self) -> None:
        """Test Steps class instance
        """
        obj_ = Steps(id='game_turns')
        assert isinstance(obj_.current, list), 'wrong current type'
        assert len(obj_.current) == 0, 'wrong current len'
        assert obj_.last is None, 'wrong last'

    def test_steps_clear_last(self, obj_: Steps) -> None:
        """Test clear() clear last
        """
        obj_.deal()
        obj_.pop()
        assert obj_.last, 'empty last'
        obj_.clear()
        assert obj_.last is None, 'nonempty last'

    def test_steps_add_step(self, obj_: Steps) -> None:
        """Test add step to steps
        """
        obj_.add(Step(id='omg', priority=42))
        assert obj_.c.omg.id == 'omg', 'stuff not added'

    def test_by_id(self, obj_: Steps) -> None:
        """Test by_id()
        """
        obj_.deal()
        assert isinstance(obj_.by_id('step1'), list), 'wrong type'
        assert len(obj_.by_id('step1')) == 1, 'wrong len'
        assert obj_.by_id('step1')[0].id == 'step1', 'wrong search'
        assert obj_.by_id('why') == [], 'wrong search'
        obj_.clear()
        assert obj_.by_id('step1') == [], 'wrong search'

    def test_push(self, obj_: Steps) -> None:
        """Test push to steps
        """
        s = Step(id='omg', priority=42)
        obj_.push(s)
        assert len(obj_.current) == 1, 'not pushed'
        assert obj_.current[0].id == 'omg', 'wrong id'
        assert id(obj_.current[0].id) != id(s), 'not replaced'

    def test_pops(self, obj_: Steps) -> None:
        """Test pull step from steps
        """
        s = Step(id='omg', priority=42)
        obj_.push(s)
        step = obj_.pops()
        assert step.id == 'omg', 'wrong step'
        assert obj_.last.id == 'omg', 'wrong step'
        assert id(step) == id(obj_.last), 'wrong steps ids'

    def test_steps_deal(self, obj_: Steps) -> None:
        """Test start new cycle of turn
        """
        result = obj_.deal().current
        assert len(result) == 2, 'wrong len'
        assert len(obj_.current_ids) == 2, 'wrong current names len'
        assert obj_.current_ids[0] == 'step1', 'wrong current names'
        current = obj_.pops()
        assert len(obj_.current) == 1, 'wrong len'
        assert current.id == 'step1', 'wrong current step'
        assert obj_.last.id == 'step1', 'wrong current step'
        current = obj_.pops()
        assert len(obj_.current) == 0, 'wrong len'
        assert current.id == 'asteP', 'wrong current step'
        assert obj_.last.id == 'asteP', 'wrong current step'
        with pytest.raises(
            IndexError,
            match='index out of range'
                ):
            obj_.pops()
        result = obj_.deal().current
        assert len(result) == 2, 'turn not clean'

    def test_steps_deal_from_list(self, obj_: Steps) -> None:
        """Test steps deal() from items
        """
        items = ['step1', 'asteP', 'asteP']
        result = obj_.deal(items).current
        assert len(result) == 3, 'wrong current len'
        assert len(obj_.current_ids) == 3, 'wrong current names len'
        assert obj_.current_ids[0] == 'step1', 'wrong current names'
        obj_.pops()
        assert len(result) == 2, 'wrong current len'
        assert obj_.current_ids[0] == 'asteP', 'wrong current names'
