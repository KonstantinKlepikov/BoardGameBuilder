"""Game players classes
"""
from typing import Optional, Literal, List
from collections import Counter
from abc import ABC
from dataclasses import dataclass, field
from bgameb.base import Base
# from bgameb.constructs import BasePlayer


@dataclass
class BasePlayer(Base, ABC):
    """Base class for game players and bots

    Attrs

        - name (str): player name
        - counter (Counter): counter object for count any items
        - is_active (bool): Default to True.
        - has_priority (bool): Default to False
        - team (str, optioanl): team name for this player
        - owner_of (List[str]): list of objects owned by player Default to []
        - user_of (List[str]): list of objects used by player Default to []

    """
    name: str
    counter: Counter = field(
        default_factory=Counter,
        init=False,
        )
    is_active: bool = True
    has_priority: bool = False
    team: Optional[str] = None
    owner_of: List[str] = field(default_factory=list, init=False)
    user_of: List[str] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass
class Player(BasePlayer):
    """Base class to create a player
    """

    def __post_init__(self) -> None:
        super().__post_init__()


# @dataclass
# class Bot(BasePlayer):
#     """Base class to create a bot player
#     """
#     name: Optional[str] = None
#     counter: Counter = field(
#         default_factory=Counter,
#         init=False,
#         )

#     def __post_init__(self) -> None:
#         super().__post_init__()


PLAYERS = {
    'player': Player,
    # 'bot': Bot,
}
PLAERS_TYPES = Literal['player',]
