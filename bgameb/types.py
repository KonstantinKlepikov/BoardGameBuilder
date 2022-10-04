from typing import Literal, Dict, Any
from bgameb.tools import TOOLS, TOOLS_TYPES
from bgameb.stuff import STUFF, STUFF_TYPES
from bgameb.players import PLAYERS, PLAERS_TYPES
from bgameb.rules import RULES, RULES_TYPES


component_type = Literal[
    STUFF_TYPES,
    TOOLS_TYPES,
    PLAERS_TYPES,
    RULES_TYPES
    ]

COMPONENTS: Dict[component_type, Any] = {}
for d in (TOOLS, STUFF, PLAYERS, RULES): COMPONENTS.update(d)
