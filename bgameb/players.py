"""Game players classes
"""
from dataclasses import dataclass
from bgameb.constructs import BasePlayer


@dataclass
class Human(BasePlayer):
    """Base class to create a human palyer
    """


@dataclass
class Bot(BasePlayer):
    """Base class to create a bot player
    """
