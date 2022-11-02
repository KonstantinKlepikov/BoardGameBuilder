"""Game dices, coins, cards and other stuffs
"""
import collections
from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json
from bgameb.base import Base


@dataclass_json
@dataclass(repr=False)
class BaseMarker(Base):
    """Base class for game stuff (like dices or cards)
    """

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json
@dataclass(repr=False)
class Counter(BaseMarker):
    """Counter is a class that count some statistics for other
    objects. It use `python collections/Counter
    <https://docs.python.org/3/library/collections.html#collections.Counter>`_

    Aargs:
        current (Counter): collections.Counter obkject
                           is a current order of steps.
    """
    current: collections.Counter = field(
        default_factory=collections.Counter
        )
    _type: str = field(
        default='counter',
        metadata=config(exclude=lambda x: True),  # type: ignore
        repr=False
        )

    def __post_init__(self) -> None:
        super().__post_init__()

    def clear(self) -> None:
        """Clear the current queue
        """
        self.current = collections.Counter()
