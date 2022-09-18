import json, pytest
from typing import Tuple, List
from bgameb.game import Game
from bgameb.tools import Shaker, Deck
from bgameb.stuff import Card
from bgameb.constructs import Components, BaseGame
from bgameb.errors import StuffDefineError


class TestShaker:
    """Test Shaker class
    """

    @pytest.fixture
    def game_inst(self) -> BaseGame:
        game = Game(name='game')
        game.add('roller', name='dice')
        game.add('roller', name='dice_nice')
        return game

    def test_shaker_instanciation(self, game_inst: BaseGame) -> None:
        """Test shaker correct created
        """
        assert not Shaker.name, 'Shaker class has name'
        shaker = Shaker(name='shaker', _game=game_inst)
        assert shaker.name == 'shaker', 'wrong name'
        assert isinstance(shaker.last, dict), 'nondict last'
        assert isinstance(shaker.stuff, Components), 'wrong type of stuff'
        assert len(shaker.stuff) == 0, 'nonempty stuff'

    def test_add_stuff_to_shaker_raise_errors_if_wrong_count(
        self, game_inst: BaseGame
            ) -> None:
        """Test need count of stuff no less than 1
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        with pytest.raises(
            StuffDefineError, match="Can't add"
            ):
            shaker.add('dice', count=0)

    def test_add_stuff_to_shaker_raise_errors_if_wrong_name(
        self, game_inst: BaseGame
            ) -> None:
        """Test need exist roller
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        with pytest.raises(
            StuffDefineError, match="'somestuff' not exist in a game"
            ):
            shaker.add('somestuff')

    def test_double_add_stuff_to_shaker_encrease_count(
        self, game_inst: BaseGame
            ) -> None:
        """Test double add roller with same name increase count,
        not raises error
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice')
        shaker.add('dice')
        assert shaker.stuff.dice.count == 2, 'not increased'

    def test_add_stuff_to_shaker(self, game_inst: BaseGame) -> None:
        """Test shaker add()
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice')
        assert shaker.stuff.dice.count == 1, 'wrong count added'
        shaker.add('dice', count=10)
        assert shaker.stuff.dice.count == 11, 'wrong count added'
        shaker.add('dice_nice')
        assert len(shaker.stuff) == 2, 'wrong count of stuff'

    def test_shaker_are_converted_to_json(self, game_inst: BaseGame) -> None:
        """Test to json convertatrion
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice')
        j = json.loads(shaker.to_json())
        assert j['name'] == 'shaker', 'wrong name'
        assert j['last'] == {}, 'wrong last result'
        assert len(j['stuff']) == 1, 'wrong num of stuff'

    def test_remove_all(self, game_inst: BaseGame) -> None:
        """Test remove all stuff from shaker
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice')
        shaker.add('dice_nice')
        assert len(shaker.stuff) == 2, 'wrong number of stuff'
        shaker.remove()
        assert len(shaker.stuff) == 0, 'wrong number of stuff'
        assert isinstance(shaker.stuff, Components), 'wrong type os stuff attr'

    def test_remove_by_name(self, game_inst: BaseGame) -> None:
        """Test remove stuff by name from shaker
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice')
        shaker.add('dice_nice')
        assert len(shaker.stuff) == 2, 'wrong number of stuff'
        shaker.remove(name='dice')
        assert len(shaker.stuff) == 1, 'wrong number of stuff'
        shaker.remove(name='dice_nice')
        assert len(shaker.stuff) == 0, 'wrong number of stuff'

    def test_remove_stuff(self, game_inst: BaseGame) -> None:
        """Test remove stuff
        """
        shaker = Shaker(name='shaker', _game=game_inst)
        shaker.add('dice', count=5)
        shaker.add('dice_nice', count=5)

        assert len(shaker.stuff) == 2, 'wrong number of stuff'
        shaker.remove('dice', count=3)
        assert len(shaker.stuff) == 2, 'wrong number of stuff'
        assert shaker.stuff['dice'].count == 2, 'wrong count of stuff'
        shaker.remove('dice', count=50)
        assert len(shaker.stuff) == 1, 'wrong number of stuff'
        with pytest.raises(
            StuffDefineError, match="Count must be a integer"
        ):
            shaker.remove('dice_nice', count=0)
        print(shaker.stuff)
        with pytest.raises(
            StuffDefineError, match="not exist in tool"
        ):
            shaker.remove('dice', count=1)
        shaker.remove(count=50)
        assert len(shaker.stuff) == 0, 'stuff not removed'

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

    @pytest.fixture
    def cards(self) -> Tuple[Components, List[str]]:
        game = Game(name='game')
        names = ['this', 'that', 'some']
        for name in names:
            game.add_stuff(Card, name=name)
        return game.game_cards, names

    def test_shaker_instanciation(self, cards: Tuple[Components, List[str]]) -> None:
        """Test sdeck correct created
        """
        assert not Deck.name, 'Deck class has name'
        deck = Deck(cards[0])
        assert isinstance(deck.name, str), 'wrong name'
        assert isinstance(deck.deck_cards, dict), 'nondict cards'
        assert isinstance(deck.dealt_cards, tuple), 'nondict dealt cards'
        assert len(deck.deck_cards) == 0, 'nonempty cards'

    def test_add_cards_to_deck_raise_errors_if_wrong_count(
        self, cards: Tuple[Components, List[str]]
            ) -> None:
        """Test need count of cards no less than 1
        """
        deck = Deck(cards[0], name='deck')
        with pytest.raises(
            StuffDefineError, match="Can't add"
            ):
            deck.add('this', count=0)

    def test_add_cards_to_deck_raise_raise_errors_if_wrong_name(
        self, cards: Tuple[Components, List[str]]
            ) -> None:
        """Test need exist card
        """
        deck = Deck(cards[0], name='deck')
        with pytest.raises(
            StuffDefineError, match="'stuff' not exist in a game"
            ):
            deck.add('stuff')

    def test_add_card_to_deck(
        self, cards: Tuple[Components, List[str]]
            ) -> None:
        """Test deck add()
        """
        deck = Deck(cards[0], name='deck')
        names = cards[1]
        deck.add(names[0])
        assert deck.deck_cards == {names[0]: 1}, 'wrong card added'
        deck.add(names[1])
        assert deck.deck_cards == {names[0]: 1, names[1]: 1}, 'wrong card added'
        deck.add(names[1], count=50)
        assert deck.deck_cards == {names[0]: 1, names[1]: 51}, 'wrong card added'
        deck.add(names[2], count=50)
        assert deck.deck_cards == {
            names[0]: 1,
            names[1]: 51,
            names[2]: 50,
            }, 'wrong card added'

    def test_deck_are_converted_to_json(
        self, cards: Tuple[Components, List[str]]
        ) -> None:
        """Test to json convertatrion
        """
        deck = Deck(cards[0], name='deck')
        deck.add(cards[1][0])
        j = json.loads(deck.to_json())
        assert j['name'] == 'deck', 'wrong name'
        assert len(j['deck_cards']) == 1, 'wrong num of cards'

    def test_remove_all_cards(self, cards: Tuple[Components, List[str]]) -> None:
        """Test remove all cards from deck
        """
        deck = Deck(cards[0], name='deck')
        for i in cards[1]:
            deck.add(i)
        assert len(deck.deck_cards) == 3, 'wrong number of cards'
        deck.remove()
        assert len(deck.deck_cards) == 0, 'wrong number of cards'
        assert isinstance(deck.deck_cards, dict), 'wrong type os cards attr'

    def test_remove_cards_by_name(self, cards: Tuple[Components, List[str]]) -> None:
        """Test remove cards by name from shaker
        """
        deck = Deck(cards[0], name='deck')
        deck.add('this')
        for i in cards[1]:
            deck.add(i)
        assert len(deck.deck_cards) == 3, 'wrong number of cards'
        assert deck.deck_cards['this'] == 2, 'wrong number of cards'
        deck.remove(name='this')
        assert len(deck.deck_cards) == 2, 'wrong number of cards'
        assert 'this' not in deck.deck_cards.keys(), 'cards not removed'
        deck.remove(name='that')
        assert len(deck.deck_cards) == 1, 'wrong number of cards'

    def test_remove_cards(self, cards: Tuple[Components, List[str]]) -> None:
        """Test remove cards
        """
        deck = Deck(cards[0], name='deck')
        for i in cards[1]:
            deck.add(i, count=5)
        assert len(deck.deck_cards) == 3, 'wrong number of cards'
        deck.remove(cards[1][0], count=3)
        assert len(deck.deck_cards) == 3, 'wrong number of cards'
        assert deck.deck_cards[cards[1][0]] == 2, \
            'wrong count of cards'
        deck.remove(cards[1][0], count=50)
        assert len(deck.deck_cards) == 2, 'wrong number of cards'
        with pytest.raises(
            StuffDefineError, match="Count must be a positive"
        ):
            deck.remove(cards[1][0], count=0)
        with pytest.raises(
            StuffDefineError, match="not exist in dec"
        ):
            deck.remove('hocho', count=1)
        deck.remove(count=3)
        assert len(deck.deck_cards) == 2, 'wrong count of cards'
        assert deck.deck_cards[cards[1][1]] == 2, \
            'wrong count of cards'
        deck.remove(count=50)
        assert deck.deck_cards == {}, 'cards not removed'
