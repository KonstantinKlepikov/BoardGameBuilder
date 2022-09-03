from bgameb._version import __version__
PUB_VERSION = __version__.public()

from bgameb.games import Game
from bgameb.players import Human, Bot
from bgameb.rollers import Dice, Coin
from bgameb.shakers import Shaker