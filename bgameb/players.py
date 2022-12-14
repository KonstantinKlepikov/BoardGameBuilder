"""Game players classes
"""
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from bgameb.base import Base


@dataclass(repr=False)
class BasePlayer(Base, DataClassJsonMixin):
    """Base class for game players and bots
    """

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(repr=False)
class Player(BasePlayer, DataClassJsonMixin):
    """Player
    """

    def __post_init__(self) -> None:
        super().__post_init__()

















# @dataclass_json
# @dataclass(repr=False)
# class Player(Base):
#     """Base class for game players and bots
#     """

#     def __post_init__(self) -> None:
#         super().__post_init__()
#         self._types_to_add = ITEMS_TOOLS
