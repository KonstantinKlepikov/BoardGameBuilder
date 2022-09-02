import json, pytest
import bgameb
from bgameb.rolled import RollOrFlip
from bgameb.utils import RolledWithoutSidesError


class TestNameAndJson:
    """Test creation with names and json schemes
    """
    params = [
        (RollOrFlip, 'default'),
        (bgameb.Dice, 'dice'),
        (bgameb.Coin, 'coin'),
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


class TestRollOrFlip:
    """Test RollOrFlip class
    """

    # def test_rolled_append_available_colors(self) -> None:
    #     """Test we can set colors to rolled object
    #     """
    #     with pytest.raises(TypeError, match="unexpected keyword argument"):
    #         dice = Dice(colors = set(['green', 'red']))
    #     dice = Dice()
    #     assert dice.colors == set(), 'wrong empty init of colors'
    #     dice.colors.update(['green', 'red'])
    #     assert dice.colors == set(['green', 'red']), 'colors not set'
    #     dice.colors.update(['green', 'yellow'])
    #     assert dice.colors == set(['green', 'red', 'yellow']), 'colors not unique'
    #     dice.colors.add('white')
    #     assert 'white' in dice.colors, 'single color not appended'


    def test_rolled_hase_sides_defined_as_none(self) -> None:
        """Dise class initialised with None sides
        """
        rolled = RollOrFlip()
        assert rolled.sides == None, 'wrong init of sides'


    def test_roll_rolled_raise_error(self) -> None:
        """We cant roll dice from base class
        """
        rolled = RollOrFlip()
        with pytest.raises(
            RolledWithoutSidesError,
            match='Is not defined number of sizes'
            ):
            rolled.roll()
        assert rolled._range_to_roll == [], 'range to roll isnt empty'


class TestDice:
    """Test Dice
    """

    def test_dice_init_sides(self) -> None:
        """Test sides attribute initialisation for dice
        """
        dice = bgameb.Dice()
        assert dice.sides == 6, 'wrong number of sides after empty init'
        dice = bgameb.Dice(sides=2)
        assert dice.sides == 2, 'wrong number of sidesafter init'
        dice = bgameb.Dice()
        dice.sides = 2
        assert dice.sides == 2, 'cant change number of sides'


    def test_roll_dice_without_sides_raise_error(self) -> None:
        """We cant roll dice if sides not defined
        """
        dice = bgameb.Dice()
        dice.sides = None
        with pytest.raises(
            RolledWithoutSidesError,
            match='Is not defined number of sizes'
            ):
            dice.roll()


    def test_dice_has_correct_range_to_roll(self) -> None:
        """Range to roll dice is correct
        """
        dice = bgameb.Dice()
        assert dice._range_to_roll == [1, 2, 3, 4, 5, 6], \
            'wrong range to roll'


    def test_dice_return_roll_result(self) -> None:
        """Test dice roll return result
        """
        dice = bgameb.Dice()
        roll = dice.roll()
        assert isinstance(roll, int), 'dice roll returns not int'


class TestCoin:
    """Test Coin
    """

    def test_coin_hase_sides_defined_as_two(self) -> None:
        """Coin class initialised with 2 sides
        """
        coin = bgameb.Coin()
        assert coin.sides == 2, 'wrong init of sides'


    def test_coin_has_correct_range_to_roll(self) -> None:
        """Range to roll coin is correct
        """
        coin = bgameb.Coin()
        assert coin._range_to_roll == [1, 2], \
            'wrong range to roll'


    def test_coin_return_roll_result(self) -> None:
        """Test coin roll return result
        """
        coin = bgameb.Coin()
        roll = coin.roll()
        assert isinstance(roll, int), 'coin roll returns not int'
