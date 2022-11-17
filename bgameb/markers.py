"""Game markers, like counters and etc
"""
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from bgameb.base import Base


@dataclass_json
@dataclass(repr=False)
class BaseMarker(Base):
    """Base class for game markers
    """

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass_json
@dataclass(order=True, repr=False)
class Step(BaseMarker):
    """Game steps or turns

    Attr:
        - priority (int): priority queue number. Default to 0.
    """
    priority: int = 0

    def __post_init__(self) -> None:
        super().__post_init__()
