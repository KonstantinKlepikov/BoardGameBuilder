"""Game players classes
"""
from typing import Optional, Literal, List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from bgameb.base import Base


@dataclass_json
@dataclass(repr=False)
class Player(Base):
    """Base class for game players and bots

    Args:

        - name (str): player name
        - has_priority (bool): Priority flag. Default to False
        - team (str, optioanl): team name for player. Default to None
        - owner_of (List[str]): list of object names owned by
                                player Default to []

    """
    is_active: bool = True
    has_priority: bool = False
    team: Optional[str] = None
    owner_of: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()


PLAYERS = {Player.__name__.lower(): Player, }
PLAERS_TYPES = Literal['player', ]
