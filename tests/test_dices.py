import json
import pytest
import bgameb
from bgameb.dices import Dice
from bgameb.utils import DiceWithoutSidesError


class TestDice:
    """Test Dice class
    """

    def test_dice_class_created_with_name(self) -> None:
        """Test dice name instancing
        """
        dice = Dice()
        assert dice.name == 'default_dice', 'wrong default name'
        dice = Dice(name='This Dice')
        assert dice.name == 'This Dice', 'not set name for instance'


    def test_dice_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        dice = Dice()
        j = json.loads(dice.to_json())
        assert j['name'] == 'default_dice', 'not converted to json'


    def test_dices_append_available_colors(self) -> None:
        """Test we can set colors to dice object
        """
        with pytest.raises(TypeError, match="unexpected keyword argument"):
            dice = Dice(colors = set(['green', 'red']))
        dice = Dice()
        assert dice.colors == set(), 'wrong empty init of colors'
        dice.colors.update(['green', 'red'])
        assert dice.colors == set(['green', 'red']), 'colors not set'
        dice.colors.update(['green', 'yellow'])
        assert dice.colors == set(['green', 'red', 'yellow']), 'colors not unique'
        dice.colors.add('white')
        assert 'white' in dice.colors, 'single color not appended'


    def test_dice_hase_sides_defined_as_none(self) -> None:
        """Dise class initialised with None sides
        """
        dice = Dice()
        assert dice.sides == None, 'wrong init of sides'


    def test_roll_dice_raise_error(self) -> None:
        """We cant roll dice from base class
        """
        dice = Dice()
        with pytest.raises(
            DiceWithoutSidesError,
            match='Is not defined number of sizes for default_dice'
            ):
            dice.roll()
        assert dice._range_to_roll == [], 'range to roll isnt empty'


class TestTrueDice:
    """Test dices with sides
    """

    def test_true_dice_created_with_name(self) -> None:
        """Test TrueDice name instancing
        """
        dice = bgameb.TrueDice()
        assert dice.name == 'default_dice', 'wrong default name'
        dice = bgameb.TrueDice(name='This Dice')
        assert dice.name == 'This Dice', 'not set name for instance'

    def test_true_dice_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        dice = bgameb.TrueDice()
        j = json.loads(dice.to_json())
        assert j['name'] == 'default_dice', 'not converted to json'


    def test_true_dice_init_sides(self) -> None:
        """Test sides attribute initialisation for true dice
        """
        dice = bgameb.TrueDice()
        assert dice.sides == 6, 'wrong number of sides after empty init'
        dice = bgameb.TrueDice(sides=2)
        assert dice.sides == 2, 'wrong number of sidesafter init'
        dice = bgameb.TrueDice()
        dice.sides = 2
        assert dice.sides == 2, 'cant change number of sides'


    def test_roll_true_dice_raise_error(self) -> None:
        """We cant roll dice if sides not defined
        """
        dice = bgameb.TrueDice()
        dice.sides = None
        with pytest.raises(
            DiceWithoutSidesError,
            match='Is not defined number of sizes for default_dice'
            ):
            dice.roll()


    def test_true_dice_has_correct_range_to_roll(self) -> None:
        """Range to roll dice is correct
        """
        dice = bgameb.TrueDice()
        assert dice._range_to_roll == [1, 2, 3, 4, 5, 6], \
            'wrong range to roll'


    def test_true_dice_return_roll_result(self) -> None:
        """Test true dice roll return result
        """
        dice = bgameb.TrueDice()
        roll = dice.roll()
        assert isinstance(roll, int), 'dice roll returns not int'
