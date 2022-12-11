"""Game players classes
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from bgameb.base import Base
from bgameb.constraints import ITEMS_TOOLS


@dataclass_json
@dataclass(repr=False)
class Player(Base):
    """Base class for game players and bots
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        self._types_to_add = ITEMS_TOOLS
