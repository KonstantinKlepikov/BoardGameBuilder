"""Types of package objects
"""
from typing import Literal, Dict
from bgameb.base import Base
from bgameb.markers import MARKERS, MARKERS_TYPES
from bgameb.items import ITEMS, ITEMS_TYPES
from bgameb.tools import TOOLS, TOOLS_TYPES
from bgameb.players import PLAYERS, PLAERS_TYPES


COMPONENTS_TYPES = Literal[
    MARKERS_TYPES,
    ITEMS_TYPES,
    TOOLS_TYPES,
    PLAERS_TYPES,
    ]

COMPONENTS: Dict[COMPONENTS_TYPES, Base] = {}
for d in (MARKERS, TOOLS, ITEMS, PLAYERS):
    COMPONENTS.update(d)  # type: ignore

MARKERS_MORE = [
    n for n
    in COMPONENTS.keys() if
    n not in MARKERS.keys()
    ]
ITEMS_MORE = [
    n for n
    in COMPONENTS.keys() if
    n not in MARKERS.keys()
    and n not in ITEMS.keys()
    ]
TOOLS_MORE = [
    n for n
    in COMPONENTS.keys() if
    n not in MARKERS.keys()
    and n not in ITEMS.keys()
    and n not in TOOLS.keys()
    ]
