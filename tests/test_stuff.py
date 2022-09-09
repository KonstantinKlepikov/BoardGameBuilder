import json, pytest
from bgameb.stuff import (
    Dice, Coin, BaseRoller, Card, CardTexts
)
from bgameb.errors import RollerSidesError


class TestNameAndJson:
    """Test creation with names and json schemes
    """
    params = [
        (BaseRoller, BaseRoller.name),
        (Dice, Dice.name),
        (Coin, Coin.name),
    ]

    @pytest.mark.parametrize("_class, name", params)
    def test_rolled_classes_created_with_name(self, _class, name: str) -> None:
        """Test rolled classes name instancing
        """
        rolled = _class()
        assert rolled.name == name, 'wrong default name'
        rolled = _class(name='This Rolled')
        assert rolled.name == 'This Rolled', 'not set name for instance'

    @pytest.mark.parametrize("_class, name", params)
    def test_rolled_classes_are_converted_to_json(self, _class, name: str) -> None:
        """Test to json convertatrion
        """
        rolled = _class()
        j = json.loads(rolled.to_json())
        assert j['name'] == name, 'not converted to json'


class TestBaseRoller:
    """Test BaseRoller class
    """

    def test_rolled_have_sides_defined_as_none(self) -> None:
        """Rolled class initialised with None sides
        """
        rolled = BaseRoller()
        assert rolled.sides == None, 'wrong init of sides'

    def test_roll_rolled_raise_error(self) -> None:
        """We cant use roll() method from base class
        """
        rolled = BaseRoller()
        with pytest.raises(
            RollerSidesError,
            match='Is not defined number of sizes'
            ):
            rolled.roll()
        assert rolled._range == [], 'range to roll isnt empty'


class TestDice:
    """Test Dice
    """

    def test_dice_init_sides(self) -> None:
        """Test sides attribute initialisation for dice
        """
        dice = Dice()
        assert dice.sides == 6, 'wrong number of sides after empty init'
        dice = Dice(sides=2)
        assert dice.sides == 2, 'wrong number of sidesafter init'
        dice = Dice()
        dice.sides = 2
        assert dice.sides == 2, 'cant change number of sides'

    def test_roll_dice_without_sides_raise_error(self) -> None:
        """We cant roll dice if sides not defined
        """
        dice = Dice()
        dice.sides = None
        with pytest.raises(
            RollerSidesError,
            match='Is not defined number of sizes'
            ):
            dice.roll()

    def test_dice_has_correct_range(self) -> None:
        """Range to roll dice is correct
        """
        dice = Dice()
        assert dice._range == [1, 2, 3, 4, 5, 6], \
            'wrong range to roll'

    def test_dice_return_roll_result(self) -> None:
        """Test dice roll return result
        """
        dice = Dice()
        roll = dice.roll()
        assert isinstance(roll, int), 'dice roll returns not int'


class TestCoin:
    """Test Coin
    """

    def test_coin_hase_sides_defined_as_two(self) -> None:
        """Coin class initialised with 2 sides
        """
        coin = Coin()
        assert coin.sides == 2, 'wrong init of sides'

    def test_coin_has_correct_range(self) -> None:
        """Range to roll coin is correct
        """
        coin = Coin()
        assert coin._range == [1, 2], \
            'wrong range to roll'

    def test_coin_return_roll_result(self) -> None:
        """Test coin roll return result
        """
        coin = Coin()
        roll = coin.roll()
        assert isinstance(roll, int), 'coin roll returns not int'


class TestCardText:
    """Test CardText class
    """

    def test_card_text_operations(self) -> None:
        """Test get, set and delete operations of
        CardText
        """
        text = CardTexts()
        text.this = 'this'
        assert text.this == 'this', 'not set or cant get'
        assert text.__repr__() == "CardTexts(this='this')", 'wrong repr'
        text.this = 'that'
        assert text.this == 'that', 'not set or cant update'
        del text.this
        with pytest.raises(
            AttributeError, match='this'
            ):
            text.this
        with pytest.raises(
            KeyError, match='this'
            ):
            del text.this

    def test_card_text_equal(self) -> None:
        """Test equal of CardTexts
        """
        text1 = CardTexts()
        text2 = CardTexts()
        assert text1 == text2, 'not equal'
        text2.this = 'this'
        assert text1 != text2, 'equal'


class TestCard:
    """Test Card class"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        card = Card()
        assert card.name == 'card', 'wrong name'
        assert card.open == False, 'card is open'
        assert card.tapped == False, 'card is tapped'
        assert card.side == None, 'defined wrong side'
        assert isinstance(card.text, CardTexts), 'texts not seted'

    def test_card_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        card = Card()
        j = json.loads(card.to_json())
        assert j['name'] == 'card', 'not converted to json'

    def test_card_texts(self) -> None:
        """Test card text can be set, get, delete
        """
        card = Card()
        card.text.this = 'this'
        assert card.text.this == 'this', 'not set or cant get'
        del card.text.this
        with pytest.raises(
            AttributeError, match='this'
            ):
            card.text.this

    def test_flip(self) -> None:
        """Test flip card
        """
        card = Card()
        card.flip()
        assert card.open, 'card not oppened'
        card.flip()
        assert not card.open, 'card oppened'

    def test_fase_up(self) -> None:
        """Test face up open card and return text
        """
        card = Card()
        texts = card.face_up()
        assert card.open, 'card not open'
        assert isinstance(texts, CardTexts), 'wrong text'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        card = Card()
        card.open = True
        card.face_down()
        assert not card.open, 'card not open'

    def test_tap_tap_card_and_set_side(self) -> None:
        """Test tap card tap and set side
        """
        card = Card()
        card.tap(side='left')
        assert card.tapped, 'card not tapped'
        assert card.side == 'left', 'wrong side'

    def test_untap_card(self) -> None:
        """Test tap card tap and set side
        """
        card = Card()
        card.tapped = True
        assert card.tapped, 'card not tapped'
        card.untap()
        assert not card.tapped, 'card not untapped'