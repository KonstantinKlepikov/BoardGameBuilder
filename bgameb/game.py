"""Main engine to create games
"""
from typing import Optional, Literal
from dataclasses import dataclass, field
from bgameb.tools import TOOLS, TOOLS_TYPES
from bgameb.stuff import STUFF, STUFF_TYPES
from bgameb.errors import ComponentClassError
from bgameb.constructs import Components, Base


@dataclass
class Game(Base):
    """Create the game object
    """
    name: Optional[str] = None
    stuff: Components = field(default_factory=Components, init=False)
    tools: Components = field(default_factory=Components, init=False)

    # shakers: Components = field(default_factory=Components, init=False)
    # decks: Components = field(default_factory=Components, init=False)
    # game_rollers: Components = field(default_factory=Components, init=False)
    # game_cards: Components = field(default_factory=Components, init=False)

    def __post_init__(self) -> None:
        self.stuff = Components()
        self.tools = Components()

        # self.shakers = Components()
        # self.decks = Components()
        # self.game_rollers = Components()
        # self.game_cards = Components()
        super().__post_init__()

    # def add_stuff(self, stuff: Type[BaseStuff], **kwargs) -> None:
    #     """Add component to game

    #     Args:
    #         stuff (Type[game_stuff_type]): any class instance of game stuffs
    #         like rollers, cards etc
    #         kwargs: additional arguments of component
    #     """
    #     if issubclass(stuff, BaseRoller):
    #         self.game_rollers.add(stuff, **kwargs)
    #         self.logger.info(f'Roller added: {self.game_rollers=}.')
    #     elif issubclass(stuff, BaseCard):
    #         self.game_cards.add(stuff, **kwargs)
    #         self.logger.info(f'Card added: {self.game_cards=}.')
    #     else:
    #         raise ComponentClassError(obj_=stuff)

    # def _add_stuff(
    #     self, stuff: STUFF_TYPES, name: Optional[str] = None
    #         ) -> None:
    #     """Add stuff component type to game

    #     Args:
    #         stuff (Literal['roller', 'card']): type of available game stuff
    #         kwargs: additional arguments of component
    #     """
    #     if stuff in STUFF.keys():
    #         self.stuff.add(STUFF[stuff], name=name)
    #         self.logger.info(f'{stuff} is added: {self.stuff.get_names()}.')
    #     else:
    #         raise ComponentClassError(stuff, self.logger)


    # def add_tool(
    #     self, tool: TOOLS_TYPES, name: Optional[str] = None
    #         ) -> None:
    #     """Add tool component to game

    #     Args:
    #         stuff (Literal-'shaker', 'deck'): available game tool
    #         name (str): name for added tool
    #     """
    #     if tool in TOOLS.keys():
    #         self.tools.add(TOOLS[tool], name=name)
    #         self.logger.info(f'{tool} is added: {self.tools.get_names()}.')
    #     else:
    #         raise ComponentClassError(tool, self.logger)

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
            self.tools.add(TOOLS[component], name=name)
            self.logger.info(
                f'{component} is added: {self.tools.get_names()}.'
                )
        else:
            raise ComponentClassError(component, self.logger)


    # def add_shaker(self, name: Optional[str] = None) -> None:
    #     """Add shaker to game shakers

    #     Args:
    #         name (str): name for added shaker
    #     """
    #     if name:
    #         self.shakers.add(
    #             Shaker, name=name, _game_rollers=self.game_rollers
    #             )
    #     else:
    #         self.shakers.add(
    #             Shaker, name=Shaker.name, _game_rollers=self.game_rollers
    #             )
