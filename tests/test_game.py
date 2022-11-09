import json
import pytest
from bgameb.game import Game
from bgameb.base import Components, Base
from bgameb.types import COMPONENTS
from bgameb.items import Dice, Card
from bgameb.tools import Steps, Deck, Shaker
from bgameb.markers import Counter
from bgameb.types import COMPONENTS
from bgameb.errors import ComponentClassError, ComponentNameError


class TestGame:
    """Test Game class
    """

    def test_game_class_created_with_name(self) -> None:
        """Test Game name instancing
        """
        obj_ = Game(name='this_game')
        assert obj_.name == 'this_game', 'not set name for instance'
        assert isinstance(obj_.game_steps, Steps), \
            'steps isnt component'
        assert isinstance(obj_, Components), 'isnt component'
        assert obj_._types_to_add == COMPONENTS, 'wrong _types_to_add'

    def test_game_class_is_converted_to_json(self) -> None:
        """Test to json convertatrion
        """
        obj_ = Game(name='game')
        j = json.loads(obj_.to_json())
        assert j['name'] == 'game', 'not converted to json'

    components = [
        (Game, 'subgame'),
        (Dice, 'dice_nice'),
        (Card, 'card_ward'),
        (Steps, 'steps_new'),
        (Deck, 'deck_some'),
        (Shaker, 'shaker_this'),
        (Counter, 'counter_less'),
        ]

    @pytest.mark.parametrize("_class,name", components)
    def test_add_new_component_to_game(
        self, _class: Base, name: str) -> None:
        """Test add new component to Game
        """
        obj_ = Game(name='game')
        cl = _class(name)
        obj_.add(component=_class(name))
        assert obj_[cl.name].name == name, \
            'component not added'

    # def test_add_new_component_to_game(self) -> None:
    #     """Test new() tool or stuff add to game
    #     """
    #     obj_ = Game(name='game')
    #     for n in COMPONENTS.keys():
    #         obj_.new(name=n, type_=n)
    #         assert obj_[n].name == n, 'component not added'

    # def test_add_new_component_with_kwargs(self) -> None:
    #     """Test new() add to game with kwargs
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('dice', type_='dice', sides=42)
    #     assert obj_.dice.sides == 42, 'wrong count'

    def test_add_new_wrong_component_to_game(self) -> None:
        """Test cant add new wrong component to game
        """
        obj_ = Game(name='game')
        class G(): _type = 'wrong'
        with pytest.raises(
            ComponentClassError,
            match='not a component'
                ):
            obj_.add(G())

    # def test_add_new_wrong_component_to_game(self) -> None:
    #     """Test we cant add new notexisted tool or stuff to game
    #     """
    #     obj_ = Game(name='game')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.new('chocho', type_='this')

    @pytest.mark.parametrize("_class,name", components)
    def test_cant_add_new_existed_component(
        self, _class: Base, name: str) -> None:
        """Test cant add new object with same existed name in a game
        """
        obj_ = Game(name='game')
        cl = _class(name)
        obj_.add(component=cl)
        with pytest.raises(
            ComponentNameError,
            match='is exist in'
                ):

            obj_.add(component=cl)

    # def test_add_new_existed_object(self) -> None:
    #     """Test new() method for add new object to existed component
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('this', type_='shaker')
    #     obj_.new('that', type_='dice', target='this', count=10)
    #     with pytest.raises(
    #         ComponentNameError,
    #         match='is exist in'
    #             ):

    #         obj_.new('that', type_='dice', target='this', count=10)

    # def test_add_new_wrong_component_to_existed_object(self) -> None:
    #     """Test new() cant add new wrong object to existed component
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('this', type_='shaker')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.new('that', type_='what', target='this', count=10)

    # def test_add_new_wrong_component_to_notexisted_object(self) -> None:
    #     """Test new() cant add new wrong object to notexisted component
    #     """
    #     obj_ = Game(name='game')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.new('that', type_='what', target='this', count=10)

    # def test_add_new_component_to_notexisted_object(self) -> None:
    #     """Test new() cant add new object to notexisted component
    #     """
    #     obj_ = Game(name='game')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.new('that', type_='dice', target='this', count=10)

    # def test_add_new_stuff_to_nontools(self) -> None:
    #     """Test new() cant add new stuff to nontools/players
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('this', type_='dice')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.new('that', type_='dice', target='this')

    # def test_add_new_nonstuff_to_tools(self) -> None:
    #     """Test new() cant add new stuff to nontools/players
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('this', type_='shaker')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.new('that', type_='shaker', target='this', count=10)

    # def test_copy_component_from_game_to_another_component(self) -> None:
    #     """Test copy() existed component to another component
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('this', type_='shaker')
    #     obj_.new('that', type_='dice')
    #     obj_.copy('that', 'this')
    #     assert obj_.this.that.name == 'that', 'not copied'

    # def test_copy_component_with_kwargs(self) -> None:
    #     """Test copy() existed component to another component
    #     with kwargs
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('this', type_='shaker')
    #     obj_.new('that', type_='dice')
    #     obj_.copy('that', 'this', count=6)
    #     assert obj_.that.count == 1, 'wrong count'
    #     assert obj_.this.that.count == 6, 'not copied with new count'

    # def test_copy_notexisted_component_to_tool(self) -> None:
    #     """Test copy() cant copy notexisted stuff
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('this', type_='shaker')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.copy('that', 'this', count=6)

    # def test_copy_component_to_notexisted_tool(self) -> None:
    #     """Test copy() cant copy to notexisted tool
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('that', type_='dice')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.copy('that', 'this', count=6)

    # def test_copy_not_stuff_or_not_to_tool(self) -> None:
    #     """Test copy() missed type
    #     """
    #     obj_ = Game(name='game')
    #     obj_.new('that', 'shaker')
    #     obj_.new('this', 'dice')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.copy('this', 'this')
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.copy('that', 'that', count=10)
    #     with pytest.raises(
    #         ComponentClassError,
    #         match='not a component'
    #             ):
    #         obj_.copy('that', 'this', count=10)
