"""Types of package objects
"""
from typing import Literal, Dict, Any
from bgameb.tools import TOOLS, TOOLS_TYPES
from bgameb.stuff import STUFF, STUFF_TYPES
from bgameb.players import PLAYERS, PLAERS_TYPES


COMPONENTS_TYPES = Literal[
    STUFF_TYPES,
    TOOLS_TYPES,
    PLAERS_TYPES,
    ]

COMPONENTS: Dict[COMPONENTS_TYPES, Any] = {}
for d in (TOOLS, STUFF, PLAYERS):
    COMPONENTS.update(d)  # type: ignore

# other objects, like tools and players
NONSTUFF_TYPES = Literal[
    TOOLS_TYPES,
    PLAERS_TYPES,
    ]

NONSTUFF: Dict[NONSTUFF_TYPES, Any] = {}
for d in (TOOLS, PLAYERS):
    NONSTUFF.update(d)  # type: ignore

# stuff that can be added to stuff
SPETIAL_STUFF = {
    'counter': STUFF['counter'],
    }
