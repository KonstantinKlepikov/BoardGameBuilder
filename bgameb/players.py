"""Game players classes
"""
from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from bgameb.base import Base
from bgameb.constraints import ITEMS_TOOLS


@dataclass_json
@dataclass(repr=False)
class Player(Base):
    """Base class for game players and bots

    Attr:
        - is_active (bool, optioanl): Activity flag. Default to None
        - has_priority (bool, optioanl): Priority flag. Default to None
        - team (str, optioanl): team name for player. Default to None

    """
    is_active: Optional[bool] = None
    has_priority: Optional[bool] = None
    team: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self._types_to_add = ITEMS_TOOLS
