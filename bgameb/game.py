"""Main engine to create games
"""
from typing import Optional, Literal
from dataclasses import dataclass, field
from bgameb.tools import TOOLS, TOOLS_TYPES
from bgameb.stuff import STUFF, STUFF_TYPES
from bgameb.players import PLAYERS, PLAERS_TYPES
from bgameb.errors import ComponentClassError
from bgameb.constructs import Components, BaseGame


@dataclass
class Game(BaseGame):
    """Create the game object
    """
    name: Optional[str] = None
    stuff: Components = field(default_factory=Components, init=False)
    tools: Components = field(default_factory=Components, init=False)
    players: Components = field(default_factory=Components, init=False)

    def __post_init__(self) -> None:
        super().__post_init__()

    def add(
        self,
        component: Literal[STUFF_TYPES, TOOLS_TYPES, PLAERS_TYPES],
        name: Optional[str] = None,
        **kwargs
            ) -> None:
        for source in [
            (STUFF, self.stuff), (TOOLS, self.tools), (PLAYERS, self.players)
            ]:
            if component in source[0].keys():
                source[1].add(source[0][component], name=name, **kwargs)
                self.logger.info(f'{component} is added: {source[1].get_names()}.')
                break
        else:
            raise ComponentClassError(component, self.logger)
