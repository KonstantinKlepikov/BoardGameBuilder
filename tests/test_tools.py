import json, pytest
from typing import Tuple, List
from bgameb.game import Game
from bgameb.tools import Shaker, Deck
from bgameb.stuff import Dice, Coin, Card
from bgameb.constructs import Components
from bgameb.errors import StuffDefineError


class TestShaker:
    """Test Shaker class
    """

    @pytest.fixture(params=[
        (Dice, 'dice'),
        (Coin, 'coin'),
        ])
    def rollers(self, request) -> Tuple[Components, str]:
        game = Game(name='game')
        game.add_stuff(request.param[0], name=request.param[1])
        return game.game_rollers, request.param[1]

    def test_shaker_instanciation(self, rollers: Tuple[Components, str]) -> None:
        """Test shaker correct created
        """
        assert not Shaker.name, 'Shaker class has name'
        shaker = Shaker(rollers[0])
        assert isinstance(shaker.name, str), 'wrong name'
        assert isinstance(shaker.last, dict), 'nondict last'
        assert isinstance(shaker.rollers, dict), 'nondict rollers'
        assert len(shaker.rollers) == 0, 'nonempty rollers'

    def test_add_rollers_to_shaker_raise_errors_if_wrong_count(
        self, rollers: Tuple[Components, str]
            ) -> None:
        """Test need count of rollers no less than 1
        """
        shaker = Shaker(rollers[0], name='shaker')
        with pytest.raises(
            StuffDefineError, match="Can't add"
            ):
            shaker.add(rollers[1], count=0)

    def test_add_rollers_to_shaker_raise_errors_if_wrong_name(
        self, rollers: Tuple[Components, str]
            ) -> None:
        """Test need exist roller
        """
        shaker = Shaker(rollers[0], name='shaker')
        with pytest.raises(
            StuffDefineError, match="'somestuff' not exist in a game"
            ):
            shaker.add('somestuff')

    def test_add_rollers_to_shaker(self, rollers: Tuple[Components, str]) -> None:
        """Test shaker add()
        """
        shaker = Shaker(rollers[0], name='shaker')
        shaker.add(rollers[1])
        assert shaker.rollers == {'colorless': {rollers[1]: 1}}, 'wrong roller added'
        shaker.add(rollers[1], color="white")
        assert shaker.rollers == {
            'colorless': {rollers[1]: 1},
            'white': {rollers[1]: 1},
            }, 'wrong roller added'
        shaker.add(rollers[1], count=50)
        assert shaker.rollers == {
            'colorless': {rollers[1]: 51},
            'white': {rollers[1]: 1},
            }, 'wrong roller added'
        shaker.add(rollers[1], color='red', count=50)
        assert shaker.rollers == {
            'colorless': {rollers[1]: 51},
            'white': {rollers[1]: 1},
            'red': {rollers[1]: 50},
            }, 'wrong roller added'

    def test_shaker_are_converted_to_json(self, rollers: Tuple[Components, str]) -> None:
        """Test to json convertatrion
        """
        shaker = Shaker(rollers[0], name='shaker')
        shaker.add(rollers[1])
        j = json.loads(shaker.to_json())
        assert j['name'] == 'shaker', 'wrong name'
        assert j['last'] == {}, 'wrong last result'
        assert len(j['rollers']['colorless']) == 1, 'wrong num of rollers'

    def test_remove_all(self, rollers: Tuple[Components, str]) -> None:
        """Test remove all rollers from shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove()
        assert len(shaker.rollers) == 0, 'wrong number of rollers'
        assert isinstance(shaker.rollers, dict), 'wrong type os rollers attr'

    def test_remove_by_colors(self, rollers: Tuple[Components, str]) -> None:
        """Test remove rollers by color from shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove(color='white')
        assert len(shaker.rollers) == 2, 'wrong number of rollers'

    def test_remove_by_name(self, rollers: Tuple[Components, str]) -> None:
        """Test remove rollers by name from shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        rollers[0].__dict__.update({'this': Dice(name='this')})
        shaker.add('this', color='white')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        assert len(shaker.rollers['white']) == 2, 'wrong number of rollers'
        shaker.remove(name='this')
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        assert len(shaker.rollers['white']) == 1, 'wrong number of rollers'
        shaker.remove(name=rollers[1])
        assert len(shaker.rollers) == 0, 'wrong number of rollers'

    def test_remove_rollers(self, rollers: Tuple[Components, str]) -> None:
        """Test remove rollers
        """
        shaker = Shaker(rollers[0], name='shaker')
        rollers[0].__dict__.update({'this': Dice(name='this')})
        shaker.add('this', color='white')
        for i in ['white', 'red', 'green']:
            shaker.add(rollers[1], color=i, count=5)

        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        shaker.remove(rollers[1], color="red", count=3)
        assert len(shaker.rollers) == 3, 'wrong number of rollers'
        assert shaker.rollers['red'][rollers[1]] == 2, \
            'wrong count of rollers'
        shaker.remove(rollers[1], color="red", count=50)
        assert len(shaker.rollers) == 2, 'wrong number of rollers'
        with pytest.raises(
            StuffDefineError, match="Count must be a positive"
        ):
            shaker.remove(rollers[1], color="white", count=0)
        with pytest.raises(
            StuffDefineError, match="not exist in shaker"
        ):
            shaker.remove(rollers[1], color="black", count=1)
        shaker.remove(count=50)
        assert shaker.rollers == {}, 'rollers not removed'

    def test_roll_shaker(self, rollers: Tuple[Components, str]) -> None:
        """Test roll shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
        for i in ['white', 'red', 'white']:
            shaker.add(rollers[1], color=i)
        roll = shaker.roll()
        assert len(roll['red'][rollers[1]]) == 1, 'wrong roll result'
        assert len(roll['white'][rollers[1]]) == 2, 'wrong roll result'
        assert isinstance(roll['white'][rollers[1]][0], int), 'wrong roll result'
        assert len(shaker.last) == 2, 'wrong last'

    def test_roll_empty_shaker(self, rollers: Tuple[Components, str]) -> None:
        """Test roll empty shaker
        """
        shaker = Shaker(rollers[0], name='shaker')
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
