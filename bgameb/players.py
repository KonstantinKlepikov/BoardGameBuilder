"""Game players classes
"""
from typing import Optional
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from bgameb.base import Base
from bgameb.types import MARKERS_ITEMS_TOOLS


@dataclass_json
@dataclass(repr=False)
class Player(Base):
    """Base class for game players and bots

    Attr:
        - name (str): player name
        - has_priority (bool): Priority flag. Default to False
        - team (str, optioanl): team name for player. Default to None

    """
    is_active: bool = True
    has_priority: bool = False
    team: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()
        self._types_to_add = MARKERS_ITEMS_TOOLS
