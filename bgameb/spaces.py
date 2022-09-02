from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin


@dataclass
class DiceTower(DataClassJsonMixin):
    """Create dice tower
    """
    name: str = 'dice_tower'

    def add_dices(self) -> None:
        raise NotImplementedError

    def roll_dices(self) -> None:
        raise NotImplementedError

    @property
    def last_roll(self):
        raise NotImplementedError