"""Types of package objects
"""
from typing import List


ITEMS: List[str] = ['dice', 'card', 'step', ]
TOOLS: List[str] = ['shaker', 'deck', 'steps']
PLAYERS: List[str] = ['player', ]
GAMES: List[str] = ['game', ]

ITEMS_TOOLS = ITEMS + TOOLS
COMPONENTS = ITEMS_TOOLS + PLAYERS + GAMES
