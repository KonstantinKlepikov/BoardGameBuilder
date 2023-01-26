from pprint import pprint
from typing import Optional
from pydantic import Field
from bgameb import (
    Game, Player, Steps, Step, Deck, Card, Shaker, Dice,
    Bag, log_enable
        )


if __name__ == '__main__':
    log_enable()

    # Creating of the game
    class MyGame(Game):
        steps: Steps
        deck: Deck
        shaker: Shaker
        bag: Bag
        players: list[Player] = []

    # The Player and Game are an obstract containeers for tools and stuff.
    # Deck, Bag, Shaker and Steps are tools. Dice, Card and Step are items.

    G = MyGame(
        id='one board game',
        steps=Steps(id='steps'),
        deck=Deck(id='deck'),
        shaker=Shaker(id='shaker'),
        bag=Bag(id='bag'),
        players=[Player(id='player1'), Player(id='player2')]
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
    last = G.steps.pop()

    # Adding of cards to deck. "count" parameter define how mutch
    # copies of card we must deal.
    G.deck.add(
        Card(id='First', description='story', count=2)
            )
    G.deck.add(Card(id='Second', count=1))

    # All items in tools are saved in spetial object Component.
    # Is a dict-like class. Component is predefined as attribute "c".
    # A component usied as base for other operations with items.
    cards_component = G.deck.c

    # Any item is available in Component with dot or classic dict
    # notation. Names for that notation is transited from ids of items.
    card = G.deck.c.first
    card = G.deck.c['first']

    # You can get item by its id
    card = G.deck.c.by_id('First')

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
            fields = {'opened': 'is_open'}

        @property
        def my_calculated_field(self) -> str:
            return self.some_text.upper()

    G.deck.add(
        MyCard(id='Thierd', description='story', count=3)
            )

    # Use default counters of any objects - counters not added to schema
    G.deck.c.first._counter['yellow'] = 12
    G.deck.c.second._counter['banana'] = 0

    # Dealing and shuffling of deck
    G.deck.deal().shuffle()

    # Adding dices to shaker
    G.shaker.add(
        Dice(id='dice#8', sides=8, count=10)
            )

    # Roll dices
    result = G.shaker.c.dice_8.roll()

    # Use bag as collection of any items
    G.bag.add(Dice(id='dice'))
    G.bag.add(Card(id='card'))

    print('='*20 + '\n')
    print(f'Repr: {G}')
    print('='*20 + '\n')
    pprint(G.dict(by_alias=True))
    print('='*20 + '\n')
    print(f'Result of shake: {result}')
    print('='*20 + '\n')
    print(f'Dir: {dir(G)}')
