"""Main engine to create game
"""
from typing import Union
from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from bgameb.base import Base, Component, log_enable
from bgameb.players import Player, BasePlayer
from bgameb.items import Dice, Card, Step, BaseItem
from bgameb.tools import Shaker, Deck, Bag, Steps, BaseTool
from bgameb.errors import ComponentClassError


Item = Union[Card, Dice, Step]
Tool = Union[Shaker, Bag, Deck, Steps]
Stuff = Union[Player, Item, Tool]


@dataclass(repr=False)
class BaseGame(Base, DataClassJsonMixin):
    """The main game object
    """
    p: Component[Player] = field(default_factory=Component)
    i: Component[Item] = field(default_factory=Component)
    t: Component[Tool] = field(default_factory=Component)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.p = Component()
        self.i = Component()
        self.t = Component()

    def add(self, stuff: Stuff) -> None:
        """Add stuff to component

        Args:
            stuff (Stuff): game stuff
        """
        if issubclass(stuff.__class__, BasePlayer):
            self.p._update(stuff)
            self._logger.info(f'"{stuff.id}" is added to p".')
        elif issubclass(stuff.__class__, BaseItem):
            self.i._update(stuff)
            self._logger.info(f'"{stuff.id}" is added to i".')
        elif issubclass(stuff.__class__, BaseTool):
            self.t._update(stuff)
            self._logger.info(f'"{stuff.id}" is added to t".')
        else:
            raise ComponentClassError(stuff, self._logger)


@dataclass(repr=False)
class Game(BaseGame, DataClassJsonMixin):
    """The main game object
    """

    def __post_init__(self) -> None:
        super().__post_init__()










# TypeComp = Type[Union[
#     'bgameb.Card', 'bgameb.Dice', 'bgameb.Step',
#     'bgameb.Player', 'bgameb.Game', 'bgameb.Steps',
#     'bgameb.Bag', 'bgameb.Shaker', 'bgameb.Deck',
#     'bgameb.Steps',
#         ]]


# @dataclass_json
# @dataclass(repr=False)
# class Game(Base):
#     """The main game object
#     """

#     def __post_init__(self) -> None:
#         super().__post_init__()
#         self._types_to_add = COMPONENTS


#     def __getattr__(self, attr: str) -> TypeComp:
#         try:
#             return self.__dict__[attr]
#         except KeyError:
#             raise AttributeError(attr)


if __name__ == '__main__':
    import bgameb
    from pprint import pprint
    log_enable()

    G = Game('one board game')
    G.add(Player('Player'))
    print(G)
    print(G.p._inclusion)
    print(G.p.player.id)
    pprint(G.to_dict())
    # game.steps.add(bgameb.Step('step 0'))
    # game.steps.add(bgameb.Step('step 1', priority=1))
    # game.steps.deal()
    # game.add(bgameb.Deck('Deck'))
    # game.deck.add(
    #     bgameb.Card('First', description='story', count=3)  # type: ignore
    #         )
    # game.deck.add(bgameb.Card('Second', count=1))

    # print(f'Other: {game.deck.first.other}')
    # game.deck.first.counter['yellow'] = 12
    # game.deck.second.counter['banana'] = 0

    # steps = game.steps.deal()
    # game.deck.deal().shuffle()
    # deck = game.deck.current

    # game.IS_ACTIVE = True  # type: ignore

    # game.add(bgameb.Shaker('blue shaker'))
    # game.blue_shaker.add(
    #     bgameb.Dice('dice#8', sides=8, count=10)
    #         )

    # result = game.blue_shaker.dice_8.roll()

    # print(f'Result of shake: {result}')
    # print('='*20 + '\n')
    # print(f'Repr: {repr(game)}')
    # print('='*20 + '\n')
    # print(f'Print: {game}')
    # print('='*20 + '\n')
    # pprint(game.to_dict())
    # print('='*20 + '\n')
    # pprint(deck)
    # print('='*20 + '\n')
    # print(f'Current deck ids: {game.deck.current_ids()}')
    # print('='*20 + '\n')
    # print(f'Names in game: {game.get_names()}')
    # print('='*20 + '\n')
    # print(
    #     'Get by id "Game Steps" in game: '
    #     f'{game.by_id("Game Steps")}'
    #         )
    # print('='*20 + '\n')
    # print(f'Dir: {dir(game)}')





    # game = bgameb.Game('one board game')
    # game.add(bgameb.Steps('Steps'))
    # game.steps.add(bgameb.Step('step 0'))
    # game.steps.add(bgameb.Step('step 1', priority=1))
    # game.steps.deal()
    # game.add(bgameb.Deck('Deck'))
    # game.deck.add(
    #     bgameb.Card('First', description='story', count=3)  # type: ignore
    #         )
    # game.deck.add(bgameb.Card('Second', count=1))

    # print(f'Other: {game.deck.first.other}')
    # game.deck.first.counter['yellow'] = 12
    # game.deck.second.counter['banana'] = 0

    # steps = game.steps.deal()
    # game.deck.deal().shuffle()
    # deck = game.deck.current

    # game.IS_ACTIVE = True  # type: ignore

    # game.add(bgameb.Shaker('blue shaker'))
    # game.blue_shaker.add(
    #     bgameb.Dice('dice#8', sides=8, count=10)
    #         )

    # result = game.blue_shaker.dice_8.roll()

    # print(f'Result of shake: {result}')
    # print('='*20 + '\n')
    # print(f'Repr: {repr(game)}')
    # print('='*20 + '\n')
    # print(f'Print: {game}')
    # print('='*20 + '\n')
    # pprint(game.to_dict())
    # print('='*20 + '\n')
    # pprint(deck)
    # print('='*20 + '\n')
    # print(f'Current deck ids: {game.deck.current_ids()}')
    # print('='*20 + '\n')
    # print(f'Names in game: {game.get_names()}')
    # print('='*20 + '\n')
    # print(
    #     'Get by id "Game Steps" in game: '
    #     f'{game.by_id("Game Steps")}'
    #         )
    # print('='*20 + '\n')
    # print(f'Dir: {dir(game)}')
