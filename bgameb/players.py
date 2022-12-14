"""Game players classes
"""
from dataclasses import dataclass
from dataclasses_json import (
    DataClassJsonMixin, dataclass_json, Undefined
        )
from bgameb.base import Base


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class BasePlayer(Base, DataClassJsonMixin):
    """Base class for game players and bots
    """

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(repr=False)
class Player(BasePlayer, DataClassJsonMixin):
    """Player or bot
    """

    def __post_init__(self) -> None:
        super().__post_init__()
