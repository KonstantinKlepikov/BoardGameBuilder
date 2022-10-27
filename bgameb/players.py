"""Game players classes
"""
from typing import Optional, Literal, List
from collections import Counter
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from bgameb.base import Base


@dataclass_json
@dataclass(repr=False)
class BasePlayer(Base):
    """Base class for game players and bots

    Args:

        - name (str): player name
        - counter (Counter): counter object for count any items
        - has_priority (bool): Priority flag. Default to False
        - team (str, optioanl): team name for player. Default to None
        - owner_of (List[str]): list of object names owned by
                                player Default to []

    """
    counter: Counter = field(
        default_factory=Counter,
        init=False,
        )
    is_active: bool = True
    has_priority: bool = False
    team: Optional[str] = None
    owner_of: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json
@dataclass(repr=False)
class Player(BasePlayer):
    """Player class
    """
    _type: str = field(
        default='player',
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()


PLAYERS = {Player._type: Player, }
PLAERS_TYPES = Literal['player', ]
