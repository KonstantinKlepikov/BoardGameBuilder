from dataclasses import dataclass


@dataclass
class Player:
    """Base class to create a player
    """


@dataclass
class Human(Player):
    """Base class to create a human palyer
    """


@dataclass
class Bot(Player):
    """Base class to create a bot player
    """
