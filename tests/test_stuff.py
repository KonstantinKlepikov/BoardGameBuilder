import json, pytest
from bgameb.stuff import (
    RollerType, Roller, CardType, Card
    )
from bgameb.errors import StuffDefineError


class TestBaseStuff:
    """Test creation with names and json schemes
    """
    params = [
        (Roller, 'roller'),
        (Card, 'card'),
        (RollerType, 'roller_type'),
        (CardType, 'card_type'),
    ]

    @pytest.mark.parametrize("_class, name", params)
    def test_stuff_classes_created_with_name(self, _class, name: str) -> None:
        """Test stuff classes instancing
        """
        assert not _class.name, 'class has name'
        stuff = _class()
        assert isinstance(stuff.name, str), 'wrong default name'
        stuff = _class(name='This Rolled')
        assert stuff.name == 'This Rolled', 'not set name for instance'

    @pytest.mark.parametrize("_class, name", params)
    def test_stuff_classes_are_converted_to_json(self, _class, name: str) -> None:
        """Test to json convertatrion
        """
        stuff = _class(name=name)
        j = json.loads(stuff.to_json())
        assert j['name'] == name, 'not converted to json'


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
