from pprint import pprint
from typing import Optional
from pydantic import Field
from bgameb import (
    Game, Player, Steps, Step, Deck, Card, Shaker, Dice,
    log_enable
        )


if __name__ == '__main__':
    log_enable()

    # Defining a classes
    class MyPlayer(Player):
        name: str
        deck: Deck

    # Creating of the game
    class MyGame(Game):
        steps: Steps
        shaker: Shaker
        me: MyPlayer
        opponent = MyPlayer

    # The Player and Game are an obstract containeers for tools and stuff.
    # Deck, Bag, Shaker and Steps are tools. Dice, Card and Step are items.

    G = MyGame(
        steps=Steps(),
        shaker=Shaker(),
        me = MyPlayer(name='Me', deck=Deck()),
        opponent = MyPlayer(name='Opponent', deck=Deck()),
            )

    # The tool objects must be filled by items by method add().
    # That because we use some other methods for check
    # data types and makes some operations with items inside tool.

    # Adding game tuns order in Steps tool
    G.steps.add(Step(id='step0'))
    G.steps.add(Step(id='step1', priority=1))

    # Starting of new turn
    current_steps = G.steps.deal()

    # Game steps is a priority queue, ordered by "priority" attribute
    last = G.steps.pops()

    # Adding of cards to deck. "count" parameter define how mutch
    # copies of card we must deal.
    G.me.deck.add(
        Card(id='First', description='story', count=2)
            )
    G.me.deck.add(Card(id='Second', count=1))

    # All items in tools are saved in spetial object Component.
    # Is a dict-like class. Component is predefined as attribute "c".
    # A component usied as base for other operations with items.
    cards_component = G.me.deck.c

    # Any item is available in Component with dot or classic dict
    # notation. Names for that notation is transited from ids of items.
    card = G.me.deck.c.first
    card = G.me.deck.c['first']

    # You can get item by its id
    card = G.me.deck.c.by_id('First')

    # If you relocate some bult-in attrs, inherite from stuff classes,
    # then define aliases for attributes. In this example we use two
    # different solution: Field aliase and config.
    # Dont forget use G.dict(by_alias=True) to get aliases.
    # More infoshere:
    # https://docs.pydantic.dev/usage/model_config/#alias-generator
    # Finaly, if you need use callbacs to export data from some
    # function as field values - define properties.
    class MyCard(Card):
        description: Optional[str] = Field(None, alias='some_bla_bla')
        some_text: Optional[str] = 'some texts'

        class Config(Card.Config):
            fields = {'is_revealed': 'is_open'}

        @property
        def my_calculated_field(self) -> str:
            return self.some_text.upper()

    G.me.deck.add(
        MyCard(id='Thierd', description='story', count=3)
            )

    # Use default counters of any objects - counters not added to schema
    G.me.deck.c.first._counter['yellow'] = 12
    G.me.deck.c.second._counter['banana'] = 0

    # Dealing and shuffling of deck
    G.me.deck.deal().shuffle()

    # Adding dices to shaker
    G.shaker.add(
        Dice(id='dice#8', sides=8, count=10)
            )

    # Roll dices
    result = G.shaker.c.dice_8.roll()

    print('='*20 + '\n')
    print(f'Repr: {G}')
    print('='*20 + '\n')
    pprint(G.dict(by_alias=True))
    print('='*20 + '\n')
    print(f'Result of shake: {result}')
    print('='*20 + '\n')
    print(f'Dir: {dir(G)}')
