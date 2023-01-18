import json
import pytest
from loguru._logger import Logger
from collections import Counter
from bgameb.game_ import Game_


class TestGame:
    """Test Game class
    """

    @pytest.fixture(scope='function')
    def game(self) -> Game_:
        return Game_(id='game')

    def test_game_class_created(self, game: Game_) -> None:
        """Test Game instancing
        """
        assert game.id == 'game', 'not set id for instance'
        assert isinstance(game.counter, Counter), 'wrong counter type'
        assert len(game.counter) == 0, 'counter not empty'
        assert isinstance(game._to_relocate, dict), 'wrong _to_relocate'
        assert isinstance(game._logger, Logger), 'wrong _to_relocate'
        assert json.loads(game.json())['id'] == 'game', \
            'not converted to json'

    # def test_relocate_all(self, game: Game) -> None:
    #     """Test relocations of attrs in game class
    #     """
    #     @dataclass
    #     class PlayMe(Player):
    #         this: str = field(default_factory=str)

    #         def __post_init__(self) -> None:
    #             super().__post_init__()
    #             self._to_relocate = {
    #                 'this': 'id'
    #             }

    #     @dataclass
    #     class ShakeMe(Shaker):
    #         ups: list = field(default_factory=list)
    #         this: Optional[dict[str, list[int]]] = None

    #         def __post_init__(self) -> None:
    #             super().__post_init__()
    #             self._to_relocate = {
    #                 'ups': 'current',
    #                 'this': 'last'
    #                     }

    #     game.add(PlayMe('billy'))
    #     game.add(ShakeMe('some'))
    #     game.c.some.add(Dice('six'))
    #     game.c.some.deal()
    #     assert isinstance(game.relocate_all(), Game), 'wrong return'
    #     assert game.c.billy.this == game.c.billy.id, 'not relocated'
    #     assert game.c.some.ups == game.c.some.current, 'not relocated'
    #     assert game.c.some.this == game.c.some.last, 'not relocated'
