from pprint import pprint
from typing import Optional
from dataclasses import dataclass
# from bgameb import (
#     Game, Player, Steps, Step, Deck, Card, Shaker, Dice,
#     Bag, log_enable
#         )
from bgameb import (
    Game_, Player_, Steps_, Step_, Deck_, Card_, Shaker_, Dice_,
    Bag_, log_enable
        )


if __name__ == '__main__':
    log_enable()

    # Creating of the game
    class MyGame(Game_):
        steps: Steps_
        deck: Deck_
        shaker: Shaker_
        bag: Bag_
        players: list[Player_] = []

    # The Player and Game are an obstract containeers for tools and stuff.
    # Deck, Bag, Shaker and Steps are tools. Dice, Card and Step are items.

    G = MyGame(
        id='one board game',
        steps=Steps_(id='steps'),
        deck=Deck_(id='deck'),
        shaker=Shaker_(id='shaker'),
        bag=Bag_(id='bag'),
        players=[Player_(id='player1'), Player_(id='player2')]
            )

    # The tool objects must be filled by items by method add().
    # That because we use some other methods for check
    # data types and makes some operations with items inside tool.

    # Adding game tuns order in Steps tool
    G.steps.add(Step_(id='step0'))
    G.steps.add(Step_(id='step1', priority=1))

    # Starting of new turn
    current_steps = G.steps.deal()

    # Game_steps is a priority queue, ordered by "priority" attribute
    last = G.steps.pop()

    # Adding of cards to deck. "count" parameter define how mutch
    # copies of card we must deal.
    G.deck.add(
        Card_(id='First', description='story', count=3)
            )
    G.deck.add(Card_(id='Second', count=1))

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

    # If you need more clear schema, inherite from any class.
    # Additional, you can define _to_relocate mapping -this
    # help move values from some attrs to another or convert some
    # values to related with Game outsade-hosted schema
    class MyCard(Card_):
        description: Optional[str] = None
        some_text: Optional[str] = 'some texts'
        is_open: Optional[bool] = None

    G.deck.add(
        MyCard(id='Thierd', description='story', count=12)
            )

    # Use default counters of any objects - counters not added to schema
    G.deck.c.first.counter['yellow'] = 12
    G.deck.c.second.counter['banana'] = 0

    # # relocate values
    # G.c.deck.c.thierd.relocate()

    # Dealing and shuffling of deck
    G.deck.deal().shuffle()

    # Adding dices to shaker
    G.shaker.add(
        Dice_(id='dice#8', sides=8, count=10)
            )

    # Roll dices
    result = G.shaker.c.dice_8.roll()

    # Use bag as collection of any items
    G.bag.add(Dice_(id='dice'))
    G.bag.add(Card_(id='card'))

    # # components and technical attrs not added to shcema.
    # # You can reconstruct full schema fit build_json() method
    # schema = G.relocate_all().to_json()

    print('='*20 + '\n')
    print(f'Repr: {G}')
    print('='*20 + '\n')
    pprint(G.dict())
    # print('='*20 + '\n')
    # print(f'Schema: {schema}')
    # print('='*20 + '\n')
    print(f'Result of shake: {result}')
    print('='*20 + '\n')
    print(f'Dir: {dir(G)}')
