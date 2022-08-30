from ._version import __version__
PUB_VERSION = __version__.public()

from .games import Game
from .players import Human, Bot
from .dices import Dice, DiceTower
