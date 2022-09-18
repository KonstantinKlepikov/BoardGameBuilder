import json, pytest
from bgameb.stuff import RollerType, Roller, CardType, Card
from bgameb.errors import StuffDefineError


class TestNameAndJson:
    """Test creation with names and json schemes
    """
    params = [
        (Roller, 'roller'),
        (Card, 'card'),
        (RollerType, 'roller_type'),
        (CardType, 'card_type'),
    ]

    @pytest.mark.parametrize("_class, name", params)
    def test_rolled_classes_created_with_name(self, _class, name: str) -> None:
        """Test rolled classes name instancing
        """
        assert not _class.name, 'class has name'
        rolled = _class()
        assert isinstance(rolled.name, str), 'wrong default name'
        rolled = _class(name='This Rolled')
        assert rolled.name == 'This Rolled', 'not set name for instance'

    @pytest.mark.parametrize("_class, name", params)
    def test_rolled_classes_are_converted_to_json(self, _class, name: str) -> None:
        """Test to json convertatrion
        """
        rolled = _class(name=name)
        j = json.loads(rolled.to_json())
        assert j['name'] == name, 'not converted to json'
        with pytest.raises(
            KeyError,
            match='_range'
            ):
            j['_range']


class TestRollers:
    """Test RollerType class
    """

    def test_roller_type_have_sides_defined_less_than_two(self) -> None:
        """Test RollerType class initialised with less than 2 sides
        """
        with pytest.raises(
            StuffDefineError,
            match='Needed >= 2'
            ):
            RollerType(name='base', sides=1)

    def test_roller_correctly_filled_from_roller_type(self) -> None:
        """_summary_
        """
        dice_type = RollerType(name='dice', sides=6)
        dice = Roller(**dice_type.to_dict())
        assert isinstance(dice, Roller), 'wrong type'
        assert dice.name == 'dice', 'wrong name'
        assert dice.sides == 6, 'wrong sides'
        assert dice.count == 0, 'wrong count'
        assert len(dice._range) == 6, 'wrong _range'

    def test_roller_roll(self) -> None:
        """Test roller roll return result
        """
        dice = Roller(name='dice', count=5)
        roll = dice.roll()
        assert isinstance(roll, list), 'roll returns not list'
        assert len(roll) == 5, 'wrong count of rolls'
        assert isinstance(roll[0], int), 'ot an int in a list'
        dice = Roller(name='dice')
        roll = dice.roll()
        assert len(roll) == 0, 'is roled, but count is 0'


# class TestCard:
#     """Test Card class"""

#     def test_card_instanciation(self) -> None:
#         """Test card correct created
#         """
#         card = Card(name='card')
#         assert card.name == 'card', 'wrong name'
#         assert card.open == False, 'card is open'
#         assert card.tapped == False, 'card is tapped'
#         assert card.side == None, 'defined wrong side'
#         assert isinstance(card.text, CardTexts), 'texts not seted'

#     def test_card_class_is_converted_to_json(self) -> None:
#         """Test to json convertatrion
#         """
#         card = Card(name='card')
#         j = json.loads(card.to_json())
#         assert j['name'] == 'card', 'not converted to json'

#     def test_card_texts(self) -> None:
#         """Test card text can be set, get, delete
#         """
#         card = Card(name='card')
#         card.text.this = 'this'
#         assert card.text.this == 'this', 'not set or cant get'
#         del card.text.this
#         with pytest.raises(
#             AttributeError, match='this'
#             ):
#             card.text.this

#     def test_flip(self) -> None:
#         """Test flip card
#         """
#         card = Card(name='card')
#         card.flip()
#         assert card.open, 'card not oppened'
#         card.flip()
#         assert not card.open, 'card oppened'

#     def test_fase_up(self) -> None:
#         """Test face up open card and return text
#         """
#         card = Card(name='card')
#         texts = card.face_up()
#         assert card.open, 'card not open'
#         assert isinstance(texts, CardTexts), 'wrong text'

#     def test_fase_down(self) -> None:
#         """Test face up hide card
#         """
#         card = Card(name='card')
#         card.open = True
#         card.face_down()
#         assert not card.open, 'card not open'

#     def test_tap_tap_card_and_set_side(self) -> None:
#         """Test tap card tap and set side
#         """
#         card = Card(name='card')
#         card.tap(side='left')
#         assert card.tapped, 'card not tapped'
#         assert card.side == 'left', 'wrong side'

#     def test_untap_card(self) -> None:
#         """Test tap card tap and set side
#         """
#         card = Card(name='card')
#         card.tapped = True
#         assert card.tapped, 'card not tapped'
#         card.untap()
#         assert not card.tapped, 'card not untapped'


class TestCard:
    """Test Card classes"""

    def test_card_instanciation(self) -> None:
        """Test card correct created
        """
        card = CardType(name='card')
        assert card.name == 'card', 'wrong name'
        assert card.open == False, 'card is open'
        assert card.tapped == False, 'card is tapped'
        assert card.side == None, 'defined wrong side'

    def test_flip(self) -> None:
        """Test flip card
        """
        card = Card(name='card')
        card.flip()
        assert card.open, 'card not oppened'
        card.flip()
        assert not card.open, 'card oppened'

    def test_fase_up(self) -> None:
        """Test face up open card
        """
        card = Card(name='card')
        card.face_up()
        assert card.open, 'card not open'

    def test_fase_down(self) -> None:
        """Test face up hide card
        """
        card = Card(name='card')
        card.open = True
        card.face_down()
        assert not card.open, 'card not open'

    def test_tap_tap_card_and_set_side(self) -> None:
        """Test tap card tap and set side
        """
        card = Card(name='card')
        card.tap(side='left')
        assert card.tapped, 'card not tapped'
        assert card.side == 'left', 'wrong side'

    def test_untap_card(self) -> None:
        """Test tap card tap and set side
        """
        card = Card(name='card')
        card.tapped = True
        assert card.tapped, 'card not tapped'
        card.untap()
        assert not card.tapped, 'card not untapped'
