"""Game players classes
"""
from typing import Optional, Literal
from dataclasses import dataclass
from bgameb.constructs import BasePlayer


@dataclass
class Player(BasePlayer):
    """Base class to create a human palyer
    """
    name: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass
class Bot(BasePlayer):
    """Base class to create a bot player
    """
    name: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()


PLAYERS = {
    'player': Player,
    'bot': Bot,
}
PLAERS_TYPES = Literal['player', 'bot']
