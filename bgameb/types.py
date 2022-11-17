"""Types of package objects
"""
from typing import List


MARKERS: List[str] = ['step']
ITEMS: List[str] = ['dice', 'card', ]
TOOLS: List[str] = ['shaker', 'deck', 'steps']
PLAYERS: List[str] = ['player', ]
GAMES: List[str] = ['game', ]

MARKERS_ITEMS = MARKERS + ITEMS
MARKERS_ITEMS_TOOLS = MARKERS_ITEMS + TOOLS
COMPONENTS = MARKERS_ITEMS_TOOLS + PLAYERS + GAMES
