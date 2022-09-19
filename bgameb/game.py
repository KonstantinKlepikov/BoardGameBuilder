"""Main engine to create games
"""
from typing import Optional, Literal
from dataclasses import dataclass, field
from bgameb.tools import TOOLS, TOOLS_TYPES
from bgameb.stuff import STUFF, STUFF_TYPES
from bgameb.errors import ComponentClassError
from bgameb.constructs import Components, BaseGame


@dataclass
class Game(BaseGame):
    """Create the game object
    """
    name: Optional[str] = None
    stuff: Components = field(default_factory=Components, init=False)
    tools: Components = field(default_factory=Components, init=False)

    def __post_init__(self) -> None:
        self.stuff = Components()
        self.tools = Components()
        super().__post_init__()

    def add(
        self,
        component: Literal[STUFF_TYPES, TOOLS_TYPES],
        name: Optional[str] = None,
            ) -> None:
        if component in STUFF.keys():
            self.stuff.add(STUFF[component], name=name)
            self.logger.info(
                f'{component} is added: {self.stuff.get_names()}.'
                )
        elif component in TOOLS.keys():
            self.tools.add(TOOLS[component], _game=self, name=name)
            self.logger.info(
                f'{component} is added: {self.tools.get_names()}.'
                )
        else:
            raise ComponentClassError(component, self.logger)
